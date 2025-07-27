# 環境変数設定手順

## 概要

このプロジェクトを動作させるために必要な環境変数の取得・設定手順を説明します。AWS Bedrock AgentCoreとメモリ機能を使用するため、適切なAWS認証とIAM権限の設定が必要です。

## 必要な環境変数一覧

### 必須環境変数

```bash
# AWS基本認証
AWS_ACCESS_KEY_ID=<your-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-west-2

# AgentCore Runtime
AGENT_RUNTIME_ARN=<your-agent-runtime-arn>
```

### オプション環境変数

```bash
# AgentCore Memory（高度な権限管理用）
MEMORY_EXECUTION_ROLE_ARN=<your-memory-execution-role-arn>

# デバッグ用
LOG_LEVEL=INFO
```

## 環境変数取得手順

### 1. AWS認証情報の取得

#### 方法A: AWS CLIを使用（推奨）

##### 前提条件の確認

```bash
# AWS CLIのバージョン確認
aws --version

# インストールされていない場合
# macOS
brew install awscli

# または
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

##### ステップ1: 既存のAWS設定確認

```bash
# 現在のAWS設定を確認
aws configure list

# 出力例（設定済みの場合）:
#       Name                    Value             Type    Location
#       ----                    -----             ----    --------
#    profile                <not set>             None    None
# access_key     ****************ABCD  shared-credentials-file    
# secret_key     ****************xyz   shared-credentials-file    
#     region                us-west-2      config-file    ~/.aws/config

# 設定されていない場合は以下のような表示
#       Name                    Value             Type    Location
#       ----                    -----             ----    --------
#    profile                <not set>             None    None
# access_key                <not set>             None    None
# secret_key                <not set>             None    None
#     region                <not set>             None    None
```

##### ステップ2: AWS認証情報の設定場所

**オプション1: 既存のAWSアカウント設定ファイルから取得**

```bash
# 設定ファイルの場所確認
ls -la ~/.aws/

# 認証情報ファイルの内容確認（既に設定済みの場合）
cat ~/.aws/credentials

# 出力例:
# [default]
# aws_access_key_id = AKIA****************
# aws_secret_access_key = ****************************************

# 設定ファイルの内容確認
cat ~/.aws/config

# 出力例:
# [default]
# region = us-west-2
# output = json
```

**オプション2: 新しいIAMユーザーとアクセスキーを作成**

#### 2-1. 必要なポリシー一覧

このプロジェクトを動作させるために必要なポリシー：

**必須ポリシー:**
- `AmazonBedrockFullAccess` - Claude モデルの呼び出し
- `BedrockAgentCoreFullAccess` - AgentCore Runtime の利用
- `AmazonEC2ContainerRegistryReadOnly` - ECR からのコンテナイメージ取得

**推奨ポリシー:**
- `CloudWatchFullAccessV2` - ログ出力と監視
- `AWSXRayDaemonWriteAccess` - 分散トレーシング（デバッグ用）

#### 2-2. IAMユーザー作成手順

1. **AWSマネジメントコンソールにログイン**
   - https://console.aws.amazon.com/ にアクセス
   - 既存のAWSアカウントでログイン

2. **IAMサービスに移動**
   - 検索バーで「IAM」と入力
   - 「IAM」サービスを選択

3. **新しいユーザーを作成**
   - 左側メニューから「ユーザー」を選択
   - 「ユーザーを作成」ボタンをクリック
   - ユーザー名を入力（例：`strands-agentcore-dev`）
   - 「AWS マネジメントコンソールへのユーザーアクセスを提供する」をチェック（オプション）
   - 「IAM ユーザーを作成したい」を選択
   - パスワード設定（自動生成またはカスタム）
   - 「次へ」をクリック

4. **ポリシーをアタッチ**
   - 「ポリシーを直接アタッチする」を選択
   - 以下のポリシーを検索してチェック：
     - ✅ `AmazonBedrockFullAccess`
     - ✅ `BedrockAgentCoreFullAccess`
     - ✅ `AmazonEC2ContainerRegistryReadOnly`
     - ✅ `CloudWatchFullAccessV2`
     - ✅ `AWSXRayDaemonWriteAccess`
   - 「次へ」をクリック

5. **ユーザー作成の完了**
   - 設定内容を確認
   - 「ユーザーを作成」をクリック

#### 2-3. アクセスキー作成

1. **作成したユーザーを選択**
   - IAM → ユーザー → 作成したユーザー名をクリック

2. **アクセスキー作成**
   - 「セキュリティ認証情報」タブをクリック
   - 「アクセスキー」セクションで「アクセスキーを作成」をクリック
   - 「Command Line Interface (CLI)」を選択
   - 「上記の推奨事項を理解し、アクセスキーを作成します。」にチェック
   - 「次へ」をクリック

3. **タグ設定（オプション）**
   - 説明タグ（例：「Strands AgentCore Development」）を入力
   - 「アクセスキーを作成」をクリック

4. **認証情報をメモ**
   ```
   アクセスキー ID: AKIA****************
   シークレットアクセスキー: ****************************************
   ```
   **重要**: この画面を閉じると二度とシークレットキーは表示されません！

#### 2-4. 最小権限版（セキュリティ重視の場合）

より厳格な権限管理が必要な場合は、カスタムポリシーを作成：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow", 
            "Action": [
                "bedrock-agentcore:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:GetAuthorizationToken"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

**カスタムポリシー作成手順：**
1. IAM → ポリシー → ポリシーを作成
2. JSONタブを選択
3. 上記のJSONをコピー&ペースト
4. ポリシー名：`StrandsAgentCoreMinimal`
5. ポリシーを作成
6. ユーザーにこのポリシーをアタッチ

##### ステップ3: AWS CLIに認証情報を設定

```bash
# 対話的設定
aws configure

