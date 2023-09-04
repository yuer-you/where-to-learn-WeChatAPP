#!
# -*- coding: utf-8 -*-

import cgi
import requests
import json
import pymysql
import os
from normalizeOpenidAPI import remove_special_characters

# 数据库连接参数
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "你的用户名",
    "password": "你的密码",
    "database": "user",
    "charset": "utf8"
}


# 判断openid是否在users表中
def is_openid_exists(openid, cursor):
    query = "SELECT COUNT(*) FROM users WHERE openid = %s"
    cursor.execute(query, (openid,))
    result = cursor.fetchone()
    return result[0] > 0

# 调用存储过程创建用户记录
def create_user_record(openid, table, cursor):
    cursor.callproc("create_user", (openid, table))
    # 提交事务
    cursor.execute("COMMIT")

# 获取openid并格式化课表表的命名
def get_openid(js_code):
    # 微信开放平台提供的APPID和APPSECRET
    appid = '你的APPID'
    appsecret = '你的APPSECRET'

    # 使用code换取openid的请求URL
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={appsecret}&js_code={js_code}&grant_type=authorization_code'

    try:
        response = requests.get(url)
        data = response.json()
        # print('Content-type: application/json\n')
        # print(data)
        openid = data.get('openid', None)
        session_key = data.get('session_key', None)
        return openid, session_key
    except requests.exceptions.RequestException as e:
        print('Content-type: application/json\n')
        print('{"error": "get_openid_false_function"}')
        return None, None

# 根据openid查找username
def find_username_by_openid(openid):
    out = []
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # 执行查询
        query = "SELECT username, bool_schedule, star_classroom_1, star_classroom_2, star_classroom_3, bool_classroom, time_ocr FROM users WHERE openid = %s"
        cursor.execute(query, (openid,))
        result = cursor.fetchone()

        if result:
            out.append(result[0])  # 返回username
            out.append(result[1])  # 返回bool_schedule
            out.append(result[2])  # 返回star_classroom1
            out.append(result[3])  # 返回star_classroom2
            out.append(result[4])  # 返回star_classroom3
            out.append(result[5])  # 返回bool_classroom
            out.append(result[6])  # 返回time_ocr
            return out

        else:
            return None  # 没有匹配的行

    except pymysql.Error as err:
        print('Content-type: application/json\n')
        print('{"error": "error1"}')
        return None

    finally:
        if connection:
            cursor.close()
            connection.close()

# 使用天数
def call_register_day(openid):
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # 调用存储过程并获取输出
        cursor.callproc("register_day", (openid,))
        output_result = cursor.fetchone()  # 获取存储过程的输出

        if output_result:
            result = output_result[0]
            return result
        else:
            return None

    except pymysql.Error as err:
        return f'Error: {err}'

    finally:
        if connection:
            cursor.close()
            connection.close()

# 创建openid文件夹
def create_folder(folder_name):
    try:
        # 获取当前脚本的绝对路径
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # 构建新文件夹的完整路径
        new_folder_path = os.path.join(script_directory, "image", folder_name)

        os.makedirs(new_folder_path)
        return 1
    except OSError as error:
        return 2

# 查询1.png是否存在
def photo_exist(table):
    # 构建完整的文件路径
    folder_path = 'C:\\inetpub\\wx\\image\\' + table
    file_path = os.path.join(folder_path, '1.png')

    # 判断文件是否存在
    if os.path.exists(file_path):
        return 1
    else:
        return 0


# 创建一个 CGIFieldStorage 对象来获取链接传递的参数
form = cgi.FieldStorage()

# 获取链接传递的参数 js_code
js_code = form.getvalue('js_code', None)
folder = 0

if js_code:
    openid, session_key = get_openid(js_code)

    if openid:
        table = remove_special_characters(openid)  # openid规范化命名库

        # 创建openid用户，并创建课表表
        try:
            # 连接数据库
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            # 若用户不存在
            if not is_openid_exists(openid, cursor):
                create_user_record(openid, table, cursor)  # 创建用户记录
                folder = create_folder(table)  # 创建用户文件夹

        except pymysql.Error as err:
            print('Content-type: application/json\n')
            print('{"error": "error2"}')

        finally:
            if connection:
                cursor.close()
                connection.close()

        # 获取用户信息
        out = find_username_by_openid(openid)
        day = call_register_day(openid)

        username = out[0]
        bool_schedule = out[1]
        star_classroom_1 = out[2]
        star_classroom_2 = out[3]
        star_classroom_3 = out[4]
        bool_classroom = out[5]
        time_ocr = out[6]

        # 判断用户头像是否存在
        photo = photo_exist(table)

        # 将多个变量组装成一个字典
        response_data = {
            'openid': openid,
            'table': table,
            'day': day,
            'username': username,
            'bool_schedule': bool_schedule,
            'star_classroom_1': star_classroom_1,
            'star_classroom_2': star_classroom_2,
            'star_classroom_3': star_classroom_3,
            'bool_classroom': bool_classroom,
            'time_ocr': time_ocr,
            'folder': folder,
            'photo': photo
        }
        # 将字典转换成 JSON 格式的字符串
        response_json = json.dumps(response_data, ensure_ascii=True)

        # 设置响应头，指定返回内容为JSON格式
        print('Content-type: application/json; charset=utf-8\n')
        # 输出 JSON 格式的字符串
        print(response_json)
    else:
        print('Content-type: application/json\n')
        print('{"error": "get_openid_false_down"}')
else:
    print('Content-type: application/json\n')
    print('{"error": "no_js_code"}')
