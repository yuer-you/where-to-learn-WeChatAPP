#!
# -*- coding: utf-8 -*-

import cgi
import json
import pymysql

# 设置数据库连接信息
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "你的用户名",
    "password": "你的密码",
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
        # 出现错误时回滚更改并返回错误响应
        db.rollback()
        print("Content-type: application/json\n")
        print(f'{{"false": false, "message": "change fail: {str(e)}"}}')
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# 获取CGI参数
form = cgi.FieldStorage()
openid = form.getvalue('openid')

# 处理time_ocr操作
time_ocr_query = "UPDATE users SET time_ocr = time_ocr - 1 WHERE openid = %s"
time_ocr_success = update_db(time_ocr_query, (openid,))

# 处理bool_schedule操作
bool_schedule_query = "UPDATE users SET bool_schedule = 1 WHERE openid = %s"
bool_schedule_success = update_db(bool_schedule_query, (openid,))

# 输出JSON响应
print("Content-type: application/json\n")
response = {
    "time_ocr_success": time_ocr_success,
    "bool_schedule_success": bool_schedule_success
}
print(json.dumps(response))
