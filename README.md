# HealthCan
## 💡 Overview
- Python（Tornado） + Docker を利用して健康管理アプリケーションを制作
- 身長, 体重を入力するとBMIや適正体重などを算出してグラフ表示する
  - 体重の変化などが一眼でわかる
- 基本機能
  - アカウント管理
  - データ追加
  - データ管理
  - グラフ可視化

## ⚡ Configure
| 言語/フレームワーク	| バージョン |
| :---: | :---: |
| Docker | 20.10.5 |
| docker-compose | 1.29.0 |
| MySQL	| 8.0.24 |
| Python | 3.9.0 |
| pip | 21.0.1 |

## 🚀 Usage
```
### コンテナ用のネットワークを作成
$ docker network create healthcan_link

### ビルド & 実行
$ docker-compose up -d --build

### JupyterNotebook コンテナに入る
$ docker-compose exec jupyternotebook bash

a. ビルド時のみ
### データベースへの接続 && カーソルの生成
# python3 hc_server.py migrate

b. 2回目以降
### docker-compose を起動させるだけ
$ docker-compose start
```

## 🌱 Access
- indexページ：[http://localhost:3000/](http://localhost:3000/)
- JupyterNotebook：[http://localhost:8888/](http://localhost:8888/)

## 📝 UnitTests
```
$ make app/healthcan
# make 

# python3 -m unittest [フォルダ].[ファイル].[クラス].[テスト関数]

ex:) model/project.py
All. python3 -m unittest tests.test_project.test_project

ex:) model/healthcan.py
All. python3 -m unittest tests.test_healthcan.test_healthcan
1.   python3 -m unittest tests.test_healthcan.test_healthcan.test_db_is_working
2.   python3 -m unittest tests.test_healthcan.test_healthcan.test_is_valid
3.   python3 -m unittest tests.test_healthcan.test_healthcan.test_is_valid_with_invalid_attrs
4.   python3 -m unittest tests.test_healthcan.test_healthcan.test_build
5.   python3 -m unittest tests.test_healthcan.test_healthcan.test__index

ex:) model/user.py
All. python3 -m unittest tests.test_user.test_user
1.   python3 -m unittest tests.test_user.test_user.test_db_is_working
2.   python3 -m unittest tests.test_user.test_user.test_find_by_email
3.   python3 -m unittest tests.test_user.test_user.test_is_valid
4.   python3 -m unittest tests.test_user.test_user.test_is_valid_with_invarid_attrs
5.   python3 -m unittest tests.test_user.test_user.test_build
6.   python3 -m unittest tests.test_user.test_user.test_db_save_insert
7.   python3 -m unittest tests.test_user.test_user.test_db_save_update
```

## 💪 pip3
```
### pip3 リスト
$ pip3 list

### インストール済みのパッケージのうち、最新でないものを表示する
$ pip3 list --outdated

### インストール済みパッケージのうち、最新でないものをアップデートする
$ pip3 list --outdated | awk 'NR>2 {print $1}' | xargs pip install -U
```



