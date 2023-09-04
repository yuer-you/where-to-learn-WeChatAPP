#!
# -*- coding: utf-8 -*-

import cgi
import cgitb
import pymysql
import json
cgitb.enable()

# ���ݿ����Ӳ���
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "����û���",
    "password": "�������",
    "database": "user",
    "charset": "utf8"
}

def update_db(query, values):
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
        cursor.close()


# ����һ�� FieldStorage ʵ���Ի�ȡ GET ����
form = cgi.FieldStorage()

openid = form.getvalue('openid')
change_classroom = form.getvalue('change_classroom')
history_classroom = form.getvalue('history_classroom')

change_classroom = json.loads(change_classroom)
history_classroom = json.loads(history_classroom)

# �����û�����
update_users_classroom = "UPDATE users SET star_classroom_1 = %s, star_classroom_2 = %s, star_classroom_3 = %s WHERE openid = %s"
update_users_classroom_success = update_db(update_users_classroom, (change_classroom[0], change_classroom[1], change_classroom[2], openid))

# �����ӵĽ���+1
update_all_classroom_success = True

update_number_classroom_plus = f"UPDATE classroom_collect SET collect = collect + 1 WHERE classroom = %s"
for i in range(3):
    if (change_classroom[i] != None):
        update_all_classroom_success = (update_all_classroom_success and update_db(update_number_classroom_plus, (change_classroom[i],)))

# ɾ���Ľ���-1
update_number_classroom_subtract = f"UPDATE classroom_collect SET collect = collect - 1 WHERE classroom = %s"
for i in range(3):
    if (history_classroom[i] != None):
        update_all_classroom_success = (update_all_classroom_success and update_db(update_number_classroom_subtract, (history_classroom[i],)))

# ����bool_classroom
if (change_classroom[0] == None and change_classroom[1] == None and change_classroom[2] == None):
    update_bool_classroom = "UPDATE users SET bool_classroom = 0 WHERE openid = %s"
else:
    update_bool_classroom = "UPDATE users SET bool_classroom = 1 WHERE openid = %s"
update_bool_classroom_success = update_db(update_bool_classroom, (openid,))

# ���JSON��Ӧ
print("Content-type: application/json\n")
response = {
    "update_users_classroom_success": update_users_classroom_success,
    "update_all_classroom_success": update_all_classroom_success,
    "update_bool_classroom_success": update_bool_classroom_success
}
print(json.dumps(response))

