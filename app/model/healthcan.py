import MySQLdb
import datetime
import pytz
import decimal
from _pydecimal import Decimal
from decimal import Decimal
from db import DBConnector
from model.project import project


class healthcan:
    # init runs initialization.
    def __init__(self):
        self.attr = {}
        self.attr["id"] = None  # ID
        self.attr["user_id"] = None  # ユーザID
        self.attr["name"] = None  # 名前
        self.attr["date"] = None  # 日
        self.attr["time"] = None  # 時
        self.attr["height"] = None  # 身長
        self.attr["weight"] = None  # 体重
        self.attr["bmi"] = None  # BMI
        self.attr["pro_weight"] = None  # 適正体重
        self.attr["diff_weight"] = None  # 適正体重までの差（体重-適正体重）

    # is_valid determines the correctness of the value.
    def is_valid(self):
        return all(
            [
                self.attr["id"] is None or type(self.attr["id"]) is int,
                self.attr["user_id"] is not None and type(self.attr["user_id"]) is int,
                self.attr["name"] is not None
                and type(self.attr["name"]) is str
                and len(self.attr["name"]) > 0,
                self.attr["date"] is not None
                and type(self.attr["date"]) is datetime.date
                or type(self.attr["date"]) is str
                or type(self.attr["date"]) is int,
                self.attr["time"] is not None,
                self.attr["height"] is not None,
                self.attr["weight"] is not None,
                self.attr["bmi"] is not None,
                self.attr["pro_weight"] is not None,
                self.attr["diff_weight"] is not None,
            ]
        )

    # build returns the format of each element.
    @staticmethod
    def build():
        hc = healthcan()
        now = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
        hc.attr["date"] = "{0:%Y-%m-%d}".format(now.date())
        hc.attr["time"] = "{0:%H:%M:%S}".format(now.time())
        hc.attr["height"] = Decimal(0)
        hc.attr["weight"] = Decimal(0)
        hc.attr["bmi"] = Decimal(0)
        hc.attr["pro_weight"] = Decimal(0)
        hc.attr["diff_weight"] = Decimal(0)

        return hc

    # save returns _db_save when validation is successful.
    def save(self):
        if self.is_valid:
            return self._db_save()
        return False

    # _db_save returns if the id is None, execute insert, and the id exists, execute update.
    def _db_save(self):
        if self.attr["id"] == None:
            return self._db_save_insert()
        return self._db_save_update()

    ##############
    ### INSERT ###
    ##############
    # _db_save_insert insert the data.
    def _db_save_insert(self):
        with DBConnector(
            dbName="db_%s" % project.name()
        ) as con, con.cursor() as cursor:
            # データの保存(INSERT)
            cursor.execute(
                """
                INSERT INTO healthcan
                    (user_id, name, date, time, height, weight, bmi, pro_weight, diff_weight)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s); """,
                (
                    self.attr["user_id"],
                    self.attr["name"],
                    self.attr["date"],
                    self.attr["time"],
                    self.attr["height"],
                    self.attr["weight"],
                    self.attr["bmi"],
                    self.attr["pro_weight"],
                    self.attr["diff_weight"],
                ),
            )

            # INSERTされたAUTO INCREMENT値を取得
            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]

    ##############
    ### SELECT ###
    ##############
    # find returns the recode matched by id.
    @staticmethod
    def find(id):
        with DBConnector(dbName="db_%s" % project.name()) as con, con.cursor(
            MySQLdb.cursors.DictCursor
        ) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM   healthcan
                WHERE  id = %s;
            """,
                (id,),
            )
            results = cursor.fetchall()

        if len(results) == 0:
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

    # select_by_user_id returns the recode matched by user_id.
    @staticmethod
    def select_by_user_id(user_id):
        with DBConnector(dbName="db_%s" % project.name()) as con, con.cursor(
            MySQLdb.cursors.DictCursor
        ) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM   healthcan
                WHERE  user_id = %s;
            """,
                (user_id,),
            )
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

    # weight returns the weight.
    @staticmethod
    def weight(user_id):
        with DBConnector(dbName="db_%s" % project.name()) as con, con.cursor(
            MySQLdb.cursors.DictCursor
        ) as cursor:
            cursor.execute(
                """
                SELECT weight FROM healthcan
                WHERE user_id = %s
                ORDER BY `id` ASC; """,
                (user_id,),
            )
            con.commit()
            recodes = cursor.fetchall()

            return recodes

    # bmi returns the bmi.
    @staticmethod
    def bmi(user_id):
        with DBConnector(dbName="db_%s" % project.name()) as con, con.cursor(
            MySQLdb.cursors.DictCursor
        ) as cursor:
            cursor.execute(
                """
                SELECT bmi FROM healthcan
                WHERE user_id = %s
                ORDER BY `id` ASC; """,
                (user_id,),
            )
            con.commit()
            recodes = cursor.fetchall()

            return recodes

    # _index returns the id.
    @staticmethod
    def _index(user_id):
        with DBConnector(
            dbName="db_%s" % project.name()
        ) as con, con.cursor() as cursor:
            cursor.execute(
                """
                SELECT id FROM healthcan
                WHERE user_id = %s; """,
                (user_id,),
            )
            con.commit()
            recodes = cursor.fetchall()

        ids = [recode[0] for recode in recodes]

        return ids

    ##############
    ### DELETE ###
    ##############
    # _db_save_delete delete the recode.
    def _db_save_delete(self):
        if self.attr["id"] == None:
            return None
        with DBConnector(
            dbName="db_%s" % project.name()
        ) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute(
                """
                DELETE FROM healthcan
                WHERE id = %s; """,
                (self.attr["id"],),
            )
            con.commit()

        return self.attr["id"]

    ##############
    ### UPDATE ###
    ##############
    # _db_save_update update the recode.
    def _db_save_update(self):
        with DBConnector(
            dbName="db_%s" % project.name()
        ) as con, con.cursor() as cursor:
            # データの保存(UPDATE)
            cursor.execute(
                """
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
                (
                    self.attr["user_id"],
                    self.attr["name"],
                    self.attr["date"],
                    self.attr["time"],
                    self.attr["height"],
                    self.attr["weight"],
                    self.attr["bmi"],
                    self.attr["pro_weight"],
                    self.attr["diff_weight"],
                ),
                self.attr["id"],
            )
            con.commit()

        return self.attr["id"]

    ############
    ### mock ###
    ############
    # Create mock data definition.
    @staticmethod
    def migrate():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS db_%s;" % project.name())
            cursor.execute("USE db_%s;" % project.name())
            cursor.execute(
                """
                CREATE TABLE `healthcan` (
                  `id`          int(11) unsigned NOT NULL AUTO_INCREMENT,
                  `user_id`     int(11) unsigned NOT NULL,
                  `name`        varchar(256)     DEFAULT NULL,
                  `date`        date             NOT NULL,
                  `time`        time             NOT NULL,
                  `height`      decimal(4,1)     NOT NULL,
                  `weight`      decimal(4,1)     NOT NULL,
                  `bmi`         decimal(3,1)     NOT NULL,
                  `pro_weight`  decimal(5,2)     NOT NULL,
                  `diff_weight` decimal(4,2)     NOT NULL,
                  PRIMARY KEY (`id`),
                  KEY `user_id` (`user_id`),
                  KEY `name` (`name`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8; """
            )
            con.commit()

    # Delete mock DB
    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS db_%s;" % project.name())
            con.commit()
