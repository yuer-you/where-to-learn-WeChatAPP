#!
# -*- coding: utf-8 -*-
import cv2 as cv
import os
from PIL import Image

def cut(folder_name):
    # �����ļ���·��
    folder_path = os.path.join(".", "image", folder_name)

    # ��ȡ�ļ����еĵ�һ��ͼƬ�ļ�
    image_file = os.path.join(folder_path, "schedule.png")

    # ��ȡ����ͼ��
    img = cv.imread(image_file, 0)
    original_image = cv.imread(image_file)

    # ��ȡ���
    size = original_image.shape
    w = size[1]    # ���
    h = size[0]    # �߶�

    if (w < h):
        return 0

    # Ӧ��Canny��Ե���
    edges = cv.Canny(img, threshold1=50, threshold2=150)

    # Ѱ������
    contours, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Ѱ���������
    max_contour = max(contours, key=cv.contourArea)

    # ��ȡ��������ı߽��
    x, y, w, h = cv.boundingRect(max_contour)

    # ��ȡ�γ̱���
    course_table = original_image[y:y+h, x:x+w]

    height, width = course_table.shape[:2]

    # �������ű���
    target_height = 699
    scale_factor = target_height / height

    # �������ź�Ŀ��
    target_width = int(width * scale_factor)

    # ����ͼ��
    resized_image = cv.resize(course_table, (target_width, target_height))

    save_file = os.path.join(folder_path, "cut.png")

    cv.imwrite(save_file, resized_image)

    return save_file
