# oop2_healthcan
## Name
- ~ Healthcan ~
  - 健康（Health）
  - Scan（調べる）
  - Can（管理）

## Overview
- Python（Tornade） + Docker を利用して健康管理アプリケーションを制作
- 身長, 体重を入力するとBMIや適正体重などを算出してグラフ表示する
  - 体重の変化などが一眼でわかる
- 基本機能
  - アカウント管理
  - データ追加
  - データ管理
  - グラフ可視化

## Description
- 環境構築
  ```
  ###コ ンテナ用のネットワークを作成
  $ docker network create healthcan_link

  ### ビルド & 実行
  $ docker-compose up -d --build

  ### JupyterNotebook コンテナに入る
  $ docker-compose exec jupyternotebook bash
  ```
- 実行
  ```
  a. 初期起動時の場合
  ### 既存のDBを削除
  # python hc_server.py db_cleaner

  ### データベースへの接続 && カーソルの生成
  # python hc_server.py migrate

  ### サーバ起動
  # python hc_server.py

  ------------------------------------------------------------

  b. 2回目以降
  ### サーバ起動
  # python hc_server.py
  ```
- アクセス
  - Healthcan
    - http://localhost:3000/
  - JupyterNotebook  
    - http://localhost:8888/tree?

## CodeTest
- `# python -m unittest [フォルダ].[ファイル].[クラス].[テスト関数]`
  - 例：）`# python -m unittest tests.test_hero.test_hero.test_is_valid`

## Other：Docker Command
- docker：コンテナ操作
  ```
  ### ステータ確認
  $ docker ps
  
  ### コンテナリスト
  $ docker ps -a
  
  ### 起動
  $ docker start [コンテナ名]
  
  ### 停止
  $ docker stop [コンテナ名]
  
  ### 再起動
  $ docker restart [コンテナ名]
  
  ### コンテナ削除
  $ docker rm [コンテナ名]
  
  ### イメージリスト
  $ docker images
  
  ### イメージ削除
  $ docker rmi [イメージID]
  
  ## コンテナログ
  $ docker logs [コンテナ名]

  ## イメージヒストリ
  $ docker history [イメージ名]
  ```
 - docker-compose：複数コンテナ操作
   ```
   ### 起動
   $ docker-compose start
   
   ### 停止
   $ docker-compose stop
   
   ### 再起動
   $ docker-compose restart
   
   ### コンテナ & イメージ をまとめて削除
   $ docker-compose down
   
   ### ビルド & 実行
   $ docker-compose up -d --build
   
   ### 詳細表示
   $ docker-compose config
    
   ### ステータス確認
   $ docker-compose ps 
   ### インスタンスログ
   $ docker-compose logs
   ```
- docker network：コンテナ間通信
  ```
  ### ネットワークの作成
  $ docker network create [ネットワーク名]
  
  ### ネットワークの詳細表示
  $ docker network inspect  [ネットワークID]    
  
  ### ネットワークの一覧表示
  $ docker network ls
  
  ### 既存ネットワークの削除
  docker network rm [ネットワークID]
  ```
