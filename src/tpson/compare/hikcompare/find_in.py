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
# ROOT_PATH = r'd:\hikcompare'
gIdList = []
gMapList = []

class Unit:
    def __init__(self, index, content):
        self.index = index
        self.content = content

def main():
    file_utils.removeFile(ROOT_PATH + r'\result.csv')

    # 读取待确认表 0,4,5,9,10
    sub_sheet = pd.read_excel(ROOT_PATH + r'\sub.xls')
    for i, row in sub_sheet.iterrows():
        gIdList.append(row[7])

    # 遍历总表
    os.chdir(ROOT_PATH)
    files = os.listdir(ROOT_PATH)
    for f in files:
        if f.startswith('all'):
            print(f)
            map = {}
            gMapList.append(map)
            all_sheet = pd.read_excel(f)
            for i, row in all_sheet.iterrows():
                map[row[10]] = row;
    
    for i, id in enumerate(gIdList):
        writeContent = ""
        flag = 0
        counter = 0
        for j, map in enumerate(gMapList):
            counter += 1
            if id in map:
                row = map[id]
                if counter == 1:
                    writeContent += '%s,\t%s,\t%s,\t%s,\t%s' % (row[0], row[4], id, row[5], row[9])
                else :
                    writeContent += ',\t%s,\t%s' % (row[5], row[9])
            else:
                if counter == 1:
                        writeContent += '%s,\t%s,\t%s,\t%s,\t%s' % ("NA", "NA", id, "NA", "NA")
                else :
                    writeContent += ',\t%s,\t%s' % ("NA", "NA")

        # bitmap        
        if writeContent.find(u"在线") >= 0:
            flag |= 1
        if writeContent.find(u"离线") >= 0:
            flag |= 2
        if writeContent.find(u"故障") >= 0:
            flag |= 4
        writeContent += ',\t' + str(flag) + '\n'
        print(writeContent)
        file_utils.encodingWrite(ROOT_PATH + r'\result.csv', 'gbk', writeContent, True)
            
if __name__ == '__main__':
    main()
