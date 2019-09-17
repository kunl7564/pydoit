# -*- coding=utf-8 -*-
import datetime
from time import sleep

from lk.utils import file_utils
from lk.utils import web_api
from lk.utils.web_api import workdayType


def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return dates

if __name__ == '__main__':
    for date in dateRange('20190516', '20200101'):
        workdayType = web_api.workdayType(date)
        isWorkday = 1
        if workdayType == 0 or workdayType == 2:
            isWorkday = 1
        else :
            isWorkday = 0
            
        file_utils.write(r'd:\tmp\date_2019.csv', ('%s,%s,%s\n' % (date, workdayType, isWorkday)), True)
        sleep(1)
