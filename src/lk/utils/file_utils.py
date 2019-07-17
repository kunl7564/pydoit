import os
from shutil import copyfile, rmtree
import shutil

def read(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r') as f:
        # print(f.read())
        return(f.read())

def write(file_path, content):
    pardir = os.path.dirname(file_path)
    if not os.path.exists(pardir):
        os.makedirs(pardir)
    with open(file_path, 'w') as f:
        f.write(content)
        
def copy(src, dist):
    if os.path.exists(src):
        copyfile(src, dist)
    
def rename(src, dist):
    if os.path.exists(src):
        os.rename(src, dist)

def removeOld(path):
    if os.path.isdir(path):
        os.removedirs(path)    
        return
    os.remove(path)
    
def remove(path):
    if os.path.exists(path):
        rmtree(path)
    
def get_filename(file_path):
    return (os.path.split(file_path)[1])

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
