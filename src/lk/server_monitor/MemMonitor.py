# coding=utf-8
import os
import sys
import MailUtils
import threading
from time import sleep
import SystemUtils

class MemMonitorThread(threading.Thread):
    def __init__(self, serverName, threshold=1200, pollingGap=5):
        threading.Thread.__init__(self)
        self.serverName = serverName
        self.threshold = threshold
        self.pollingGap = pollingGap
    def run(self):
        print "Starting MemMonitorThread on " + self.serverName
        subject = self.serverName + " 内存报警!"
        alarm = False
#         maillist = "liangkun@tpson.cn;"
        maillist = "liuandong@tpson.cn;wuqinghua@tpson.cn;mayuefeng@tpson.cn;liangkun@tpson.cn;caifushou@tpson.cn"
        while True:
            freeMem = SystemUtils.getFreeMemory()
            if SystemUtils.getFreeMemory() < self.threshold:
                if alarm == False:
                    alarm = True
                    content = "剩余内存 " + str(freeMem) + "Mb\n" + SystemUtils.getAllProcessMemInfo() + "\n" + os.popen('top -b -n 1').read()
                    MailUtils.sendMail(maillist, subject, content)
            else:
                alarm = False
            sleep(self.pollingGap)
