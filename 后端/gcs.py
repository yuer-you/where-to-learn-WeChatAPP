#!
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()

from getClassroomStateAPI import MysqlConect

# ����һ�� FieldStorage ʵ���Ի�ȡ GET ����
form = cgi.FieldStorage()

# ��ȡ����ֵ
building = form.getvalue("building")
data = form.getvalue("data")

# ���� MysqlConect ʵ��
mysql_connector = MysqlConect()

# �������ݿⲢ��ȡ����
state = mysql_connector.connect(building, data)

# ���� CGI ͷ��
print("Content-Type: application/json\n")  # ���� JSON ��ʽ����

# �������
print(state)
