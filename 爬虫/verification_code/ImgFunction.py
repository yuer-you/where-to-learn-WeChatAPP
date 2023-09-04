import os
import cv2 as cv
import numpy as np


# 读取文件名(for循环是用来处理训练图片用的，但是仍然保留，因为不影响使用效果)
# directory_name：文件夹名
def read_directory(directory_name):
    array_img = []
    array_name = []
    for filename in os.listdir(r"./" + directory_name):
        img = cv.imread(directory_name + "/" + filename)
        array_img.append(img)
        array_name.append(filename)
    # print(filename)
    return array_img, array_name


# 图像二值化&降噪
# img：cv.imread读取后的矩阵
def ImgProcess(img):
    # 对图片进行预处理，去除噪点
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    a, gray = cv.threshold(gray, 135, 255, cv.THRESH_BINARY)
    # 降噪
    gray = cv.morphologyEx(gray, cv.MORPH_CLOSE, np.ones(shape=(2, 2)))
    return gray


# 取列表的列表的第一个元素排列
def takeFirst(elem):
    return elem[0]


# 图像切割
# img：cv.imread读取后的矩阵
# num：用户自定义图像切割后每个小图片的编号（只能定义第一个，后面的累加）
# address：切割后存放的位置
# name：原图像的名称
def CutImg(img, num, address, name):
    contours, hierarchy = cv.findContours(img, 1, 2)
    flag = num
    coord = []
    # 记录每个有效矩形的坐标左上角坐标(x, y), 宽和高(w, h)
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        if x != 0 and y != 0 and w * h >= 30:
            coord.append([x, y, w, h])
    # 按x大小进行排序
    coord.sort(key=takeFirst)
    # 若倒数第二个y > 倒数第一个y, 则调换两个数组的位置(防止等号的第二条线变成第一条线)
    if (coord[-2][1] > coord[-1][1]):
        a = []
        a = coord[-2]
        coord[-2] = coord[-1]
        coord[-1] = a
    x_old = 0
    y_old = 0
    w_old = 0
    h_old = 0
    # 进行裁剪
    for i in coord:
        # print('矩形坐标：', i)
        x = i[0]
        y = i[1]
        w = i[2]
        h = i[3]
        # 如果两矩形x值的差的绝对值小于等于2，则将两矩形合并输出，并删除上一张输出的图片(实际上就是将等号的两条横线合并输出)
        if (abs(x - x_old) <= 2):
            os.remove(address + '/%s_%s.png' % (name, flag - 1))
            # print('删除的裁剪矩形：', address + '%s_%s.png' % (name, flag - 1))
            # 从第一条线的y, 到第一条线的y + 第二条线的h + 第一条线的高; 从两条线最小的x, 到两条线最大的x + 两条线最大的w
            cv.imwrite(address + '/%s_%s.png' % (name, flag), img[y_old:y_old + h + h_old, min(x, x_old):max(x, x_old) + max(w, w_old)])
        else:
            cv.imwrite(address + '/%s_%s.png' % (name, flag), img[y:y + h, x:x + w])
        # print('裁剪后的矩形：' + '%s_%s.png' % (name, flag))
        # print('\n')
        flag += 1
        x_old = x
        y_old = y
        w_old = w
        h_old = h


# # 取列表的列表的第二个元素排列
# def takeSecond(elem):
#     return elem[1]


# 将全部裁剪图片处理为相等的尺寸
# InPath：裁剪图像的储存路径
# OutPath：处理后图像储存路径
def EnlargeImg(InPath, OutPath):
    Img, Name = read_directory(InPath)
    h = 0
    w = 0
    hw = []
    for i in Img:
        h, w = i.shape[:2]
        hw.append([h, w])
    # 获取全部图片中的最大h和w
    # hMax = max(hw, key=takeFirst)[0]
    # wMax = max(hw, key=takeSecond)[1]
    hMax = 32
    wMax = 32
    j = 0
    for i in list(zip(Img, Name)):
        h = hw[j][0]
        w = hw[j][1]
        # 判断h和w是否能被2整除，不能就-1，凑为2的倍数
        if (h % 2 == 0 and w % 2 == 0):
            # 上、下、左、右
            img = cv.copyMakeBorder(i[0], int((hMax - h) / 2), int((hMax - h) / 2), int((wMax - w) / 2), int((wMax - w) / 2), cv.BORDER_CONSTANT, value=[255, 255, 255])
        elif (h % 2 != 0 and w % 2 == 0):
            img = i[0][0:h - 1, 0:w]
            h, w = img.shape[:2]
            img = cv.copyMakeBorder(img, int((hMax - h) / 2), int((hMax - h) / 2), int((wMax - w) / 2), int((wMax - w) / 2), cv.BORDER_CONSTANT, value=[255, 255, 255])
        elif (h % 2 == 0 and w % 2 != 0):
            img = i[0][0:h, 0:w - 1]
            h, w = img.shape[:2]
            img = cv.copyMakeBorder(img, int((hMax - h) / 2), int((hMax - h) / 2), int((wMax - w) / 2), int((wMax - w) / 2), cv.BORDER_CONSTANT, value=[255, 255, 255])
        else:
            img = i[0][0:h - 1, 0:w - 1]
            h, w = img.shape[:2]
            img = cv.copyMakeBorder(img, int((hMax - h) / 2), int((hMax - h) / 2), int((wMax - w) / 2), int((wMax - w) / 2), cv.BORDER_CONSTANT, value=[255, 255, 255])
        h, w = img.shape[:2]
        # print(h, w)
        cv.imwrite(OutPath + '/%s.png' % i[1], img)
        # print('放大后的矩形：' + '%s.png' % i[1])
        j += 1


# 最终处理函数(全部图像读取；全部图像二值化、降噪；全部图像裁剪)
# InPath：未处理图片存储路径
# OutPath：裁剪后图片存储路径
def ImgInOut(InPath, OutPath):
    # 待处理图片路径
    Img, Name = read_directory(InPath)
    for i in list(zip(Img, Name)):
        # 处理图片并返回矩阵
        gray = ImgProcess(i[0])
        # 每组图片从1开始计数
        num = 1
        # 图片切割
        CutImg(gray, num, OutPath, i[1])
