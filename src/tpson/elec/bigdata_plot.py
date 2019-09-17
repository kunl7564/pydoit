# coding=utf-8
from Cython.Compiler.Options import annotate
__author__ = "Liang Kun"
__copyright__ = "Tpson 2018"
__version__ = "2.0.0"
__license__ = "tpson"

import os
import json
import time
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
from mpl_toolkits.mplot3d import Axes3D
from lk.utils import file_utils as fu
import itertools

# http://www.runoob.com/numpy/numpy-matplotlib.html
# https://blog.csdn.net/qq_34337272/article/details/79555544
def main():
# https://www.cnblogs.com/heitaoq/p/7994842.html read_csv
# House 21
# 0.Aggregate,
# 1.Fridge-Freezer, Samsung, SR-L3216B
# 2.Tumble Dryer, Unknown, Unknown
# 3.Washing Machine, Beko, WMB81241LW
# 4.Dishwasher, AEG, FAVORIT
# 5.Food Mixer, Unknown, Unknown
# 6.Television, Unknown, Unknown
# 7.Kettle, Unknown, Unknown, (Changes 16 Aug 2014)
# 8.Vivarium, Unknown, Unknown
# 9.Pond Pump, Unknown, Unknown
    elec_data = pd.read_csv('F:\data\elec_bigdata\CLEAN_REFIT_081116\CLEAN_House21_lk.csv', header=0, nrows=200000)
    print(len(elec_data))
    data_len = len(elec_data)
    x_axis = elec_data['Unix'] - elec_data['Unix'][0]
#     x_axis = np.linspace(1, data_len, data_len, endpoint=True, dtype=int)
    colors = itertools.cycle(["r", "g", "b", "c", "m", "y", "k", "w"])

    aggregate = elec_data['Aggregate']
    plt.subplot(2, 1, 1)
    plt.title("Aggregate", fontsize=12)
    plt.plot(x_axis, aggregate, color=next(colors), linestyle='-')
 
    plt.subplot(2, 1, 2)
#     Appliance1 = elec_data['Appliance1']
#     plt.title("Appliance1", fontsize=12)
#     plt.plot(x_axis, Appliance1, color=next(colors))

    Appliance2 = elec_data['Appliance2']
    plt.title("Appliance2", fontsize=12)
    plt.plot(x_axis, Appliance2, color=next(colors))
    
#     Appliance3 = elec_data['Appliance3']
#     plt.title("Appliance3", fontsize=12)
#     plt.plot(x_axis, Appliance3, color=next(colors))
#     
#     Appliance4 = elec_data['Appliance4']
#     plt.title("Appliance4", fontsize=12)
#     plt.plot(x_axis, Appliance4, color=next(colors))
#     
#     Appliance5 = elec_data['Appliance5']
#     plt.title("Appliance5", fontsize=12)
#     plt.plot(x_axis, Appliance5, color=next(colors))
#     
#     Appliance6 = elec_data['Appliance6']
#     plt.title("Appliance6", fontsize=12)
#     plt.plot(x_axis, Appliance6, color=next(colors))
#     
#     Appliance7 = elec_data['Appliance7']
#     plt.title("Appliance7", fontsize=12)
#     plt.plot(x_axis, Appliance7, color=next(colors))
#     
#     Appliance8 = elec_data['Appliance8']
#     plt.title("Appliance8", fontsize=12)
#     plt.plot(x_axis, Appliance8, color=next(colors))
#     
#     Appliance9 = elec_data['Appliance9']
#     plt.title("Appliance9", fontsize=12)
#     plt.plot(x_axis, Appliance9, color=next(colors))
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
