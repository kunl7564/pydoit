#!/usr/bin/python
# coding=utf-8
import sys;

# 由于 python 并不支持 switch 语句，所以多个条件判断，只能用 elif 来实现
num = 5     
if num == 3:  # 判断num的值
    print 'boss'        
elif num == 2:
    print 'user'
elif num == 1:
    print 'worker'
elif num < 0:  # 值小于零时输出
    print 'error'
else:
    print 'roadman'  # 条件均不成立时输出

num = 10
if num < 0 or num > 10:  # 判断值是否在小于0或大于10
    print 'hello'
else:
    print 'undefine'
# 输出结果: undefine
 
num = 8
# 判断值是否在0~5或者10~15之间
if (num >= 0 and num <= 5) or (num >= 10 and num <= 15):    
    print 'hello'
else:
    print 'undefine'


var = 100 
 
if (var == 100) : print "变量 var 的值为100" 
