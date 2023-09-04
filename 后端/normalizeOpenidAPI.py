#!
# -*- coding: utf-8 -*-
import re

def remove_special_characters(input_string):
    # 使用正则表达式匹配特殊符号并替换为空字符串
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)

    # 在字符串前添加 "table_" 前缀
    formatted_string = 'table_' + cleaned_string
    return formatted_string[:64]
