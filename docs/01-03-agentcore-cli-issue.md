# AgentCore CLI バージョン確認エラー

## 発生したエラー

```bash
→ agentcore --version
Usage: agentcore [OPTIONS] COMMAND [ARGS]...
Try 'agentcore --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────────────────╮
│ No such option: --version                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

## 問題分析

### 現在の状況
- AgentCore CLI はインストールされている
- `--version` オプションが存在しない
- CLIのコマンド構造が想定と異なる

### 原因
AgentCore CLIのバージョンまたはインターフェースが想定と異なる可能性があります。

## 対処法

### 1. 正しいヘルプの確認

```bash
# 利用可能なコマンドとオプションを確認
agentcore --help

# より詳細な情報
agentcore help
```

### 2. 代替バージョン確認方法

```bash
# pipでインストール済みパッケージ確認
pip list | grep -E "(bedrock|agentcore|strands)"

# 具体的なバージョン確認
pip show bedrock-agentcore
pip show bedrock-agentcore-starter-toolkit
pip show strands-agents
```

### 3. AgentCore CLI機能確認

```bash
# 利用可能なコマンド一覧
agentcore

# 設定関連コマンド確認
agentcore configure --help

# デプロイ関連コマンド確認
agentcore launch --help
```

## 期待される出力

### agentcore --help の例
```
Usage: agentcore [OPTIONS] COMMAND [ARGS]...

Commands:
  configure  Configure agent runtime
  launch     Launch/deploy agent runtime
  list       List deployed runtimes
  status     Check runtime status
  logs       View runtime logs
  destroy    Remove runtime
```

### pip list の例
```
bedrock-agentcore              0.1.0
bedrock-agentcore-starter-toolkit  0.1.1
strands-agents                 1.0.1
```

## 次のステップ

### まずは現状確認
```bash
# 1. ヘルプ確認
agentcore --help

# 2. インストール済みパッケージ確認
pip list | grep -E "(bedrock|agentcore|strands)"

# 3. 直接設定コマンド試行
agentcore configure --help
```

### もしコマンドが異なる場合
```bash
# パッケージの再インストール
pip uninstall bedrock-agentcore bedrock-agentcore-starter-toolkit strands-agents
pip install strands-agents==1.0.1 bedrock-agentcore==0.1.0 bedrock-agentcore-starter-toolkit==0.1.1

# 再度確認
agentcore --help
```

## トラブルシューティング

### 1. パッケージ競合の可能性
```bash
# 環境の確認
which agentcore
pip list | grep agentcore

# 仮想環境使用推奨
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install strands-agents==1.0.1 bedrock-agentcore==0.1.0 bedrock-agentcore-starter-toolkit==0.1.1
```

### 2. Pythonパス問題
```bash
# Pythonとpipの確認
which python
which pip
python --version
```

### 3. インストール場所確認
```bash
# agentcoreコマンドの場所
which agentcore
ls -la $(which agentcore)
```

## 代替アプローチ

もしAgentCore CLIに問題がある場合：

### 1. Python直接実行
```bash
# Pythonモジュールとして実行
python -m bedrock_agentcore --help

# または
python -c "import bedrock_agentcore; print(bedrock_agentcore.__version__)"
```

### 2. 手動設定
AgentCore CLIが不安定な場合、設定ファイルを手動作成する可能性もあります。

## 想定される解決パターン

### パターン1: 正常（バージョンオプションなし）
```bash
agentcore --help  # 正常に表示される
agentcore configure --entrypoint src/main.py  # 次のステップに進める
```

### パターン2: 再インストール必要
```bash
# 再インストール後
agentcore --help  # 正常に表示される
```

### パターン3: 異なるコマンド構造
```bash
# 実際のコマンドが異なる場合
agentcore version  # または他の形式
```

## 確認結果

### パッケージインストール状況 ✅

```bash
→ pip list | grep -E "(bedrock|agentcore|strands)"
bedrock-agentcore                       0.1.0
bedrock-agentcore-starter-toolkit       0.1.1
strands-agents                          1.0.1
```

**結果**: 必要なパッケージは正常にインストール済み

### 結論

- AgentCore CLIは正常にインストールされている
- `--version` オプションは存在しないが、これは仕様
- 次のステップ（設定・デプロイ）に進むことが可能

## 次のアクション

1. **ヘルプ確認** - `agentcore --help` 実行して利用可能コマンド確認
2. **IAMロール問題解決** - 01-02の権限エラーを先に解決
3. **AgentCore設定** - `agentcore configure` でエントリーポイント設定
4. **デプロイ実行** - `agentcore launch --codebuild`

## 推奨順序

### 1. まずは利用可能コマンド確認
```bash
agentcore --help
```

### 2. IAMロール権限問題を解決
- 01-02のエラーを先に解決する必要あり
- `iam:CreateRole` 権限の追加が必要

### 3. 権限解決後の実行手順
```bash
# IAMロール作成
aws iam create-role --role-name BedrockAgentCoreExecutionRole ...

# AgentCore設定
agentcore configure --entrypoint src/main.py -er <ROLE_ARN>

# デプロイ
agentcore launch --codebuild
```

## メモ
- 日時: 2025-07-27
- 段階: AgentCore CLI確認フェーズ完了
- 状況: パッケージインストール正常
- 次の課題: IAMロール権限問題（01-02）