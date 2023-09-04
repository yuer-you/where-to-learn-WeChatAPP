#!
# -*- coding: UTF-8 -*-

import pymysql
import cgi
import cgitb
import json
cgitb.enable()  # 显示错误信息

# 数据库连接信息
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "你的用户名",
    "password": "你的密码",
    "database": "user",
    "charset": "utf8"
}

# 连接数据库
db = pymysql.connect(**db_config)
cursor = db.cursor()

# 查询并排序collect列
query = "SELECT * FROM classroom_collect ORDER BY collect DESC LIMIT 10"
cursor.execute(query)
results = cursor.fetchall()

# 提取结果并保存到数组
collect_values = [result for result in results]

# 关闭数据库连接
cursor.close()
db.close()

result_dict = {'classroomRanking': collect_values}
result_json = json.dumps(result_dict, ensure_ascii=True)

# 输出Content-Type头和JSON格式的数据
print("Content-Type: application/json; charset=utf-8\n")
print(result_json)
