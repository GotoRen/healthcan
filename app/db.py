import MySQLdb
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Providing information related to database connections.
class DBConnector(object):
    def __init__(self, dbName=None):
        load_dotenv(verbose=True)
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.account = {
            'host': os.environ.get("DB_HOST"),
            'user': os.environ.get("DB_USER"),
            'passwd': os.environ.get("DB_PASS"),
            'charset': os.environ.get("DB_CHAR")
        }
        self.db = dbName

    def __enter__(self):
        if self.db == None:
            self.connect = MySQLdb.connect(
                host=self.account["host"],
                user=self.account["user"],
                passwd=self.account["passwd"],
                charset=self.account["charset"]
            )
        else:
            self.connect = MySQLdb.connect(
                host=self.account["host"],
                user=self.account["user"],
                passwd=self.account["passwd"],
                db=self.db,
                charset=self.account["charset"]
            )
            
        return self.connect

    def __exit__(self, exception_type, exception_value, traceback):
        if self.connect:
            self.connect.close()
