#!/usr/bin/python
# coding=utf-8
import os
import socket
from time import sleep
import time
import urllib

import chardet
from win32api import GetSystemMetrics

print('start')
# data = urllib.urlopen('http://www.tpson.cn').read()
# print data
x = 1
def initFeatureList():
    global x
    print(x)
    x = 3
    return True

print(x)
initFeatureList();
print(x)
