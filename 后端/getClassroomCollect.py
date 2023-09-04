#!
# -*- coding: utf-8 -*-

import cgi
import pymysql
import datetime
import json
import re

# 数据库连接信息字典
def config(database):
    db_config = {
        "host": "localhost",
        "port": 3306,
        "user": "你的用户名",
        "password": "你的密码",
        "database": database,
        "charset": "utf8"
    }
    return db_config

# 数据库连接
def connect_and_query(query, values, database):
    db_config = config(database)

    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            # 执行查询语句
            cursor.execute(query, values)
            result = cursor.fetchall()

            # 提取查询结果中的实际数据部分
            data_list = [list(result) for result in result]
            data_list = data_list[0]

            return data_list

    except Exception as e:
        print("Content-type: text/json\n")
        print(e)

    finally:
        # 关闭数据库连接
        connection.close()


# 获取今天的日期
today = datetime.datetime.today()

# 获取今天是星期几（0表示星期一，6表示星期日）
day_of_week = today.weekday()

# 提取年、月、日
year = today.year
month = today.month
day = today.day

# 拼接为年.月.日的字符串
year_month_day = f"{year}.{month}.{day}"    # 表名

# 获取传递的参数
form = cgi.FieldStorage()
buildingName = json.loads(form.getvalue('buildingName'))
classroomNumber = json.loads(form.getvalue('classroomNumber'))

# 查找数据
classroomState = [None, None, None]    # 结果
for i in range(3):
    if (buildingName[i] is not None):
        q = f"SELECT * FROM `{year_month_day}` WHERE classroom = %s"
        classroomState[i] = connect_and_query(q, (classroomNumber[i],), buildingName[i])
    else:
        classroomState[i] = None

# 构建结果字典
result_dict = {'classroomState': classroomState, 'today_name': day_of_week}

# 将结果字典转换为 JSON 格式的字符串
result_json = json.dumps(result_dict, ensure_ascii=True)
# 返回结果
print("Content-type: application/json; charset=utf-8\n")
print(result_json)
