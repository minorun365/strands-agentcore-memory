# AgentCore設定ファイル更新が必要

## 現在の状況確認

```bash
→ cat .agentcore/config.json 2>/dev/null || echo "config.json 未存在"
config.json 未存在

# IAMロールポリシーアタッチ実行
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn arn:aws:iam::aws:***AWS_SECRET_ACCESS_KEY***
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccessV2
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess

→ aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

→ agentcore launch --codebuild
❌ Launch failed: Parameter validation failed:
Invalid length for parameter RoleName, value: 0, valid min length: 1
```

## 問題分析

### 成功した部分 ✅
- IAMロール存在確認: `arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole`
- 必要ポリシーアタッチ完了

### 問題部分 ❌
- `.agentcore/config.json` ファイルが存在しない
- 設定でロールARNが不完全: `arn:aws:iam::XXXXXXXXXXXX:role/` (ロール名部分が空)

## 根本原因

AgentCoreが `.bedrock_agentcore.yaml` から不完全な設定を読み込んでいる可能性。正しいロールARNで設定を更新する必要があります。

## 解決手順

### ステップ1: 現在の設定ファイル確認

```bash
# .bedrock_agentcore.yaml の内容確認
cat .bedrock_agentcore.yaml

# AgentCore関連の全設定ファイル確認
find . -name "*agentcore*" -type f
```

### ステップ2: AgentCore設定の更新

```bash
# 正しいロールARNで設定更新
agentcore configure --entrypoint src/main.py -er arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

# 設定確認
cat .agentcore/config.json
```

### ステップ3: 設定ファイル手動確認・修正（必要に応じて）

```bash
# .bedrock_agentcore.yaml を確認して、execution_role_arn を修正
# 現在の値から正しい値に変更:
# 修正前: execution_role_arn: "arn:aws:iam::XXXXXXXXXXXX:role/"
# 修正後: execution_role_arn: "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole"
```

### ステップ4: 再デプロイ

```bash
# 設定更新後、再度デプロイ実行
agentcore launch --codebuild
```

## 想定される設定ファイル内容

### 正しい .agentcore/config.json の例
```json
{
  "entrypoint": "src/main.py",
  "execution_role_arn": "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
  "ecr_repository_uri": "XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main",
  "region": "us-west-2"
}
```

### 正しい .bedrock_agentcore.yaml の例
```yaml
agent_name: main
entrypoint: src/main.py
execution_role_arn: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
ecr_repository_uri: XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main
region: us-west-2
```

## トラブルシューティング

### 1. agentcore configure エラー
```bash
# エラーが出る場合は手動で .agentcore ディレクトリ作成
mkdir -p .agentcore

# 手動設定ファイル作成
cat > .agentcore/config.json << EOF
{
  "entrypoint": "src/main.py",
  "execution_role_arn": "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
  "ecr_repository_uri": "XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main",
  "region": "us-west-2"
}
EOF
```

### 2. .bedrock_agentcore.yaml 手動修正
```bash
# バックアップ作成
cp .bedrock_agentcore.yaml .bedrock_agentcore.yaml.backup

# viまたはエディタで編集
# execution_role_arn の行を探して正しいARNに修正
```

### 3. 設定確認コマンド
```bash
# 現在の設定状況確認
agentcore status

# または設定詳細確認
cat .bedrock_agentcore.yaml
cat .agentcore/config.json 2>/dev/null || echo "config.json なし"
```

## 期待される成功時の出力

### agentcore configure 成功時
```bash
✅ Agent configuration updated successfully
Configuration saved to .agentcore/config.json
```

### agentcore launch --codebuild 成功時
```bash
Launching Bedrock AgentCore (codebuild mode)...
✅ Using execution role: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
✅ CodeBuild project created successfully
✅ Build started
⠼ Building and deploying...
✅ Agent Runtime deployed successfully!
Runtime ARN: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:agent-runtime/xxxxx
```

## 次のアクション

1. **設定ファイル確認**: `cat .bedrock_agentcore.yaml`
2. **設定更新**: `agentcore configure` 実行
3. **再デプロイ**: `agentcore launch --codebuild`

## メモ
- 日時: 2025-07-27
- 段階: AgentCore設定更新フェーズ
- 完了: IAMロール作成・ポリシーアタッチ
- 課題: 設定ファイルのロールARNが不完全
- 次のアクション: agentcore configure 実行