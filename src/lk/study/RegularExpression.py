#!/usr/bin/python
# coding=utf-8
# https://baike.baidu.com/item/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/1700215?fr=aladdin
import os

import re
print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))  # 不在起始位置匹配

line = "Cats are smarter than dogs"
matchObj = re.match('(.*?) are (.*?) (.*)', line, re.M | re.I)
# matchObj = re.match('(.*?) are (.*) (.*)', line, re.M | re.I)
# matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
# 括号里的就是group ?是非贪婪模式，找到第一个就停止
 
if matchObj:
   print "matchObj.group() : ", matchObj.group(), matchObj.span();
   print "matchObj.group(1) : ", matchObj.group(1)
   print "matchObj.group(2) : ", matchObj.group(2)
   print "matchObj.group(3) : ", matchObj.groups()
else:
   print "No match!!"

# re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配
line = "Cats are smarter than dogs";
 
matchObj = re.match(r'dogs', line, re.M | re.I)
if matchObj:
   print "match --> matchObj.group() : ", matchObj.group()
else:
   print "No match!!"
 
matchObj = re.search(r'dogs', line, re.M | re.I)
if matchObj:
   print "search --> matchObj.group() : ", matchObj.group()
else:
   print "No match!!"


phone = "2004-959-559 1# 这是一个国外电话号码"
 
# 删除字符串中的 Python注释 
num = re.sub(r'#.*$', "", phone)
print "电话号码是: ", num
 
# 删除非数字(-)的字符串 
num = re.sub(R'\D', "", phone)  # \D表示非数字，\d表示数字
print "电话号码是 : ", num


# 将匹配的数字乘于 2
def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)
 
s = 'A23G4HFD567'
print(re.sub('(?P<value>\d+)', double, s))

s = re.split('oo|b', 'runoob, runoob, runoob.')
print s
s = re.split('(\W+)', 'runoob, runoob, runoob.') 
print s
