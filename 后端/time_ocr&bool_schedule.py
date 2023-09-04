#!
# -*- coding: utf-8 -*-

import cgi
import json
import pymysql

# �������ݿ�������Ϣ
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "����û���",
    "password": "�������",
    "database": "user",
    "charset": "utf8"
}

def update_db(query, values=None):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        connection.commit()
        return True
    except Exception as e:
        # ���ִ���ʱ�ع����Ĳ����ش�����Ӧ
        db.rollback()
        print("Content-type: application/json\n")
        print(f'{{"false": false, "message": "change fail: {str(e)}"}}')
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ��ȡCGI����
form = cgi.FieldStorage()
openid = form.getvalue('openid')

# ����time_ocr����
time_ocr_query = "UPDATE users SET time_ocr = time_ocr - 1 WHERE openid = %s"
time_ocr_success = update_db(time_ocr_query, (openid,))

# ����bool_schedule����
bool_schedule_query = "UPDATE users SET bool_schedule = 1 WHERE openid = %s"
bool_schedule_success = update_db(bool_schedule_query, (openid,))

# ���JSON��Ӧ
print("Content-type: application/json\n")
response = {
    "time_ocr_success": time_ocr_success,
    "bool_schedule_success": bool_schedule_success
}
print(json.dumps(response))
