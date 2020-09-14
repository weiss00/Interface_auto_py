# -*- coding:utf-8 -*-

'''
    DB数据库工具类
'''

import pymysql

class dbUtils:

    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.conn, self.cursor = self.db_connect(host, user, password, port, database)

    def db_connect(self, host, user, password, port, database, charset='utf8'):
        try:
            conn = pymysql.connect(host=host,user=user,password=password,port=port,database=database, charset=charset)
            cursor = conn.cursor()
            return conn, cursor
        except:
            raise RuntimeError("数据库连接失败")

    def select_sql_one(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result[0]
        except:
            print("Error: unable to fetch data")
        finally:
            self.close_conn()

    def select_sql_more(self):
        pass

    def update_sql(self, conn, sql):
        pass

    def delete_sql(self, conn, sql):
        pass

    def insert_sql(self, conn, sql):
        pass

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
