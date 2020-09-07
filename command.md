### <font color=Gray>Dockerコンテナを構築</font>
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

### <font color=Gray>環境の確立</font>
- 実行環境
  - 『jupyternotebook』を使用する場合
    - <u>http://localhost:8888/tree?<u>
    - jupyternotebookの「Terminal」を利用する
  - Macのターミナルから事項する場合
    - `$ docker-compose exec jupyternotebook bash`
    - もとのユーザに戻すとき
    - `# exit`
- サーバの起動方法
  - 初期起動時の場合
    1. 既存のDBを削除
      - `# python hc_server.py db_cleaner`
    2. DBに接続する
      - `# python hc_server.py migrate`
    3. サーバを起動する
      - `# python hc_server.py`
 - 以降
   - `# python hc_server.py`

### <font color=Gray>Webサイト</font>
- <font color=Blue>_HealthCan_</font>
  - <u>http://localhost:3000/</u>

### 単体テスト
- `# python -m unittest [フォルダ].[ファイル].[クラス].[テスト関数]`
  - 例：）`# python -m unittest tests.test_hero.test_hero.test_is_valid`
