#!
# -*- coding: utf-8 -*-
import pymysql
import cgi

# ���ݿ����Ӳ���
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "qwer0000A.",
    "database": "user",
    "charset": "utf8"
}

try:
    # �������ݿ�
    connection = pymysql.connect(**db_config)

    # �����α����
    with connection.cursor() as cursor:
        # ������䣬�� time_ocr �е�ֵ����Ϊ 3
        update_query = "UPDATE users SET time_ocr = %s"

        # ִ�и��²���
        cursor.execute(update_query, (3,))

        # �ύ����
        connection.commit()

        print('Content-type: application/json; charset=utf-8\n')
        print("Update successful")

except pymysql.Error as e:
    # ������ִ��󣬴�ӡ������Ϣ
    print('Content-type: application/json; charset=utf-8\n')
    print("Error:", e)

finally:
    # �ر����ݿ�����
    if connection:
        connection.close()
