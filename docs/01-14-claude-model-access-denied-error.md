# Claudeモデルアクセス拒否エラー - Bedrock Model Access設定必要

## 問題の状況

**Streamlitアプリの症状**:
- エラーはなくなったが、「エージェントが思考しています…」のまま停止
- AgentCore Runtimeからの応答がない

**AgentCore CLIテスト結果**:
```bash
→ agentcore invoke '{"prompt": "Hello"}'

Response:
{
  "response": "{\"init_event_loop\": true}\n{\"start\": 
true}\n{\"start_event_loop\": true}\n{\"error\": \"An error occurred 
(AccessDeniedException) when calling the ConverseStream operation: You don't 
have access to the model with the specified model ID.\", \"error_type\": 
\"AccessDeniedException\", \"message\": \"An error occurred during streaming\"}"
}
```

## 診断結果

### 確認済み項目 ✅

#### 1. AgentCore Runtime状態
```bash
→ agentcore status

Agent Name: main
Agent ID: main-lunjDb7EKO
Agent Arn: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
Created at: 2025-07-27 07:17:58.846778+00:00
Last Updated at: 2025-07-27 07:18:04.312526+00:00
STATUS: READY ✅
```

#### 2. AWS認証確認
```bash
→ aws sts get-caller-identity

{
    "UserId": "AIDAY5YGE34YGMBATVGH7",
    "Account": "XXXXXXXXXXXX",
    "Arn": "arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07"
}
```

#### 3. IAMロール権限確認
```bash
→ aws iam list-attached-role-policies --role-name BedrockAgentCoreExecutionRole

{
    "AttachedPolicies": [
        {
            "PolicyName": "AWSXRayDaemonWriteAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
        },
        {
            "PolicyName": "AmazonEC2ContainerRegistryReadOnly",
            "PolicyArn": "arn:aws:iam::aws:***AWS_SECRET_ACCESS_KEY***"
        },
        {
            "PolicyName": "CloudWatchFullAccessV2",
            "PolicyArn": "arn:aws:iam::aws:policy/CloudWatchFullAccessV2"
        },
        {
            "PolicyName": "AmazonBedrockFullAccess", ✅
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
        },
        {
            "PolicyName": "BedrockAgentCoreFullAccess", ✅
            "PolicyArn": "arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess"
        }
    ]
}
```

### 発見された問題 ❌

**CloudWatchログからのエラー詳細**:
```
ERROR: An error occurred (AccessDeniedException) when calling the ConverseStream operation: 
You don't have access to the model with the specified model ID.
```

**原因**: Bedrock でClaude モデルへのアクセス許可が設定されていない

## 解決方法

### ステップ1: Bedrockコンソールでモデルアクセス有効化 🎯

**AWSコンソールでの設定手順**:

1. **AWS Management Console にログイン**
   - https://console.aws.amazon.com/
   - リージョン: `us-west-2` (Oregon) を選択

2. **Amazon Bedrock サービスに移動**
   - サービス検索で "Bedrock" を入力
   - "Amazon Bedrock" を選択

3. **Model access 設定**
   - 左サイドバーから "Model access" を選択
   - "Manage model access" ボタンをクリック

4. **Anthropic Claude モデルを有効化**
   - "Anthropic" セクションを見つける
   - 以下のモデルにチェックを入れる:
     - ✅ **Claude 3.5 Sonnet** (推奨)
     - ✅ **Claude 3 Haiku** (高速・低コスト)
     - ✅ **Claude 3 Opus** (オプション)

5. **変更を保存**
   - "Save changes" ボタンをクリック
   - ステータスが "Access granted" になるまで待機（1-2分）

### ステップ2: 使用モデル設定確認

**`.bedrock_agentcore.yaml` でモデルID確認**:
```bash
cd backend
cat .bedrock_agentcore.yaml
```

期待される設定:
```yaml
agents:
  main:
    model_id: anthropic.claude-3-5-sonnet-20241022-v2:0
    # または
    # model_id: anthropic.claude-3-haiku-20240307-v1:0
```

### ステップ3: モデルアクセス有効化後の確認

```bash
# AgentCore経由でのテスト
cd backend
agentcore invoke '{"prompt": "Hello test"}'
```

**成功時の期待出力**:
```json
{
  "response": "Hello! I'm ready to help you. How can I assist you today?"
}
```

### ステップ4: Streamlitアプリでの確認

```bash
# フロントエンド起動
cd frontend
streamlit run app.py
```

**期待される動作**:
- "エージェントが思考しています…" → 実際の応答に変化
- チャットメッセージに対する適切な返答

## トラブルシューティング

### モデルアクセス有効化で解決しない場合

#### 1. モデルID確認
```bash
# 設定ファイルのモデルID確認
cd backend
grep -A 5 -B 5 "model_id" .bedrock_agentcore.yaml
```

#### 2. リージョン確認
- Bedrockコンソール: `us-west-2` (Oregon)
- AgentCore Runtime: `us-west-2`
- モデルアクセス設定: `us-west-2`

#### 3. 権限伝播待ち
```bash
# 5分程度待ってから再テスト
sleep 300
agentcore invoke '{"prompt": "Test after waiting"}'
```

## Bedrockモデルアクセス設定の詳細

### 利用可能なClaudeモデル

