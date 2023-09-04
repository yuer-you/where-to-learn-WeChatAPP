#!
# -*- coding: utf-8 -*-

import cgi
import pymysql
import datetime
import json

# 获取今天的日期
today = datetime.datetime.today()

# 获取今天是星期几（0表示星期一，6表示星期日）
day_of_week = today.weekday()

# 获取传递的参数
form = cgi.FieldStorage()
table = form.getvalue('table')
table = table.lower()

# 数据库连接信息字典
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "你的用户名",
    "password": "你的密码",
    "database": "user",
    "charset": "utf8"
}

# 创建数据库连接
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # 调用存储过程
        cursor.callproc('schedule_search', (table,))

        # 获取所有结果行
        result = cursor.fetchall()

        # 构建结果列表
        result_list = []

        if result:
            for row in result:
                row_values = list(row)  # 将元组转换为列表
                result_list.append(row_values)

            for row in result_list:
                for i in range(len(row)):
                    if row[i] and '\n' in row[i]:
                        split_elements = row[i].split('\n')
                        if split_elements[-1] == '':
                            split_elements = split_elements[:-1]  # 去掉末尾的空元素
                        result_list[result_list.index(row)][i] = split_elements

        # 处理输出
        processed_output = []
        for item in result_list:
            if item[0] is not None:
                processed_output.append(item[0])
            else:
                processed_output.append(None)

        # 构建结果字典
        result_dict = {'today_name': day_of_week,'today_schedule': processed_output}

        # 将结果字典转换为 JSON 格式的字符串
        result_json = json.dumps(result_dict, ensure_ascii=True)
        # 返回结果
        print("Content-type: application/json; charset=utf-8\n")
        print(result_json)

finally:
    connection.close()
