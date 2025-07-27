# IAMロール作成権限エラーの対処法

## 発生したエラー

```bash
An error occurred (AccessDenied) when calling the CreateRole operation: 
User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 
is not authorized to perform: iam:CreateRole on resource: 
arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole 
because no identity-based policy allows the iam:CreateRole action
```

## 問題分析

### 現在の状況
- **IAMユーザー**: `stands-agentcore-memory-2025-07`
- **アカウントID**: `XXXXXXXXXXXX`
- **不足権限**: `iam:CreateRole`
- **必要なロール**: `BedrockAgentCoreExecutionRole`

### 原因
現在のIAMユーザーにIAMロール作成権限がありません。AgentCoreデプロイには専用の実行ロールが必要です。

## 解決方法

### 方法1: IAM管理権限の追加（推奨）

IAMユーザーに以下のポリシーを追加：

```
IAMFullAccess
```

**手順:**
1. AWSコンソール → IAM → ユーザー → `stands-agentcore-memory-2025-07`
2. 「許可」タブ → 「許可を追加」→ 「ポリシーを直接アタッチする」
3. `IAMFullAccess` を検索してチェック
4. 「許可を追加」をクリック

### 方法2: 最小権限カスタムポリシー（セキュリティ重視）

IAMロール管理に必要な最小限の権限のみ付与：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:GetRole",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy",
                "iam:ListAttachedRolePolicies",
                "iam:PassRole",
                "iam:DeleteRole"
            ],
            "Resource": [
                "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
                "arn:aws:iam::XXXXXXXXXXXX:role/BedrockMemoryExecutionRole"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:ListPolicies",
                "iam:GetPolicy"
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
4. ポリシー名: `StrandsAgentCoreIAMAccess`
5. 「ポリシーを作成」
6. ユーザーにアタッチ

### 方法3: AWS管理者に依頼

もしセキュリティポリシーで制限がある場合、AWS管理者に以下のロール作成を依頼：

```bash
# 管理者に実行してもらうコマンド
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

# ロールARNを取得
aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
```

## 権限確認

### 現在の権限チェック
```bash
# アタッチされているポリシー確認
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07

# IAMロール作成権限テスト
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 \
    --action-names iam:CreateRole \
    --resource-arns "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole"
```

## 代替アプローチ: 既存ロールの確認

もしかすると、組織で既にロールが存在している可能性があります：

```bash
# 既存のBedrockロールを検索
aws iam list-roles --query 'Roles[?contains(RoleName, `Bedrock`) || contains(RoleName, `AgentCore`)].{RoleName:RoleName,Arn:Arn}'

# 特定ロール名で確認
aws iam get-role --role-name BedrockAgentCoreExecutionRole 2>/dev/null || echo "ロールが存在しません"
```

## 修正後の実行手順

権限追加後、以下のコマンドを再実行：

```bash
# IAMロール作成
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

# 成功時の出力確認
echo "ロール作成成功。ARN:"
aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
```

## 更新された必要ポリシー一覧

**現在必要なポリシー:**
- `AmazonBedrockFullAccess` - Claude モデルの呼び出し
- `BedrockAgentCoreFullAccess` - AgentCore Runtime の利用
- `AmazonEC2ContainerRegistryFullAccess` - ECR の完全操作
- `IAMFullAccess` - IAMロール作成・管理 ⭐**追加**

**推奨ポリシー:**
- `CloudWatchFullAccessV2` - ログ出力と監視
- `AWSXRayDaemonWriteAccess` - 分散トレーシング

## CodeBuild関連権限（次に必要になる可能性）

AgentCoreデプロイ時に追加で必要になる可能性がある権限：

```
AWSCodeBuildDeveloperAccess
```

## 次のアクション

1. **権限修正** - IAMFullAccess または カスタムポリシー追加
2. **IAMロール作成** - BedrockAgentCoreExecutionRole
3. **ポリシーアタッチ** - 必要な権限をロールに付与
4. **AgentCore設定** - ロールARNを指定
5. **デプロイ実行**

## メモ
- 日時: 2025-07-27
- 段階: IAMロール作成フェーズ
- 必要な権限が段階的に判明
- セキュリティ vs 利便性のバランス考慮が必要