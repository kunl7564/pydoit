#!/usr/bin/python
# coding=utf-8
import sys;
# 定义函数
def printme(str):
   "打印任何传入的字符串"
   print str;
   return;
 
# 调用函数
printme("我要调用用户自定义函数!");
printme("再次调用同一函数");

# 缺省参数
def printinfo(name, age=35):
   "打印任何传入的字符串"
   print "Name: ", name;
   print "Age ", age;
   return;
 
# 调用printinfo函数
printinfo(age=50, name="miki");
printinfo(name="miki");


# 可写函数说明
def printinfo2(arg1, *vartuple):
   "打印任何传入的参数"
   print "输出: "
   print "arg1", arg1
   for var in vartuple:
      print var
   return;
 
# 调用printinfo 函数
printinfo2(10);
printinfo2(70, 60, 50);

# 匿名函数
# 可写函数说明
sum = lambda arg1, arg2: arg1 + arg2;
 
# 调用sum函数
print "相加后的值为 : ", sum(10, 20)
print "相加后的值为 : ", sum(20, 20)


# 全局变量想作用于函数内，需加 global
globvar = 0

def set_globvar_to_one():
    global globvar  # 使用 global 声明全局变量
    globvar = 1

def print_globvar():
    print(globvar)  # 没有使用 global

set_globvar_to_one()
print  globvar  # 输出 1
print_globvar()  # 输出 1，函数内的 globvar 已经是全局变量
