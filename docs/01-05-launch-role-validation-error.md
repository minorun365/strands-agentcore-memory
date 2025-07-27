# AgentCore Launch - ロール設定エラー

## 発生したエラー

```bash
→ agentcore launch --codebuild
Launching Bedrock AgentCore (codebuild mode)...

Starting CodeBuild ARM64 deployment for agent 'main' to account XXXXXXXXXXXX (us-west-2)
Setting up AWS resources (ECR repository, execution roles)...
Getting or creating ECR repository for agent: main
Repository doesn't exist, creating new ECR repository: bedrock-agentcore-main
⠼ Launching Bedrock AgentCore...✅ ECR repository available: XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main
Using execution role from config: arn:aws:iam::XXXXXXXXXXXX:role/
❌ Launch failed: Parameter validation failed:
Invalid length for parameter RoleName, value: 0, valid min length: 1
```

## 問題分析

### 現在の状況
- AgentCore launch が実行された
- ECRリポジトリ自動作成成功: `bedrock-agentcore-main`
- **問題**: 実行ロールARNが不完全
  - 設定値: `arn:aws:iam::XXXXXXXXXXXX:role/` (ロール名が空)
  - 必要: `arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole`

### 根本原因
`.bedrock_agentcore.yaml` またはAgentCore設定でIAMロールARNが正しく設定されていない。

## 進捗確認

### 成功した部分 ✅
1. AgentCore CLIの動作確認
2. ECRリポジトリ自動作成
3. CodeBuildデプロイプロセス開始

### 失敗した部分 ❌
1. IAMロール設定が不完全

## 解決手順

### ステップ1: 現在の設定確認

```bash
# 設定ファイル内容確認
cat .bedrock_agentcore.yaml

# .agentcore設定確認（存在する場合）
cat .agentcore/config.json 2>/dev/null || echo "config.json 未存在"
```

### ステップ2: IAMロール作成（まだ未作成の場合）

#### 方法A: AWS管理者権限がある場合
```bash
# BedrockAgentCoreExecutionRole作成
aws iam create-role \
    --role-name BedrockAgentCoreExecutionRole \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "bedrock-agentcore.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }'

# 必要なポリシーをアタッチ
aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:***AWS_SECRET_ACCESS_KEY***

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccessV2

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess

# ロールARN取得
aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
```

#### 方法B: 既存ロール確認
```bash
# 既存ロールの検索
aws iam list-roles --query 'Roles[?contains(RoleName, `Bedrock`) || contains(RoleName, `AgentCore`)].{RoleName:RoleName,Arn:Arn}'

# 特定ロール確認
aws iam get-role --role-name BedrockAgentCoreExecutionRole 2>/dev/null || echo "ロール未存在"
```

### ステップ3: AgentCore設定更新

#### 正しいロールARNで設定
```bash
# agentcore configure で設定更新
agentcore configure --entrypoint src/main.py -er arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

# 設定確認
cat .agentcore/config.json
```

#### 手動設定ファイル修正（代替案）
```bash
# .bedrock_agentcore.yaml を直接編集
cp .bedrock_agentcore.yaml .bedrock_agentcore.yaml.backup

# 設定ファイル内のロールARNを修正
# execution_role_arn: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
```

### ステップ4: 再デプロイ

```bash
# 設定確認後、再度launch
agentcore launch --codebuild
```

## 想定される修正後の動作

### 成功時の出力例
```bash
Launching Bedrock AgentCore (codebuild mode)...
Starting CodeBuild ARM64 deployment for agent 'main' to account XXXXXXXXXXXX (us-west-2)
✅ ECR repository available: XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main
Using execution role from config: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
✅ CodeBuild project created successfully
✅ Build started: bedrock-agentcore-main-xxxxx
⠼ Building and deploying...
✅ Agent Runtime deployed successfully!
Runtime ARN: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:agent-runtime/xxxxx
```

## 追加で作成されたリソース

### 新しいECRリポジトリ
- **名前**: `bedrock-agentcore-main` 
- **URI**: `XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main`
- **既存のもの**: `strands-agentcore-memory` (未使用)

## トラブルシューティング

### 1. ロール作成権限エラー
```bash
# エラー: iam:CreateRole not authorized
# 解決: 01-02の権限問題を解決
```

### 2. ロールARN形式エラー
```bash
# 正しい形式確認
aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
# 出力例: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
```

### 3. 設定ファイル確認
```bash
# 現在の設定内容を確認
cat .bedrock_agentcore.yaml
cat .agentcore/config.json 2>/dev/null
```

## 次のアクション優先順位

1. **設定ファイル確認** - 現在の設定内容を確認
2. **IAMロール作成/確認** - 必要に応じてロール作成
3. **AgentCore設定更新** - 正しいロールARNで設定
4. **再デプロイ実行** - `agentcore launch --codebuild`

## メモ
- 日時: 2025-07-27
- 段階: AgentCoreデプロイ実行フェーズ
- 問題: 実行ロールARNが不完全（ロール名空文字）
- 進捗: ECRリポジトリ自動作成成功
- 次のアクション: ロール設定修正後の再デプロイ