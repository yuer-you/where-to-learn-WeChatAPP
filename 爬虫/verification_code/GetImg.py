import requests
from bs4 import BeautifulSoup
import os
import shutil


# 获取验证码图片的url
def GetUrl():
    req = requests.get(url="https://cas.bjtu.edu.cn/auth/login/?next=/o/authorize/%3Fresponse_type%3Dcode%26client_id%3DaGex8GLTLueDZ0nW2tD3DwXnSA3F9xeFimirvhfo%26state%3D1683170670%26redirect_uri%3Dhttps%3A//mis.bjtu.edu.cn/auth/callback/%3Fredirect_to%3D/home/")
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, features="html5lib")
    url_str = str(soup.find_all("img", class_="captcha"))
    url = ''
    a = b = 0
    for i in url_str:
        if (i == '/' and a == 0):
            url = url + i
            a += 1
            b = 1
        elif (b == 1):
            if (i == '"'):
                url = url[:-1]
                # print(url)
                break
            url = url + i
    return url


# 下载验证码图片
def Download(url, path):
    url = 'https://cas.bjtu.edu.cn' + url
    print(url)
    r = requests.get(url)
    with open(path + '/vcCode.png', 'wb') as f:
        f.write(r.content)
        f.close()


# 整合前两个函数
def getImg(path):
    url = GetUrl()
    Download(url, path)


# 创建文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            # makedirs 创建文件时如果路径不存在会创建这个路径
        return path


# 删除文件夹
def deldir(path):
    shutil.rmtree(path)   # 删除文件
