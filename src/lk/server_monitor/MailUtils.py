#!/usr/bin/python
# coding=utf-8
import smtplib
from email.mime.text import MIMEText

# sender = '9687564@qq.com'
# smtpserver = 'smtp.qq.com'
# password = 'ffxihxwhomecbgga'
# username = sender
sender = 'kun.liang@coollu.com.cn'
smtpserver = 'smtp.exmail.qq.com'
password = 'wix9RjiLR6sc6eJX'
username = sender

def sendMail(receiver, subject, content):    
    '''中文需参数‘utf-8’ ，单字节字符不需要'''
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = "liangkun<liangkun@tpson.cn>"
    msg['To'] = receiver
    smtp = smtplib.SMTP_SSL(smtpserver, port=465)
    smtp.connect(smtpserver)
    loginRet = smtp.login(username, password)
    sendRet = smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print ("Email has been sent out!", loginRet, sendRet)
    return

sendMail("9687564@qq.com", "subject", "content")
