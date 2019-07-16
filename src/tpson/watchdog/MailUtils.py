#!/usr/bin/python
# coding=utf-8
#!/usr/bin/python
# coding=utf-8
import smtplib
from email.mime.text import MIMEText

# sender = '9687564@qq.com'
# smtpserver = 'smtp.qq.com'
# MailUtils.sendMail("liangkun@tpson.cn", "重要通知", "明天开会")
sender = 'kun.liang@coollu.com.cn'
smtpserver = 'smtp.exmail.qq.com'  # kun.liang
password = 'wix9RjiLR6sc6eJX'  # kun.liang
username = 'kun.liang@coollu.com.cn'

def sendMail(receiver, subject, content):    
    '''中文需参数‘utf-8’ ，单字节字符不需要'''
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
    [code1, msg2] = smtp.connect(smtpserver)
    print msg2
    [code2, resp] = smtp.login(username, password)
    print resp
    senderrs = smtp.sendmail(sender, receiver, msg.as_string())
    print senderrs
    smtp.quit()
    print ("Email has been sent out!")
    return
