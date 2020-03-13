from path import Path
import jieba
import jieba.analyse
import pandas as pd
import argparse
from  utils import  readlines,stopwordslist,writelines
parser = argparse.ArgumentParser(description="precess tree file to a doc")

parser.add_argument('--doc',default='./data/txt4.txt')
parser.add_argument('--seged_doc',default='./data/seged_doc_4.txt')
parser.add_argument('--graph_tab_csv',default='./data/graph_tab_4.csv')
parser.add_argument('--stop_words_file',default='./data/stopwords.txt')



args = parser.parse_args()
Level = {
'.1':1,
'.2':2,
'.3':3,
'.4':4,
'.5':5,
'.0':6
}
cnt = {'.0':0,
           '.1':0,
           '.2':0,
           '.3':0,
           '.4':0,}

def seg2words(args):
    stop_words_file = Path(args.stop_words_file)
    stopwords = stopwordslist(stop_words_file)


    doc = Path(args.doc)
    lines = readlines(doc)
    ret_lines = []
    for line in lines:
        if line=='':
            pass
        elif line[:2]=='.0':# 叶子节点， 描述性质的话
            words = jieba.lcut(line[2:])
            words_list=[]
            for word in words:
                if word not in stopwords:
                    if word != '\t':
                        words_list.append(word)
            words_list = post_precess_words(words_list)#去掉重复和其他无关字符
            for word in words_list:
                ret_lines.append(word)
        else:
            ret_lines.append(line)
    writelines(args.seged_doc,ret_lines)

def post_precess_words(words):
    ret = []
    for item in words:#去重去杂
        if item!='' and item not in ret and len(item)>1:
            ret.append('.0 '+item)
    return  ret
def jieba_process(str):
    words = jieba.lcut(str)
    return  words

def infer_graph_table(args):
    '''
    这里输入已经分词之后的doc, doc6有1700+ 行
    空行已经删除,
    :param args:
    :return:
    '''
    src_file = Path(args.seged_doc)
    if not src_file.exists():
        print('seged_doc file does not exist')
        return
    lines = readlines(src_file)






    i =0
    stack = ['none']  # record id
    id_list = []
    nodes_words = {}
    leaf_words = {}
    parents = {}
    id_word={}
    while i< len(lines):
        lv = get_level(lines[i])
        word = get_word(lines[i])

        if i==0:#第一个一定不是叶子
            id = lv+'.{:02d}'.format(cnt[lv])
            id_list.append(id)#rejister id
            parents[id] = []
            parents[id].append(stack[-1])
            nodes_words[word] = id
            id_word[id] = word
            stack.append(id)
            cnt[lv]+=1
        elif Level[lv] > Level[ get_level(stack[-1])]:
            #不是叶子
            if lv!='.0':
                id = lv + '.{:02d}'.format(cnt[lv])
                id_list.append(id)
                nodes_words[word] = id
                id_word[id] = word

                parents[id]= []
                parents[id].append(stack[-1])
                stack.append(id)
                cnt[lv]+=1#当前级别结点数量++
            else:#叶子结点, 且已经与词典里的词出现重复

                if word in leaf_words.keys() :
                    id = leaf_words[word]
                    parents[id].append(stack[-1])#叶子结点关键词重复, 增加父母结点
                else:#新叶子结点
                    id = lv + '.' + str(cnt[lv])  # id解算
                    id_list.append(id)
                    leaf_words[word]=id
                    id_word[id] = word

                    parents[id]=[]
                    parents[id].append(stack[-1])
                    #stack.append(id)
                    cnt[lv]+=1
        elif Level[lv] == Level[get_level(stack[-1])]:
            # 不是叶子
            if lv != '.0':

                id = lv + '.{:02d}'.format(cnt[lv])



                id_list.append(id)
                stack.pop()
                parents[id]=[]

                parents[id].append(stack[-1])
                stack.append(id)
                nodes_words[word] = id
                id_word[id] = word
                cnt[lv] += 1  # 当前级别结点数量++
            else:  # 叶子结点
                if word in leaf_words.keys():
                    id = leaf_words[word]
                    parents[id].append(stack[-1])  #
                else:  # 新叶子结点
                    id = lv + '.' + str(cnt[lv])  # id解算
                    id_list.append(id)
                    leaf_words[word] = id
                    id_word[id] = word

                    parents[word] = []
                    parents[id].append(stack[-1])
                    # stack.append(id)
                    cnt[lv] += 1
        elif Level[lv] < Level[get_level(stack[-1])]:#一定不是叶子结点
            id = lv + '.{:02d}'.format(cnt[lv])

            id_list.append(id)

            nodes_words[word] = id
            id_word[id] = word

            stack.pop()
            parents[id]=[]
            parents[id].append(stack[-1])
            stack.append(id)
            cnt[lv]+=1
        i+=1

    with open(args.graph_tab,'w',encoding='utf-8') as txt:
        for id in id_list:
            #if str(parent)[1:-1]=='':
             #   txt.writelines(id + '\t' + word + '\t' + 'none' + '\n')
            #else:
            if id[:2]=='.0':
                txt.writelines(id+'\t'+id_word[id]+'\t'+str(parents[id])[1:-1]+'\n')
            else:
                txt.writelines(id+'\t'+id_word[id]+'\t'+str(parents[id])[1:-1]+'\n')

