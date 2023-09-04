#!
# -*- coding: utf-8 -*-
import re

def remove_special_characters(input_string):
    # ʹ��������ʽƥ��������Ų��滻Ϊ���ַ���
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)

    # ���ַ���ǰ��� "table_" ǰ׺
    formatted_string = 'table_' + cleaned_string
    return formatted_string[:64]
