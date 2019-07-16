#!/usr/bin/python
# coding=utf-8
import smtplib
from email.mime.text import MIMEText

def parse(path):    
    with open(path,"r") as f:
        lines=f.readlines()
    for line in lines:
        lineData=line.strip().split(',') #去除空白和逗号“,”
        if random.random()<0.7:  #数据集分割比例
            trainingData.append(lineData) #训练数据集
        else:
            testData.append(lineData) #测试数据集
    return
