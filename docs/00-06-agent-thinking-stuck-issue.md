# エージェント思考中フリーズ問題 - AgentCore Runtime 接続確認

## 問題の状況

**Streamlitアプリの状態**:
- ✅ 環境変数エラーは解決済み
- ✅ AGENT_RUNTIME_ARN が正常に読み込まれている
- ❌ "エージェントが思考しています…" のまま応答が停止
- ❌ AgentCore Runtime からの応答がない

## 原因分析

**可能な問題**:
1. **AgentCore Runtime の動作状態** - Runtime が正常稼働していない
2. **AWS認証問題** - boto3 クライアントの認証エラー
3. **ネットワーク接続問題** - Runtime エンドポイントへの接続失敗
4. **リクエスト形式問題** - payload や API 呼び出し形式の不備
5. **権限問題** - AgentCore 呼び出し権限不足

## 診断手順

### ステップ1: AgentCore Runtime状態確認

```bash
# AgentCore CLI でステータス確認
agentcore status

# Runtime ARN の動作確認
agentcore list

# 簡単なテスト実行
agentcore invoke '{"prompt": "Hello"}'
```

### ステップ2: AWS認証確認

```bash
# AWS認証状態確認
aws sts get-caller-identity

# Bedrock AgentCore サービス確認
aws bedrock-agentcore list-agent-runtimes --region us-west-2

# 具体的なRuntime確認
aws bedrock-agentcore get-agent-runtime \
    --agent-runtime-arn arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO \
    --region us-west-2
```

### ステップ3: CloudWatch ログ確認

```bash
# Runtime ログの確認
aws logs tail /aws/bedrock-agentcore/runtimes/main-lunjDb7EKO-DEFAULT --follow

# 過去30分のログ確認
aws logs tail /aws/bedrock-agentcore/runtimes/main-lunjDb7EKO-DEFAULT --since 30m

# エラーログの検索
aws logs filter-log-events \
    --log-group-name /aws/bedrock-agentcore/runtimes/main-lunjDb7EKO-DEFAULT \
    --filter-pattern "ERROR" \
    --start-time $(date -d "30 minutes ago" +%s)000
```

### ステップ4: フロントエンド デバッグ用修正

`frontend/app.py` にデバッグ情報を追加:

```python
# app.py の修正（デバッグ用）
import streamlit as st
import os
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv('../.env')

# デバッグ情報表示
st.sidebar.write("**デバッグ情報**")
st.sidebar.write(f"AGENT_RUNTIME_ARN: {os.getenv('AGENT_RUNTIME_ARN')}")
st.sidebar.write(f"AWS_DEFAULT_REGION: {os.getenv('AWS_DEFAULT_REGION')}")

# AWS認証確認
try:
    import boto3
    sts_client = boto3.client('sts')
    identity = sts_client.get_caller_identity()
    st.sidebar.write(f"AWS User: {identity.get('Arn', 'Unknown')}")
except Exception as e:
    st.sidebar.error(f"AWS認証エラー: {e}")
```

### ステップ5: ネットワーク接続確認

```bash
# Bedrock AgentCore エンドポイント確認
nslookup bedrock-agentcore.us-west-2.amazonaws.com

# 接続テスト（curl）
curl -I https://bedrock-agentcore.us-west-2.amazonaws.com

# AWS CLI で直接呼び出しテスト
aws bedrock-agentcore invoke-agent-runtime \
    --agent-runtime-arn arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO \
    --runtime-session-id test-session-123 \
    --payload '{"input": {"prompt": "Hello"}}' \
    --region us-west-2
```

## 修正方法

### 修正1: stream_processor.py にエラーハンドリング強化

