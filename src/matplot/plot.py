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
from utils import file_utils as fu


# http://www.runoob.com/numpy/numpy-matplotlib.html
# https://blog.csdn.net/qq_34337272/article/details/79555544

def main():
# https://www.cnblogs.com/heitaoq/p/7994842.html read_csv
    dataframeOrg = pd.read_csv("F:\data\compare\dataset_0425\cleanerMin_heater\out\combined_26496.csv", header=None)
    print(len(dataframeOrg))
    currentOrg = dataframeOrg[0]
    voltageOrg = dataframeOrg[1]
    
    dataframeCombined = pd.read_csv("F:\data\compare\dataset_0425\heater_cleanerMin\out\combined_51968.csv", header=None)
    currentCombined = dataframeCombined[0]
    voltageCombined = dataframeCombined[1]
    
#     dataframeDisaggregate = pd.read_csv("C:\Users\kunl\Desktop\data\data_banbo\out\disaggregate_98944.csv", header=None)
    dataframeDisaggregate = pd.read_csv("F:\data\compare\dataset_0425\heater_cleanerMin\out\disaggregate_34432.csv", header=None)
    currentDisaggregate = dataframeDisaggregate[0]
    voltageDisaggregate = dataframeDisaggregate[1]
    
    delta = currentOrg - currentDisaggregate
    
    euclideanD = np.sqrt(np.sum(np.square(currentOrg - currentDisaggregate)))
#     euclideanD = np.linalg.norm(currentOrg - currentDisaggregate)
    pearsonr = stats.pearsonr(currentOrg , currentDisaggregate)
    cosineS = cosine_similarity(currentOrg, currentDisaggregate)
    
    mean = np.mean(currentDisaggregate)
    variance = np.var(currentDisaggregate)
    std = np.std(currentDisaggregate)
    dt = np.sqrt(np.dot(currentOrg, currentDisaggregate))
    ln = np.linalg.norm(currentOrg)
    md = np.max(delta)  # max delta
    
    delta_sum = 0
    for i in range(len(delta)):
        delta_sum += abs(delta[i])
    ab = delta_sum / len(delta)  # average bias
    
    abscissa = np.linspace(1, 384, 384, endpoint=True, dtype=int)

#     dpi默认是100,尺寸是乘以100后的
#     fig = plt.figure(facecolor='white', figsize=(19.2, 10.8))
    
#     fig3d = plt.figure(facecolor='white', figsize=(19.2, 10.8))
#     ax3d = Axes3D(fig3d)
#     ax3d.plot(abscissa, currentOrg, 'b:.')
#     plt.show(fig3d)

    plt.subplot(2, 2, 1)
    plt.title("combined", fontsize=12)
    plt.plot(abscissa, currentCombined, 'k:.')

    plt.subplot(2, 2, 2)
    plt.title(u"vol", fontproperties='SimHei', fontsize=12)
    plt.plot(abscissa, voltageDisaggregate, 'g.')

    plt.subplot(2, 2, 3)
    plt.plot(abscissa, currentOrg, 'b:.', label='true')
    plt.title("estimated", fontsize=12)

    text = "sim = %.3f\nmn = %.3f\nvr = %.3f\nsd = %.3f\ndt = %.3f\nln = %.3f\nmd = %.3f\nab = %.3f" \
        % (cosineS[0][0], mean, variance, std, dt, ln, md, ab)
    plt.text(500, np.min(currentDisaggregate), text , fontsize=13)
    plt.plot(abscissa, currentDisaggregate, 'r:.', label='estimated')
    plt.suptitle("Generated at %s" % (time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))))

    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
