# フロントエンドデプロイ手順

## 🎉 バックエンドデプロイ完了

Agent Runtime ARN: `arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO`

## 次のステップ: フロントエンド設定・起動

### ステップ1: 環境変数設定

プロジェクトルートで.envファイルを更新：

```bash
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory

# .envファイル更新（実際のRuntime ARNを使用）
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

### ステップ2: .envファイル確認

```bash
# .envファイルの内容確認
cat .env

# AWS認証情報が正しく設定されているか確認
echo "AWS Access Key: $(grep AWS_ACCESS_KEY_ID .env)"
echo "Agent Runtime ARN: $(grep AGENT_RUNTIME_ARN .env)"
```

### ステップ3: フロントエンド依存関係インストール

```bash
# フロントエンドディレクトリに移動
cd frontend

# 依存関係インストール
pip install -r requirements.txt
```

### ステップ4: Streamlitアプリ起動

```bash
# Streamlitアプリ起動
streamlit run app.py
```

## 期待される動作

### Streamlitアプリ起動成功時の出力
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

### ブラウザアクセス
- ローカル: http://localhost:8501
- ネットワーク: http://192.168.1.x:8501 (環境による)

## アプリケーション機能

### 主要機能
1. **AgentCore Memory Chat**: 記憶機能付きチャット
2. **Sub-Agentサポート**: 
   - AWS Knowledge MCP（AWS情報問い合わせ）
   - Japanese Holiday API（日本の祝日情報）
3. **リアルタイムストリーミング**: 応答のリアルタイム表示
4. **セッション管理**: 会話履歴の保持
5. **メモリ管理**: 長期記憶機能

### 使用方法
1. ブラウザでStreamlitアプリにアクセス
2. チャット欄にメッセージを入力
3. AgentCoreからの応答を確認
4. Sub-Agentの機能（AWS情報、祝日情報）を試用

## 動作確認方法

### 基本動作確認
```bash
# AgentCore状態確認
agentcore status

# 簡単なテスト（ターミナルから）
agentcore invoke '{"prompt": "Hello"}'
```

### ログ確認
```bash
# リアルタイムログ監視
aws logs tail /aws/bedrock-agentcore/runtimes/main-lunjDb7EKO-DEFAULT --follow

# 過去1時間のログ
aws logs tail /aws/bedrock-agentcore/runtimes/main-lunjDb7EKO-DEFAULT --since 1h
```

## トラブルシューティング

### 環境変数エラー
```bash
# .envファイルが正しく読み込まれているか確認
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('AGENT_RUNTIME_ARN:', os.getenv('AGENT_RUNTIME_ARN'))
print('AWS_DEFAULT_REGION:', os.getenv('AWS_DEFAULT_REGION'))
"
```

### AWS認証エラー
```bash
# AWS認証確認
aws sts get-caller-identity

# AgentCore設定確認
agentcore status
```

### ストリーミングエラー
- ネットワーク接続確認
- AWS Bedrock権限確認
- Runtime ARNの正確性確認

## 機能別テスト

### 1. 基本チャット機能
入力例: "こんにちは"
期待応答: AgentCoreからの挨拶

### 2. AWS Knowledge MCP
入力例: "EC2の料金について教えて"
期待応答: AWS MCP経由でのEC2情報

### 3. Japanese Holiday API
入力例: "今日は祝日ですか？"
期待応答: 祝日API経由での祝日情報

### 4. メモリ機能
入力例: "私の名前は田中です"
→ 後で "私の名前は何ですか？"
期待応答: メモリ機能による名前の記憶・回答

## 成功確認項目

- [ ] .envファイル正常作成
- [ ] フロントエンド依存関係インストール完了
- [ ] Streamlit起動成功（http://localhost:8501）
- [ ] AgentCoreとの接続確認
- [ ] 基本チャット機能動作
- [ ] Sub-Agent機能動作（AWS Knowledge, Holiday API）
- [ ] メモリ機能動作
- [ ] ストリーミング表示正常

## 完了後の状態

### バックエンド ✅
- AgentCore Runtime稼働中
- ECRイメージデプロイ済み
- CloudWatchログ出力中

### フロントエンド ✅
- Streamlitアプリ起動
- AgentCoreと接続
- 全機能利用可能

## 参考情報

### 作成されたAWSリソース
- **ECRリポジトリ**: `XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-main`
- **Agent Runtime**: `arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO`
- **S3バケット**: `bedrock-agentcore-codebuild-sources-XXXXXXXXXXXX-us-west-2`
- **CodeBuildプロジェクト**: `bedrock-agentcore-main-builder`

### 設定ファイル
- **AgentCore設定**: `.bedrock_agentcore.yaml`
- **環境変数**: `.env`
- **フロントエンド設定**: `frontend/requirements.txt`

## 次のフェーズ（オプション）

### 運用・監視
- CloudWatchダッシュボード設定
- アラート設定
- ログ分析

### 機能拡張
- 新しいSub-Agentの追加
- カスタムメモリ機能
- UI/UXの改善

## メモ
- 日時: 2025-07-27
- 段階: フロントエンドデプロイ手順準備完了
- Runtime ARN: `arn:aws:bedrock-agentcore:us-west-2:XXXXXXXXXXXX:runtime/main-lunjDb7EKO`
- 次のアクション: 環境変数設定 → 依存関係インストール → Streamlit起動