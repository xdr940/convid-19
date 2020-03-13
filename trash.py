
def main(args):
    '''
        read txt文件
    :param args:
    :return:
    '''
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


def write_dict_tab(tab):
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


def set_draw_thr(df):
    draw = []
    for idx,row in df.iterrows():
        if row['id'][:2]!='.0':
            draw.append(1)
        else:
            if len(row['parents'])>draw_th:
                draw.append(1)
            else:
                draw.append(0)
    df['draw'] = draw
def set_draw_leaf(df):
    '''
        不画叶子
    :param df:
    :return:
    '''

    draw =[]
    for idx, row in df.iterrows():
        if row['id'][:2] != '.0':
            draw.append(1)
        else:
            draw.append(0)
    df['draw'] = draw

def put_nodes_edge_df(df):

    for idx,row in df.iterrows():
        if row['draw']==1:
            G.add_node(row['id'])
    for idx,row in df.iterrows():
        for parent in row['parents']:
            if (parent!='none') and (parent in df['id'].values) and row['draw']==1:
                G.add_edge(parent,row['id'])


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

