# Streamlit ファイルエンコーディングエラー - .py　ファイル名問題

## 問題の状況

```bash
(venv)  ~/train/handson/strands-agentcore-memory/frontend main
→ streamlit run app.py　
Usage: streamlit run [OPTIONS] TARGET [ARGS]...
Try 'streamlit run --help' for help.

Error: Streamlit requires raw Python (.py) files, not .py　.
For more information, please see https://docs.streamlit.io
```

## 原因分析

**ファイル名に見えない文字が含まれている**
- `app.py` の後に全角スペース（　）または特殊文字が含まれている
- Streamlitが `.py　` として認識し、通常の `.py` ファイルではないと判断
- コマンドライン入力時の文字エンコーディング問題

## 解決方法

### ステップ1: ファイルの存在確認

```bash
# 現在のディレクトリ確認
pwd
# 期待値: /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/frontend

# ファイル一覧確認
ls -la

# app.pyの存在確認
ls -la app.py
```

### ステップ2: 正しいファイル名でのStreamlit実行

```bash
# 正確なファイル名で実行（タブ補完使用推奨）
streamlit run app.py

# またはタブ補完を使用
streamlit run app<TAB>
```

### ステップ3: ファイル名を明示的に指定

```bash
# フルパスで指定
streamlit run /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/frontend/app.py

# 相対パスで明示的に指定
streamlit run ./app.py
```

### ステップ4: ファイル内容確認（念のため）

```bash
# app.pyの最初の数行確認
head -5 app.py

# ファイルタイプ確認
file app.py
# 期待値: app.py: Python script, UTF-8 Unicode text executable
```

## デバッグ用確認コマンド

### ファイル名の詳細確認

```bash
# ファイル名の16進ダンプ確認（特殊文字検出）
ls | od -c | grep app

# ファイル名とinode情報
ls -lai app.py

# ファイルの詳細情報
stat app.py
```

### 文字エンコーディング確認

```bash
# 現在のロケール確認
locale

# ターミナルの文字エンコーディング確認
echo $LANG
```

## 代替解決方法

### 方法1: ファイル名をコピー&ペースト

```bash
# ファイル一覧から正確な名前をコピー
ls -1 *.py

# 表示された名前を正確にコピー&ペーストして実行
streamlit run [ここにコピーしたファイル名]
```

### 方法2: ワイルドカードを使用

```bash
# app.pyにマッチするファイルを実行
streamlit run app.*

# または
streamlit run *.py
```

### 方法3: ファイル名の確認と修正

```bash
# ファイル名に問題がある場合は修正
mv app.py app_clean.py
streamlit run app_clean.py
```

## 正常実行時の期待される出力

```bash
Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501

  For better performance, install the following packages:
  - watchdog
```

## トラブルシューティング

### app.pyが見つからない場合

```bash
# Pythonファイル一覧確認
find . -name "*.py" -type f

# app.pyの場所検索
find /Users/uchinishi.koichi/train/handson/strands-agentcore-memory -name "app.py" -type f
```

### 権限問題の場合

```bash
# ファイル権限確認
ls -la app.py

# 実行権限追加（必要に応じて）
chmod +x app.py
```

### 仮想環境問題の場合

```bash
# 仮想環境確認
which python
which streamlit

# 仮想環境の再アクティベート
deactivate
source venv/bin/activate
```

## 推奨解決手順

### 1. ファイル確認

```bash
cd /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/frontend
ls -la app.py
```

### 2. 正確なコマンド実行

```bash
# タブ補完を使用して正確なファイル名を取得
streamlit run app<TAB>

# または直接入力
streamlit run app.py
```

### 3. 環境変数確認

```bash
# .envファイルの存在確認（プロジェクトルート）
ls -la ../.env

# 内容確認
cat ../.env
```

## 成功確認

### ブラウザアクセス確認
- ローカル: http://localhost:8501
- Streamlitアプリの正常表示

### アプリケーション機能確認
1. **UI表示**: Streamlitインターフェースが正常表示
2. **チャット機能**: 入力欄とメッセージ表示
3. **AgentCore接続**: バックエンドとの通信確認

## よくある文字エンコーディング問題

### 全角スペースの混入
```bash
# 問題のあるコマンド（全角スペース含む）
streamlit run app.py　

# 正しいコマンド（半角スペースのみ）
streamlit run app.py
```

### 特殊文字の混入
- コピー&ペースト時の見えない文字
- ターミナルの文字エンコーディング不一致
- 異なるエディタからのコピー時の文字化け

## 次のアクション

1. **正確なファイル名確認** - ls -la で実際のファイル名確認
2. **タブ補完使用** - 正確なファイル名の自動補完
3. **Streamlit実行** - 正しいコマンドでアプリ起動
4. **ブラウザアクセス** - http://localhost:8501 で動作確認

## エラー回避のベストプラクティス

- **タブ補完の活用**: ファイル名入力時は必ずタブ補完使用
- **コピー&ペースト注意**: 外部からのテキストコピー時は特殊文字に注意
- **ターミナル設定**: UTF-8エンコーディングの確認
- **ファイル名の標準化**: ASCII文字のみを使用

## メモ
- 日時: 2025-07-27
- 段階: Streamlitファイルエンコーディングエラー解決
- 問題: ファイル名に見えない文字（全角スペース等）が混入
- 解決策: 正確なファイル名でのコマンド実行（タブ補完推奨）