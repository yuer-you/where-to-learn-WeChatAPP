#!
# -*- coding: utf-8 -*-

import pymysql

class MysqlConect:

    def __init__(self):
        pass

    def connect(self, building, data):
        host = "localhost"
        user_server = "你的用户名"
        password_server = "你的密码"
        database = building
        classroom = []

        # 获取连接
        try:
            connection = pymysql.connect(host=host,
                                         user=user_server,
                                         password=password_server,
                                         database=database)
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM `{data}`"
                cursor.execute(sql)
                result = cursor.fetchall()

                # 获取行数和列数
                row = len(result)
                column = len(result[0]) if row > 0 else 0
                classroom = [[0] * (column - 1) for _ in range(row)]

                # 将教室数据存入列表
                for i in range(row):
                    for j in range(column):
                        classroom[i][j - 1] = result[i][j]

        except pymysql.Error as e:
            print(f"Error: {e}")

        finally:
            if connection:
                connection.close()

        return classroom