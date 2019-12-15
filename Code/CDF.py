import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import os
import networkx as nx
import NetworkAlgorithm as na
from networkx.algorithms import approximation as approx

karatepath = "./Data/karate/karate.gml"
powerpath = "./Data/power/power.gml"
dolphinspath = "./Data/dolphins/dolphins.gml"
adjnounpath = "./Data/adjnoun/adjnoun.gml"

karateG = nx.read_gml(karatepath, label=None)
dolphins = nx.read_gml(dolphinspath, label=None)
adjnoun = nx.read_gml(adjnounpath, label=None)
power = nx.read_gml(powerpath, label=None)

font={'family': 'Times New Roman','color': 'black','weight': 'normal', 'size': 40}

def return_node(corelist):
    node = []
    initialnum = corelist[-1,1]
    no = 1
    for i in range(len(corelist)):
        if corelist[-(i+1), 1] == initialnum:
            corelist[-(i+1), 1] = no
        else:
            initialnum = corelist[-(i+1), 1]
            no += 1
            corelist[-(i+1), 1] = no
    return corelist


def plotCDF(G, name):
    k_shell_result = na.k_shell(G)
    k_shell_result = return_node(k_shell_result)
    hist, edges = np.histogram(k_shell_result[:,1], bins=max(k_shell_result[:,1]))
    k_shell_cdf = np.cumsum(hist/sum(hist))
    k_shell_cdf = np.concatenate(([0], k_shell_cdf))

    DC_core_result = na.DC_core(G)
    DC_core_result = return_node(DC_core_result)
    hist, edges = np.histogram(DC_core_result[:,1], bins=int(max(DC_core_result[:,1])))
    DC_core_cdf = np.cumsum(hist/sum(hist))
    DC_core_cdf = np.concatenate(([0], DC_core_cdf))

    WKS_core_result = na.WKS_core(G, 0.5)
    WKS_core_result = return_node(WKS_core_result)
    hist, edges = np.histogram(WKS_core_result[:,1], bins=int(max(WKS_core_result[:,1])))
    WKS_core_cdf = np.cumsum(hist/sum(hist))
    WKS_core_cdf = np.concatenate(([0], WKS_core_cdf))

    MDD_core_result = na.MDD_core(G, 0.5)
    MDD_core_result = return_node(MDD_core_result)
    print(len(MDD_core_result))
    hist, edges = np.histogram(WKS_core_result[:,1], bins=int(max(MDD_core_result[:,1])))
    MDD_core_cdf = np.cumsum(hist/sum(hist))
    print(len(MDD_core_cdf))
    MDD_core_cdf = np.concatenate(([0], MDD_core_cdf))


    EWC_core_result = na.EWC_core(G)
    EWC_core_result = return_node(EWC_core_result)
    hist, edges = np.histogram(EWC_core_result[:,1], bins=int(max(EWC_core_result[:,1])))
    EWC_core_cdf = np.cumsum(hist/sum(hist))
    EWC_core_cdf = np.concatenate(([0], EWC_core_cdf))


    plt.plot(k_shell_cdf, marker='o',  label = "K-shell")
    plt.plot(DC_core_cdf, marker='v', label = "DC")
    plt.plot(WKS_core_cdf, marker='s', label = "WKS")
    plt.plot(MDD_core_cdf, marker='x', label = "MDD")
    plt.plot(EWC_core_cdf, marker='h', label = "EWC")
    plt.title(name+" CDF", fontdict=font)
    plt.xlabel('Ranking',fontdict=font)
    plt.ylabel('CDF', fontdict=font)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.legend(fontsize=30)
    plt.margins(0,0)
    plt.show()

plotCDF(karateG, "Zachary")
plotCDF(dolphins, "Dolphins")
plotCDF(adjnoun, "Adjacency")
plotCDF(power, "Power Grid")