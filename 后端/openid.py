#!
# -*- coding: utf-8 -*-

import cgi
import requests
import json
import pymysql
import os
from normalizeOpenidAPI import remove_special_characters

# ���ݿ����Ӳ���
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "����û���",
    "password": "�������",
    "database": "user",
    "charset": "utf8"
}


# �ж�openid�Ƿ���users����
def is_openid_exists(openid, cursor):
    query = "SELECT COUNT(*) FROM users WHERE openid = %s"
    cursor.execute(query, (openid,))
    result = cursor.fetchone()
    return result[0] > 0

# ���ô洢���̴����û���¼
def create_user_record(openid, table, cursor):
    cursor.callproc("create_user", (openid, table))
    # �ύ����
    cursor.execute("COMMIT")

# ��ȡopenid����ʽ���α�������
def get_openid(js_code):
    # ΢�ſ���ƽ̨�ṩ��APPID��APPSECRET
    appid = '���APPID'
    appsecret = '���APPSECRET'

    # ʹ��code��ȡopenid������URL
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

# ����openid����username
def find_username_by_openid(openid):
    out = []
    try:
        # �������ݿ�
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # ִ�в�ѯ
        query = "SELECT username, bool_schedule, star_classroom_1, star_classroom_2, star_classroom_3, bool_classroom, time_ocr FROM users WHERE openid = %s"
        cursor.execute(query, (openid,))
        result = cursor.fetchone()

        if result:
            out.append(result[0])  # ����username
            out.append(result[1])  # ����bool_schedule
            out.append(result[2])  # ����star_classroom1
            out.append(result[3])  # ����star_classroom2
            out.append(result[4])  # ����star_classroom3
            out.append(result[5])  # ����bool_classroom
            out.append(result[6])  # ����time_ocr
            return out

        else:
            return None  # û��ƥ�����

    except pymysql.Error as err:
        print('Content-type: application/json\n')
        print('{"error": "error1"}')
        return None

    finally:
        if connection:
            cursor.close()
            connection.close()

# ʹ������
def call_register_day(openid):
    try:
        # �������ݿ�
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # ���ô洢���̲���ȡ���
        cursor.callproc("register_day", (openid,))
        output_result = cursor.fetchone()  # ��ȡ�洢���̵����

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

# ����openid�ļ���
def create_folder(folder_name):
    try:
        # ��ȡ��ǰ�ű��ľ���·��
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # �������ļ��е�����·��
        new_folder_path = os.path.join(script_directory, "image", folder_name)

        os.makedirs(new_folder_path)
        return 1
    except OSError as error:
        return 2

# ��ѯ1.png�Ƿ����
def photo_exist(table):
    # �����������ļ�·��
    folder_path = 'C:\\inetpub\\wx\\image\\' + table
    file_path = os.path.join(folder_path, '1.png')

    # �ж��ļ��Ƿ����
    if os.path.exists(file_path):
        return 1
    else:
        return 0


# ����һ�� CGIFieldStorage ��������ȡ���Ӵ��ݵĲ���
form = cgi.FieldStorage()

# ��ȡ���Ӵ��ݵĲ��� js_code
js_code = form.getvalue('js_code', None)
folder = 0

if js_code:
    openid, session_key = get_openid(js_code)

    if openid:
        table = remove_special_characters(openid)  # openid�淶��������

        # ����openid�û����������α��
        try:
            # �������ݿ�
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            # ���û�������
            if not is_openid_exists(openid, cursor):
                create_user_record(openid, table, cursor)  # �����û���¼
                folder = create_folder(table)  # �����û��ļ���

        except pymysql.Error as err:
            print('Content-type: application/json\n')
            print('{"error": "error2"}')

        finally:
            if connection:
                cursor.close()
                connection.close()

        # ��ȡ�û���Ϣ
        out = find_username_by_openid(openid)
        day = call_register_day(openid)

        username = out[0]
        bool_schedule = out[1]
        star_classroom_1 = out[2]
        star_classroom_2 = out[3]
        star_classroom_3 = out[4]
        bool_classroom = out[5]
        time_ocr = out[6]

        # �ж��û�ͷ���Ƿ����
        photo = photo_exist(table)

        # �����������װ��һ���ֵ�
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
        # ���ֵ�ת���� JSON ��ʽ���ַ���
        response_json = json.dumps(response_data, ensure_ascii=True)

        # ������Ӧͷ��ָ����������ΪJSON��ʽ
        print('Content-type: application/json; charset=utf-8\n')
        # ��� JSON ��ʽ���ַ���
        print(response_json)
    else:
        print('Content-type: application/json\n')
        print('{"error": "get_openid_false_down"}')
else:
    print('Content-type: application/json\n')
    print('{"error": "no_js_code"}')
