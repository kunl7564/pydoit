# coding=utf-8
import os
import sys
import psutil
import platform
import time
# https://blog.csdn.net/bubu8633/article/details/8258342

def getCpuUsage(interval=1):  
    return psutil.cpu_percent(interval)

# free memory, MB
def getFreeMemory():   
    phymem = psutil.virtual_memory()
    if platform.system() == u'Linux':
        return (phymem.free + phymem.buffers + phymem.cached) / 1024 / 1024 
    else:
        return phymem.free / 1024 / 1024 

def getAllProcessMemInfo():
    
    processes = psutil.process_iter()
    processes = sorted(processes, key=lambda process:process.memory_info().rss, reverse=True)

    allProcesses = ""
    for p in processes:
        try:
            line = '%d\t%s\t%dm' % (p.pid , p.name(), p.memory_info().rss / 1024 / 1024)
            allProcesses = allProcesses + line + "\n"
        except psutil.AccessDenied:
            continue
        except psutil.NoSuchProcess:
            continue
#     pids = psutil.pids()
#     for pid in pids:
#         p = psutil.Process(pid)
#         print str(p.pid) + "\t" + p.name() + "\t" + str(p.memory_info().rss / 1024 / 1024)
    return allProcesses

print getAllProcessMemInfo()
