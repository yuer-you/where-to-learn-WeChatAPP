#!
# -*- coding: utf-8 -*-

import cgi
import pymysql
import datetime
import json
import re

# ���ݿ�������Ϣ�ֵ�
def config(database):
    db_config = {
        "host": "localhost",
        "port": 3306,
        "user": "����û���",
        "password": "�������",
        "database": database,
        "charset": "utf8"
    }
    return db_config

# ���ݿ�����
def connect_and_query(query, values, database):
    db_config = config(database)

    try:
        # �������ݿ�
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            # ִ�в�ѯ���
            cursor.execute(query, values)
            result = cursor.fetchall()

            # ��ȡ��ѯ����е�ʵ�����ݲ���
            data_list = [list(result) for result in result]
            data_list = data_list[0]

            return data_list

    except Exception as e:
        print("Content-type: text/json\n")
        print(e)

    finally:
        # �ر����ݿ�����
        connection.close()


# ��ȡ���������
today = datetime.datetime.today()

# ��ȡ���������ڼ���0��ʾ����һ��6��ʾ�����գ�
day_of_week = today.weekday()

# ��ȡ�ꡢ�¡���
year = today.year
month = today.month
day = today.day

# ƴ��Ϊ��.��.�յ��ַ���
year_month_day = f"{year}.{month}.{day}"    # ����

# ��ȡ���ݵĲ���
form = cgi.FieldStorage()
buildingName = json.loads(form.getvalue('buildingName'))
classroomNumber = json.loads(form.getvalue('classroomNumber'))

# ��������
classroomState = [None, None, None]    # ���
for i in range(3):
    if (buildingName[i] is not None):
        q = f"SELECT * FROM `{year_month_day}` WHERE classroom = %s"
        classroomState[i] = connect_and_query(q, (classroomNumber[i],), buildingName[i])
    else:
        classroomState[i] = None

# ��������ֵ�
result_dict = {'classroomState': classroomState, 'today_name': day_of_week}

# ������ֵ�ת��Ϊ JSON ��ʽ���ַ���
result_json = json.dumps(result_dict, ensure_ascii=True)
# ���ؽ��
print("Content-type: application/json; charset=utf-8\n")
print(result_json)
