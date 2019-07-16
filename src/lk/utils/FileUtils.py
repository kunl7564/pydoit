#!/usr/bin/python
# coding=utf-8
import os;
print os.getcwd()
# File 对象方法: file对象提供了操作文件的一系列方法。
# OS 对象方法: 提供了处理文件及目录的一系列方法。
import os;

document = open("testfile.txt", "w+");
print "文件名: ", document.name;
document.write("123456789");
document.truncate(3);
print document.tell();
# 输出当前指针位置
document.seek(os.SEEK_SET);
# 设置指针回到文件最初
context = document.read();
print context;
document.close();
