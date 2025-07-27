# AgentCore設定ファイル未存在エラー

## 発生したエラー

```bash
→ cat .agentcore/config.json
cat: .agentcore/config.json: No such file or directory
```

## 問題分析

### 現在の状況
- `.agentcore/config.json` ファイルが存在しない
- AgentCoreの設定がまだ実行されていない
- `agentcore configure` コマンドをまだ実行していない

### 原因
AgentCoreの設定手順を実行する前に設定ファイルを確認しようとしたため、ファイルが存在しません。

## 現状確認

### 1. ディレクトリ構造確認
```bash
# 現在のディレクトリ確認
pwd

# .agentcoreディレクトリの存在確認
ls -la | grep agentcore

# backendディレクトリにいるか確認
ls -la | grep -E "(src|requirements.txt)"
```

### 2. 正しいディレクトリへ移動
```bash
# プロジェクトルートの場合
cd backend

# backendディレクトリにいることを確認
ls -la
# 期待される出力: src/ requirements.txt などが表示される
```

## 正しい手順

### ステップ1: 前提条件の確認
```bash
# backendディレクトリにいることを確認
pwd
# 期待される出力: /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/backend

# 必要なファイルの存在確認
ls -la src/main.py
# 期待される出力: -rw-r--r--  1 ... src/main.py
```

### ステップ2: IAMロール問題の解決
現在、IAMロール作成権限がないため、まずこれを解決する必要があります：

```bash
# 既存ロールの確認（権限がある場合）
aws iam get-role --role-name BedrockAgentCoreExecutionRole 2>/dev/null && echo "ロール存在" || echo "ロール未作成"
```

### ステップ3: AgentCore設定の実行
IAMロール問題解決後：

```bash
# 設定実行（ロールARNは実際の値に置き換え）
agentcore configure --entrypoint src/main.py -er arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

# 設定確認
cat .agentcore/config.json
```

## 想定される設定ファイル内容

### 成功時の config.json 例
```json
{
  "entrypoint": "src/main.py",
  "execution_role_arn": "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
  "ecr_repository_uri": "XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/strands-agentcore-memory",
  "region": "us-west-2"
}
```

## トラブルシューティング

### 1. ディレクトリ問題
```bash
# 正しいディレクトリにいない場合
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/backend
```

### 2. 権限問題（IAMロール未作成）
```bash
# エラー例
# Error: Role arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole does not exist

# 解決策: 01-02のIAM権限問題を先に解決
```

### 3. エントリーポイント問題
```bash
# src/main.py が存在しない場合
ls -la src/
# main.py の存在確認

# ファイルが異なる名前の場合
find src/ -name "*.py" -type f
```

## 代替設定方法

### 手動設定ファイル作成
もしagentcore configureに問題がある場合：

```bash
# .agentcoreディレクトリ作成
mkdir -p .agentcore

# 設定ファイル手動作成
cat > .agentcore/config.json << EOF
{
  "entrypoint": "src/main.py",
  "execution_role_arn": "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
  "ecr_repository_uri": "XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/strands-agentcore-memory",
  "region": "us-west-2"
}
EOF
```

## 次のアクション手順

### 優先順位
1. **ディレクトリ確認** - backendディレクトリにいるか確認
2. **IAMロール解決** - 01-02の権限問題を解決
3. **設定実行** - `agentcore configure` の実行
4. **設定確認** - `.agentcore/config.json` の内容確認

### 実行コマンド
```bash
# 1. ディレクトリ移動と確認
cd backend && pwd && ls -la src/main.py

# 2. AgentCore設定（IAMロール解決後）
agentcore configure --entrypoint src/main.py -er arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

# 3. 設定確認
cat .agentcore/config.json
```

## ブロッカー

現在のブロッカー:
- **IAMロール権限不足**（01-02）: `iam:CreateRole` 権限が必要
- この問題を解決しないと AgentCore設定に進めない

## 追加確認結果

### ディレクトリ・ファイル確認 ✅

```bash
→ pwd
/Users/uchinishi.koichi/train/handson/strands-agentcore-memory/backend

→ ls -la | grep agentcore
-rw-r--r--@  1 uchinishi.koichi  staff  824 Jul 27 15:34 .bedrock_agentcore.yaml

→ ls -la | grep -E "(src|requirements.txt)"
-rw-r--r--@  1 uchinishi.koichi  staff   61 Jul 27 14:28 requirements.txt
drwxr-xr-x@  8 uchinishi.koichi  staff  256 Jul 27 14:28 src
```

### 重要な発見

- **正しいディレクトリ**: backend/ にいることを確認 ✅
- **必要ファイル存在**: src/ と requirements.txt 存在 ✅  
- **設定ファイル発見**: `.bedrock_agentcore.yaml` が既に存在 ⭐

### 結論

`.bedrock_agentcore.yaml` ファイルが既に存在していることから、AgentCoreの何らかの設定または初期化が既に行われている可能性があります。

## 追加確認推奨

### 1. 既存設定ファイル確認
```bash
cat .bedrock_agentcore.yaml
```

### 2. .agentcore ディレクトリ確認
```bash
ls -la .agentcore/ 2>/dev/null || echo ".agentcore ディレクトリ未存在"
```

### 3. AgentCore status 確認
```bash
agentcore status
```

## 可能性

1. **設定済み**: 既に一部設定が完了している
2. **自動生成**: インストール時に自動生成された
3. **デフォルト設定**: テンプレート設定ファイル

## メモ
- 日時: 2025-07-27
- 段階: AgentCore設定前の確認フェーズ
- 発見: `.bedrock_agentcore.yaml` ファイル存在
- 次のアクション: 既存設定ファイルの内容確認