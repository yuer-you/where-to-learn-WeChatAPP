#!
# -*- coding: utf-8 -*-

import cgi
import pymysql
import datetime
import json

# ��ȡ���������
today = datetime.datetime.today()

# ��ȡ���������ڼ���0��ʾ����һ��6��ʾ�����գ�
day_of_week = today.weekday()

# ��ȡ���ݵĲ���
form = cgi.FieldStorage()
table = form.getvalue('table')
table = table.lower()

# ���ݿ�������Ϣ�ֵ�
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "����û���",
    "password": "�������",
    "database": "user",
    "charset": "utf8"
}

# �������ݿ�����
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # ���ô洢����
        cursor.callproc('schedule_search', (table,))

        # ��ȡ���н����
        result = cursor.fetchall()

        # ��������б�
        result_list = []

        if result:
            for row in result:
                row_values = list(row)  # ��Ԫ��ת��Ϊ�б�
                result_list.append(row_values)

            for row in result_list:
                for i in range(len(row)):
                    if row[i] and '\n' in row[i]:
                        split_elements = row[i].split('\n')
                        if split_elements[-1] == '':
                            split_elements = split_elements[:-1]  # ȥ��ĩβ�Ŀ�Ԫ��
                        result_list[result_list.index(row)][i] = split_elements

        # �������
        processed_output = []
        for item in result_list:
            if item[0] is not None:
                processed_output.append(item[0])
            else:
                processed_output.append(None)

        # ��������ֵ�
        result_dict = {'today_name': day_of_week,'today_schedule': processed_output}

        # ������ֵ�ת��Ϊ JSON ��ʽ���ַ���
        result_json = json.dumps(result_dict, ensure_ascii=True)
        # ���ؽ��
        print("Content-type: application/json; charset=utf-8\n")
        print(result_json)

finally:
    connection.close()
