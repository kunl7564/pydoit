#!/usr/bin/python
# coding=utf-8
import json
import math
import os
import time

from Cython.Compiler.Options import annotate
from mpl_toolkits.mplot3d import Axes3D
from pip._vendor.pyparsing import unicodeString
from pylab import *
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
import xlrd

from lk.utils import file_utils as fu
import mail_utils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__author__ = "Liang Kun"
__copyright__ = "Tpson 2019"
__version__ = "1.0.0"
__license__ = "tpson"

ROOT_PATH = r'd:\tmp\growup_diary\tp_score'
class Member:
    def __init__(self, name, email, department):
        self.name = name
        self.email = email
        self.department = department

class Scores:
    def __init__(self, time, name, type, base, ratio, delta, description, comment):
        self.time = time
        self.name = name
        self.type = type
        self.base = base
        self.ratio = ratio
        self.delta = delta
        self.description = description
        if comment == comment:  # NaN判断
            self.comment = comment.replace('\n', '')
        else:
            self.comment = ''
        # '时间    姓名    分值类型    基础分    系数    分值变化    说明    备注'
        self.content = (u'| %s | %s | 基础分%s | 系数%s | 分值变化%s | 团队评价: %s' % (description, type, base, ratio, delta, self.comment))

gMembers = {}
gScores = {}
gWorkdays = {}

def main():
    # 读取团队
    record_sheet = pd.read_excel(ROOT_PATH + r'\team_member.xlsx', sheetname='member')
    for i, row in record_sheet.iterrows():
        gMembers[row[0]] = Member(row[0], row[1], row[2])
    
    # 读取工作日判断
    workday_sheet = pd.read_csv(ROOT_PATH + r'\date_2019.csv', header=None)
    for i, row in workday_sheet.iterrows():
        gWorkdays[row[0]] = row[2]
    
    # 读取tp分记录
    files = os.listdir(ROOT_PATH)
    for f in files:
        if f.startswith('record_'):
            print(f)
            member_sheet = pd.read_excel(ROOT_PATH + r'\record_201909.xlsx', sheetname='record', skiprows=0)
#             print(member_sheet.head())
            for i, row in member_sheet.iterrows():
                if gScores.has_key(row[1]) == False:
                    scoreList = []
                    gScores[row[1]] = scoreList
                scoreList = gScores[row[1]]
                scoreList.append(Scores(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                if row[7] != row[7]:  # NaN not a number
                    print(row[1])

    # 统计分数并发送邮件
    for name in sorted(gScores.keys()):
        totalDelta = 0
        totalDeltaContent = u'本期tp分变化：'
        mailContent = u''
        goodContent = u'\n以下项获得了点赞:\n'
        skipGood = True
        badContent = u'\n团队希望你提升的项:\n'
        skipBad = True
        if gScores.has_key(name):
            scoreList = gScores[name]
            for score in scoreList:
                totalDelta += score.delta
                if score.delta > 0 and score.ratio > 1 and score.comment == score.comment:
                    print (score.name + score.content)
                    goodContent += score.content + '\n'
                    skipGood = False
                if (score.delta < 0 or score.ratio < 1) and score.comment == score.comment :
                    badContent += score.content + '\n'
                    skipBad = False
        if skipGood:
            goodContent = ''
        if skipBad:
            badContent = ''

        totalDeltaContent += str(totalDelta) + '\n'
        if gMembers.has_key(name):
            member = gMembers[name]
            print(member.email)
            mailContent += totalDeltaContent + goodContent + badContent + u'\n本邮件为自动发送请勿回复,任何建议请联系tp分管理委员会'
            mail_utils.sendMail(member.email, 'TP分通知', mailContent)

if __name__ == '__main__':
    main()
