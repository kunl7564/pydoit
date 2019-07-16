#!/usr/bin/python
# coding=utf-8
import sys;
# dir() 函数一个排好序的字符串列表，内容是一个模块里定义过的变量和函数。
import Function;
content = dir(Function)
print content
print globals() 
print locals()

