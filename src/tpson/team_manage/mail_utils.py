#!/usr/bin/python
# coding=utf-8

from email.mime.text import MIMEText
import smtplib

sender = '9687564@qq.com'
smtpserver = 'smtp.qq.com'
# MailUtils.sendMail("liangkun@tpson.cn", "重要通知", "明天开会")
def sendMail(receiver, subject, content):    
    # sender = 'kun.liang@coollu.com.cn'
    # receiver = 'liangkun@tpson.cn'
    password = 'ffxihxwhomecbgga'
    username = '9687564@qq.com'
    # smtpserver = 'smtp.exmail.qq.com'#kun.liang
    # username = 'kun.liang@coollu.com.cn'#kun.liang
    # password = 'wix9RjiLR6sc6eJX'#kun.liang
    '''中文需参数‘utf-8’ ，单字节字符不需要'''
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = "研发AI小助手<9687564@qq.com>"
    msg['To'] = receiver
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print ("Email has been sent out!")
    return
