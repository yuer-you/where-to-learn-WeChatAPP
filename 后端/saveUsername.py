#!
# -*- coding: utf-8 -*-
import cgi
import pymysql

def save_username_to_database(openid, username):
    # 连接数据库
    connection = pymysql.connect(host="localhost",
                                 port=3306,
                                 user="你的用户名",
                                 password="你的密码",
                                 database="user",
                                 charset="utf8")

    try:
        with connection.cursor() as cursor:
            # 查询是否有该openid记录，若没有则插入新记录，否则更新username字段
            query = "SELECT * FROM users WHERE openid=%s"
            cursor.execute(query, (openid,))
            result = cursor.fetchone()
            if result:
                # 已有记录，更新username字段
                update_query = "UPDATE users SET username=%s WHERE openid=%s"
                cursor.execute(update_query, (username, openid))
            else:
                # 没有记录，报错
                print("Content-type: text/html\n")
                print("<html><body><h1>user inexistence</h1></body></html>")

        # 提交更改
        connection.commit()

    except Exception as e:
        # 出现错误时回滚更改并返回错误响应
        db.rollback()
        print("Content-type: application/json\n")
        print(f'{{"success": false, "message": "change fail: {str(e)}"}}')

    finally:
        connection.close()

# 获取GET请求参数
form = cgi.FieldStorage()

# 检查是否存在username参数
if "openid" in form and "username" in form:
    openid = form.getvalue("openid")
    username = form.getvalue("username")
    # 存入数据库
    save_username_to_database(openid, username)
    print("Content-type: text/html\n")
    print("<html><body><h1>success</h1></body></html>")
else:
    print("Content-type: text/html\n")
    print("<html><body><h1>no username/openid</h1></body></html>")
