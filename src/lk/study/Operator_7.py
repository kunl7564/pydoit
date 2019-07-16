#!/usr/bin/python
# coding=utf-8
import sys;

# **    幂 - 返回x的y次幂
# //    取整除 - 返回商的整数部分

# Python2.x 里，整数除整数，只能得出整数。如果要得到小数部分，把其中一个数改成浮点数即可
print 1 / 2
print 1.0 / 2
print 1.0 / float(2)

# <>    不等于 - 比较两个对象是否不相等 同!=
a = 21
b = 21
c = 0
if (a <> b):
   print "a 不等于 b"
else:
   print "a 等于 b"
   
# and    x and y    布尔"与" - 如果 x 为 False，x and y 返回 False，否则它返回 y 的计算值。    (a and b) 返回 20
# or    x or y    布尔"或"    - 如果 x 是非 0，它返回 x 的值，否则它返回 y 的计算值。    (a or b) 返回 10
# not    not x    布尔"非" - 如果 x 为 True，返回 False 。如果 x 为 False，它返回 True。    not(a and b) 返回 False
if (a and b):
   print "1 - 变量 a 和 b 都为 true"
else:
   print "1 - 变量 a 和 b 有一个不为 true"

# in    如果在指定的序列中找到值返回 True，否则返回 False。    x 在 y 序列中 , 如果 x 在 y 序列中返回 True
# not in    如果在指定的序列中没有找到值返回 True，否则返回 False。    x 不在 y 序列中 , 如果 x 不在 y 序列中返回 True
list = [1, 21, 3, 4, 5 ];
if (a in list):
   print "1 - 变量 a 在给定的列表中 list 中"
else:
   print "1 - 变量 a 不在给定的列表中 list 中"
   
# is    is 是判断两个标识符是不是引用自一个对象    x is y, 类似 id(x) == id(y) , 如果引用的是同一个对象则返回 True，否则返回 False
# is not    is not 是判断两个标识符是不是引用自不同对象    x is not y ， 类似 id(a) != id(b)。如果引用的不是同一个对象则返回结果 True，否则返回 False。

# is 与 == 区别：
# is 用于判断两个变量引用对象是否为同一个， == 用于判断引用变量的值是否相等。