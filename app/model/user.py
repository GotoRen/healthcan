import MySQLdb
import datetime
from db import DBConnector
from model.project import project

class user:
    def __init__(self):
        self.attr = {}
        self.attr["id"] = None              
        self.attr["email"] = None           
        self.attr["name"] = None            
        self.attr["password"] = None        
        self.attr["last_updated"] = None

    @staticmethod
    def migrate():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            cursor.execute('USE db_%s;' % project.name())
            cursor.execute('DROP TABLE IF EXISTS table_user;')
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

    # db_creaner clears the database.
    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    # find returns matching elements (returns data by id).
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

    # find_by_email returns matching elements (returns data by email).
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
    
    # is_valid determines the correctness of the value.
    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["email"] is not None and type(self.attr["email"]) is str,
          self.attr["name"] is None or type(self.attr["name"]) is str,
          self.attr["password"] is not None and type(self.attr["password"]) is str,
          self.attr["last_updated"] is not None and type(self.attr["last_updated"]) is datetime.datetime
        ])

    # build builds each data.
    @staticmethod
    def build():
        now = datetime.datetime.now()
        u = user()
        u.attr["last_updated"] = now
        return u

    # save runs _db_save.
    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False

    # _db_save runs _db_save_insert.
    def _db_save(self):
        if self.attr["id"] == None:
            return self._db_save_insert()
        return self._db_save_update()

    # _db_save_insert inserts saved data.
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

            # INSERTされたAUTO INCREMENT値を取得
            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]
    
    # _db_save_update updates the data.
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
