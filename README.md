# : HealthCan （Health+Scan & Health+Can）

## 💡 Overview

- **Description**<br>
  &emsp;Our team created a health management application using Python (Tornado) + Docker.<br>
  &emsp;When you enter your height and weight, BMI and proper weight are calculated and displayed as a graph.<br>
  &emsp;If you use this application, you can see the change of weight etc. at a glance!!<br>
- **BasicFunction**
  - account management
  - add data
  - data management
  - graph visualization

## ⚡ Configure

| Language/Framework | Version |
| :----------------: | :-----: |
|       Docker       | 20.10.5 |
|   docker-compose   | 1.29.0  |
|       MySQL        | 8.0.24  |
|       Python       |  3.9.0  |
|        pip3        | 21.1.1  |

## 🙏 Init Require

```
### app
$ cp app/.env{.sample,}

### db
$ cp db/.env{.sample,}
$ cp db/access.cnf{.sample,}
```

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

### 確認
=== * 起動するDockerコンテナ * ===
$ docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                               NAMES
111a64977445   healthcan_db    "docker-entrypoint.s…"   44 seconds ago   Up 38 seconds   33060/tcp, 0.0.0.0:3307->3306/tcp   healthcan_db
f13ed74a7c79   healthcan/app   "python3 hc_server.py"   44 seconds ago   Up 39 seconds   0.0.0.0:3000->3000/tcp              healthcan_app

=== * 作成されるDockerイメージ * ===
$ docker images
REPOSITORY                           TAG        IMAGE ID       CREATED         SIZE
healthcan/app                        latest     421f0ec4569f   2 minutes ago   906MB
healthcan_db                         latest     b8c3ff9f8811   2 weeks ago     556MB

=== * 作成されるDockerネットワーク * ===
$ docker network ls
NETWORK ID     NAME             DRIVER    SCOPE
8267c6d5107e   healthcan_link   bridge    local
```

## 🌱 Access

- Index：[http://localhost:3000/](http://localhost:3000/)

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
