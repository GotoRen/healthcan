import MySQLdb
import datetime
import pytz
import decimal
from _pydecimal import Decimal
from decimal import Decimal
from db import DBConnector
from model.project import project

class healthcan:
    def __init__(self):
        self.attr = {}
        self.attr["id"] = None          # ID
        self.attr["user_id"] = None     # ユーザID
        self.attr["name"] = None        # 名前
        self.attr["date"] = None        # 日
        self.attr["time"] = None        # 時
        self.attr["height"] = None      # 身長
        self.attr["weight"] = None      # 体重
        self.attr["bmi"] = None         # BMI
        self.attr["pro_weight"] = None  # 適正体重
        self.attr["diff_weight"] = None # 適正体重までの差（体重-適正体重）

    @staticmethod
    def migrate():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            cursor.execute('USE db_%s;' % project.name())
            cursor.execute('DROP TABLE IF EXISTS HEALTH;')
            cursor.execute("""
                CREATE TABLE `HEALTH` (
                `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                `user_id` int(11) unsigned NOT NULL,
                `name` varchar(255) DEFAULT NULL,
                `date` date NOT NULL,
                `time` time NOT NULL,
                `height` decimal(4,1) NOT NULL DEFAULT '0',
                `weight` decimal(4,1) NOT NULL DEFAULT '0',
                `bmi` decimal(3,1) NOT NULL DEFAULT '0',
                `pro_weight` decimal(5,2) NOT NULL DEFAULT '0',
                `diff_weight` decimal(4,2) NOT NULL DEFAULT '0',
                PRIMARY KEY (`id`),
                KEY `user_id` (`user_id`),
                KEY `name` (`name`)
            )""")
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
                FROM   HEALTH
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        hc = healthcan()
        hc.attr["id"] = data["id"]
        hc.attr["user_id"] = data["user_id"]
        hc.attr["name"] = data["name"]
        hc.attr["date"] = data["date"]
        hc.attr["time"] = data["time"]
        hc.attr["height"] = data["height"]
        hc.attr["weight"] = data["weight"]
        hc.attr["bmi"] = data["bmi"]
        hc.attr["pro_weight"] = data["pro_weight"]
        hc.attr["diff_weight"] = data["diff_weight"]
        return hc

    # is_valid determines the correctness of the value.
    def is_valid(self):
        return all([
            self.attr["id"] is None or type(self.attr["id"]) is int,
            self.attr["user_id"] is not None and type(self.attr["user_id"]) is int,
            self.attr["name"] is not None and type(self.attr["name"]) is str and len(self.attr["name"]) > 0,
            self.attr["date"] is not None and type(self.attr["date"]) is datetime.date or type(self.attr["date"]) is str or type(self.attr["date"]) is int,
            self.attr["time"] is not None,
            self.attr["height"] is not None and type(self.attr["height"]) is decimal.Decimal,
            self.attr["weight"] is not None and type(self.attr["weight"]) is decimal.Decimal,
            self.attr["bmi"] is not None and type(self.attr["bmi"]) is decimal.Decimal,
            self.attr["pro_weight"] is not None and type(self.attr["pro_weight"]) is decimal.Decimal,
            self.attr["diff_weight"] is not None and type(self.attr["diff_weight"]) is decimal.Decimal,
        ])      

    # build builds each data.
    @staticmethod
    def build():
        hc = healthcan()
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        hc.attr["date"] = '{0:%Y-%m-%d}'.format(now.date())
        hc.attr["time"] = '{0:%H:%M:%S}'.format(now.time())
        hc.attr["height"] = Decimal(0)
        hc.attr["weight"] = Decimal(0)
        hc.attr["bmi"] = Decimal(0)
        hc.attr["pro_weight"] = Decimal(0)
        hc.attr["diff_weight"] = Decimal(0)
        return hc

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
                INSERT INTO HEALTH
                    (user_id, name, date, time, height, weight, bmi, pro_weight, diff_weight)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s); """,
                (self.attr["user_id"],
                self.attr["name"],
                self.attr["date"],
                self.attr["time"],
                self.attr["height"],
                self.attr["weight"],
                self.attr["bmi"],
                self.attr["pro_weight"],
                self.attr["diff_weight"]
                ))
                
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
                UPDATE  
                SET user_id = %s,
                    name = %s,
                    date = %s,
                    time = %s,
                    height = %s,
                    weight = %s,
                    bmi = %s,
                    pro_weight = %s,
                    diff_weight = %s
                WHERE id = %s; """,
                (self.attr["user_id"],
                self.attr["name"],
                self.attr["date"],
                self.attr["time"],
                self.attr["height"],
                self.attr["weight"],
                self.attr["bmi"],
                self.attr["pro_weight"],
                self.attr["diff_weight"]),
                self.attr["id"])
            con.commit()
        
        return self.attr["id"]
    
    # select_by_user_id gets the user.
    @staticmethod
    def select_by_user_id(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   HEALTH
                WHERE  user_id = %s;
            """, (user_id,))
            results = cursor.fetchall()
        
        records = []
        for data in results:
            hc = healthcan()
            hc.attr["id"] = data["id"]
            hc.attr["user_id"] = data["user_id"]
            hc.attr["name"] = data["name"]
            hc.attr["date"] = data["date"]
            hc.attr["time"] = data["time"]
            hc.attr["height"] = data["height"]
            hc.attr["weight"] = data["weight"]
            hc.attr["bmi"] = data["bmi"]
            hc.attr["pro_weight"] = data["pro_weight"]
            hc.attr["diff_weight"] = data["diff_weight"]
            records.append(hc)
        
        return records
       
    # delete deletes the data.
    def delete(self):
        if self.attr["id"] == None: return None
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM HEALTH
                WHERE id = %s; """,
                (self.attr["id"],))
            con.commit()

        return self.attr["id"]

    # _index returns an index list of data.
    @staticmethod
    def _index(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT id FROM HEALTH
                WHERE user_id = %s; """,
                (user_id,))
            con.commit()
            recodes = cursor.fetchall()
        
        ids = [recode[0] for recode in recodes]
        return ids

    # weight gets weight data.
    @staticmethod
    def weight(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT weight FROM HEALTH
                WHERE user_id = %s
                ORDER BY `id` ASC; """,
                (user_id,))
            con.commit()
            recodes = cursor.fetchall()
            return recodes

    # bmi gets bmi data.
    @staticmethod
    def bmi(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT bmi FROM HEALTH
                WHERE user_id = %s
                ORDER BY `id` ASC; """,
                (user_id,))
            con.commit()
            recodes = cursor.fetchall()
            return recodes
