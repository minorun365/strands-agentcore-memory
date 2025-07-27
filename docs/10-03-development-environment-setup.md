# 開発環境セットアップ編 - 必要なツールとプロジェクトの準備

## 🎯 この章の目標

AI エージェントを動かすために必要なソフトウェアをインストールし、プロジェクトファイルをダウンロードします。

## 📋 作業の流れ

1. **Python インストール** (プログラミング言語)
2. **Git インストール** (バージョン管理ツール)
3. **AgentCore CLI インストール** (AI エージェント管理ツール)
4. **プロジェクトダウンロード** (ソースコードの取得)

---

## ステップ 1: Python のインストール

### 🐍 Python とは？
Python は AI・機械学習でよく使われるプログラミング言語です。このプロジェクトでは Python 3.10 以降が必要です。

### 💻 macOS の場合

#### 方法 1: Homebrew を使う（推奨）

```bash
# Homebrew がインストールされていない場合
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python をインストール
brew install python@3.10
```

#### 方法 2: 公式サイトからダウンロード

1. https://www.python.org/downloads/ にアクセス
2. **Python 3.10** または **3.11** をダウンロード
3. ダウンロードした `.pkg` ファイルを実行してインストール

### 🖥️ Windows の場合

1. https://www.python.org/downloads/ にアクセス
2. **Python 3.10** または **3.11** をダウンロード
3. インストール時に **「Add Python to PATH」** に必ずチェック
4. **「Install Now」** をクリック

### ✅ インストール確認

```bash
python3 --version
# または
python --version
```

`Python 3.10.x` または `Python 3.11.x` と表示されれば成功です。

---

## ステップ 2: Git のインストール

### 📚 Git とは？
Git はソースコードの管理ツールです。プロジェクトファイルをダウンロードするために使用します。

### 💻 macOS の場合

```bash
# Homebrew を使う場合
brew install git

# または Xcode Command Line Tools
xcode-select --install
```

### 🖥️ Windows の場合

1. https://git-scm.com/download/win にアクセス
2. **Download for Windows** をクリック
3. ダウンロードしたファイルを実行
4. インストール設定はデフォルトのままでOK

### ✅ インストール確認

```bash
git --version
```

バージョン情報が表示されれば成功です。

---

## ステップ 3: AgentCore CLI のインストール

### 🤖 AgentCore CLI とは？
AI エージェントを簡単に管理・デプロイできるコマンドラインツールです。

### 📦 pip を使ってインストール

```bash
# Python のパッケージ管理ツール pip を最新版に更新
python3 -m pip install --upgrade pip

# AgentCore CLI をインストール
pip3 install bedrock-agentcore-starter-toolkit
```

### ✅ インストール確認

```bash
agentcore --version
```

バージョン情報が表示されれば成功です。

### 🚨 インストールに失敗する場合

#### 権限エラーの場合
```bash
# ユーザー権限でインストール
pip3 install --user bedrock-agentcore-starter-toolkit
```

#### Python のパスエラーの場合
```bash
# Python のパスを確認
which python3
which pip3

# パスが見つからない場合は PATH 環境変数を設定
export PATH="$PATH:/usr/local/bin:/opt/homebrew/bin"
```

---

## ステップ 4: プロジェクトファイルのダウンロード

### 📁 作業ディレクトリの作成

```bash
# ホームディレクトリに移動
cd ~

# プロジェクト用フォルダを作成
mkdir -p projects
cd projects
```

### 📥 GitHub からプロジェクトをクローン

> **注意**: 実際のプロジェクトでは、ここでプロジェクトの Git リポジトリからクローンしますが、  
> このガイドでは既にプロジェクトファイルがある前提で進めます。

```bash
# 例: プロジェクトをクローンする場合
# git clone https://github.com/your-username/strands-agentcore-memory.git
# cd strands-agentcore-memory

# 既存のプロジェクトディレクトリに移動
cd /path/to/your/strands-agentcore-memory
```

### 📂 プロジェクト構造の確認

プロジェクトディレクトリ内に以下のファイル・フォルダがあることを確認:

```
strands-agentcore-memory/
├── backend/                 # AI エージェントのコード
│   ├── src/                # Python ソースコード
│   ├── .bedrock_agentcore.yaml  # AgentCore 設定ファイル
│   └── requirements.txt    # Python パッケージ一覧
├── frontend/               # ウェブ画面のコード
│   ├── app.py             # Streamlit アプリのメイン
│   ├── requirements.txt   # Python パッケージ一覧
│   └── *.py               # その他の Python ファイル
├── docs/                  # ドキュメント
└── README.md             # プロジェクト説明
```

---

## ステップ 5: 環境の動作確認

### 🔍 各ツールの動作確認

```bash
# Python の確認
python3 --version

# Git の確認
git --version

# AWS CLI の確認
aws --version

# AgentCore CLI の確認
agentcore --version

# AWS 認証の確認
aws sts get-caller-identity
```

すべてのコマンドが正常に実行されれば、環境セットアップ完了です！

---

## 🚨 トラブルシューティング

### よくある問題と解決方法

#### 1. 「command not found」エラー
```bash
# 問題: インストールしたコマンドが見つからない
# 解決: PATH 環境変数に追加

# macOS の場合
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Windows の場合は環境変数の設定画面から PATH を編集
```

#### 2. Python のバージョンが古い
```bash
# 問題: Python 3.9 以下がインストールされている
# 解決: pyenv を使って複数バージョンを管理

# pyenv のインストール（macOS）
brew install pyenv
pyenv install 3.10.12
pyenv global 3.10.12
```

#### 3. pip のインストールエラー
```bash
# 問題: pip でパッケージがインストールできない
# 解決: pip のアップグレードと権限確認

python3 -m pip install --upgrade pip
pip3 install --user [パッケージ名]
```

#### 4. AgentCore CLI が見つからない
```bash
# 問題: agentcore コマンドが認識されない
# 解決: pip のインストール場所を確認

# インストール場所を確認
pip3 show bedrock-agentcore-starter-toolkit

# PATH に追加
export PATH="$PATH:~/.local/bin"
```

### 🆘 困ったときのチェックリスト

- [ ] Python 3.10 以降がインストールされている
- [ ] Git がインストールされている
- [ ] AWS CLI が設定されている
- [ ] AgentCore CLI がインストールされている
- [ ] プロジェクトファイルがダウンロードされている
- [ ] 各コマンドが正常に実行される

---

## 🎊 完了確認

以下がすべて完了していれば、次の章に進めます:

- ✅ Python 3.10+ インストール完了
- ✅ Git インストール完了
- ✅ AgentCore CLI インストール完了
- ✅ プロジェクトファイル準備完了
- ✅ 各ツールの動作確認完了

## 📌 この章で学んだこと

- ✅ AI 開発に必要な基本ツールの種類
- ✅ Python、Git、AgentCore CLI のインストール方法
- ✅ プロジェクト構造の理解
- ✅ 基本的なトラブルシューティング

**次の章**: 10-04 Bedrock モデルアクセス設定編

---

## 📚 用語解説

- **Python**: プログラミング言語、AI 開発でよく使われる
- **pip**: Python のパッケージ管理ツール
- **Git**: バージョン管理システム、ソースコードの履歴管理
- **CLI**: Command Line Interface、コマンドライン操作ツール
- **PATH**: 実行可能ファイルの場所をシステムに教える設定
- **環境変数**: システム全体で使える設定値

## 💡 次章の予告

次の章では、AWS Bedrock で AI モデル（Claude）を使えるようにする設定を行います。  
これが完了すると、いよいよ AI エージェントの構築に入ります！