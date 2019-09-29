#!/usr/bin/python
# coding=utf-8
import json
import json
import urllib

import requests

key = '8da9f1a2e8c3a678e91504801b087558'
# http://api.goseek.cn/Tools/holiday?date=20190912
def getWeather(num):
    """
    通过快递单号获取快递详情方法
    :param num: Numbers 快递单号
    :return: mixed      快递详细
    """
    # get请求
    url = 'https://restapi.amap.com/v3/weather/weatherInfo?city=110101&key=' + key  # get请求通过url传值
    r = requests.get(url)  # python3应该可以通过检测data是否携带参数来判断是get请求还是post请求
    text = json.loads(r.text)  # dict
    print(text)
    print(text['lives'])
    lives = text['lives']  # list
    print(lives)
    print(lives[0])
#     for city in r.text["lives"]:
#         if city["cityId"] == 4:
#             print(city)

def isWorkday(date):
    # get请求 正常工作日对应结果为 0, 法定节假日对应结果为 1, 节假日调休补班对应的结果为 2，休息日对应结果为 3
    # {"code":10000,"data":0}
    url = 'http://api.goseek.cn/Tools/holiday?date=' + str(date)  # get请求通过url传值
    r = requests.get(url)  # python3应该可以通过检测data是否携带参数来判断是get请求还是post请求
    text = json.loads(r.text)  # dict
    print(str(text) + ' ' + str(date))
    if text['data'] == 0:
        return 1
    else:
        return 0

def workdayType(date):
    # get请求 正常工作日对应结果为 0, 法定节假日对应结果为 1, 节假日调休补班对应的结果为 2，休息日对应结果为 3
    # {"code":10000,"data":0}
    url = 'http://api.goseek.cn/Tools/holiday?date=' + str(date)  # get请求通过url传值
    r = requests.get(url)  # python3应该可以通过检测data是否携带参数来判断是get请求还是post请求
    text = json.loads(r.text)  # dict
    print(str(text) + ' ' + str(date))
    return text['data']

# isWorkday(20190912)
