#!
# -*- coding: utf-8 -*-

import pymysql
import cgi
import json

# 连接信息字典
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "你的用户名",
    "password": "你的密码",
    "database": "user",
    "charset": "utf8"
}

# 获取表名
form = cgi.FieldStorage()
table = form.getvalue('table')
table_name = table.lower()

# 建立数据库连接
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# 查询数据
try:
    query = f"SELECT * FROM {table_name} LIMIT 7"
    cursor.execute(query)
    rows = cursor.fetchall()

    # # 提取3列到9列的数据
    original_data = [[row[i] for i in range(2, 9)] for row in rows]

    for row in original_data:
        for i in range(len(row)):
            if row[i] and '\n' in row[i]:
                split_elements = row[i].split('\n')
                if split_elements[-1] == '':
                    split_elements = split_elements[:-1]  # 去掉末尾的空元素
                original_data[original_data.index(row)][i] = split_elements

    response_data = {'schedule': original_data}
    # 将字典转换成 JSON 格式的字符串
    response_json = json.dumps(response_data, ensure_ascii=True)
    # 设置响应头，指定返回内容为JSON格式
    print('Content-type: application/json; charset=utf-8\n')
    # 输出 JSON 格式的字符串
    print(response_json)

except Exception as e:
    print("Content-type: text/json\n")
    print(e)

finally:
    cursor.close()
    connection.close()
