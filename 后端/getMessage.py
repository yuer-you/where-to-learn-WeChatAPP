#!
# -*- coding: utf-8 -*-

import cgi
import pymysql
import json

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
    # ���ӵ����ݿ�
    connection = pymysql.connect(**db_config)

    # �����α����
    cursor = connection.cursor()

    # ��ѯ���ݿ��е���Ϣ
    cursor.execute("SELECT message FROM broadcast")

    # ��ȡ��ѯ���
    result = cursor.fetchone()

    if result:
        # ����ѯ���ת��Ϊ JSON ��ʽ
        data = {
            "text": result[0]
        }
        json_data = json.dumps(data, ensure_ascii=True)
        # ������Ӧͷ��ָ����������ΪJSON
        print("Content-type: application/json; charset=utf-8\n")
        print(json_data)
    else:
        # ���û�н��������һ���� JSON ����
        print(json.dumps({}))

except Exception as e:
    print("Content-type: text/json\n")
    print(e)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
