# android-app-python

このリポジトリは Kivy を使ったシンプルな Android アプリのサンプルです。

準備とビルド手順（ホストで buildozer を使う場合）:

1. buildozer をインストール（Ubuntu 22.04/24.04 での例）:

```bash
sudo apt update
sudo apt install -y buildozer build-essential git python3-pip python3-venv
pip3 install --user --upgrade buildozer
```

2. Android SDK/NDK 等を自動でダウンロードするために buildozer を初回実行:

```bash
cd /path/to/repo
buildozer android debug
```

3. デバッグ用 APK をデバイスにインストールして実行:

```bash
buildozer android debug deploy run
```

注意:
- CI 環境や macOS では手順が異なります。
- buildozer はローカルで Android ツールチェインをダウンロードするためネットワーク接続が必要です。
- 必要に応じて `buildozer.spec` を編集して `requirements` や `package.domain` を調整してください。

簡単なアプリの説明:
- `main.py` に基本的なラベルとボタンがあります。ボタンを押すとテキストが変わります。
