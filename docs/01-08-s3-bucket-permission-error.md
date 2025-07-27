# AgentCore Launch - S3バケット権限エラー

## Launch実行結果

```bash
→ agentcore launch --codebuild
Launching Bedrock AgentCore (codebuild mode)...

Starting CodeBuild ARM64 deployment for agent 'main' to account XXXXXXXXXXXX (us-west-2)
Setting up AWS resources (ECR repository, execution roles)...
Getting or creating ECR repository for agent: main
✅ Reusing existing ECR repository: XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main
✅ ECR repository available: XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main
Using execution role from config: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
✅ Execution role validation passed: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
Preparing CodeBuild project and uploading source...
Getting or creating CodeBuild execution role for agent: main
Role name: AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
CodeBuild role doesn't exist, creating new role: AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
Creating IAM role: AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
✓ Role created: arn:aws:iam::XXXXXXXXXXXX:role/AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
Attaching inline policy: CodeBuildExecutionPolicy to role: AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
✓ Policy attached: CodeBuildExecutionPolicy
Waiting for IAM role propagation...
CodeBuild execution role creation complete: arn:aws:iam::XXXXXXXXXXXX:role/AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3

❌ Launch failed: An error occurred (AccessDenied) when calling the CreateBucket operation: 
User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 
is not authorized to perform: s3:CreateBucket on resource: 
"arn:aws:s3:::bedrock-agentcore-codebuild-sources-XXXXXXXXXXXX-us-west-2" 
because no identity-based policy allows the s3:CreateBucket action
```

## 進捗分析

### 成功した部分 ✅
1. **ECRリポジトリ**: 既存リポジトリ再利用成功
2. **実行ロール検証**: BedrockAgentCoreExecutionRole 検証成功
3. **CodeBuild用IAMロール作成**: 自動作成成功
   - ロール名: `AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3`
   - ポリシーアタッチ: `CodeBuildExecutionPolicy` 成功
4. **IAMロール伝播**: 正常完了

### 失敗した部分 ❌
**S3バケット作成権限不足**
- 必要なバケット: `bedrock-agentcore-codebuild-sources-XXXXXXXXXXXX-us-west-2`
- 不足権限: `s3:CreateBucket`
- 原因: CodeBuildのソースコード格納用S3バケットの作成権限なし

## 問題解決

### 解決方法1: S3関連権限の追加（推奨）

IAMユーザーにS3権限を追加：

```bash
# S3フルアクセス権限追加
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

### 解決方法2: 最小権限カスタムポリシー（セキュア）

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:PutBucketVersioning"
            ],
            "Resource": [
                "arn:aws:s3:::bedrock-agentcore-codebuild-sources-*",
                "arn:aws:s3:::bedrock-agentcore-codebuild-sources-*/*"
            ]
        }
    ]
}
```

**カスタムポリシー作成手順:**
```bash
# ポリシーファイル作成
cat > s3-agentcore-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:PutBucketVersioning"
            ],
            "Resource": [
                "arn:aws:s3:::bedrock-agentcore-codebuild-sources-*",
                "arn:aws:s3:::bedrock-agentcore-codebuild-sources-*/*"
            ]
        }
    ]
}
EOF

# ポリシー作成
aws iam create-policy \
    --policy-name StrandsAgentCoreS3Access \
    --policy-document file://s3-agentcore-policy.json

# ポリシーアタッチ（ARNは出力から取得）
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::XXXXXXXXXXXX:policy/StrandsAgentCoreS3Access
```

## 現在のステータス確認

### AgentCore状態
```bash
→ agentcore status
Agent is configured, but not launched yet.
```

**注目点:**
- ECRリポジトリが設定に追加された: `XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main`
- その他の設定は変更なし

### 作成されたリソース
1. **ECRリポジトリ**: `bedrock-agentcore-main` （既存）
2. **CodeBuild用IAMロール**: `AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3` ✅

## 権限修正後の再実行手順

### ステップ1: 権限追加
```bash
# 方法1: S3フルアクセス（簡単）
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# 権限確認
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07
```

### ステップ2: 再デプロイ実行
```bash
# S3権限追加後、再度実行
agentcore launch --codebuild
```

### ステップ3: 成功確認
```bash
# デプロイ成功後のステータス確認
agentcore status

# Runtime ARN取得
agentcore list
```

## 期待される成功時の出力

```bash
Launching Bedrock AgentCore (codebuild mode)...
✅ S3 bucket created: bedrock-agentcore-codebuild-sources-XXXXXXXXXXXX-us-west-2
✅ Source uploaded to S3
✅ CodeBuild project created: bedrock-agentcore-main-xxxxx
✅ Build started: build-xxxxx
⠼ Building Docker image...
⠼ Pushing to ECR...
⠼ Creating Agent Runtime...
✅ Agent Runtime deployed successfully!
Runtime ARN: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:agent-runtime/xxxxx
```

