﻿import requests
from bs4 import BeautifulSoup
import datetime


def jwxt1():
    headers = {
        "Content-Type":
        "application/x-www-form-urlencoded",
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }

    with open('cookie.txt', 'r', encoding='utf-8') as f:  # 设置文件对象
        headers["cookie"] = f.readline()
    f.close()  # 关闭文件

    url = "https://aa.bjtu.edu.cn/classroom/timeholdresult/room_view/?zc=15&page=1"
    _session = requests.session()

    totaldata = []
    now = ""
    num = 0

    for zhou in range(1, 20):
        day = []
        for page in range(1, 16):
            url = "https://aa.bjtu.edu.cn/classroom/timeholdresult/room_view/?zc=%d&page=%d" % (
                zhou, page)
            responce_tesys = _session.get(url,
                                          headers=headers,
                                          allow_redirects=True)
            soup_data = BeautifulSoup(responce_tesys.text, "html.parser")
            jiaoshi = soup_data.find_all("td")
            riqi = soup_data.find_all("span",
                                      attrs={"style": "font-weight: normal"})
            ke = soup_data.find_all("td")

            print(url)
            for x in riqi:
                day.append(str(x.string).lstrip())

                print(x.string)
            for x in jiaoshi:
                if (str(x).find("span") != -1):
                    print(str(x.text).split(" ")[0])

            for x in ke:
                if (str(x).find("span") != -1):
                    now = str(x.text).split(" ")[0]
                    totaldata.append(now)
                    num = num + 1
                elif (str(x).find("background-color") != -1):
                    if (str(x).find("#fff") != -1):
                        ls = int(str(x).partition("星期")[2][0]) - 1
                        totaldata[num -
                                  1] = totaldata[num -
                                                 1] + "@" + day[ls] + "&0"
                    else:
                        ls = int(str(x).partition("星期")[2][0]) - 1
                        totaldata[num -
                                  1] = totaldata[num -
                                                 1] + "@" + day[ls] + "&1"

                # print(x)

    fenlei = {
        "十七教（建艺）": "202@203@204@205@206@207@208@209@211",

        "思源楼":
        "SY101@SY102@SY103@SY104@SY105@SY106@SY107@SY108@SY109@SY201@SY202@SY203@SY204@SY205@SY206@SY207@SY208@SY209@SY210@SY301@SY302@SY303@SY305@SY306@SY307@SY308@SY309@SY401@SY402@SY403@SY405@SY406@SY407@SY408@SY410@SY411@SY412",

        "思源西楼":
        "SX101@SX105@SX106@SX107@SX201@SX202@SX203@SX204@SX205@SX302@SX303@SX304@SX305@SX401@SX402@SX403@SX404@SX405@SX406@SX407@SX501@SX502@SX503@SX504@SX505@SX506@SX507",

        "思源东楼":
        "SD102@SD103@SD104@SD106@SD107@SD108@SD201@SD202@SD203@SD205@SD206@SD207",

        "九教": "东102@东201@东203@中102@中心报告厅@九教南212@九教南216",

        "八教":
        "8103@8104@8105@8108@8109@8201@8202@8203@8204@8205@8207@8208@八教三层实验室",

        "逸夫楼":
        "YF101机房@YF104@YF106@YF108@YF204@YF205@YF207@YF208@YF209@YF301@YF302@YF303@YF304@YF305@YF307@YF308@YF309@YF310@YF312@YF313@YF401@YF403@YF404@YF406@YF408@YF409@YF410@YF411@YF413@YF414@YF415@YF501@YF503@YF504@YF505@YF507@YF508@YF509@YF510@YF512@YF513@YF514@YF601@YF603@YF604@YF606@YF608@YF609@YF610@YF611@YF613@YF614@YF615@YF东701@YF东702@YF东703@YF东705@YF东706@YF东707@YF东708@YF西7层实验室",

        "机械楼":
        "Z101@Z104@Z105@Z106@Z107@Z108@Z109@Z201@Z204@Z207@Z305@Z306@Z307@Z308@Z309@Z310@Z606",

        "东区一教":
        "DQ102@DQ103@DQ104@DQ105@DQ106@DQ107@DQ108@DQ110@DQ201@DQ202@DQ203@DQ204@DQ205@DQ206@DQ208@DQ209@DQ210@DQ212@DQ213@DQ214@DQ215@DQ216@DQ302@DQ303@DQ304@DQ305@DQ306@DQ308@DQ309@DQ310@DQ311@DQ312@DQ313@DQ314@DQ401@DQ402@DQ403@DQ404@DQ405@DQ406@DQ408@DQ409@DQ410@DQ412@DQ413@DQ414@DQ415@DQ505@DQ510",
    }

    with open('data.txt', 'w+', encoding='utf-8') as f:
        buildname = fenlei.keys()
        buildhave = fenlei.values()
        for x in totaldata:
            for y in range(0, len(buildhave)):
                z = list(buildhave)[y]
                if (str(z).find(str(x).split("@")[0]) != -1):
                    m = str(x).split("@")
                    for n in range(1, len(m), 7):
                        ls = list(buildname)[y] + "&" + str(x).split("@")[0] + "&"

                        if (int(m[n].split("&")[0].split("月")[0]) == 1):
                            ls = ls + str(int(datetime.datetime.now().strftime('%Y')) + 1) + "." + str(
                                int(m[n].split("&")[0].split("月")[0])) + "." + str(
                                    int(m[n].split("&")[0].split("月")[1].split("日")[0]))
                        else:
                            ls = ls + datetime.datetime.now().strftime('%Y') + "." + str(
                                int(m[n].split("&")[0].split("月")[0])) + "." + str(
                                    int(m[n].split("&")[0].split("月")[1].split("日")[0]))

                        for ls2 in range(0, 7):
                            ls = ls + "&" + m[n + ls2].split("&")[1]
                        ls = ls + "\n"
                        f.write(ls)
                    break

                elif (str(z).find(str(x).split("@")[0]) == -1
                      and y == len(buildhave)):
                    f.write("CAN\'T_FIND")
                    print("CAN\'T_FIND")

    f.close()  # 关闭文件
