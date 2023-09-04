#!
# -*- coding: utf-8 -*-
import pymysql

# 数据库连接参数
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "qwer0000A.",
    "database": "user",
    "charset": "utf8"
}

try:
    # 连接数据库
    connection = pymysql.connect(**db_config)

    # 创建游标对象
    with connection.cursor() as cursor:
        # 更新语句，将 time_ocr 列的值更新为 3
        update_query = "UPDATE users SET time_ocr = 3"
        
        # 执行更新操作
        cursor.execute(update_query)
        
        # 提交更改
        connection.commit()
        
        print("Update successful")
        
except pymysql.Error as e:
    # 如果出现错误，打印错误信息
    print("Error:", e)

finally:
    # 关闭数据库连接
    if connection:
        connection.close()
