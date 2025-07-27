# IAM権限伝播問題 - CodeBuild権限エラー継続

## 問題の状況

権限確認では `AWSCodeBuildDeveloperAccess` が正しく追加されているにも関わらず、CodeBuildプロジェクト作成時にまだアクセス拒否が発生しています。

```bash
→ agentcore launch --codebuild
❌ Launch failed: An error occurred (AccessDeniedException) when calling the CreateProject operation: 
User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 
is not authorized to perform: codebuild:CreateProject on resource: 
arn:aws:codebuild:us-west-2:XXXXXXXXXXXX:project/bedrock-agentcore-main-builder 
because no identity-based policy allows the codebuild:CreateProject action
```

## 根本原因分析

### 可能な原因
1. **IAM権限伝播の遅延**: AWS IAMの権限変更が完全に反映されるまで時間がかかる
2. **AWS CLIキャッシュ**: ローカルのAWS認証情報キャッシュが古い
3. **ポリシー条件**: `AWSCodeBuildDeveloperAccess` に特定の条件がある可能性

## 解決方法

### 方法1: IAM権限伝播待ち（5-10分）

```bash
# 5分待機してから再実行
echo "IAM権限伝播のため5分待機中..."
sleep 300
agentcore launch --codebuild
```

### 方法2: AWS CLI認証情報更新

```bash
# 現在の認証情報確認
aws sts get-caller-identity

# AWS設定確認
aws configure list

# 認証情報を明示的に更新
aws configure get aws_access_key_id
aws configure get aws_secret_access_key

# 再実行
agentcore launch --codebuild
```

### 方法3: より具体的なCodeBuild権限ポリシー作成

`AWSCodeBuildDeveloperAccess` が期待通りに動作しない場合、カスタムポリシーを作成：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "codebuild:CreateProject",
                "codebuild:UpdateProject",
                "codebuild:BatchGetProjects",
                "codebuild:StartBuild",
                "codebuild:BatchGetBuilds",
                "codebuild:StopBuild",
                "codebuild:ListProjects",
                "codebuild:ListBuilds"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::XXXXXXXXXXXX:role/AmazonBedrockAgentCoreSDKCodeBuild-*"
            ]
        }
    ]
}
```

**カスタムポリシー作成手順:**
```bash
# ポリシーファイル作成
cat > codebuild-custom-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "codebuild:CreateProject",
                "codebuild:UpdateProject",
                "codebuild:BatchGetProjects",
                "codebuild:StartBuild",
                "codebuild:BatchGetBuilds",
                "codebuild:StopBuild",
                "codebuild:ListProjects",
                "codebuild:ListBuilds"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::XXXXXXXXXXXX:role/AmazonBedrockAgentCoreSDKCodeBuild-*"
            ]
        }
    ]
}
EOF

# カスタムポリシー作成
aws iam create-policy \
    --policy-name StrandsAgentCoreCodeBuildAccess \
    --policy-document file://codebuild-custom-policy.json

# カスタムポリシーアタッチ
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::XXXXXXXXXXXX:policy/StrandsAgentCoreCodeBuildAccess
```

### 方法4: AWSCodeBuildFullAccess使用

より包括的な権限で試行：

```bash
# より強い権限を一時的に追加
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess

# 再実行
agentcore launch --codebuild
```

## デバッグ用確認コマンド

### 権限の詳細確認
```bash
# 現在のユーザー確認
aws sts get-caller-identity

# アタッチされたポリシー確認
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07

# CodeBuild関連権限のシミュレーション
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 \
    --action-names codebuild:CreateProject \
    --resource-arns "arn:aws:codebuild:us-west-2:XXXXXXXXXXXX:project/bedrock-agentcore-main-builder"
```

### CodeBuildサービス確認
```bash
# CodeBuildサービス利用可能性確認
aws codebuild list-projects --region us-west-2

# 既存プロジェクト確認
aws codebuild batch-get-projects --names bedrock-agentcore-main-builder --region us-west-2 2>/dev/null || echo "プロジェクト未存在"
```

## 推奨解決順序

### 1. まずは時間待ち（推奨）
```bash
# 10分待機
echo "IAM権限伝播のため10分待機..."
sleep 600
agentcore launch --codebuild
```

### 2. それでも失敗する場合
```bash
# より強い権限を追加
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess

# 再実行
agentcore launch --codebuild
```

## 一時的な回避策

もしCodeBuildが継続して問題となる場合、以下の代替手段も検討可能：

1. **手動でCodeBuildプロジェクト作成**
2. **異なるデプロイ方法使用** (CodeBuildを使わない方法)
3. **AWS管理者に権限確認依頼**

## 次のアクション

1. **10分待機** してから再実行
2. 失敗する場合は **AWSCodeBuildAdminAccess** 追加
3. それでも失敗する場合は **カスタムポリシー** 作成

## 5分待機後の結果

```bash
→ echo "IAM権限伝播のため5分待機中..."
sleep 300
agentcore launch --codebuild
IAM権限伝播のため5分待機中...

❌ Launch failed: An error occurred (AccessDeniedException) when calling the CreateProject operation: 
User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 
is not authorized to perform: codebuild:CreateProject on resource: 
arn:aws:codebuild:us-west-2:XXXXXXXXXXXX:project/bedrock-agentcore-main-builder 
because no identity-based policy allows the codebuild:CreateProject action
```

## 時間待ちでも解決せず ❌

5分間待機しても同じエラーが継続。IAM権限の問題が伝播遅延ではなく、ポリシー条件やより根本的な問題である可能性が高い。

## 次の解決策: より強い権限の追加

### AWSCodeBuildAdminAccess追加

```bash
# より包括的なCodeBuild権限を追加
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess

# 権限確認
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07

# 再実行
agentcore launch --codebuild
```

### 代替案: カスタムポリシーの作成

もしAWSCodeBuildAdminAccessでも解決しない場合：

```bash
# カスタムポリシーファイル作成
cat > codebuild-explicit-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "aws:RequestedRegion": "us-west-2"
                }
            }
        }
    ]
}
EOF

# ポリシー作成
aws iam create-policy \
    --policy-name StrandsAgentCoreFullAccess \
    --policy-document file://codebuild-explicit-policy.json

# ポリシーアタッチ
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::XXXXXXXXXXXX:policy/StrandsAgentCoreFullAccess
```

### 権限確認コマンド

```bash
# 権限シミュレーション詳細確認
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07 \
    --action-names codebuild:CreateProject \
    --resource-arns "arn:aws:codebuild:us-west-2:XXXXXXXXXXXX:project/bedrock-agentcore-main-builder" \
    --region us-west-2

# 現在のポリシー詳細確認
aws iam get-policy --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess
```

## 推奨アクション

1. **AWSCodeBuildAdminAccess**を追加して再試行
2. それでも失敗する場合は**カスタムポリシー**を作成
3. **AWS管理者に相談**（企業環境の場合）

## メモ
- 日時: 2025-07-27
- 段階: IAM権限伝播問題（時間待ち失敗）
- 問題: 5分待機後も同じエラー継続
- 原因: ポリシー条件またはより根本的な権限問題
- 次の対策: より強い権限（AWSCodeBuildAdminAccess）の追加