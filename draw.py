import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import numpy as np
from  path import Path
import pydot
import matplotlib as mpl
import pandas_profiling
from networkx.drawing.nx_pydot import graphviz_layout
from utils import  readlines,value,read_as_list,parents_format,merge_list,merge_list2,normalize,recolor
parser = argparse.ArgumentParser(description="precess tree file to a doc")
parser.add_argument('--graph_tab_csv',default='./data/graph_tab_2.csv')
parser.add_argument('--graph_tab_sta',default='./data/graph_tab_sta_4.csv')

draw_th=1

G = nx.MultiDiGraph()
args = parser.parse_args()

vec_class=['.1','.2','.3','.4','.5','.0']
level_color = {
    '.1': 1.0,
    '.2':0.8,
    '.3':0.6,
    '.4':0.4,
    '.0': 0.0}
id_draw = {}

def main():
    #pandas_report(args)
    # csv_G_csv(args)
    draw_graph_csv(args)


def Draw_2(G, df):
    '''

    :param G:
    :param df:
    :return:
    '''
    # doc6         病原学特点, 流行病学特点,诊断标准
    # key_nodes = ['.1.00','.1.01',  '.1.03', '.1.07']
    # key_nodes=['.1.00','.1.01','.1.03','.1.07','.1.08']
    # key_nodes=['.1.00','.1.01','.1.02','.1.03','.1.04','.1.05','.1.06','.1.07','.1.09','.1.10','.1.11']

    key_nodes = ['.1.00']
    if len(key_nodes) != 0:
        nodes = []
        for item in key_nodes:
            nodes.append(get_children(item))
        all_nodes = merge_list(nodes) + key_nodes
        del (nodes)

        # all_nodes = merge_list2(nodes[0],nodes[1])

        # (all_nodes)
        print(len(all_nodes))
        sub_g = G.subgraph(all_nodes)
        G = nx.MultiDiGraph(sub_g)
    else:
        pass

    in_deg = [item for item in G.in_degree]
    in_deg = dict(in_deg)
    out_deg = [item for item in G.out_degree]
    out_deg = dict(out_deg)

    # REMOVE NODES
    Gnodes = list(G.nodes)  # deep copy
    for node in Gnodes:
        if node[:2] == '.0' and in_deg[node] < draw_th:
            G.remove_node(node)
    print('AFTER REMOVE')
    print(len(G.nodes))
    print(len(G.edges))

    # define key edges
    key_edges = []
    for (o, i, j) in G.edges:
        if is_leaf(i) == False:  # 如果边的入结点不是叶子, 那边就是干
            key_edges.append((o, i, j))

    # with labels
    labels = {}
    for node in G.nodes:
        labels[node] = node  # df['id'].at(node)
    # 1. node color size
    node_color = []
    node_size = []
    for node in G.nodes():
        ns = in_deg[node]
        node_size.append(ns)
        c = cnt_sub_nodes(node)
        node_color.append(c)
    node_size = np.array(node_size) * 200 + 200
    node_color = np.array(node_color)

    # edge color size
    edge_width = []
    edge_color = []
    for (x, y, i) in G.edges:
        c = cnt_sub_nodes(y)
        edge_width.append(c)
        if is_leaf(y):
            edge_color.append('lightskyblue')
        else:
            edge_color.append('red')

    edge_width = np.array(edge_width)

    min = edge_width.min()
    max = edge_width.max()
    if min!=max:
        edge_width = (edge_width - min) / (max - min)
    else:
        pass
    edge_width = 2 * edge_width + 1

    if len(key_nodes) == 1:
        edge_width = 1
    # draw
    # pos = nx.spring_layout(G)
    pos = graphviz_layout(G, prog='sfdp')
    # pos = nx.spectral_layout(sub_g)
    # print(edge_width)
    # print(edge_color)
    # print(node_color)
    # print(node_size)
    nx.draw(G, pos,
            cmap=plt.get_cmap('Wistia'),
            node_color=node_color,  # same size with nodes
            node_size=node_size,
            # edge
            edge_color=edge_color,
            # edge_cmap=plt.get_cmap('Blues'),
            width=edge_width,
            # label_color='white',
            # labels = labels,
            with_labels=True)
    plt.axis('off')
    plt.show()


def get_children(node):
    children = []
    def get_(node):
        if node not in children:
            children.append(node)
        for item in G.successors(node):
            if item ==[]:
                return
            else:
                get_(item)
    get_(node)
    children.remove(node)
    return children
def cnt_sub_nodes(node):
    sub_nodes =[]

    for item in G.successors(node):
        sub_nodes.append(item)

    if sub_nodes ==[]:
        return 0
    else:
        cnt=len(sub_nodes)
        for node in sub_nodes:
            cnt+=cnt_sub_nodes(node)
        return cnt


def put_all_G(df):
    '''
        没有条件, 所有点边全部加上去
    :param df:
    :return:
    '''

    for idx,row in df.iterrows():
        G.add_node(row['id'],message= row['word'])
    print('put g nodes '+str(len(G.nodes())))
    for idx,row in df.iterrows():
        for parent in row['parents'] :
            if parent!='none':
                G.add_edge(parent,row['id'])
    print('put g edges '+str(len(G.edges())))

def read_graph(args):
    df = pd.read_csv(args.graph_tab_csv)

    # parents
    df['parents'] = parents_format(df['parents'])
    return df

def csv_G_csv(args):
    '''
        丰富df文件信息
    :param df:
    :return:
    '''
    df = read_graph(args)

    put_all_G(df)
    # succesors, pres(order), ,indeg,outdeg

