#!
# -*- coding: utf-8 -*-
import cv2 as cv
import os
from PIL import Image

def cut(folder_name):
    # 构建文件夹路径
    folder_path = os.path.join(".", "image", folder_name)

    # 获取文件夹中的第一个图片文件
    image_file = os.path.join(folder_path, "schedule.png")

    # 读取输入图像
    img = cv.imread(image_file, 0)
    original_image = cv.imread(image_file)

    # 获取宽高
    size = original_image.shape
    w = size[1]    # 宽度
    h = size[0]    # 高度

    if (w < h):
        return 0

    # 应用Canny边缘检测
    edges = cv.Canny(img, threshold1=50, threshold2=150)

    # 寻找轮廓
    contours, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 寻找最大轮廓
    max_contour = max(contours, key=cv.contourArea)

    # 获取最大轮廓的边界框
    x, y, w, h = cv.boundingRect(max_contour)

    # 截取课程表部分
    course_table = original_image[y:y+h, x:x+w]

    height, width = course_table.shape[:2]

    # 计算缩放比例
    target_height = 699
    scale_factor = target_height / height

    # 计算缩放后的宽度
    target_width = int(width * scale_factor)

    # 缩放图像
    resized_image = cv.resize(course_table, (target_width, target_height))

    save_file = os.path.join(folder_path, "cut.png")

    cv.imwrite(save_file, resized_image)

    return save_file
