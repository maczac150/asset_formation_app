## 概要

ハッカソンで、ユーザーのライフプランに基づいた資産計画を立てるアプリを作成しました。

## 準備

1. リポジトリをクローン
   ```bash
   git clone https://github.com/maczac150/asset_formation_app.git
   ```
2. 仮想環境(以下では venv という名前)を作成
   ```bash
   python3 -m venv venv
   ```
3. 仮想環境を有効化
   ```bash
   source venv/bin/activate
   ```
4. 必要なパッケージをインストール
   ```bash
   pip install -r requirements.txt
   ```
5. OpenAI の公式サイトにサインイン後、API キーを取得する。.env ファイルに以下を追記
   ```bash
   OPENAI_API_KEY=hogehoge
   ```

## 使用方法

1. FastAPI アプリケーションをローカルで立ち上げるためのスクリプトを実行
   ```bash
   python3 run.py
   ```
2. ローカルサーバーにアクセス (http://127.0.0.1:8000)
