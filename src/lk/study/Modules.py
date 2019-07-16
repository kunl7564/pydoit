#!/usr/bin/python
# coding=utf-8
# http://www.runoob.com/python/python-modules.html
import sys;
count = 0
while (count < 9):
   print 'The count is:', count
   count = count + 1
 
print "Good bye!"

# 在 python 中，while … else 在循环条件为 false 时执行 else 语句块：
count = 0
while count < 5:
   print count, " is  less than 5"
   count = count + 1
else:
   print count, " is not less than 5"
s = 'qazxswedcvfr'
for i in range(0, len(s), 2):
    print s[i]
    
sequence = [12, 34, 34, 23, 45, 76, 89]
for i, j in enumerate(sequence):
    print i, j
    