def infer_graph_csv_table(args):
    '''
    这里输入已经分词之后的doc, doc6有1700+ 行
    空行已经删除,输出csv table, 此为图的最小完备信息描述
    :param args:
    :return:
    '''
    src_file = Path(args.seged_doc)
    lines = readlines(src_file)

    i =0
    stack = ['none']  # record id
    id_list = []
    id_nodes_words = {}
    id_leaf_words = {}
    id_parents = {}
    id_word={}
    while i< len(lines):
        lv = get_level(lines[i])
        word = get_word(lines[i])

        if i==0:#第一个一定不是叶子
            id = lv+'.{:02d}'.format(cnt[lv])
            id_list.append(id)#rejister id
            id_parents[id] = []
            id_parents[id].append(stack[-1])
            id_nodes_words[word] = id
            id_word[id] = word
            stack.append(id)
            cnt[lv]+=1
        elif Level[lv] > Level[ get_level(stack[-1])]:
            #不是叶子
            if lv!='.0':
                id = lv + '.{:02d}'.format(cnt[lv])
                id_list.append(id)
                id_nodes_words[word] = id
                id_word[id] = word

                id_parents[id]= []
                id_parents[id].append(stack[-1])
                stack.append(id)
                cnt[lv]+=1#当前级别结点数量++
            else:#叶子结点, 且已经与词典里的词出现重复

                if word in id_leaf_words.keys() :
                    id = id_leaf_words[word]
                    id_parents[id].append(stack[-1])#叶子结点关键词重复, 增加父母结点
                else:#新叶子结点
                    id = lv + '.' + str(cnt[lv])  # id解算
                    id_list.append(id)
                    id_leaf_words[word]=id
                    id_word[id] = word

                    id_parents[id]=[]
                    id_parents[id].append(stack[-1])
                    #stack.append(id)
                    cnt[lv]+=1
        elif Level[lv] == Level[get_level(stack[-1])]:
            # 不是叶子
            if lv != '.0':

                id = lv + '.{:02d}'.format(cnt[lv])
                id_list.append(id)
                stack.pop()
                id_parents[id]=[]

                id_parents[id].append(stack[-1])
                stack.append(id)
                id_nodes_words[word] = id
                id_word[id] = word
                cnt[lv] += 1  # 当前级别结点数量++
            else:  # 叶子结点
                if word in id_leaf_words.keys():
                    id = id_leaf_words[word]
                    id_parents[id].append(stack[-1])  #
                else:  # 新叶子结点
                    id = lv + '.' + str(cnt[lv])  # id解算
                    id_list.append(id)
                    id_leaf_words[word] = id
                    id_word[id] = word

                    id_parents[word] = []
                    id_parents[id].append(stack[-1])
                    # stack.append(id)
                    cnt[lv] += 1
        elif Level[lv] < Level[get_level(stack[-1])]:#一定不是叶子结点
            stack.pop()
            i-=1
#
        i+=1

    parents = [id_parents[id] for id in id_list]
    words = [id_word[id] for id in id_list]
    df = pd.DataFrame({'id':id_list,'word':words,'parents':parents})
    order = ['id','word','parents']
    df = df[order]
    df.to_csv(args.graph_tab_csv,index=False)



def get_level(str):
    return str[:2]
def get_word(str):
    return str[3:]

if __name__ == '__main__':
    seg2words(args)#格式化好的文本, 变成词序列
    infer_graph_csv_table(args)#词序列变成表格, generate graph_tab.txt
