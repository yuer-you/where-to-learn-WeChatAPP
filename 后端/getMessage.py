#!
# -*- coding: utf-8 -*-

import cgi
import pymysql
import json

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
    # 连接到数据库
    connection = pymysql.connect(**db_config)

    # 创建游标对象
    cursor = connection.cursor()

    # 查询数据库中的信息
    cursor.execute("SELECT message FROM broadcast")

    # 获取查询结果
    result = cursor.fetchone()

    if result:
        # 将查询结果转换为 JSON 格式
        data = {
            "text": result[0]
        }
        json_data = json.dumps(data, ensure_ascii=True)
        # 设置响应头，指定内容类型为JSON
        print("Content-type: application/json; charset=utf-8\n")
        print(json_data)
    else:
        # 如果没有结果，返回一个空 JSON 对象
        print(json.dumps({}))

except Exception as e:
    print("Content-type: text/json\n")
    print(e)

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
