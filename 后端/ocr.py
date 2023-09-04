#!
# -*- coding: GBK -*-

import cgi
import csv
import numpy as np
import re
from paddleocr import PaddleOCR as Po
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pymysql
from imageCutAPI import cut

time2 = 0
time1 = 0
VAR = 5  # �����ж�ʱ���������


def ocr_PaddleOCR(img):
    # time1 = time.time()
    ocr = Po(use_angle_cls=True, use_gpu=False, lang="ch", show_log=False)
    result = ocr.ocr(img)
    # time2 = time.time()
    # print(time2 - time1)
    # print(result)
    return result


def sort_list(address, i):  # ������ i=0ʱ���պ������С��������
    return sorted(address, key=(lambda address: address[0][i]))


def judge_col(input):  # Ѱ���еĶ�Ӧ�����������ڣ�
    input2 = np.array(input)
    input2 = input2[:, 0].tolist()
    input2 = np.array(input2)
    input2 = input2[:, 0].tolist()
    for i in range(len(input2)):
        if (np.var(input2[0 + i:14 + i]) < VAR):
            input = edulcoration(input, i, 14)
            break
    input2 = np.array(input)
    input2 = input2[:, 0].tolist()
    input2 = np.array(input2)
    input2 = input2[:, 1].tolist()
    return input2


def judge_row(input):  # Ѱ���еĶ�Ӧ���������ڼ��ڿΣ�
    input2 = np.array(input)
    input2 = input2[:, 0].tolist()
    input2 = np.array(input2)
    input2 = input2[:, 1].tolist()
    for i in range(len(input2)):
        if (np.var(input2[0 + i:7 + i]) < VAR):
            input = edulcoration(input, i, 7)
            break
    input2 = np.array(input)
    input2 = input2[:, 0].tolist()
    input2 = np.array(input2)
    input2 = input2[:, 0].tolist()
    return input2


def edulcoration(input, start, num):
    input2 = input[start:num + start]
    input2 = np.array(input2)
    input2 = input2[:, 1].tolist()
    if (num == 14):
        pa = re.compile(r'[��һ?��]')
    else:
        pa = re.compile(r'[����һ?]')
    j = start
    input_j = []
    for i in input2:
        if (pa.match(i)):
            input_j.append(input[j])
        j = j + 1
    if (num == 14):
        return sort_list(input_j, 1)
    else:
        return sort_list(input_j, 0)


def coordinate(row, col):  # ������������װ�ɶ�ά����
    result = []
    for i in row:
        for j in col:
            result.append([i, j])
    return result


def find_nearest(array, value):
    if (value >= array[len(array) - 1]):
        return len(array) - 1
    idx = np.searchsorted(array, value, side="left")
    if abs(value - array[idx]) == 0:
        return idx
    else:
        return idx - 1


def find_index(address):  # �ҵ�ÿ�����ݵĶ�Ӧ��άλ��
    for i in address:
        find_row = find_nearest(row, i[0][0])
        find_col = find_nearest(col, i[0][1])
        i.append([find_row, find_col])
    return address


def sure_index(address):  # ���ݶ�ά���꽫������װ��ÿ����Ԫ��
    result_last = [[] for _ in range(49)]
    for i in address:
        if (i[2][0] >= 0 and i[2][1] >= 0 and i[2][0] <= 7 and i[2][1] <= 7):
            row_last = int(i[2][1])
            col_last = int(i[2][0])

            index = row_last * 7 + col_last
            if (not (i[1][0] >= 'A' and i[1][0] <= 'Z')):
                result_last[index].append(i[1] + '\n')

    return result_last


def mkdir_csv(path, content):  # д��csv
    if (os.path.isfile(path)):
        with open(path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(content)
    else:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "openid", "class", "monday", "tuesday", "wednesday",
                "thursday", "friday", "saturday", "sunday"
            ])
            writer.writerow(content)


