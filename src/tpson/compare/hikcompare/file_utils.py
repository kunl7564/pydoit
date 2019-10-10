#!/usr/bin/python
# coding=utf-8
import codecs
import os
from shutil import copyfile, rmtree
import shutil
import sys

# 
# reload(sys)
# sys.setdefaultencoding("utf-8")
def read(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r') as f:
        # print(f.read())
        return(f.read())

def write(file_path, content, append):
    pardir = os.path.dirname(file_path)
    if not os.path.exists(pardir):
        os.makedirs(pardir)
    if append == True:
        with open(file_path, 'a+') as f:
            f.write(content)
    else:
        with open(file_path, 'w+') as f:
            f.write(content)
        
def encodingWrite(file_path, codec, content, append):
    pardir = os.path.dirname(file_path)
    if not os.path.exists(pardir):
        os.makedirs(pardir)
    if append == True:
        f = codecs.open(file_path, 'a', encoding=codec)
        f.write(content)
        f.close()
    else:
        with codecs.open(file_path, 'w', encoding=codec) as f:
            f.write(content)
        
def copy(src, dist):
    if os.path.exists(src):
        copyfile(src, dist)
    
def rename(src, dist):
    if os.path.exists(src):
        os.rename(src, dist)

def removeFile(path):
    if os.path.isdir(path):
        os.removedirs(path)    
        return
    if os.path.exists(path):  
        os.remove(path)
    
def removeDir(path):
    if os.path.exists(path):
        rmtree(path)
    
def get_filename(file_path):
    return (os.path.split(file_path)[1])

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# def getFileDir():
#     return os.path.split(os.path.realpath(__file__))[0]
