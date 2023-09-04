#!
# -*- coding: utf-8 -*-
import cgi
import pymysql
from normalizeOpenidAPI import remove_special_characters

def delete_table_row(table_name, condition_column, condition_value, schedule_table_name):
    try:
        # 建立数据库连接
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='你的用户名',
                             password='你的密码',
                             database='user',
                             charset='utf8')

        # 创建一个游标对象
        cursor = db.cursor()

        # 执行删除指定行的操作
        sql = f"DELETE FROM {table_name} WHERE {condition_column} = %s;"
        cursor.execute(sql, (condition_value, ))

        # 执行删除表的操作
        sql = f"DROP TABLE IF EXISTS {schedule_table_name};"
        cursor.execute(sql)

        # 提交更改到数据库
        db.commit()

        print('success', end="")

    except Exception as e:
        # 发生异常时回滚
        db.rollback()
        print("Error:", e)

    finally:
        # 关闭游标和数据库连接
        cursor.close()
        db.close()


print("Content-type: text/html; charset=utf-8")
print()
form = cgi.FieldStorage()
# 获取openid参数的值，如果存在的话
openid = form.getvalue('openid', '')
schedule_table_name = remove_special_characters(openid)  # openid规范化命名库

# 调用删除表和行的函数
table_name_to_delete_from = "users"     # 不用变
condition_column_to_delete = "openid"   # 不用变
delete_table_row(table_name_to_delete_from, condition_column_to_delete, openid, schedule_table_name)
