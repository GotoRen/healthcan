### <font color=Orange>Docker</font>
| コマンド（$） | 意味 |
| :---- | :---- |
| $ container_id | コンテナID （__CONTAINER ID__）|
| $ name | Dockerfileが格納されているフォルダ名<br>(コマンドcdで指定する) |
| $ dir | .  を指定する |
| $ container_name | コンテナの名前 （__NAMES__）|
| $ imagename | コンテナのイメージの名前（__IMAGE__） |
| $ sql_container_name | mysqlコンテナの名前（__NAMES__） |

- ファイルの名前、拡張子を変更する
  - `$ mv Dockerfile.txt Dockerfile`  
    - ファイルタイプを『Dockerfile.txt』から『Dockerfile』に
- 現在稼働中のコンテナ一覧を表示する
  - `$ docker ps`
- 保持する全てのコンテナ一覧を表示する    
  - `$ docker ps -a`
- ディレクトリ`$ dir`に配置されている`Dockerfile`を読み込んでビルドを実行する
  - `$ docker build -t $ name $ dir`
    - 指定したディレクトリ`$ dir`に配置されている`Dockerfile`を読み込んで新しくイメージを作成する
    - 全てのコンテナはイメージから作成される
    - 1つのイメージから複数の名前の異なるコンテナを作ることができる
- イメージからコンテナを作成する
  - `$ docker run -d --name $ container_name -p 127.0.0.1:8888:8888 $ imagename`
    - コンテナ作成時に元となるイメージやコンテナの名前や通信ポートの設定が可能
    - `--name`オプションを省略すると勝手に選ばれた英単語がコンテナ名に与えられる
    - 混乱をさけるためにもコンテナ名は必ずつける
    - 同じコンテナ名でコンテナを作成することはできないので仮想環境の多重起動防止にもなる
    - `-d`オプションを指定することでデーモン化（プロセスの常駐化）ができる
    - Webブラウザからアクセスするアプリなどはデーモン化させないとプロセスが終了する
- 実行中のコンテナIDを指定してコンテナを停止する
  - `$ docker stop $ container_id`
- 実行中のコンテナIDを指定して実行する
  - `$ docker start $container_id`
- 実行中のコンテナIDを指定して再び実行する
  - `$ docker restart $container_id`
- 停止状態のコンテナを削除する
  - `$ docker rm $ container_id`
    - 稼働中のコンテナは削除することができない
    - 削除したコンテナは元に戻すことができない
    - <font color=Red>※ 使用の際は慎重に！！</font>
- mysqlコンテナを作成する
  - `$ docker run -d --name $ sql_container_name -e MYSQL_ROOT_PASSWORD=abc123 -p 3306:3306 $ imagename`
    - `MYSQL_ROOT_PASSWORD`にはアクセス時のパスワードを設定する
    - `-p`にはイメージファイルからSQLに接続する際のポートを設定する
- Jupyter Notebookでmysqlコンテナを起動する
  - `$ docker run -d --name $ container_name --link $ sql_container_name:mysql -p 127.0.0.1:8889:8888 $ imagename`
- mysqlコンテナのホストIDを表示する
  - `$ docker exec -it $ sql_container_name hostname`
    - mysqlコンテナを起動した状態でないとホストIDを表示できない
- mysqlコンテナを再起動する
  - `$ docker restart $ sql_container_name`
    - Jupyter Notebookにおいてプログラムは正しいのに動かない等の事象が発生した場合などに再起動してみる