```python
# stream_processor.py の修正
async def process_stream_interactive(user_message, main_container, agent_core_client):
    """エラーハンドリングを強化したストリーム処理"""
    
    processor = StreamlitStreamProcessor()
    session_id = st.session_state.current_thread_id
    
    # 環境変数確認
    agent_runtime_arn = os.getenv("AGENT_RUNTIME_ARN")
    if not agent_runtime_arn:
        st.error("AGENT_RUNTIME_ARN が設定されていません")
        return ""
    
    st.info(f"デバッグ: Runtime ARN = {agent_runtime_arn}")
    
    # 初期思考状態を作成
    processor._create_initial_status(main_container)
    
    # ペイロード作成
    payload = json.dumps({
        "input": {
            "prompt": user_message,
            "session_id": session_id
        }
    }).encode()
    
    st.info(f"デバッグ: Session ID = {session_id}")
    st.info(f"デバッグ: Payload = {payload.decode()}")
    
    try:
        # タイムアウト付きでAgentCore呼び出し
        agent_response = agent_core_client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            runtimeSessionId=session_id,
            payload=payload,
            qualifier="DEFAULT"
        )
        
        st.info("デバッグ: AgentCore呼び出し成功")
        
        # レスポンス処理...
        
    except Exception as e:
        st.error(f"AgentCore呼び出しエラー: {e}")
        st.error(f"エラータイプ: {type(e).__name__}")
        import traceback
        st.text(traceback.format_exc())
        return ""
```

### 修正2: boto3 クライアント設定の確認

```python
# app.py でのboto3クライアント初期化を修正
import boto3
from botocore.config import Config

# タイムアウト設定付きでクライアント作成
config = Config(
    read_timeout=300,
    connect_timeout=60,
    retries={
        'max_attempts': 3,
        'mode': 'adaptive'
    }
)

# Bedrock AgentCoreクライアントを初期化
agent_core_client = boto3.client(
    'bedrock-agentcore',
    region_name=os.getenv('AWS_DEFAULT_REGION', 'us-west-2'),
    config=config
)
```

## トラブルシューティング順序

### 1. 基本確認（最優先）
```bash
# AgentCore Runtime が稼働中か確認
agentcore status
agentcore invoke '{"prompt": "test"}'
```

### 2. CloudWatch ログ確認
```bash
# リアルタイムログ監視
aws logs tail /aws/bedrock-agentcore/runtimes/main-lunjDb7EKO-DEFAULT --follow
```

### 3. デバッグ情報追加
- app.py にデバッグ表示追加
- stream_processor.py にエラーハンドリング追加

### 4. AWS CLI テスト
```bash
# 直接API呼び出しテスト
aws bedrock-agentcore invoke-agent-runtime \
    --agent-runtime-arn arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO \
    --runtime-session-id debug-test \
    --payload '{"input": {"prompt": "Hello"}}' \
    --region us-west-2 \
    --output json
```

## よくある問題と解決策

### 問題1: Runtime が停止している
```bash
# Runtime 再起動
agentcore restart

# または再デプロイ
agentcore launch --codebuild
```

### 問題2: 権限不足
```bash
# 現在の権限確認
aws iam list-attached-user-policies --user-name stands-agentcore-memory-2025-07

# 不足している場合は BedrockAgentCoreFullAccess 確認
aws iam get-policy --policy-arn arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess
```

### 問題3: ネットワーク・タイムアウト
- boto3 設定でタイムアウトを延長
- ネットワーク接続確認
- リージョン設定確認

## 期待される正常動作

### 正常時のログ出力例
```
デバッグ: Runtime ARN = arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
デバッグ: Session ID = thread_xxxxx
デバッグ: Payload = {"input": {"prompt": "test", "session_id": "thread_xxxxx"}}
デバッグ: AgentCore呼び出し成功
```

### 正常時のCloudWatchログ例
```
[INFO] Received request for session: thread_xxxxx
[INFO] Processing prompt: test
[INFO] Response generated successfully
```

## 次のアクション

### 即座に実行すべきコマンド
1. `agentcore status` - Runtime状態確認
2. `agentcore invoke '{"prompt": "test"}'` - 基本動作確認
3. CloudWatchログ確認
4. デバッグ情報追加してStreamlit再起動

