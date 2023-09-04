#!
# -*- coding: utf-8 -*-

import pymysql
import cgi
import json

# ������Ϣ�ֵ�
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "����û���",
    "password": "�������",
    "database": "user",
    "charset": "utf8"
}

# ��ȡ����
form = cgi.FieldStorage()
table = form.getvalue('table')
table_name = table.lower()

# �������ݿ�����
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# ��ѯ����
try:
    query = f"SELECT * FROM {table_name} LIMIT 7"
    cursor.execute(query)
    rows = cursor.fetchall()

    # # ��ȡ3�е�9�е�����
    original_data = [[row[i] for i in range(2, 9)] for row in rows]

    for row in original_data:
        for i in range(len(row)):
            if row[i] and '\n' in row[i]:
                split_elements = row[i].split('\n')
                if split_elements[-1] == '':
                    split_elements = split_elements[:-1]  # ȥ��ĩβ�Ŀ�Ԫ��
                original_data[original_data.index(row)][i] = split_elements

    response_data = {'schedule': original_data}
    # ���ֵ�ת���� JSON ��ʽ���ַ���
    response_json = json.dumps(response_data, ensure_ascii=True)
    # ������Ӧͷ��ָ����������ΪJSON��ʽ
    print('Content-type: application/json; charset=utf-8\n')
    # ��� JSON ��ʽ���ַ���
    print(response_json)

except Exception as e:
    print("Content-type: text/json\n")
    print(e)

finally:
    cursor.close()
    connection.close()
