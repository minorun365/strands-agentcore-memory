# ECR権限エラーの対処法

## 発生したエラー

```bash
→ aws ecr create-repository --repository-name strands-agentcore-memory

An error occurred (AccessDeniedException) when calling the CreateRepository operation: 
User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 
is not authorized to perform: ecr:CreateRepository on resource: 
arn:aws:ecr:us-west-2:XXXXXXXXXXXX:repository/strands-agentcore-memory 
because no identity-based policy allows the ecr:CreateRepository action
```

## 問題分析

### 現在の状況
- **IAMユーザー**: `stands-agentcore-memory-2025-07`
- **アカウントID**: `XXXXXXXXXXXX`
- **リージョン**: `us-west-2`
- **不足権限**: `ecr:CreateRepository`

### 原因
現在アタッチされている `AmazonEC2ContainerRegistryReadOnly` ポリシーは読み取り専用のため、リポジトリ作成権限がありません。

## 解決方法

### 方法1: 管理ポリシーの追加（推奨）

IAMユーザーに以下のポリシーを追加でアタッチ：

```
AmazonEC2ContainerRegistryFullAccess
```

**手順:**
1. AWSコンソール → IAM → ユーザー → `stands-agentcore-memory-2025-07`
2. 「許可」タブ → 「許可を追加」→ 「ポリシーを直接アタッチする」
3. `AmazonEC2ContainerRegistryFullAccess` を検索してチェック
4. 「許可を追加」をクリック

### 方法2: カスタムポリシーの作成（最小権限）

ECR操作に必要な最小限の権限のみ付与：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:CreateRepository",
                "ecr:DescribeRepositories",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload"
            ],
            "Resource": "*"
        }
    ]
}
```

**カスタムポリシー作成手順:**
1. IAM → ポリシー → 「ポリシーを作成」
2. JSONタブを選択
3. 上記のJSONをコピー&ペースト
4. ポリシー名: `StrandsAgentCoreECRAccess`
5. 「ポリシーを作成」
6. ユーザーにアタッチ

### 方法3: CLI での権限追加

```bash
# 方法1: 管理ポリシーをアタッチ
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:***AWS_SECRET_ACCESS_KEY***

# 確認
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07
```

## 権限確認

### 現在の権限確認
```bash
# アタッチされているポリシー一覧
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07

# 特定のアクション権限テスト
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 \
    --action-names ecr:CreateRepository \
    --resource-arns "arn:aws:ecr:us-west-2:XXXXXXXXXXXX:repository/strands-agentcore-memory"
```

### 必要な全権限チェック
```bash
# プロジェクトに必要な全権限をテスト
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 \
    --action-names \
        ecr:CreateRepository \
        bedrock:InvokeModel \
        bedrock-agentcore:InvokeAgentRuntime \
        bedrock-agentcore:CreateAgentRuntime \
    --resource-arns "*"
```

## 修正後の再実行

権限追加後、以下のコマンドを再実行：

```bash
# ECRリポジトリ作成
aws ecr create-repository --repository-name strands-agentcore-memory

# 成功時の出力例
# {
#     "repository": {
#         "repositoryArn": "arn:aws:ecr:us-west-2:XXXXXXXXXXXX:repository/strands-agentcore-memory",
#         "registryId": "XXXXXXXXXXXX",
#         "repositoryName": "strands-agentcore-memory",
#         "repositoryUri": "XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/strands-agentcore-memory",
#         "createdAt": "2025-07-27T..."
#     }
# }

# リポジトリURI取得
aws ecr describe-repositories \
    --repository-names strands-agentcore-memory \
    --query 'repositories[0].repositoryUri' \
    --output text
```

## 更新された必要ポリシー一覧

**必須ポリシー（修正版）:**
- `AmazonBedrockFullAccess` - Claude モデルの呼び出し
- `BedrockAgentCoreFullAccess` - AgentCore Runtime の利用
- `AmazonEC2ContainerRegistryFullAccess` - ECR の完全操作 ⭐**修正**

**推奨ポリシー:**
- `CloudWatchFullAccessV2` - ログ出力と監視
- `AWSXRayDaemonWriteAccess` - 分散トレーシング

## 次のステップ

1. 権限修正
2. ECRリポジトリ作成
3. AgentCore設定・デプロイ
4. 環境変数にARN設定

## メモ
- 日時: 2025-07-27
- 最初のポリシー設定が不完全だったため権限エラー発生
- ReadOnlyポリシーではリポジトリ作成不可
- FullAccessまたはカスタムポリシーが必要