# 以下のように入力を求められます：
# AWS Access Key ID [None]: AKIA****************
# AWS Secret Access Key [None]: ****************************************
# Default region name [None]: us-west-2
# Default output format [None]: json
```

##### ステップ4: 設定の確認

```bash
# 設定確認
aws configure list

# 認証テスト
aws sts get-caller-identity

# 成功時の出力例:
# {
#     "UserId": "AIDA****************",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-username"
# }
```

##### ステップ5: 環境変数として使用

```bash
# AWS設定ファイルから環境変数を設定
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
export AWS_DEFAULT_REGION=$(aws configure get region)

# 確認
echo "Access Key: ${AWS_ACCESS_KEY_ID:0:4}***"
echo "Region: $AWS_DEFAULT_REGION"
```

#### 方法B: IAMコンソールで新しいアクセスキーを作成

1. AWS Management Consoleにログイン
2. IAM → ユーザー → 自分のユーザーを選択
3. 「セキュリティ認証情報」タブ
4. 「アクセスキーを作成」をクリック
5. 「CLI」を選択して次へ
6. Access Key IDとSecret Access Keyをメモ

### 2. IAMロールARNの取得

#### BedrockAgentCoreExecutionRole作成

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
```

#### ロールARNを取得

```bash
# 作成したロールのARNを取得
aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
```

出力例: `arn:aws:iam::123456789012:role/BedrockAgentCoreExecutionRole`

### 3. AgentCore Runtimeデプロイとarnの取得

#### ECRリポジトリ作成

```bash
# ECRリポジトリ作成
aws ecr create-repository --repository-name strands-agentcore-memory

# リポジトリURIを取得
aws ecr describe-repositories --repository-names strands-agentcore-memory --query 'repositories[0].repositoryUri' --output text
```

#### AgentCoreデプロイ

```bash
cd backend

# AgentCore設定（IAMロールARNを指定）
agentcore configure --entrypoint src/main.py -er arn:aws:iam::123456789012:role/BedrockAgentCoreExecutionRole

# デプロイ実行
agentcore launch --codebuild

# デプロイ完了後、ARNを取得
agentcore list
```

### 4. メモリ実行ロールARN取得（オプション）

#### メモリ専用ロール作成

```bash
# メモリ実行用ロール作成
aws iam create-role \
    --role-name BedrockMemoryExecutionRole \
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

# メモリ関連ポリシーをアタッチ
aws iam attach-role-policy \
    --role-name BedrockMemoryExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess

# ARNを取得
aws iam get-role --role-name BedrockMemoryExecutionRole --query 'Role.Arn' --output text
```

## 環境変数設定方法

### 方法A: .envファイル使用（開発環境推奨）

#### 自動的に.envファイルを作成

```bash
# プロジェクトルートディレクトリに移動
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory

# AWS CLIの設定から自動的に.envファイル作成
cat > .env << EOF
# AWS認証情報（aws configure から自動取得）
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_DEFAULT_REGION=$(aws configure get region)

# AgentCore Runtime ARN（後でagentcore listで取得して更新）
AGENT_RUNTIME_ARN=

# オプション: メモリ実行ロール ARN
MEMORY_EXECUTION_ROLE_ARN=
EOF

# .envファイル内容確認（機密情報をマスク）
echo "=== .env ファイルの内容確認 ==="
sed 's/AWS_SECRET_ACCESS_KEY=.*/AWS_SECRET_ACCESS_KEY=***MASKED***/' .env

# .envファイルを.gitignoreに追加（重要）
echo ".env" >> .gitignore
```

#### 手動で.envファイルを作成

