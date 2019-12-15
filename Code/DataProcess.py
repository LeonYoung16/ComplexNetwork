# -*- coding: UTF-8 -*- 

# @brief This is a program  based on EE6603 CityU.
# @author YANG Liang
# @version v1.0
# @data 19/11/2019

import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import os
import networkx as nx
import NetworkAlgorithm as na

karatepath = "./Data/karate/karate.gml"
internetpath = "./Data/Internet/Internet.gml"
dolphins = "./Data/dolphins/dolphins.gml"

karateG = nx.read_gml(karatepath, label=None)
na.G_add_edgeweight(karateG)
na.G_add_nodeweight(karateG)
# for i in karateG.nodes:
#     print(i)
#     print(karateG.nodes['nodeweight'])
nodeweight = list(karateG.nodes.data('nodeweight'))
nodeweight = [i[1] for i in nodeweight]

entropy = na.entropy(nodeweight, isNormalization=False)
print("node entropy:", entropy)

edgeweight = list(karateG.edges.data('edgeweight'))
edgeweight = [i[2] for i in edgeweight]
entropy = na.entropy(edgeweight, isNormalization=False)
print("edge entropy:", entropy)

k_g = nx.algorithms.core.k_shell(karateG)
k_g = nx.algorithms.core.core_number(k_g)
print(k_g)
# print(k_g.nodes.data())
cc = nx.algorithms.cluster.clustering(karateG)
# print(type(cc))

cc = [cc[i] for i in cc]
cc = np.exp(cc)
cc_entropy = na.entropy(cc, isNormalization=False)
print("clustring entropy:",cc_entropy)


# degree_center = nx.algorithms.centrality.degree_centrality(karateG)
# degree_center = [degree_center[i] for i in degree_center]
# print(degree_center)
# print(sum(degree_center))

degree_center = karateG.degree
degree_center = [i[1] for i in degree_center]
entropy = na.entropy(degree_center, isNormalization=False)
print("degree entropy:", entropy)

# betweenness = nx.algorithms.centrality.betweenness_centrality(karateG)
# betweenness = [betweenness[i] for i in betweenness]
# betweenness = np.exp(betweenness)
# entropy = na.entropy(betweenness, isNormalization=False)
# print("betweenness entropy:", entropy)


# clossness = nx.algorithms.centrality.closeness_centrality(karateG)
# clossness = [clossness[i] for i in clossness]
# entropy = na.entropy(clossness, isNormalization=False)
# print("clossness entropy:", entropy)

core = nx.algorithms.core.core_number(karateG)
core = [core[i] for i in core]
print(core)
entropy = na.entropy(core, isNormalization=False)
print("core entropy:", entropy)
# na.G_edgeweight(karateG)
# for i in karateG.edges:
# #     print(karateG.edges[i[0], i[1]]['edgeweight'])
plt.subplot(121)
nx.draw_shell(karateG, with_labels=True, node_size=500, node_color="white", alpha=0.5)
# plt.subplot(122)
# nx.draw_shell(k_g, with_labels=True)
plt.show()
avercc = nx.algorithms.approximation.clustering_coefficient.average_clustering(karateG)
print(avercc)