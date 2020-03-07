import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from  path import Path
from utils import  readlines,value,read_as_list
parser = argparse.ArgumentParser(description="precess tree file to a doc")
parser.add_argument('--node_file',default='./array.txt',help='output an txt to descripe file_in')
parser.add_argument('--edge-file',default='./seqsubseq.txt')
parser.add_argument('--graph_tab',default='graph_tab.txt')
parser.add_argument('--leaf_dict',default='./leaf_dict.txt')
parser.add_argument('--node_dict',default='./node_dict.txt')


draw_th=3
args = parser.parse_args()
G = nx.DiGraph()
pos = nx.circular_layout(G)  # positions for all nodes
vec_class=['.1','.2','.3','.4','.5','.0']
level_color = {
    '.1': 1.0,
    '.2':0.8,
    '.3':0.6,
    '.4':0.4,
    '.0': 0.0}
id_draw = {}


def put_nodes(tab):
    for item in tab:
        if id_draw[item[0]]==1:
            G.add_node(item[0])
def put_edges(tab):
    tem=0
    for item in tab:

        for parent in item[2]:
            if (parent!='none') and (parent in id_draw.keys()) and (id_draw[item[0]]==1):
                G.add_edge(parent,item[0])
                tem+=1
    print('multi edges '+str(tem))

def get_level(str):
    return str[:2]

def draw_graph2(args):
    lines = readlines(Path(args.graph_tab))
    tab = []
    id_list = []
    word_list = []
    freq_list = []
    for line in lines:

        #id_parents
        id_word_parent_draw=line.split('\t')
        id_word_parent_draw[2] = id_word_parent_draw[2].replace('\'','').replace(' ','').split(',')
        id = id_word_parent_draw[0]

        id_list.append(id)
        word_list.append(id_word_parent_draw[1])
        freq_list.append(len(id_word_parent_draw[2]))

        if id_word_parent_draw[0][:2]!='.0':
            id_draw[id_word_parent_draw[0]]=1
        else:
            if len(id_word_parent_draw[2])>draw_th:
                id_draw[id_word_parent_draw[0]] = 1

            else:
                id_draw[id_word_parent_draw[0]] = 0



        tab.append(id_word_parent_draw.copy())
    del(lines)
    put_nodes(tab)
    put_edges(tab)
    print('nodes '+str(len(G.nodes)))
    print('edges '+str(len(G.edges)))



#根据出入度决定结点大小
    deg = []
    for in_d, out_d in zip(list(G.in_degree), list(G.out_degree)):
        deg.append([in_d[1], out_d[1]])
    node_size = []
    base_size = 30
    for item in deg:
        if item[0] == 0:  # 入度为0, 根节点
            node_size.append(base_size)
        elif item[0] == 1 and item[1] != 0:  # 入度为1,出度不为0, 中间节点
            node_size.append(base_size)
        elif item[0] != 0 and item[1] == 0:#入度不同, 出度为0
            node_size.append(item[0] * 100 + base_size)
    print('node size '+str(len(node_size)))

#叶子颜色
    indeg_color = np.linspace(start=0.99, stop=0., num=100)
    colors = []
    for item in deg:
        #c = level_color[get_level(node)]
        c = indeg_color[item[0]]
        colors.append(c)

    pos = nx.spring_layout(G)
    nx.draw(G, pos,
            cmap=plt.get_cmap('autumn'),
            node_color=colors,  # same size with nodes
            node_size=node_size,
            edge_color='gray',
            with_labels=True)

    plt.axis('off')
    plt.show()

    #txt write
    nodes = []
    for item in tab:
        if item[0][:2]!='.0':
            nodes.append(item.copy())
    node_dict = sorted(nodes, key=lambda x: x[0])

    leaf_dict =  sorted( tab,reverse=True,key=lambda x:len(x[2]))

    with open(args.leaf_dict,'w',encoding='utf-8') as txt:
        for item in leaf_dict:
            txt.write(str(item[0])+','+str(item[1])+','+str(len(item[2]))+'\n')
    with open(args.node_dict,'w',encoding='utf-8') as txt:
        for item in node_dict:
            txt.write(str(item[0])+','+str(item[1])+'\n')
    return

def str2list(str):
    ret = str.split(',')
    print(ret)


def draw_bar(args):
    pass
if  __name__ == '__main__':

    draw_graph2(args)
