#!
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()

from getClassroomStateAPI import MysqlConect

# 创建一个 FieldStorage 实例以获取 GET 参数
form = cgi.FieldStorage()

# 获取参数值
building = form.getvalue("building")
data = form.getvalue("data")

# 创建 MysqlConect 实例
mysql_connector = MysqlConect()

# 连接数据库并获取数据
state = mysql_connector.connect(building, data)

# 设置 CGI 头部
print("Content-Type: application/json\n")  # 返回 JSON 格式数据

# 输出数据
print(state)
