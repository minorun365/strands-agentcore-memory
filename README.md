# Strands on AgentCore with Streamlit（メモリ対応版）

※AgentCore Memory周りの実装はだいぶ雑なので、お試し程度でお願いします！

<img width="1382" height="649" alt="スクリーンショット 2025-07-24 18 05 07" src="https://github.com/user-attachments/assets/c2f72236-4db8-4f20-832b-594bbb020cb6" />


## エージェント構成（サンプル）

- Supervisor
  - サブエージェント1（AWS Knowledge MCP）
  - サブエージェント2（日本の祝日API）


## 構築手順

### 環境変数のセット

```sh
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_DEFAULT_REGION=xxx
```

### ECRプライベートリポジトリ作成

```sh
aws ecr create-repository --repository-name <好きな名前>
```

### IAMポリシー作成

```sh
# ロールと信頼ポリシーを作成
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
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn
arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn
arn:aws:iam::aws:policy/AmazonBedrockFullAccess
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn
arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn
arn:aws:iam::aws:policy/CloudWatchFullAccessV2
aws iam attach-role-policy --role-name BedrockAgentCoreExecutionRole --policy-arn
arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess
```

### AgentCoreにデプロイ

```sh
cd backend
pip install strands-agents=1.0.1 bedrock-agentcore==0.1.0 bedrock-agentcore-starter-toolkit==0.1.1

# ビルド
agentcore configure --entrypoint src/server.py -er <IAMロールのARN>

# デプロイ
agentcore launch --codebuild
```

### クライアントを起動

```sh
cd ..
pip install streamlit
streamlit run frontend/app.py
```
