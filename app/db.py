import MySQLdb

class DBConnector(object):

    def __init__(self, dbName=None):
        self.account = {
            'host': 'mysql',
            'user': 'root',
            'passwd': 'abc123',
            'charset': 'utf8'
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
