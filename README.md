# oop2_healthcan
6人でチームを組んで開発
- Contents
  - JupyternoteBook
  - yaml
  - python
  - Tornado
  - html
  - js
  - css
- _Docker_
  - networksに`oop2_link`を指定して共有 
    - `$ docker network create oop2_link`
  - dockerコンテナのビルドと実行
    - `$ docker-compose up -d --build`
  - 既存のdocker-composeを削除
    - `$ docker-compose rm`
  - コンテナを起動
    - `$ docker-compose start`
  - コンテナを停止
    - `$ docker-compose stop`
  - コンテナを再起動
    - `$ docker-compose restart`
- _Up_
  - 『jupyternotebook』を使用する場合
    - <u>http://localhost:8888/tree?<u>
    - jupyternotebookの「Terminal」を利用する
  - Macのターミナルから事項する場合
    - `$ docker-compose exec jupyternotebook bash`
    - もとのユーザに戻すとき
    - `# exit`
- _Server_
  - 初期起動時の場合
    1. 既存のDBを削除
      - `# python hc_server.py db_cleaner`
    2. DBに接続する
      - `# python hc_server.py migrate`
    3. サーバを起動する
      - `# python hc_server.py`
  - 以降
    - `# python hc_server.py`
- _Location_
  - <u>http://localhost:3000/</u>
- _UnitTest_
  - `# python -m unittest [フォルダ].[ファイル].[クラス].[テスト関数]`
    - 例：）`# python -m unittest tests.test_hero.test_hero.test_is_valid`

