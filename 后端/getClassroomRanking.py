#!
# -*- coding: UTF-8 -*-

import pymysql
import cgi
import cgitb
import json
cgitb.enable()  # ��ʾ������Ϣ

# ���ݿ�������Ϣ
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "����û���",
    "password": "�������",
    "database": "user",
    "charset": "utf8"
}

# �������ݿ�
db = pymysql.connect(**db_config)
cursor = db.cursor()

# ��ѯ������collect��
query = "SELECT * FROM classroom_collect ORDER BY collect DESC LIMIT 10"
cursor.execute(query)
results = cursor.fetchall()

# ��ȡ��������浽����
collect_values = [result for result in results]

# �ر����ݿ�����
cursor.close()
db.close()

result_dict = {'classroomRanking': collect_values}
result_json = json.dumps(result_dict, ensure_ascii=True)

# ���Content-Typeͷ��JSON��ʽ������
print("Content-Type: application/json; charset=utf-8\n")
print(result_json)
