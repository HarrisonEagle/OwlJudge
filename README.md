# OwlJudge
Djangoベースのオンラインジャッジシステムです。
コードテストとコードの判定など基本的な機能が搭載されております。

関連記事:https://blog.misw.jp/entry/2020/12/17/000000

### 使用できる言語:
C、C++、Python3、Ruby、Java3、Brainfuck

### 依存ライブラリー
gcc g++ python3 ruby bf python3 python3-pip openjdk-8-jdk django psutil

## 1.ライブラリーの導入
```
sudo apt install gcc g++ python3 ruby bf python3 python3-pip openjdk-8-jdk
pip3 install django psutil
```

## 2.サーバーの起動
```
python3 manage.py runserver
```


## 3.問題の作成、サンプルケースの作成
### (1)管理者ユーザーの作成
```
python3 manage.py createsuperuser
```
### (2)問題とサンプルケースの作成
まず、先ほど作成した管理者ユーザーとしてDjangoの管理者にアクセスしてください。

Djangoの管理者画面のURLはhttp://localhost:8000/admin/ に設定されております。

問題とサンプルケースはそれぞれQuestionsとCasesモデルに対応しており、CasesのQuestionnumberを紐づけたい問題のIDに指定すると、サンプルケースが指定された問題に追加されます。



