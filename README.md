# OwlJudge
Djangoベースのオンラインジャッジシステムです。
コードテストとコードの判定など基本的な機能が搭載されております。
テスト用サーバー:http://owljudge.herokuapp.com/
関連記事:https://blog.misw.jp/entry/2020/12/17/000000

### 使用できる言語:
C、C++、Python3、Ruby、Java、Brainfuck

### 依存ライブラリー
gcc g++ ruby bf python3 python3-pip openjdk-8-jdk django psutil gunicorn whitenoise nginx

## 1.Dockerのビルド＆ローカル環境の初期化
まずは下記のテンプレートを使って`.env`と`.env-db`を作成します。
- `.env`
```
DEBUG=1
SECRET_KEY=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

DB_ENGINE=
DB_TYPE=
DB_DATABASE_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
```
- `.env-db`
```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```
次に、下記のコマンドを実行します:
```
docker-compose build
docker-compose up -d
docker exec -it owljudge_web_1 python3 manage.py migrate
```

## 2.コンテナの起動
```
docker-compose up -d
```
コンテナが全て起動した場合、http://localhost:8000 にアクセスするとOwlJudgeが開きます。

## 3.問題の作成、サンプルケースの作成
### (1)管理者ユーザーの作成
```
docker exec -it owljudge_web_1 python3 manage.py createsuperuser
```
### (2)問題とサンプルケースの作成
まず、先ほど作成した管理者ユーザーとしてDjangoの管理者にアクセスしてください。

Djangoの管理者画面のURLはhttp://localhost:8000/admin/ に設定されております。

問題とサンプルケースはそれぞれQuestionsとCasesモデルに対応しており、CasesのQuestionnumberを紐づけたい問題のIDに指定すると、サンプルケースが指定された問題に追加されます。