```bash
# プロジェクトルートに.envファイル作成
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory

cat > .env << EOF
# AWS基本認証（実際の値に置き換えてください）
AWS_ACCESS_KEY_ID=AKIA***************
AWS_SECRET_ACCESS_KEY=********************************
AWS_DEFAULT_REGION=us-west-2

# AgentCore Runtime ARN（agentcore listで取得）
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:123456789012:agent-runtime/your-runtime-id

# オプション: メモリ実行ロールARN
MEMORY_EXECUTION_ROLE_ARN=arn:aws:iam::123456789012:role/BedrockMemoryExecutionRole
EOF

# .envファイルを.gitignoreに追加（重要）
echo ".env" >> .gitignore
```

### 方法B: シェル環境変数設定

```bash
# ~/.bashrc または ~/.zshrc に追加
export AWS_ACCESS_KEY_ID="AKIA***************"
export AWS_SECRET_ACCESS_KEY="********************************"
export AWS_DEFAULT_REGION="us-west-2"
export AGENT_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-west-2:123456789012:agent-runtime/your-runtime-id"
export MEMORY_EXECUTION_ROLE_ARN="arn:aws:iam::123456789012:role/BedrockMemoryExecutionRole"

# 設定を反映
source ~/.bashrc  # または source ~/.zshrc
```

### 方法C: 実行時指定

```bash
# フロントエンド起動時に指定
AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=xxx streamlit run frontend/app.py

# バックエンド開発時に指定
AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=xxx python backend/src/main.py
```

## 設定確認手順

### 1. AWS認証確認

```bash
# AWS認証状態確認
aws sts get-caller-identity

# 出力例:
# {
#     "UserId": "AIDA***************",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-username"
# }
```

### 2. Bedrock権限確認

```bash
# Bedrock利用可能モデル確認
aws bedrock list-foundation-models --region us-west-2

# AgentCore利用確認
aws bedrock-agentcore list-agent-runtimes --region us-west-2
```

### 3. 環境変数確認

```bash
# 設定された環境変数確認
echo "AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID:0:4}***"
echo "AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY:0:4}***"
echo "AWS_DEFAULT_REGION: $AWS_DEFAULT_REGION"
echo "AGENT_RUNTIME_ARN: $AGENT_RUNTIME_ARN"
echo "MEMORY_EXECUTION_ROLE_ARN: $MEMORY_EXECUTION_ROLE_ARN"
```

## トラブルシューティング

### よくあるエラーと対処法

#### 1. 認証エラー
```
Error: The security token included in the request is invalid
```
**対処法**: アクセスキーとシークレットキーを再確認

#### 2. 権限エラー
```
Error: User is not authorized to perform: bedrock:InvokeModel
```
**対処法**: IAMユーザーにBedrock権限を付与

#### 3. AgentCore Runtime が見つからない
```
Error: Agent runtime not found
```
**対処法**: `agentcore list`でARNを確認し、正しい値を設定

### 権限確認コマンド

```bash
# 現在の権限確認
aws iam simulate-principal-policy \
    --policy-source-arn $(aws sts get-caller-identity --query Arn --output text) \
    --action-names bedrock:InvokeModel \
    --resource-arns "*"
```

### AWS CLI設定のトラブルシューティング

#### 既存設定が無い場合

```bash
# AWS設定ディレクトリが存在しない場合
mkdir -p ~/.aws

# 設定ファイルを手動作成
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = AKIA****************
aws_secret_access_key = ****************************************
EOF

cat > ~/.aws/config << EOF
[default]
region = us-west-2
output = json
EOF
```

#### 設定ファイルの権限確認

```bash
# 設定ファイルの権限を確認（セキュリティ上重要）
ls -la ~/.aws/
# credentials ファイルは 600 (rw-------) であるべき
# config ファイルは 644 (rw-r--r--) であるべき

# 権限修正（必要に応じて）
chmod 600 ~/.aws/credentials
chmod 644 ~/.aws/config
```

#### 認証情報の取得確認

```bash
# AWS CLIから認証情報が正しく取得できるかテスト
aws configure get aws_access_key_id
aws configure get aws_secret_access_key
aws configure get region

# 出力が空の場合は設定が正しくない
```

## セキュリティ注意事項

### 重要な注意点
1. **認証情報の管理**: `.env`ファイルはGitにコミットしない
2. **最小権限の原則**: 必要最小限の権限のみ付与
3. **キーローテーション**: 定期的なアクセスキー更新
4. **ロール使用推奨**: 本番環境ではIAMロールを使用

### .gitignoreの確認

```bash
# .gitignoreに機密情報が含まれていることを確認
cat .gitignore | grep -E "\.(env|key|secret)"
```

この手順に従って環境変数を正しく設定することで、プロジェクトが正常に動作します。