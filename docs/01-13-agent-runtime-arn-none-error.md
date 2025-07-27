# AgentCore Runtime ARN が None エラー - 環境変数未設定

## 問題の状況

```bash
エラーが発生しました: Parameter validation failed: Invalid type for parameter agentRuntimeArn, value: None, type: <class 'NoneType'>, valid types: <class 'str'>
```

## 原因分析

**環境変数 AGENT_RUNTIME_ARN が正しく読み込まれていない**
- .envファイルが存在しない、または内容が不正
- 環境変数の設定が反映されていない
- フロントエンドアプリが環境変数を正しく取得できていない

## 解決方法

### ステップ1: .envファイルの存在確認

```bash
# プロジェクトルートに移動
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory

# .envファイル確認
ls -la .env

# .envファイル内容確認
cat .env
```

### ステップ2: .envファイル作成/更新

```bash
# プロジェクトルートで.envファイル作成
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory

cat > .env << 'EOF'
# AWS認証情報
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_DEFAULT_REGION=us-west-2

# AgentCore Runtime ARN（実際の値）
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO

# メモリ実行ロールARN
MEMORY_EXECUTION_ROLE_ARN=arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

# オプション: ECR情報
ECR_URI=XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main:latest
EOF
```

### ステップ3: 環境変数の動的取得

AWS認証情報を動的に取得して.envに設定：

```bash
# AWS認証情報を動的に取得
AWS_ACCESS_KEY=$(aws configure get aws_access_key_id)
AWS_SECRET_KEY=$(aws configure get aws_secret_access_key)

# .envファイル更新
cat > .env << EOF
# AWS認証情報
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_KEY}
AWS_DEFAULT_REGION=us-west-2

# AgentCore Runtime ARN
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO

# メモリ実行ロールARN
MEMORY_EXECUTION_ROLE_ARN=arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
EOF
```

### ステップ4: .envファイル内容確認

```bash
# .envファイルの内容確認
cat .env

# 各環境変数の確認
echo "AWS_ACCESS_KEY_ID: $(grep AWS_ACCESS_KEY_ID .env)"
echo "AGENT_RUNTIME_ARN: $(grep AGENT_RUNTIME_ARN .env)"
```

### ステップ5: Python での環境変数読み込み確認

```bash
# フロントエンドディレクトリで環境変数テスト
cd frontend

python3 -c "
import os
from dotenv import load_dotenv

# .envファイル読み込み
load_dotenv('../.env')

# 環境変数確認
print('AGENT_RUNTIME_ARN:', os.getenv('AGENT_RUNTIME_ARN'))
print('AWS_DEFAULT_REGION:', os.getenv('AWS_DEFAULT_REGION'))
print('AWS_ACCESS_KEY_ID:', os.getenv('AWS_ACCESS_KEY_ID', 'Not set'))
"
```

### ステップ6: Streamlit アプリの再起動

```bash
# 既存のStreamlitプロセス停止（Ctrl+C）
# その後再起動

cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/frontend
streamlit run app.py
```

## デバッグ用確認

### 環境変数が None になる原因確認

```bash
# 1. .envファイルの場所確認
find /Users/uchinishi.koichi/train/handson/strands-agentcore-memory -name ".env" -type f

# 2. .envファイルの権限確認
ls -la /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/.env

# 3. .envファイルの内容確認
cat /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/.env

# 4. python-dotenvのインストール確認
pip list | grep python-dotenv
```

### フロントエンドコードの確認

```bash
# app.pyでの環境変数読み込み部分確認
grep -n "AGENT_RUNTIME_ARN" app.py
grep -n "load_dotenv" app.py
```

## 一時的な回避策

### 環境変数の直接設定

```bash
# ターミナルで直接環境変数設定
export AGENT_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO"
export AWS_DEFAULT_REGION="us-west-2"
export AWS_ACCESS_KEY_ID="$(aws configure get aws_access_key_id)"
export AWS_SECRET_ACCESS_KEY="$(aws configure get aws_secret_access_key)"

# 設定確認
echo $AGENT_RUNTIME_ARN

# Streamlit起動
cd frontend
streamlit run app.py
```

## app.py の環境変数読み込み部分修正

必要に応じてapp.pyの環境変数読み込みを確認・修正：

```python
import os
from dotenv import load_dotenv

# .envファイルのパス指定（プロジェクトルートから）
load_dotenv('../.env')

# 環境変数取得（デフォルト値付き）
AGENT_RUNTIME_ARN = os.getenv('AGENT_RUNTIME_ARN')
if not AGENT_RUNTIME_ARN:
    st.error("AGENT_RUNTIME_ARN が設定されていません。.env ファイルを確認してください。")
    st.stop()
```

## よくある問題と解決策

### 1. .envファイルの場所間違い
```bash
# 正しい場所: プロジェクトルート
/Users/uchinishi.koichi/train/handson/strands-agentcore-memory/.env

# 間違った場所: frontendディレクトリ
/Users/uchinishi.koichi/train/handson/strands-agentcore-memory/frontend/.env
```

### 2. 相対パスの問題
```python
# app.py での正しい .env 読み込み
load_dotenv('../.env')  # frontendから見たプロジェクトルート

# または絶対パス
load_dotenv('/Users/uchinishi.koichi/train/handson/strands-agentcore-memory/.env')
```

### 3. AWS認証情報の動的取得失敗
```bash
# AWS CLI設定確認
aws configure list

# 認証情報手動設定
aws configure set aws_access_key_id YOUR_ACCESS_KEY
aws configure set aws_secret_access_key YOUR_SECRET_KEY
aws configure set default.region us-west-2
```

## 成功確認

### 環境変数正常読み込み確認
```bash
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv('../.env')
arn = os.getenv('AGENT_RUNTIME_ARN')
print('Success!' if arn and arn.startswith('arn:aws:bedrock-agentcore') else 'Failed!')
print('ARN:', arn)
"
```

### Streamlit 正常起動確認
- エラーメッセージが表示されない
- ブラウザでhttp://localhost:8501にアクセス可能
- チャット機能が利用可能

## 推奨解決手順

### 1. .env ファイル確認・作成
```bash
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory
cat > .env << 'EOF'
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_DEFAULT_REGION=us-west-2
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
MEMORY_EXECUTION_ROLE_ARN=arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
EOF
```

### 2. 環境変数確認
```bash
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv('.env')
print('AGENT_RUNTIME_ARN:', os.getenv('AGENT_RUNTIME_ARN'))
"
```

### 3. Streamlit 再起動
```bash
cd frontend
streamlit run app.py
```

## 解決完了 ✅

### 修正内容
1. **frontend/app.py に環境変数読み込み追加**:
   ```python
   import os
   from dotenv import load_dotenv
   
   # .envファイルから環境変数を読み込み
   load_dotenv('../.env')
   ```

2. **.envファイル確認**:
   ```
   AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
   ```

3. **環境変数読み込み確認**:
   ```bash
   python3 -c "
   from dotenv import load_dotenv
   import os
   load_dotenv('../.env')
   print('AGENT_RUNTIME_ARN:', os.getenv('AGENT_RUNTIME_ARN'))
   "
   # 出力: AGENT_RUNTIME_ARN: arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
   ```

### 動作確認
- ✅ .envファイル存在確認
- ✅ 環境変数正常読み込み
- ✅ AGENT_RUNTIME_ARN が正しく取得

## メモ
- 日時: 2025-07-27
- 段階: AgentCore Runtime ARN環境変数エラー解決完了 ✅
- 問題: フロントエンドで load_dotenv() が呼ばれていなかった
- 解決策: app.py に load_dotenv('../.env') 追加