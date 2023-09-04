#!
# -*- coding: utf-8 -*-

import pymysql

class MysqlConect:

    def __init__(self):
        pass

    def connect(self, building, data):
        host = "localhost"
        user_server = "����û���"
        password_server = "�������"
        database = building
        classroom = []

        # ��ȡ����
        try:
            connection = pymysql.connect(host=host,
                                         user=user_server,
                                         password=password_server,
                                         database=database)
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM `{data}`"
                cursor.execute(sql)
                result = cursor.fetchall()

                # ��ȡ����������
                row = len(result)
                column = len(result[0]) if row > 0 else 0
                classroom = [[0] * (column - 1) for _ in range(row)]

                # ���������ݴ����б�
                for i in range(row):
                    for j in range(column):
                        classroom[i][j - 1] = result[i][j]

        except pymysql.Error as e:
            print(f"Error: {e}")

        finally:
            if connection:
                connection.close()

        return classroom