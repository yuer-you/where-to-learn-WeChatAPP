#!
# -*- coding: utf-8 -*-
import cgi
import os
import uuid
import json
import time
from normalizeOpenidAPI import remove_special_characters

# 将其修改为你的路径
UPLOAD_DIR = 'C:\inetpub\wx\image'
RESULT_FILE = 'C:\inetpub\wx\image\log.txt'
TIME = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def save_uploaded_file(fileitem, path, photoname):
    if not fileitem.filename:
        return None

    # 生成一个唯一的文件名以避免冲突
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
    # 创建一个FieldStorage实例来解析multipart/form-data请求
    form = cgi.FieldStorage()

    # 设置Content-Type头，指示响应的格式为JSON
    print("Content-Type: application/json")
    print()

    try:
        openid = form.getvalue('openid', None)
        photoname = form.getvalue('photoname', None)
        table = remove_special_characters(openid)  # openid规范化命名库
        TABLE_UPLOAD_DIR = os.path.join(UPLOAD_DIR, table)

        # 检查表单数据中是否有名为'image'的字段
        if 'image' not in form:
            response = {"false": False, "error": "did not receive data"}
            save_result_to_file('-1', 'none name', False, openid)  # 将结果保存到文本文件中
            print(json.dumps(response))  # 使用json.dumps确保正确编码JSON
            return

        # 获取上传的文件项
        fileitem = form['image']

        # 将上传的文件保存到服务器
        filename = save_uploaded_file(fileitem, TABLE_UPLOAD_DIR, photoname)

        if filename is not None:
            # 处理成功
            response = {"success": True, "filename": filename}
            save_result_to_file('1', filename, True, openid)  # 将结果保存到文本文件中
            print(json.dumps(response))  # 使用json.dumps确保正确编码JSON

        else:
            response = {"false": False, "error": "save file false"}
            save_result_to_file('2', 'none name', False, openid)  # 将结果保存到文本文件中
            print(json.dumps(response))  # 使用json.dumps确保正确编码JSON
    except Exception as e:
        response = {"false": False, "error": "there is a false" + str(e)}
        save_result_to_file('3', 'none name', False, openid)  # 将结果保存到文本文件中
        print(json.dumps(response))  # 使用json.dumps确保正确编码JSON

if __name__ == "__main__":
    main()
