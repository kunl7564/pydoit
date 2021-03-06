#!/usr/bin/python
# coding=utf-8
import sys

# 以下划线开头的标识符是有特殊意义的。以单下划线开头 _foo 的代表不能直接访问的类属性，需通过类提供的接口进行访问，不能用 from xxx import * 而导入；
# # 以双下划线开头的 __foo 代表类的私有成员；以双下划线开头和结尾的 __foo__ 代表 Python 里特殊方法专用的标识，如 __init__() 代表类的构造函数。
# # Python 可以同一行显示多条语句，方法是用分号 ; 分开，如：
print 'hello';print 'runoob';

# Python 的代码块不使用大括号 {} 来控制类，函数以及其他逻辑判断。python 最具特色的就是用缩进来写模块。
# 缩进的空白数量是可变的，但是所有代码块语句必须包含相同的缩进空白数量
if True:
    print "Answer"
    print "True"
    
else:
    print "Answer"
    # 没有严格缩进，在执行时会报错
    print "False"

# 但是我们可以使用斜杠（ \）将一行的语句分为多行显示，如下所示：
total = 'item_one ' + \
        'item_two'
print total
# 语句中包含 [], {} 或 () 括号就不需要使用多行连接符。如下实例：
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday']

# Python 可以使用引号( ' )、双引号( " )、三引号( ''' 或 """ ) 来表示字符串，引号的开始与结束必须的相同类型的。
# 其中三引号可以由多行组成，编写多行文本的快捷语法，常用于文档字符串，在文件的特定地点，被当做注释。
word = 'word'
sentence = "这是一个句子。"
paragraph = """这是一个段落。
包含了多个语句"""

# python 中多行注释使用三个单引号(''')或三个双引号(""")。
'''
这是多行注释，使用单引号。
这是多行注释，使用单引号。
这是多行注释，使用单引号。
'''

"""
这是多行注释，使用双引号。
这是多行注释，使用双引号。
这是多行注释，使用双引号。
"""

# 函数之间或类的方法之间用空行分隔，表示一段新的代码的开始。类和函数入口之间也用一行空行分隔，以突出函数入口的开始。


# 等待用户输入
# raw_input("按下 enter 键退出，其他任意键显示...")

# print 默认输出是换行的，如果要实现不换行需要在变量末尾加上逗号 ,
x = "a"
y = "b"
# 换行输出
print x
print y

print '---------'
# 不换行输出
print x,
print y,

# 不换行输出
print x, y


# 缩进相同的一组语句构成一个代码块，我们称之代码组。
# 像if、while、def和class这样的复合语句，首行以关键字开始，以冒号( : )结束，该行之后的一行或多行代码构成代码组。
# 我们将首行及后面的代码组称为一个子句(clause)

print sys.argv