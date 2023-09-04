#!
# -*- coding: utf-8 -*-
import cgi
import pymysql

def save_username_to_database(openid, username):
    # �������ݿ�
    connection = pymysql.connect(host="localhost",
                                 port=3306,
                                 user="����û���",
                                 password="�������",
                                 database="user",
                                 charset="utf8")

    try:
        with connection.cursor() as cursor:
            # ��ѯ�Ƿ��и�openid��¼����û��������¼�¼���������username�ֶ�
            query = "SELECT * FROM users WHERE openid=%s"
            cursor.execute(query, (openid,))
            result = cursor.fetchone()
            if result:
                # ���м�¼������username�ֶ�
                update_query = "UPDATE users SET username=%s WHERE openid=%s"
                cursor.execute(update_query, (username, openid))
            else:
                # û�м�¼������
                print("Content-type: text/html\n")
                print("<html><body><h1>user inexistence</h1></body></html>")

        # �ύ����
        connection.commit()

    except Exception as e:
        # ���ִ���ʱ�ع����Ĳ����ش�����Ӧ
        db.rollback()
        print("Content-type: application/json\n")
        print(f'{{"success": false, "message": "change fail: {str(e)}"}}')

    finally:
        connection.close()

# ��ȡGET�������
form = cgi.FieldStorage()

# ����Ƿ����username����
if "openid" in form and "username" in form:
    openid = form.getvalue("openid")
    username = form.getvalue("username")
    # �������ݿ�
    save_username_to_database(openid, username)
    print("Content-type: text/html\n")
    print("<html><body><h1>success</h1></body></html>")
else:
    print("Content-type: text/html\n")
    print("<html><body><h1>no username/openid</h1></body></html>")
