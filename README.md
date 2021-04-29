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
# python hc_server.py migrate

b. 2回目以降
### docker-compose を起動させるだけ
$ docker-compose start
```

## 🌱 Access
- indexページ：[http://localhost:3000/](http://localhost:3000/)
- JupyterNotebook：[http://localhost:8888/](http://localhost:8888/)

## 📝 UnitTests
```
# python -m unittest [フォルダ].[ファイル].[クラス].[テスト関数]

ex：）`# python -m unittest tests.test_hero.test_hero.test_is_valid`
```
