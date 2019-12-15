# -*- coding: UTF-8 -*- 

# @brief This is core algorithm code based on EE6603 CityU.
# @author YANG Liang
# @version v1.0
# @data 19/11/2019

import numpy as np
import sys
import random
import matplotlib.pyplot as plt
import os
import networkx as nx
import copy

# add attribute "edge weight"
# edge weight: w(i,j) = k(i) + k(j)
def G_add_edgeweight(G):
    for i in G.edges:
        sum = G.degree(i[0])+G.degree(i[1])
        G.add_edge(i[0],i[1], edgeweight = sum)


# add attribute "node weight"
# node weight: S(i) = sum(w(i,j))  j is the neighbors
def G_add_nodeweight(G):
    for node in G.nodes:
        nodeweightsum = 0
        for neighor in G.neighbors(node):
            nodeweightsum += G.edges[node, neighor]['edgeweight']
        G.add_node(node, nodeweight = nodeweightsum)


# calculate entropy
def entropy(datax, isNormalization=True):
    datax = np.array(datax)
    if isNormalization:
        k = 1/np.log(len(datax))
        e = -k*np.sum(datax*np.log(datax))
        return e
    elif not isNormalization:
        datax = datax/np.sum(datax)
        k = 1/np.log(len(datax))
        e = -k*np.sum(datax*np.log(datax))
        return e



# return core-n nodes
def return_core_node(corelist, core):
    node = []
    for i in range(len(corelist)):
        if corelist[i, 1] == core:
            node.append(corelist[i,0])
    return node


# return n-order vital nodes and max order
def return_order_node(corelist, order):
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
    for i in range(len(corelist)):
        if corelist[i, 1] == order:
            node.append(corelist[i,0])
    return node, no

# Find vital nodes by K-Shell 
def k_shell(G):
    core = nx.algorithms.core.core_number(G)
    core = [[i,core[i]] for i in core]
    core.sort(key=lambda x:x[1],reverse=False)
    return np.array(core)


# Find vital nodes by Degree Centrality
def DC_core(G):
    degree_centrality = nx.algorithms.centrality.degree_centrality(G)
    degree_centrality = [[i,degree_centrality[i]] for i in degree_centrality]
    degree_centrality.sort(key=lambda x:x[1],reverse=False)
    return np.array(degree_centrality)

# Weighted k-shell
# alpha a positive tuning parameter (0-1)
def WKS_core(G, alpha):
    G_add_edgeweight(G)
    G_add_nodeweight(G)
    WKS = []
    for no in G.nodes:
        nodedegree = G.degree[no]
        nodeweight = G.nodes[no]['nodeweight']
        influratio = alpha*nodedegree + (1-alpha)*nodeweight
        WKS.append([no, influratio])
    WKS.sort(key=lambda x:x[1],reverse=False)
    return np.array(WKS)


# Mixed degree distribution
def MDD_core(G, alpha):
    tG = copy.deepcopy(G)
    firstshellvalue = k_shell(tG)
    for i in tG.nodes:
        tG.add_node(firstshellvalue[i-1][0], k_shell = firstshellvalue[i-1][1])
    tempG = copy.deepcopy(tG)
    while len(tempG.nodes) > 1:
        shellvalue = tempG.nodes.data('k_shell')
        shellvalue = [i[1] for i in shellvalue]
        minshell = min(shellvalue)
        # remove minimal shell value node
        tempnodes = copy.deepcopy(tempG.nodes)
        for no in tempnodes:
            if tempG.nodes[no]['k_shell'] == minshell:
                tempG.remove_node(no)
        # update shell value
        for no in tempG.nodes:
            rsdegree = tempG.degree[no]
            exdegree = tG.degree[no] - rsdegree
            newshell = rsdegree+alpha*exdegree
            tempG.nodes[no]['k_shell'] = newshell
            tG.nodes[no]['k_shell'] = newshell
    newshell = tG.nodes.data('k_shell')
    newshell = [[i[0], i[1]] for i in newshell]
    newshell.sort(key=lambda x:x[1],reverse=False)
    # newshell = [[i[0],i[1]] for i in newshell]
    return np.array(newshell)


# entropy weight algorithm
def EWC_core(G):
    # degree entropy
    degree = G.degree
    degree = [i[1] for i in degree]
    degree_entropy = entropy(degree, isNormalization=False)
    degree_info = 1-degree_entropy   

    # node entropy
    node_w = G.nodes.data('nodeweight')
    node_w = [i[1] for i in node_w]
    node_w_entropy = entropy(node_w, isNormalization=False)
    node_w_info = 1- node_w_entropy

    # coreness entropy
    core = nx.algorithms.core.core_number(G)
    core = [core[i] for i in core]
    max_core = max(core)
    core_dist = []
    for i in range(max(core)):
        core_dist.append(core.count(i+1)/len(core))
    core_entropy = entropy(core_dist, isNormalization=True)
    core_info = 1-core_entropy

    # weight calculate
    info = [degree_info, node_w_info, core_info]
    w_degree = degree_info / sum(info)
    w_nodeweight = node_w_info / sum(info)
    w_core = core_info / sum(info)

    # calculate vital information
    DWC_core = []
    core = nx.algorithms.core.core_number(G)
    for node in G.nodes:
        wks = w_degree*G.degree(node) + \
            w_nodeweight* G.nodes[node]['nodeweight'] + \
            w_core*core[node]
        DWC_core.append([node, wks])
    DWC_core.sort(key = lambda x:x[:][1], reverse=False)
    return np.array(DWC_core)

