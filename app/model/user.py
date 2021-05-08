####################################
### Created by K18039-後藤 廉
####################################
### 内容：ユーザモデル
### ファイル：user.py
####################################

# MySQL
import MySQLdb
# 現在日時の取得
import datetime
# DB接続関連
from db import DBConnector
# プロジェクトの読み込み
from model.project import project



class user:
    

    # ユーザーモデル
    def __init__(self):
        self.attr = {}
        self.attr["id"] = None              # id int notNull
        self.attr["email"] = None           # email str notNull
        self.attr["name"] = None            # name str
        self.attr["password"] = None        # password str notNull
        self.attr["last_updated"] = None    # last_updated date notNull


    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_user;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_user` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `email` varchar(255) NOT NULL DEFAULT '',
                    `name` varchar(255) DEFAULT NULL,
                    `password` varchar(255) DEFAULT NULL,
                    `last_updated` datetime NOT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `OUTER_KEY` (`email`),
                    KEY `KEY_INDEX` (`email`)
                ); """)
            con.commit()


    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()


    @staticmethod
    def find(id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_user
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        u = user()
        u.attr["id"] = data["id"]
        u.attr["email"] = data["email"]
        u.attr["name"] = data["name"]
        u.attr["password"] = data["password"]
        u.attr["last_updated"] = data["last_updated"]
        return u


    @staticmethod
    def find_by_email(email):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_user
                WHERE  email = %s;
            """, (email,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        u = user()
        u.attr["id"] = data["id"]
        u.attr["email"] = data["email"]
        u.attr["name"] = data["name"]
        u.attr["password"] = data["password"]
        u.attr["last_updated"] = data["last_updated"]
        return u
    

    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["email"] is not None and type(self.attr["email"]) is str,
          self.attr["name"] is None or type(self.attr["name"]) is str,
          self.attr["password"] is not None and type(self.attr["password"]) is str,
          self.attr["last_updated"] is not None and type(self.attr["last_updated"]) is datetime.datetime
        ])


    @staticmethod
    def build():
        now = datetime.datetime.now()
        u = user()
        u.attr["last_updated"] = now
        return u


    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False


    def _db_save(self):
        if self.attr["id"] == None:
            return self._db_save_insert()
        return self._db_save_update()


    def _db_save_insert(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_user
                    (email, name, password, last_updated)
                VALUES
                    (%s, %s, %s, %s); """,
                (self.attr["email"],
                self.attr["name"],
                self.attr["password"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"])))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]
    
    
    def _db_save_update(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_user
                SET email = %s,
                    name = %s,
                    password = %s,
                    last_updated = %s
                WHERE id = %s; """,
                (self.attr["email"],
                self.attr["name"],
                self.attr["password"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"]),
                self.attr["id"]))

            con.commit()

        return self.attr["id"]