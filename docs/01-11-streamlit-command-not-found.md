# Streamlit コマンド未発見エラー - 依存関係未インストール

## 問題の状況

```bash
~/train/handson/strands-agentcore-memory/frontend main
→ streamlit run app.py
zsh: command not found: streamlit
```

## 原因分析

**requirements.txtにStreamlitが含まれていない**

確認されたrequirements.txt内容:
```
boto3
bedrock-agentcore
```

問題:
- `streamlit`がrequirements.txtに記載されていない
- その他の必要な依存関係も不足
- フロントエンド用の完全な依存関係リストが必要

## 解決方法

### ステップ1: 不足している依存関係を手動インストール

仮想環境が既にアクティブな状態で、必要なパッケージを追加インストール：

```bash
# 必要なパッケージを個別インストール
pip install streamlit
pip install python-dotenv
pip install anthropic
pip install asyncio

# インストール確認
pip list | grep -E "(streamlit|dotenv|anthropic)"
```

### ステップ2: requirements.txt更新（推奨）

```bash
# 完全なrequirements.txtに更新
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/frontend

cat > requirements.txt << 'EOF'
streamlit>=1.28.0
boto3>=1.34.0
bedrock-agentcore
anthropic>=0.8.0
python-dotenv>=1.0.0
asyncio
EOF
```

### ステップ3: 更新後の依存関係インストール

```bash
# 更新されたrequirements.txtから再インストール
pip install -r requirements.txt
```

### ステップ4: インストール確認

```bash
# Streamlitインストール確認
streamlit --version

# 他の主要パッケージ確認
pip list | grep -E "(streamlit|boto3|anthropic|dotenv)"
```

### ステップ5: 環境変数設定

```bash
# プロジェクトルートの.envファイル確認
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory
cat .env
```

もし.envファイルが存在しない場合：

```bash
# .envファイル作成（実際のRuntime ARN使用）
cat > .env << 'EOF'
# AWS認証情報
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_DEFAULT_REGION=us-west-2

# AgentCore Runtime ARN
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO

# メモリ実行ロールARN
MEMORY_EXECUTION_ROLE_ARN=arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
EOF
```

### ステップ6: Streamlit起動

```bash
# フロントエンドディレクトリに戻る
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/frontend

# 仮想環境が有効か確認
which python

# Streamlitアプリ起動
streamlit run app.py
```

## 期待される成功時の出力

```bash
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501

  For better performance, install the following packages:
  - watchdog
```

## 代替方法（仮想環境なし）

### グローバルインストール（非推奨）

```bash
# システム全体にインストール（非推奨）
pip3 install -r requirements.txt

# または
python3 -m pip install -r requirements.txt
```

### Homebrewでのインストール（macOS）

```bash
# Streamlitをbrewでインストール
brew install streamlit

# その他の依存関係は別途インストール
pip3 install -r requirements.txt
```

## トラブルシューティング

### Python環境確認

```bash
# Python版数確認
python --version
python3 --version

# pip確認
pip --version
pip3 --version

# インストール場所確認
which python
which pip
```

### 権限エラーの場合

```bash
# ユーザー権限でインストール
pip install --user -r requirements.txt

# または sudo使用（非推奨）
sudo pip install -r requirements.txt
```

### requirements.txtが見つからない場合

```bash
# requirements.txtの存在確認
ls -la requirements.txt

# 内容確認
cat requirements.txt
```

予想されるrequirements.txt内容：
```
streamlit>=1.28.0
boto3>=1.34.0
anthropic>=0.8.0
python-dotenv>=1.0.0
asyncio-extras>=1.3.2
```

## 推奨の完全手順

### 1. プロジェクトルートに移動

```bash
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory
```

### 2. .env確認・作成

```bash
# .env存在確認
ls -la .env

# 存在しない場合は作成
cat > .env << 'EOF'
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
AWS_DEFAULT_REGION=us-west-2
AGENT_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO
MEMORY_EXECUTION_ROLE_ARN=arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole
EOF
```

### 3. フロントエンドディレクトリに移動

```bash
cd frontend
```

### 4. 仮想環境作成・アクティベート

```bash
python -m venv venv
source venv/bin/activate
```

### 5. 依存関係インストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Streamlit起動

```bash
streamlit run app.py
```

## 成功確認

### ブラウザアクセス
- ローカル: http://localhost:8501
- ネットワーク: http://192.168.1.x:8501

### 基本動作確認
1. Streamlitアプリが正常表示
2. チャット入力欄が利用可能
3. AgentCoreとの接続確認

## 次のアクション

1. **仮想環境作成** - 依存関係の分離
2. **依存関係インストール** - requirements.txtから一括インストール
3. **環境変数確認** - .envファイルの存在・内容確認
4. **Streamlit起動** - アプリ起動・ブラウザアクセス

## エラー発生時の確認項目

- [ ] Python/pip のバージョン
- [ ] requirements.txt の存在
- [ ] 仮想環境の作成・アクティベート
- [ ] 依存関係インストール完了
- [ ] .envファイルの存在・内容
- [ ] 作業ディレクトリの確認

## メモ
- 日時: 2025-07-27
- 段階: Streamlitコマンド未発見エラー解決
- 問題: 依存関係未インストール
- 解決策: 仮想環境作成 → 依存関係インストール → Streamlit起動