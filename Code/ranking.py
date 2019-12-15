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


def plotrank(G, name, size=1):
    k_shell_result = na.k_shell(G)
    k_shell_result = return_node(k_shell_result)
    DC_core_result = na.DC_core(G)
    DC_core_result = return_node(DC_core_result)
    WKS_core_result = na.WKS_core(G, 0.7)
    WKS_core_result = return_node(WKS_core_result)
    MDD_core_result = na.MDD_core(G, 0.7)
    MDD_core_result = return_node(MDD_core_result)
    EWC_core_result = na.EWC_core(G)
    EWC_core_result = return_node(EWC_core_result)
        
    plt.scatter(k_shell_result[:,0],k_shell_result[:,1], marker='o',c='w', label='k-shell',edgecolors='k', s=size)
    plt.scatter(DC_core_result[:,0],DC_core_result[:,1], marker='v',c='w', label='DC', edgecolors='c', s=size)
    plt.scatter(WKS_core_result[:,0],WKS_core_result[:,1], marker='s',c='w', label='WKS', edgecolors='b', s=size)
    plt.scatter(MDD_core_result[:,0],MDD_core_result[:,1], marker='x',c='m', label='MDD', s=size)
    plt.scatter(EWC_core_result[:,0],EWC_core_result[:,1], marker='h',c='w', label='EWC', edgecolors='r', s=size)
    plt.title(name+" Ranking", fontdict=font)
    plt.xlabel('Nodes',fontdict=font)
    plt.ylabel('Ranking', fontdict=font)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.legend(fontsize=30)
    plt.show()
    


plotrank(karateG, 'Zachary', 150)
plotrank(dolphins, 'Dolphins',150)
plotrank(adjnoun, 'Adjacency', 150)
plotrank(power, 'Power Grid', 50)

# plt.subplot(111)
# nx.draw_spring(karateG, with_labels=True, node_size=500, node_color="white", edgecolors='k')
# plt.title('Zachary', fontsize=30)
# plt.show()
# plt.subplot(111)
# nx.draw_spring(dolphins, with_labels=True, node_size=500, node_color="white", edgecolors='k')
# plt.title('Dolphins', fontsize=30)
# plt.show()
# plt.subplot(111)
# nx.draw_spring(adjnoun, with_labels=True, node_size=500, node_color="white", edgecolors='k')
# plt.title('Adjacency', fontsize=30)
# plt.show()
# plt.subplot(111)
# nx.draw_spring(power, with_labels=False, node_size=30, node_color="white", edgecolors='k')
# plt.title('Power Grid', fontsize=30)
# plt.show()
