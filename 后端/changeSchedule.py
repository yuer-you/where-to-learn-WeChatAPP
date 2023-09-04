#!
# -*- coding: utf-8 -*-

import cgi
import cgitb
import pymysql
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

def change_day(day):
    if (day == 0):
        day = 'monday'
    elif (day == 1):
        day = 'tuesday'
    elif (day == 2):
        day = 'wednesday'
    elif (day == 3):
        day = 'thursday'
    elif (day == 4):
        day = 'friday'
    elif (day == 5):
        day = 'saturday'
    else:
       day = 'sunday'

    return day

def change_class(day):
    if (day == 0):
        day = 'first_class'
    elif (day == 1):
        day = 'second_class'
    elif (day == 2):
        day = 'third_class'
    elif (day == 3):
        day = 'fourth_class'
    elif (day == 4):
        day = 'fifth_class'
    elif (day == 5):
        day = 'sixth_class'
    else:
       day = 'seventh_class'

    return day

try:
    # ����һ�� FieldStorage ʵ���Ի�ȡ GET ����
    form = cgi.FieldStorage()

    table = form.getvalue('table')
    table = table.lower()
    day = int(form.getvalue('day'))
    day = change_day(day)
    class_num = int(form.getvalue('class'))
    class_num = change_class(class_num)
    classname = form.getvalue('classname')
    weeklong = form.getvalue('weeklong')
    teacher = form.getvalue('teacher')
    classroom = form.getvalue('classroom')

    # �������Ϊ None �ı���
    classname = classname if classname is not None else ''
    weeklong = weeklong if weeklong is not None else ''
    teacher = teacher if teacher is not None else ''
    classroom = classroom if classroom is not None else ''

    if (classname == '' and weeklong == '' and teacher == '' and classroom == ''):
        new_data = None
    else:
        new_data = classname + '\n' + weeklong + '\n' + teacher + '\n' + classroom

    # �������ݿ�
    db = pymysql.connect(**db_config)
    cursor = db.cursor()

    # ������Ҫִ�е�SQL���
    update_sql = f"UPDATE {table} SET {day} = %s WHERE class = %s"
    cursor.execute(update_sql, (new_data, class_num))
    
    # �ύ���Ĳ����سɹ���Ӧ
    db.commit()
    print("Content-type: application/json")
    print()
    print('{"success": true, "message": "change success"}')

except Exception as e:
    # ���ִ���ʱ�ع����Ĳ����ش�����Ӧ
    db.rollback()
    print("Content-type: application/json")
    print()
    print(f'{{"success": false, "message": "change fail: {str(e)}"}}')

finally:
    # �ر����ݿ�����
    db.close()
