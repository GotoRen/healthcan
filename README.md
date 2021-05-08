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
| pip3 | 21.1.1 |

## 🚀 Usage
```
### 起動
$ make

### appコンテナに入る
$ make app/healthcan

### dbコンテナに入る
$ make app/db

### dbコンテナに入る + MySQL接続
$ make mysql

### 単体テスト
$ make app/healthcan
# make
```

## 🌱 Access
- Index：[http://localhost:3000/](http://localhost:3000/)
- JupyterNotebook：[http://localhost:8888/](http://localhost:8888/)

## 📝 UnitTests
```
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