#
    in_degree = {}
    out_degree = {}
    for id, in_d, out_d in zip(list(G.nodes), list(G.in_degree), list(G.out_degree)):
        in_degree[id] = in_d
        out_degree[id] = out_d
    in_deg = []
    out_deg = []
    for idx, row in df.iterrows():
        in_deg.append(in_degree[row['id']][1])
        out_deg.append(out_degree[row['id']][1])
    df['in_deg'] = in_deg
    df['out_deg'] = out_deg


# cnt_

    succesors = []

    for idx,row in df.iterrows():
        succesors.append(cnt_sub_nodes(row['id']))
    df['succ'] = succesors


    df[['id','word','in_deg','out_deg','succ']].to_csv(args.graph_tab_sta,index=False)



def draw_graph_csv(args):
    df = read_graph(args)

    put_all_G(df)

    nums_sub = []

    for id in df['id']:
        nums_sub.append(cnt_sub_nodes(id))

    df['nums_sub_nodes'] = nums_sub

    draw = []
    for idx, row in df.iterrows():
        if row['id'][:2] != '.0':
            draw.append(1)
        else:
            if len(row['parents']) > draw_th:
                draw.append(1)
            else:
                draw.append(0)
    df['draw'] = draw
    del(draw)



#write deg to df
    in_degree={}
    out_degree={}
    for id, in_d, out_d in zip(list(G.nodes), list(G.in_degree), list(G.out_degree)):
        in_degree[id] = in_d
        out_degree[id] = out_d
    in_deg = []
    out_deg =[]
    for idx,row in df.iterrows():
        in_deg.append(in_degree[row['id']][1])
        out_deg.append( out_degree[row['id']][1])

#    df['in_deg'] = in_deg
#    df['out_deg'] = out_deg

    #del(in_degree)
    del(out_degree)
    del(in_deg)
   # del(out_deg)


    #格式化parents,str 2  listoflist
# draw
    leaves=[]
    nodes=[]
    for n,d in G.nodes(data=True):
        if is_leaf(n)==True:
            leaves.append(n)
        else:
            nodes.append(n)

    #Draw(G_leaf)
    Draw_2(G,df)
    #G_node = G.subgraph(nodes)


def pandas_report(args):
    df = pd.read_csv(args.graph_tab_sta)
    pfr = pandas_profiling.ProfileReport(df)
    pfr.to_file('./data/report.html')


def Draw_1(G,df):
    '''

    :param G:
    :param df:
    :return:
    '''
    plt.style.use('dark_background')

    #key_nodes=['.1.01','.1.00','.1.03','.1.05']
    #key_nodes=['.1.01','.1.00','.1.03','.1.05']# doc6 病原学特点, 流行病学特点,诊断标准
    #key_nodes=['.1.01','.1.00']

    nodes=[]
    for item in key_nodes:
        nodes.append(get_children(item))
    all_nodes = merge_list(nodes) + key_nodes
    del(nodes)


    #all_nodes = merge_list2(nodes[0],nodes[1])

    #(all_nodes)
    sub_g = G.subgraph(all_nodes)
    sub_g = nx.MultiDiGraph(sub_g)

    in_deg = [item for item in sub_g.in_degree]
    in_deg = dict(in_deg)

    out_deg = [item for item in sub_g.out_degree]
    out_deg=dict(out_deg)

    nodes=list(sub_g.nodes())
    for node in nodes:
        if node[:2] == '.0' and in_deg[node] < 2:
            sub_g.remove_node(node)
    print('sub graph')
    print(len(sub_g.nodes))
    print(len(sub_g.edges))

# define key edges
    key_edges = []
    for (o, i, j) in sub_g.edges:
        if is_leaf(i) == False:  # 如果边的入结点不是叶子, 那边就是干
            key_edges.append((o, i, j))
    print(key_edges)


#with labels

    labels = {}
    for node in sub_g.nodes:
        labels[node] =node# df['id'].at(node)
#1. node color
    node_color = []
    for node in sub_g.nodes:
        node_color.append(in_deg[node])
#        if is_leaf(node) == False:
#            node_color.append('red')
#            with_labels.append(True)
#        else:
#            node_color.append('yellow')
#            with_labels.append(False)
#2. node size
    base_size = 350
    k = 200
    node_size = []
    for item in sub_g.nodes:
#        if is_leaf(item) ==True:
        node_size.append(cnt_sub_nodes(item))
#            node_size.append(base_size)
        node_size = normalize(node_size)
#edge color, width

   # for edge in sub_g.edges:
   #     if edge in key_edges:
   #         edge_width.append(4)
   #         edge_color.append('blue')

   #     else:
   #         edge_width.append(0.5)
   #         edge_color.append('gray')

    edge_width = []
    edge_color = []
    base_width = 1
    base_edge_color = 1
    for (x,y,i) in sub_g.edges:
        c = cnt_sub_nodes(y)
        edge_width.append(c)
        if is_leaf(y):
            edge_color.append('lightskyblue')
        else:
            edge_color.append('deepskyblue')
        #edge_width.append(c*base_width+base_width)
#edge_width
    #edge_color = recolor(edge_color)


    pos = graphviz_layout(sub_g, prog='fdp')
    #pos = nx.spectral_layout(sub_g)
    nx.draw(sub_g, pos,
            cmap=plt.get_cmap('Wistia'),
            node_color=node_color,  # same size with nodes
            node_size=node_size,
            #edge
            edge_color=edge_color,
                 #edge_cmap=plt.get_cmap('Blues'),
            width=edge_width)
            #label_color='white',
            #labels = labels,
            #with_labels=True)
    plt.axis('off')
    plt.show()





def id2row(df,id):
    return df[df['id'].isin([id])]
def is_leaf(node):
    if node[:2]=='.0':
        return True
    else:
        return False


if  __name__ == '__main__':
   main()
