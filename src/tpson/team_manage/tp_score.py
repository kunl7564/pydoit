#!/usr/bin/python
# coding=utf-8

import datetime
import json
import math
import os
import time

import file_utils
import mail_utils
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

class Stat:
    def __init__(self, name, score, mailContent):
        self.name = name
        self.score = score
        self.mailContent = mailContent

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
        self.content = (u'【 %s 】 %s | 基础分%s | 系数%s | 分值变化%s | 团队评价: %s' % (description, type, base, ratio, delta, self.comment))

gMembers = {}
gScores = {}
gWorkdays = {}
gStats = []

def getWorkdays(beginDate, endDate):
    workdays = 0
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    date = beginDate[:]
    while date <= endDate:
        if gWorkdays.has_key(date) and gWorkdays[date] == 1:
            workdays += 1
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return workdays


def main():
    startDate = '20190901'
    endDate = '20190915'
    RANK_ALL = False

    # 读取团队
    record_sheet = pd.read_excel(ROOT_PATH + r'\team_member.xlsx', sheetname='member')
    for i, row in record_sheet.iterrows():
        gMembers[row[0]] = Member(row[0], row[1], row[2])
    
    # 读取工作日判断
    workday_sheet = pd.read_csv(ROOT_PATH + r'\date_2019.csv', header=None)
    for i, row in workday_sheet.iterrows():
        gWorkdays[str(row[0])] = row[2]
    baseScore = getWorkdays(startDate, endDate)

    # 读取tp分记录
    os.chdir(ROOT_PATH)
    files = os.listdir(ROOT_PATH)
    for f in files:
        if f.startswith('record_'):
            print(f)
            member_sheet = pd.read_excel(f, sheetname='record', skiprows=0)
#             print(member_sheet.head())
            for i, row in member_sheet.iterrows():
                if gScores.has_key(row[1]) == False:
                    scoreList = []
                    gScores[row[1]] = scoreList
                scoreList = gScores[row[1]]
                scoreList.append(Scores(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                
    totalMemberNum = len(gScores)
    print(totalMemberNum)
    
    # 统计分数并发送邮件
    for name in sorted(gScores.keys()):
        totalDelta = baseScore  # 工作日转换的基础分
        totalDeltaContent = u''
        mailContent = u''
        goodContent = u'\n以下项获得了点赞:\n'
        skipGood = True
        badContent = u'\n团队希望你提升的项:\n'
        skipBad = True
        if gScores.has_key(name):
            scoreList = gScores[name]
            for score in scoreList:
                totalDelta += score.delta
                if score.delta > 0 and score.ratio > 1 and len(score.comment) >= 2:
#                     print (score.name + score.content)
                    goodContent += score.content + '\n'
                    skipGood = False
                if (score.delta < 0 or score.ratio < 1) and len(score.comment) >= 2:
                    badContent += score.content + '\n'
                    skipBad = False
        if skipGood:
            goodContent = ''
        if skipBad:
            badContent = ''

        totalDeltaContent += str(totalDelta) + '\n'
        mailContent += goodContent + badContent + u'\n本邮件为自动发送请勿回复,任何建议请联系tp分管理委员会'
        gStats.append(Stat(name, totalDelta, mailContent))

    gStats.sort(key=getStatKey, reverse=True)
    totalReport = u''
    for i, stat in enumerate(gStats):
        print(('%s %s' % (stat.name, stat.score)).encode('utf-8'))
        if RANK_ALL == False:
            if (i + 1.0) / len(gStats) <= 0.5 or i == 0:
                mailContent = u'本期tp分变化：' + str(stat.score) + u'，进入团队前50%，继续加油\n'
            else:
                mailContent = u'本期tp分变化：' + str(stat.score)
        else:
            mailContent = u'本期tp分变化：%s，综合排名%s\n' % (stat.score, i + 1)
            
        totalReport += stat.name + ',\t' + str(stat.score) + '\n'
        mailContent += stat.mailContent
        if gMembers.has_key(stat.name):
            member = gMembers[stat.name]
            mail_utils.sendMail(member.email, (u'[%s-%s] %s TP分更新' % (startDate, endDate, stat.name)), mailContent)
    mail_utils.sendMail('liangkun@tpson.cn', ('[%s-%s] TP分更新汇总' % (startDate, endDate)), totalReport)

def getStatKey(x):
    return x.score

if __name__ == '__main__':
    main()
