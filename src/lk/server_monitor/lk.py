# coding=utf-8
from time import sleep
import sys

from CpuMonitor import CpuMonitorThread
from MemMonitor import MemMonitorThread


if __name__ == '__main__':
    server = "testserver"
    if len(sys.argv) > 1:
        server = sys.argv[1]
    cpuThread = CpuMonitorThread(server, 85, 10)
    cpuThread.start()
    memThread = MemMonitorThread(server, 1300, 1)
    memThread.start()
    sleep(1)