def process(input, id, path):  # д���һ��
    j = 1
    for i in range(7):
        result = []
        result.append(id)
        if (j == 1):
            result.append("first_class")
        if (j == 2):
            result.append("second_class")
        if (j == 3):
            result.append("third_class")
        if (j == 4):
            result.append("fourth_class")
        if (j == 5):
            result.append("fifth_class")
        if (j == 6):
            result.append("sixth_class")
        if (j == 7):
            result.append("seventh_class")
        newline = input[i * 7:(i + 1) * 7]
        for m in newline:
            if (len(m) == 0):
                result.append('')
            else:
                class_r = ""
                for n in m:
                    class_r = class_r + n
                result.append(class_r)

        mkdir_csv(path, result)
        j = j + 1


def select(input):  # �����ݸ�д��Ԥ�ڸ�ʽ
    for i in input:
        if (not len(i) == 0):

            if ('\u4e00' <= i[2][-2] <= '\u9fff'):

                if (i[2][-2] == "ͨ" or i[2][-2] == "֪"):
                    if (len(i) == 4):
                        i[2] = "��"
                        i[3] = "��"
                    else:
                        i[2] = "����"
            elif ('\u4e00' <= i[2][-6] <= '\u9fff'):
                i[2] = i[2][-5:-1]
            else:
                i[2] = i[2][-6:-1]
            if (not i[0].rfind("��") == -1):
                i[0] = (i[0][:i[0].rfind("��") - 1] + "\n")
                # print(i[0])
            if (not i[1].find("��") == -1):
                i.insert(2, i[1][i[1].find("��") + 1:])
                i[1] = (i[1][:i[1].find("��") + 1] + "\n")
                # print(i)
    return input


def check(path):  # ����Ƿ���schedule.csv������ɾȥ
    if os.path.exists(path):
        os.remove(path)


def to_csv(path, openid):  # д�����ݿ�
    sqlname = 'user'
    engine = create_engine(
        'mysql+pymysql://����û���:�������@localhost:3306/' + sqlname)
    connection = engine.connect()
    transaction = connection.begin()

    try:
        # ��ȡ����CSV�ļ�
        df = pd.read_csv(path, sep=',')

        # ���½���DataFrame����ΪMySQL�е����ݱ�������index��
        df.to_sql(name=openid, if_exists='replace', con=engine, index=False)
        transaction.commit()

    except Exception as e:
        transaction.rollback()

    finally:
        connection.close()


form = cgi.FieldStorage()
table = form.getvalue('table')
print("Content-type: application/json; charset=utf-8\n")  # CGI��Ӧͷ��

image_path = cut(table)   # ����ͼ�񲢻�ȡͼƬ·��

if (image_path == 0):
    print('{"error": False}')
else:
    try:
    
        lower_table = table.lower()
    

        folder_path = os.path.join(".", "image", table)
        csv_path = os.path.join(folder_path, "schedule.csv")

        check(csv_path)  #   ��csv�ļ����ڣ�ɾ��


        result_first = ocr_PaddleOCR(image_path)  # ͼƬ�ļ�λ��

        address = []
        for i in result_first[0]:
            address.append([i[0][0], i[1][0]])

        address_col = sort_list(address, 0)
        col = judge_col(address_col)
        col = [i - 5 for i in col]

        address_row = sort_list(address, 1)
        row = judge_row(address_row)
        row = [i - 5 for i in row]

        coordinate(row, col)

        address = find_index(address)
        result_last = sure_index(address)
        process(select(result_last), lower_table, csv_path)
        to_csv(csv_path, lower_table)  # lower_table Сдtable
    

    except Exception as err:
        print('{"error": error}')
        print(f"An error occurred: {err}")

    else:
        print('{"success": true}')

        # with open('output.txt', 'w') as f:
        #     w = csv.writer(f)
        #     for i in address:
        #         w.writerow(i)
