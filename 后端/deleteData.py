#!
# -*- coding: utf-8 -*-
import cgi
import pymysql
from normalizeOpenidAPI import remove_special_characters

def delete_table_row(table_name, condition_column, condition_value, schedule_table_name):
    try:
        # �������ݿ�����
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='����û���',
                             password='�������',
                             database='user',
                             charset='utf8')

        # ����һ���α����
        cursor = db.cursor()

        # ִ��ɾ��ָ���еĲ���
        sql = f"DELETE FROM {table_name} WHERE {condition_column} = %s;"
        cursor.execute(sql, (condition_value, ))

        # ִ��ɾ����Ĳ���
        sql = f"DROP TABLE IF EXISTS {schedule_table_name};"
        cursor.execute(sql)

        # �ύ���ĵ����ݿ�
        db.commit()

        print('success', end="")

    except Exception as e:
        # �����쳣ʱ�ع�
        db.rollback()
        print("Error:", e)

    finally:
        # �ر��α�����ݿ�����
        cursor.close()
        db.close()


print("Content-type: text/html; charset=utf-8")
print()
form = cgi.FieldStorage()
# ��ȡopenid������ֵ��������ڵĻ�
openid = form.getvalue('openid', '')
schedule_table_name = remove_special_characters(openid)  # openid�淶��������

# ����ɾ������еĺ���
table_name_to_delete_from = "users"     # ���ñ�
condition_column_to_delete = "openid"   # ���ñ�
delete_table_row(table_name_to_delete_from, condition_column_to_delete, openid, schedule_table_name)
