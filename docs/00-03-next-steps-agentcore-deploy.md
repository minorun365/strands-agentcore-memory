# AgentCore デプロイ手順

## 現在の状況

✅ **完了済み**:
- IAMユーザー作成: `stands-agentcore-memory-2025-07`
- 必要ポリシーアタッチ
- ECRリポジトリ作成: `strands-agentcore-memory`
- リポジトリURI取得: `XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/strands-agentcore-memory`

## 次のステップ

### ステップ1: IAMロール作成（AgentCore実行用）

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

# ロールARNを取得（後で使用）
aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
```

### ステップ2: Strands AgentCore CLI のインストール

```bash
# backendディレクトリに移動
cd backend

# 必要なパッケージをインストール
pip install strands-agents==1.0.1 bedrock-agentcore==0.1.0 bedrock-agentcore-starter-toolkit==0.1.1

# AgentCore CLIの確認
agentcore --version
```

### ステップ3: AgentCore設定

```bash
# AgentCore設定（IAMロールARNを指定）
agentcore configure --entrypoint src/main.py -er arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

# 設定確認
cat .agentcore/config.json
```

### ステップ4: AgentCoreデプロイ

```bash
# CodeBuildを使用してデプロイ
agentcore launch --codebuild

# デプロイ状況確認
agentcore status

# デプロイ完了後、Agent Runtime ARNを取得
agentcore list
```

### ステップ5: 環境変数設定

デプロイ完了後、取得したARNで.envファイルを更新：

```bash
# プロジェクトルートに移動
cd ..

# .envファイルを更新（AGENT_RUNTIME_ARNを設定）
cat > .env << EOF
# AWS認証情報
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_DEFAULT_REGION=us-west-2

# AgentCore Runtime ARN（agentcore listで取得した値に置き換え）
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:agent-runtime/YOUR_RUNTIME_ID

# オプション: メモリ実行ロール ARN
MEMORY_EXECUTION_ROLE_ARN=arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
EOF
```

### ステップ6: フロントエンド起動テスト

```bash
# 依存関係インストール
cd frontend
pip install -r requirements.txt

# Streamlitアプリ起動
streamlit run app.py
```

## 想定される出力・確認事項

### IAMロール作成成功時
```json
{
    "Role": {
        "Path": "/",
        "RoleName": "BedrockAgentCoreExecutionRole",
        "RoleId": "AROAXXXXXXXXXXXXXXXXX",
        "Arn": "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
        ...
    }
}
```

### AgentCore設定成功時
```json
{
    "entrypoint": "src/main.py",
    "execution_role_arn": "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
    "ecr_repository_uri": "XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/strands-agentcore-memory"
}
```

### AgentCoreデプロイ成功時
```
Agent Runtime deployed successfully!
Runtime ARN: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:agent-runtime/xxxxx
```

## トラブルシューティング

### よくあるエラー

#### 1. IAMロール作成エラー
```bash
# ロールが既に存在する場合
aws iam get-role --role-name BedrockAgentCoreExecutionRole
# 存在する場合はスキップして次に進む
```

#### 2. AgentCore CLI エラー
```bash
# パッケージ再インストール
pip install --upgrade strands-agents bedrock-agentcore bedrock-agentcore-starter-toolkit
```

#### 3. デプロイ権限エラー
```bash
# CodeBuild関連権限が不足している場合
aws iam attach-user-policy \
    --user-name stands-agentcore-memory-2025-07 \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess
```

#### 4. リージョン設定確認
```bash
# 現在のリージョン確認
aws configure get region

# us-west-2でない場合は設定
aws configure set region us-west-2
```

## 完了確認チェックリスト

- [ ] IAMロール作成完了
- [ ] AgentCore CLI インストール完了
- [ ] AgentCore 設定完了
- [ ] AgentCore デプロイ完了
- [ ] Agent Runtime ARN 取得完了
- [ ] .env ファイル更新完了
- [ ] Streamlit アプリ起動確認

## 次のドキュメント予定

デプロイ完了後：
- `00-04-frontend-testing.md` - フロントエンドテスト手順
- `01-02-deploy-results.md` - デプロイ結果とARN情報