## 更新された必要ポリシー一覧

**現在必要なポリシー:**
- `AmazonBedrockFullAccess` - Claude モデルの呼び出し
- `BedrockAgentCoreFullAccess` - AgentCore Runtime の利用
- `AmazonEC2ContainerRegistryFullAccess` - ECR の完全操作
- `IAMFullAccess` - IAMロール作成・管理
- `AmazonS3FullAccess` - S3バケット作成・操作 ⭐**追加**

## 次のアクション

1. **S3権限追加** - 上記のいずれかの方法で実行
2. **再デプロイ** - `agentcore launch --codebuild`
3. **Runtime ARN取得** - デプロイ成功後
4. **環境変数設定** - .envファイル更新

## S3権限追加後の再Launch結果

```bash
→ aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

→ agentcore launch --codebuild
Launching Bedrock AgentCore (codebuild mode)...

Starting CodeBuild ARM64 deployment for agent 'main' to account XXXXXXXXXXXX (us-west-2)
Setting up AWS resources (ECR repository, execution roles)...
Using ECR repository from config: XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main
Using execution role from config: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
✅ Execution role validation passed: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
Preparing CodeBuild project and uploading source...
Getting or creating CodeBuild execution role for agent: main
Role name: AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
Reusing existing CodeBuild execution role: arn:aws:iam::XXXXXXXXXXXX:role/AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
✅ Created S3 bucket: bedrock-agentcore-codebuild-sources-XXXXXXXXXXXX-us-west-2
Using .dockerignore with 44 patterns
✅ Uploaded source to S3: main/20250727-065510.zip

❌ Launch failed: An error occurred (AccessDeniedException) when calling the CreateProject operation: 
User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 
is not authorized to perform: codebuild:CreateProject on resource: 
arn:aws:codebuild:us-west-2:XXXXXXXXXXXX:project/bedrock-agentcore-main-builder 
because no identity-based policy allows the codebuild:CreateProject action
```

## 新たな進捗分析

### S3権限解決 ✅
1. **S3フルアクセス**: 正常追加
2. **S3バケット作成**: `bedrock-agentcore-codebuild-sources-XXXXXXXXXXXX-us-west-2` 成功
3. **ソースアップロード**: `main/20250727-065510.zip` S3アップロード成功
4. **.dockerignore**: 44パターンで正常動作

### 新しい権限課題 ❌
**CodeBuildプロジェクト作成権限不足**
- 必要なプロジェクト: `bedrock-agentcore-main-builder`
- 不足権限: `codebuild:CreateProject`

## CodeBuild権限追加

### 解決方法: CodeBuild権限追加

```bash
# CodeBuild開発者アクセス権限追加
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess
```

## 現在作成済みリソース

### 成功したリソース ✅
1. **ECRリポジトリ**: `XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main`
2. **IAMロール（実行用）**: `arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole`
3. **IAMロール（CodeBuild用）**: `arn:aws:iam::XXXXXXXXXXXX:role/AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3`
4. **S3バケット**: `bedrock-agentcore-codebuild-sources-XXXXXXXXXXXX-us-west-2` ⭐
5. **ソースコード**: `main/20250727-065510.zip` (S3アップロード済み) ⭐

## 次のアクション

### ステップ1: CodeBuild権限追加
```bash
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess
```

### ステップ2: 再デプロイ実行
```bash
agentcore launch --codebuild
```

## 更新された必要ポリシー一覧

**現在必要なポリシー:**
- `AmazonBedrockFullAccess` - Claude モデルの呼び出し
- `BedrockAgentCoreFullAccess` - AgentCore Runtime の利用
- `AmazonEC2ContainerRegistryFullAccess` - ECR の完全操作
- `IAMFullAccess` - IAMロール作成・管理
- `AmazonS3FullAccess` - S3バケット作成・操作 ✅
- `AWSCodeBuildDeveloperAccess` - CodeBuildプロジェクト作成・実行 ⭐**追加予定**

## CodeBuild権限未追加での再実行結果