### デバッグ手順
1. **基本確認** → **ログ確認** → **コード修正** → **テスト**
2. 問題が継続する場合は Runtime 再デプロイ検討

## 診断結果 ✅

### 確認済み項目
1. **AgentCore Runtime状態**: ✅ READY
   ```
   Agent Name: main
   Agent ID: main-lunjDb7EKO
   Agent Arn: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
   STATUS: READY
   ```

2. **AWS認証**: ✅ 正常
   ```
   User: arn:aws:iam::XXXXXXXXXXXX:user/stands-agentcore-memory-2025-07
   Account: XXXXXXXXXXXX
   ```

3. **IAMロール権限**: ✅ 適切
   ```
   BedrockAgentCoreExecutionRole:
   - AmazonBedrockFullAccess ✅
   - BedrockAgentCoreFullAccess ✅
   - CloudWatchFullAccessV2 ✅
   ```

### 発見された問題 ❌

**Claudeモデルへのアクセス権限不足**:
```
Error: "An error occurred (AccessDeniedException) when calling the ConverseStream operation: 
You don't have access to the model with the specified model ID."
```

## 解決方法

### ステップ1: Bedrockコンソールでモデルアクセス有効化

**AWSコンソールでの設定**:
1. AWS Console → Bedrock → Model access
2. Anthropic Claude models を有効化
3. 特に `Claude 3.5 Sonnet` または `Claude 3 Haiku` を有効化

**または CLI での確認**（参考）:
```bash
# 利用可能なモデル確認（bedrock サービスが利用可能な場合）
aws bedrock list-foundation-models --region us-west-2

# モデルアクセス確認（bedrock サービスが利用可能な場合）
aws bedrock get-model-invocation-logging-configuration --region us-west-2
```

### ステップ2: AgentCore設定でモデル指定確認

`backend/.bedrock_agentcore.yaml` でモデル設定確認:
```yaml
agents:
  main:
    model_id: anthropic.claude-3-5-sonnet-20241022-v2:0  # または他の利用可能なモデル
```

### ステップ3: モデルアクセス有効化後の確認

```bash
# AgentCore経由でのテスト
cd backend
agentcore invoke '{"prompt": "Hello"}'
```

## 推奨アクション（優先順位順）

### 1. 最重要: Bedrockモデルアクセス有効化
- AWSコンソール → Bedrock → Model access
- Anthropic Claude models を有効化

### 2. モデル設定確認
- `.bedrock_agentcore.yaml` のmodel_id確認
- 有効化されたモデルIDと一致させる

### 3. 動作確認
- `agentcore invoke` でテスト実行
- Streamlitアプリで再テスト

## Bedrockモデルアクセス有効化手順

### AWSコンソールでの設定
1. **AWS Console にログイン**
2. **Bedrock サービスに移動**
3. **左メニューから "Model access" 選択**
4. **"Manage model access" ボタンクリック**
5. **Anthropic セクションで以下を有効化**:
   - Claude 3.5 Sonnet
   - Claude 3 Haiku  
   - Claude 3 Opus（必要に応じて）
6. **"Save changes" で保存**
7. **ステータスが "Access granted" になるまで待機**

### 有効化確認
```bash
# テスト実行
cd backend
agentcore invoke '{"prompt": "Hello test"}'

# 成功時の期待出力
# Response: "Hello! I'm ready to help..."
```

## CloudWatchログから確認されたエラー詳細

```
ERROR: An error occurred (AccessDeniedException) when calling the ConverseStream operation: 
You don't have access to the model with the specified model ID.
```

**解決後の期待ログ**:
```
INFO: Successfully connected to Claude model
INFO: Generating response for prompt: "Hello"
INFO: Response generated successfully
```

## メモ
- 日時: 2025-07-27
- 段階: AgentCore Runtime接続問題診断完了
- 問題: Claudeモデルへのアクセス権限不足 ❌
- 解決策: AWSコンソール → Bedrock → Model access → Anthropic Claude有効化 🎯