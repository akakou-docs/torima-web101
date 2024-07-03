# torima-web101

Torima を使った Web アプリ入門

## 始め方

### 1. リポジトリのクローン

```sh
git clone https://github.com/akakou-docs/torima-web101
cd torima-web101
```

### 2. ngrok の設定・開始

1. 以下のリンクからアカウント作成
   https://dashboard.ngrok.com/signup

2. 以下のリンクからトークンを取り出す
   https://dashboard.ngrok.com/get-started/your-authtoken

3. 以下のコマンドからトークンをサーバに設定し、ngrok を起動する

```sh
ngrok config add-authtoken NGROKのトークン
ngrok http ポート番号
```

#### 3. Torima の設定

[これ見て](https://zenn.dev/ochanoco/articles/11f13b4319c54e)

`1. まずは LINE Login を設定！`〜`2. Torima 設定ファイルを作ります`までやる

なお、config.yaml では、host を ngrok にかかれている host に書き換えること

torima/config.yaml

```yaml
host: http://localhost:8080/ # ここを書き換える

port: 8080

default_origin: app:5000

skip_auth_list:
  - "/favicon.ico"

scheme: http
```

#### 4. Docker のポート番号を書き換える

compose.yaml

```yaml
proxy:
  image: ghcr.io/ochanoco/torima:develop
  volumes:
    - "./torima/data:/workspace/data"
    - "./torima/config.yaml:/workspace/config.yaml"
  environment:
    - TORIMA_DB_TYPE=sqlite3
    - TORIMA_DB_CONFIG=file:./data/db.sqlite3?_fk=1
  env_file:
    - ./torima/secret.env
  ports:
    - "XXXXX:8080" # ここ
```

#### 5. 実行

```env
docker-compose up
```
