#!/usr/bin/python
# coding=utf-8
import sys;
from asn1crypto.core import InstanceOf

# Python 中的变量赋值不需要类型声明。
# 每个变量在内存中创建，都包括变量的标识，名称和数据这些信息。
# 每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建
# 等号（=）运算符左边是一个变量名,等号（=）运算符右边是存储在变量中的值

counter = 100  # 赋值整型变量 int
miles = 1000.0  # 浮点型 float
name = "John"  # 字符串 str
 
print counter
print miles
print name

# Python允许你同时为多个变量赋值
a = b = c = 1
print a, b, c
a, b, c = 1, 2, "john"
print a, b, c

# Python有五个标准的数据类型：
# Numbers（数字）
# String（字符串）
# List（列表）
# Tuple（元组）
# Dictionary（字典）

# Python支持四种不同的数字类型：
# int（有符号整型）
# long（长整型[也可以代表八进制和十六进制]）
# float（浮点型）
# complex（复数）

# Python使用 L 来显示长整型
#     51924361L

# 字符串使用
str = 'Hello World!'
 
print str  # 输出完整字符串
print str[0]  # 输出字符串中的第一个字符
print str[2:5]  # 输出字符串中第三个至第五个之间的字符串
print str[2:]  # 输出从第三个字符开始的字符串
print str * 2  # 输出字符串两次
print str + "TEST"  # 输出连接的字符串

# list使用，列表用 [ ] 标识
list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
tinylist = [123, 'john']
 
print list  # 输出完整列表
print list[0]  # 输出列表的第一个元素
list[0] = 'kunl'
print list[1:3]  # 输出第二个至第三个元素 
print list[2:]  # 输出从第三个开始至列表末尾的所有元素
print tinylist * 2  # 输出列表两次
print list + tinylist  # 打印组合的列表

# 元组使用，元组用"()"标识。内部元素用逗号隔开。但是元组不能二次赋值，相当于只读列表。
tuple = ('runoob', 786 , 2.23, 'john', 70.2)
tinytuple = (123, 'john')
 
print tuple  # 输出完整元组
print tuple[0]  # 输出元组的第一个元素
print tuple[1:3]  # 输出第二个至第三个的元素 
print tuple[2:]  # 输出从第三个开始至列表末尾的所有元素
print tinytuple * 2  # 输出元组两次
print tuple + tinytuple  # 打印组合的元组


# 字典使用 字典用"{ }"标识。字典由索引(key)和它对应的值value组成。
dict = {}
dict['one'] = "This is one"
dict[2] = "This is two"
 
tinydict = {'name': 'john', 'code':6734, 'dept': 'sales'}
 
 
print dict['one']  # 输出键为'one' 的值
print dict[2]  # 输出键为 2 的值
print tinydict  # 输出完整的字典
print tinydict.keys()  # 输出所有键
print tinydict.values()  # 输出所有值

# 有时候，我们需要对数据内置的类型进行转换，数据类型的转换，你只需要将数据类型作为函数名即可。
x = 1;
x = float(x)
print x

# 查看变量类型
# python 的所有数据类型都是类,可以通过 type() 查看该变量的数据类型:
print type(x) == float
# 此外还可以用 isinstance 来判断：
print isinstance(x, int)
# isinstance()会认为子类是一种父类类型。
class A:
    pass
class B(A):
    pass
print isinstance(A(), A), isinstance(B(), A) 
# True False True False

# 数据类型 分为数字型和非数字型。
# 数字型包括整型，长整型，浮点型，复数型；
# 非数字型包括字符串，列表，元组和字典 ；
# 非数字型的共同点：都可以使用切片、链接（+）、重复（*）、取值（a[]）等相关运算;
# 非数字型的不同点：
# 列表 可以直接赋值，元组不可以赋值，字典按照 dict[k]=v 的方式赋值。

