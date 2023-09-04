#!
# -*- coding: utf-8 -*-
import cgi
import os
import uuid
import json
import time
from normalizeOpenidAPI import remove_special_characters

# �����޸�Ϊ���·��
UPLOAD_DIR = 'C:\inetpub\wx\image'
RESULT_FILE = 'C:\inetpub\wx\image\log.txt'
TIME = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def save_uploaded_file(fileitem, path, photoname):
    if not fileitem.filename:
        return None

    # ����һ��Ψһ���ļ����Ա����ͻ
    filename = photoname + '.png'
    filepath = os.path.join(path, filename)

    try:
        with open(filepath, 'wb') as f:
            f.write(fileitem.file.read())
    except IOError:
        return None

    return filename

def save_result_to_file(where, filename, success, openid):
    with open(RESULT_FILE, 'a') as f:
        f.write(TIME + ' || ' + openid + ' || ' + where + ' || ' + filename + ' || ' + str(success) + '\n')

def main():
    # ����һ��FieldStorageʵ��������multipart/form-data����
    form = cgi.FieldStorage()

    # ����Content-Typeͷ��ָʾ��Ӧ�ĸ�ʽΪJSON
    print("Content-Type: application/json")
    print()

    try:
        openid = form.getvalue('openid', None)
        photoname = form.getvalue('photoname', None)
        table = remove_special_characters(openid)  # openid�淶��������
        TABLE_UPLOAD_DIR = os.path.join(UPLOAD_DIR, table)

        # �����������Ƿ�����Ϊ'image'���ֶ�
        if 'image' not in form:
            response = {"false": False, "error": "did not receive data"}
            save_result_to_file('-1', 'none name', False, openid)  # ��������浽�ı��ļ���
            print(json.dumps(response))  # ʹ��json.dumpsȷ����ȷ����JSON
            return

        # ��ȡ�ϴ����ļ���
        fileitem = form['image']

        # ���ϴ����ļ����浽������
        filename = save_uploaded_file(fileitem, TABLE_UPLOAD_DIR, photoname)

        if filename is not None:
            # ����ɹ�
            response = {"success": True, "filename": filename}
            save_result_to_file('1', filename, True, openid)  # ��������浽�ı��ļ���
            print(json.dumps(response))  # ʹ��json.dumpsȷ����ȷ����JSON

        else:
            response = {"false": False, "error": "save file false"}
            save_result_to_file('2', 'none name', False, openid)  # ��������浽�ı��ļ���
            print(json.dumps(response))  # ʹ��json.dumpsȷ����ȷ����JSON
    except Exception as e:
        response = {"false": False, "error": "there is a false" + str(e)}
        save_result_to_file('3', 'none name', False, openid)  # ��������浽�ı��ļ���
        print(json.dumps(response))  # ʹ��json.dumpsȷ����ȷ����JSON

if __name__ == "__main__":
    main()
