#!/usr/bin/python
# coding=utf-8

import datetime
import json
import math
import os
import time

import file_utils
import numpy as np
import pandas as pd

__author__ = "Liang Kun"
__copyright__ = "Tpson 2019"
__version__ = "1.0.0"
__license__ = "tpson"

ROOT_PATH = r'.'
gAll = []

def main():

    # 读取总表
    all_sheet = pd.read_excel(ROOT_PATH + r'\all.xls')
    for i, row in all_sheet.iterrows():
        gAll.append(row[10])
    
    # 读取待确认表
    sub_sheet = pd.read_excel(ROOT_PATH + r'\sub.xls')
    file_utils.removeFile(ROOT_PATH + r'\result.csv')
    for i, row in sub_sheet.iterrows():
        if row[7] in gAll:
            content = '%s,\t%s,\t%s,\t%s,\t%s\n' % (row[0], row[4], row[5], row[6], row[7])
#             utfContent = content.encode('utf-8')
#             print(content)
            file_utils.encodingWrite(ROOT_PATH + r'\result.csv', 'gbk', content, True)
            
if __name__ == '__main__':
    main()
