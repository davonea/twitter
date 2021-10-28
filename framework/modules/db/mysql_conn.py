#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from framework.modules.bases.service_config import *
from framework.modules.bases.log import *


class Config(object):
    """
    # Config().get_content("user_information")
    """

    def get_content(self, section):
        result = {}
        for option in GET_OPTIONS(section):
            value = GET_CONF(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class BasePymysqlPool(object):
    def __init__(self, host, port, user, password, db_name=None):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None


class MyPymysqlPool(BasePymysqlPool):

    __pool = None

    def __init__(self, section):
        self.conf = Config().get_content(section)
        super(MyPymysqlPool, self).__init__(**self.conf)
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()

    def __getConn(self):
        if MyPymysqlPool.__pool is None:
            __pool = PooledDB(creator=pymysql,
                              mincached=1,
                              maxcached=20,
                              host=self.db_host,
                              port=self.db_port,
                              user=self.user,
                              passwd=self.password,
                              db=self.db,
                              use_unicode=False,
                              charset="utf8",
                              cursorclass=DictCursor)
        return __pool.connection()

    def getAll(self, sql, param=None):

        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    @log("mysql")
    def getOne(self, sql, param=None):

        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchone()
            else:
                result = False
            return result
        except Exception as e:
            logger().error(e)
            return False

    def getMany(self, sql, num, param=None):

        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertMany(self, sql, values):

        self._cursor.execute("SET CHARACTER SET utf8mb4;")
        count = self._cursor.executemany(sql, values)
        self._conn.commit()
        return count

    def __query(self, sql, param=None):
        self._cursor.execute("SET CHARACTER SET utf8mb4;")
        if param is None:
            count = self._cursor.execute(sql)
        else:
            self._cursor
            count = self._cursor.execute(sql, param)
        self._conn.commit()
        return count

    def update(self, sql, param=None):
        return self.__query(sql, param)

    @log("mysql")
    def insert(self, sql, param=None):

        try:
            return self.__query(sql, param)
        except Exception as e:
            logger().error(e)
            return 0

    def delete(self, sql, param=None):
        return self.__query(sql, param)

    def begin(self):
        self._conn.autocommit(0)

    def end(self, option='commit'):

        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):

        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()


if __name__ == '__main__':
    mysql = MyPymysqlPool("mysql")

    sqlAll = "select * from myTest.aa;"
    result = mysql.getAll(sqlAll)
    print(result)

    sqlAll = "select * from myTest.aa;"
    result = mysql.getMany(sqlAll, 2)
    print(result)

    result = mysql.getOne(sqlAll)
    print(result)

    # mysql.insert("insert into myTest.aa set a=%s", (1))

    mysql.dispose()