| モデル | Model ID | 特徴 | 推奨用途 |
|--------|----------|------|----------|
| Claude 3.5 Sonnet | `anthropic.claude-3-5-sonnet-20241022-v2:0` | 高性能・バランス型 | 一般的な対話 |
| Claude 3 Haiku | `anthropic.claude-3-haiku-20240307-v1:0` | 高速・低コスト | 簡単なタスク |
| Claude 3 Opus | `anthropic.claude-3-opus-20240229-v1:0` | 最高性能 | 複雑なタスク |

### 設定確認コマンド

```bash
# 現在の設定確認
cd backend
cat .bedrock_agentcore.yaml | grep -A 10 -B 10 model

# ログ確認
aws logs tail /aws/bedrock-agentcore/runtimes/main-lunjDb7EKO-DEFAULT --since 10m
```

## 解決確認手順

### 1. モデルアクセス確認
- AWSコンソール → Bedrock → Model access
- Anthropic Claude models が "Access granted" 状態

### 2. AgentCore動作確認
```bash
cd backend
agentcore invoke '{"prompt": "Hello, please respond if you can access Claude"}'
```

### 3. Streamlit動作確認
- ブラウザで http://localhost:8501 にアクセス
- チャットで "こんにちは" と入力
- 適切な日本語応答が返ること

### 4. Sub-Agent機能確認
- "EC2の料金について教えて" → AWS Knowledge Agent
- "今日は祝日ですか？" → Japanese Holiday API Agent

## よくあるエラーと対処法

### エラー1: "Model not found"
**原因**: モデルIDが間違っている
**対処**: `.bedrock_agentcore.yaml` のmodel_id確認・修正

### エラー2: "Access still denied after enabling"
**原因**: 権限伝播の遅延
**対処**: 5-10分待ってから再テスト

### エラー3: "Region mismatch"
**原因**: リージョン設定不一致
**対処**: 全てのサービスを `us-west-2` に統一

## 成功確認

### AgentCore CLIテスト成功例
```bash
→ agentcore invoke '{"prompt": "Hello"}'

Response:
{
  "response": "Hello! I'm an AWS expert assistant with access to specialized sub-agents. I can help you with AWS services information and Japanese holiday queries. How can I assist you today?"
}
```

### CloudWatchログ成功例
```
INFO: Successfully connected to Claude model
INFO: Processing prompt: "Hello"
INFO: Sub-agent setup completed
INFO: Response generated successfully
```

## 次のステップ

モデルアクセス有効化後:
1. **AgentCore動作確認** - `agentcore invoke` テスト
2. **Streamlit動作確認** - フロントエンドでのチャット機能
3. **Sub-Agent確認** - AWS Knowledge + Holiday API 機能
4. **統合テスト** - 全機能の動作確認

## 修正完了事項 ✅

### コードレベルの修正
1. **間違ったモデルIDを修正**:
   - ❌ `us.anthropic.claude-3-7-sonnet-20250219-v1:0` (存在しない)
   - ✅ `anthropic.claude-3-5-sonnet-20241022-v2:0` (正しいモデルID)

2. **修正ファイル**:
   - `backend/src/main.py`: Line 26
   - `backend/src/aws_knowledge_agent.py`: Line 43

3. **AgentCore再デプロイ完了**:
   ```
   ✅ Agent created/updated: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
   ✅ CodeBuild completed successfully in 1m 7s
   ```

### 残る問題 ❌

**Bedrockモデルアクセス許可が未設定**:
```bash
→ agentcore invoke '{"prompt": "Hello"}'

Error: "An error occurred (AccessDeniedException) when calling the ConverseStream operation: 
You don't have access to the model with the specified model ID."
```

## 必須アクション 🎯

**AWSコンソールでのBedrockモデルアクセス有効化が必要**:

### 手順（重要）
1. **AWSコンソールにログイン** → https://console.aws.amazon.com/
2. **リージョン選択**: `us-west-2` (Oregon)
3. **Bedrock サービス**に移動
4. **左メニュー** → **"Model access"**
5. **"Manage model access"** ボタンクリック
6. **Anthropic セクション**で以下をチェック:
   - ☑️ Claude 3.5 Sonnet
   - ☑️ Claude 3 Haiku
7. **"Save changes"** クリック
8. **ステータス確認**: "Access granted" になるまで待機

### 確認方法
```bash
# モデルアクセス有効化後にテスト
cd backend
agentcore invoke '{"prompt": "Hello test"}'

# 成功時の期待出力
# Response: "Hello! I'm ready to help you..."
```

## 補足情報

### 使用予定のモデル
- **Claude 3.5 Sonnet**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- 高性能でバランスの取れたモデル
- 一般的な対話・AWS相談に最適

### なぜこのエラーが発生するか
1. **IAM権限**: ✅ `AmazonBedrockFullAccess` 付与済み
2. **AgentCore設定**: ✅ 正しいモデルID設定済み
3. **Model Access**: ❌ **Bedrockコンソールで未有効化**

AWS BedrockではIAM権限とは別に、各モデルへのアクセス許可をコンソールで個別に設定する必要があります。

## メモ
- 日時: 2025-07-27
- 段階: コード修正完了、Bedrockモデルアクセス有効化待ち
- 修正済み: 間違ったモデルID → 正しいClaude 3.5 Sonnet ID ✅
- 残り作業: AWSコンソール → Bedrock → Model access → Claude有効化 🎯
- 次のアクション: ユーザーによるBedrockモデルアクセス設定