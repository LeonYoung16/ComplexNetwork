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

# def calmono(l):
#     l = l.tolist()
#     b = set(l)
#     s = 0
#     print(l)
#     for i in b:
#         if l.count(i) == 1:
#             s += 0
#         else:
#             s += l.count(i)
#     n = len(l)
#     nr = s
#     print(n)
#     print(nr)
#     mr = (1-nr*(nr-1)/(n*(n-1)))**2
#     return mr


# calculate monotonicity
def calmono(l):
    l = l.tolist()
    b = set(l)
    s = 0
    for i in b:
#         if l.count(i) == 1:
#             s += 0
#         else:
#             s += 1
        s += l.count(i)*(l.count(i)-1)
    n = len(l)
    nr = s
    # print(nr)
    # print(n)
    mr = (1-nr/(n*(n-1)))**2
    return mr


def printmono(G):
    k_shell_result = na.k_shell(G)
    # k_shell_result = return_node(k_shell_result)
    k_shell_rank = k_shell_result[:,1]
    k_shell_mono = calmono(k_shell_rank)

    DC_core_result = na.DC_core(G)
    # DC_core_result = return_node(DC_core_result)
    DC_core_rank = DC_core_result[:,1]
    DC_mono = calmono(DC_core_rank)

    WKS_core_result = na.WKS_core(G, 0.5)
    # WKS_core_result = return_node(WKS_core_result)
    WKS_core_result = WKS_core_result[:,1]
    WKS_mono = calmono(WKS_core_result)

    MDD_core_result = na.MDD_core(G, 0.5)
    # MDD_core_result = return_node(MDD_core_result)
    MDD_core_result = MDD_core_result[:,1]
    MDD_mono = calmono(MDD_core_result)

    EWC_core_result = na.EWC_core(G)
    # EWC_core_result = return_node(EWC_core_result)
    EWC_core_result = EWC_core_result[:,1]
    EWC_mono = calmono(EWC_core_result)

    print("k_shell mono:", k_shell_mono)
    print("DC mono:", DC_mono)
    print("WKS mono:", WKS_mono)
    print("MDD mono:", MDD_mono)
    print("EWC mono:", EWC_mono)


print("karateG")
printmono(karateG)
print(end='\n\n\n')
print("dolphins")
printmono(dolphins)
print(end='\n\n\n')
print("adjnoun")
printmono(adjnoun)
print(end='\n\n\n')
print("power")
printmono(power)