```bash
→ agentcore launch --codebuild
Launching Bedrock AgentCore (codebuild mode)...

Starting CodeBuild ARM64 deployment for agent 'main' to account XXXXXXXXXXXX (us-west-2)
Setting up AWS resources (ECR repository, execution roles)...
Using ECR repository from config: XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main
Using execution role from config: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
✅ Execution role validation passed: arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
Preparing CodeBuild project and uploading source...
Getting or creating CodeBuild execution role for agent: main
Role name: AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
Reusing existing CodeBuild execution role: arn:aws:iam::XXXXXXXXXXXX:role/AmazonBedrockAgentCoreSDKCodeBuild-us-west-2-0d6e4079e3
Using .dockerignore with 44 patterns
✅ Uploaded source to S3: main/20250727-065948.zip

❌ Launch failed: An error occurred (AccessDeniedException) when calling the CreateProject operation: 
User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 
is not authorized to perform: codebuild:CreateProject on resource: 
arn:aws:codebuild:us-west-2:XXXXXXXXXXXX:project/bedrock-agentcore-main-builder 
because no identity-based policy allows the codebuild:CreateProject action
```

## 確認事項

### 成功継続項目 ✅
- S3バケット利用: 既存バケット使用
- ソースアップロード: `main/20250727-065948.zip` (新しいタイムスタンプ)
- .dockerignore: 44パターンで正常動作

### 依然として未解決 ❌
**CodeBuild権限が追加されていない**
- 同じエラー: `codebuild:CreateProject` 権限不足
- ユーザーにCodeBuild権限の追加が必要

## 必須アクション

### CodeBuild権限追加（必須）

```bash
# CodeBuild開発者アクセス権限追加
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess

# 権限確認
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07
```

### 権限追加後の再実行
```bash
agentcore launch --codebuild
```

## 現在のブロッカー

**CodeBuild権限不足が継続中**
- この権限を追加しないとデプロイは進まない
- 他の全てのリソース（ECR、IAM、S3）は正常

## 次の必須ステップ

1. **CodeBuild権限追加** ← **必須・最優先**
2. **再デプロイ実行**
3. **Runtime ARN取得**

## 権限確認結果 ✅

```bash
→ aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07
{
    "AttachedPolicies": [
        {
            "PolicyName": "AmazonEC2ContainerRegistryFullAccess",
            "PolicyArn": "arn:aws:iam::aws:***AWS_SECRET_ACCESS_KEY***"
        },
        {
            "PolicyName": "IAMFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/IAMFullAccess"
        },
        {
            "PolicyName": "AWSXrayFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AWSXrayFullAccess"
        },
        {
            "PolicyName": "AWSCodeBuildDeveloperAccess", ✅
            "PolicyArn": "arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess"
        },
        {
            "PolicyName": "AmazonS3FullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonS3FullAccess"
        },
        {
            "PolicyName": "CloudWatchFullAccessV2",
            "PolicyArn": "arn:aws:iam::aws:policy/CloudWatchFullAccessV2"
        },
        {
            "PolicyName": "AmazonBedrockFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
        },
        {
            "PolicyName": "BedrockAgentCoreFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess"
        }
    ]
}
```

## 権限確認完了

### 全必要ポリシー確認 ✅
- `AmazonBedrockFullAccess` ✅
- `BedrockAgentCoreFullAccess` ✅
- `AmazonEC2ContainerRegistryFullAccess` ✅
- `IAMFullAccess` ✅
- `AmazonS3FullAccess` ✅
- `AWSCodeBuildDeveloperAccess` ✅ **←確認済み**
- `CloudWatchFullAccessV2` ✅
- `AWSXrayFullAccess` ✅

## IAM権限伝播の可能性

CodeBuild権限は正しく追加されているが、AWS IAM権限の伝播に時間がかかる場合があります。

### 解決方法

#### 1. IAM権限伝播待ち（1-2分）
```bash
# 1-2分待ってから再実行
sleep 60
agentcore launch --codebuild
```

#### 2. AWS CLI設定クリア・再設定
```bash
# AWS設定キャッシュクリア
aws configure list
aws sts get-caller-identity

# 再実行
agentcore launch --codebuild
```

#### 3. 一時的にユーザーを再認証
```bash
# 一時的にアクセスキーを確認
aws sts get-caller-identity

# 認証に問題がなければ再実行
agentcore launch --codebuild
```

## 推奨アクション

すべての権限が正しく設定されているため、**そのまま `agentcore launch --codebuild` を再実行**してください。

### 実行コマンド
```bash
agentcore launch --codebuild
```

## 期待される動作

権限伝播完了後は以下の流れでデプロイが進むはずです：

1. **CodeBuildプロジェクト作成**: `bedrock-agentcore-main-builder`
2. **ビルド開始**: ARM64環境でDockerビルド
3. **ECRプッシュ**: イメージをECRにアップロード
4. **AgentRuntime作成**: BedrockでRuntime起動
5. **完了**: Runtime ARN発行

## メモ
- 日時: 2025-07-27
- 段階: 権限確認完了、デプロイ実行準備完了
- 権限状態: 全必要ポリシー確認済み ✅
- 次のアクション: `agentcore launch --codebuild` 再実行