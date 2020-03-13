
from path import Path
import argparse
parser = argparse.ArgumentParser(description="precess tree file to a doc")
parser.add_argument('--file_in', default='./doc6.txt', help="Input file")
parser.add_argument('--file_out',default='./array.txt',help='output an txt to descripe file_in')
args = parser.parse_args()
template = [ '.1', '.2', '.3', '.4','.0', '']  # 树最大深度为4, 0为叶子
value={'.1':1,
         '.2':2,
         '.3':3,
         '.4':4,
         '.0':5,
         '':6}
def writelines(filename,arr):
    with open(filename,'w',encoding='UTF-8') as txt:
        txt.write(str(arr[0] ))
        for item in arr[1:]:
            txt.write('\n'+str(item))

def writelist(filename,arr):
    with open(filename,'w') as txt:
        txt.write(str(arr[0] )[1:-1])
        for item in arr[1:]:
            txt.write('\n'+str(item)[1:-1])
def readlines(filename):
    """Read all the lines in a text file and return as a list
    """
    if not filename.exists():
        return
    with open(filename, 'r', encoding='UTF-8' ) as txt:
        lines = txt.read().splitlines()
        for i in range( len(lines)):
            lines[i] = lines[i].strip(' ')


    return lines
def read_as_list(file_name):
    if not file_name.exists():
        return
    ret_list=[]
    with open(file_name,'r',encoding='UTF-8') as txt:
        lines = txt.read().splitlines()
        for i in range(len(lines)):
            line=[]
            if lines[i][0]=='[' and lines[i][-1]==']':
                for item in  lines[i][1:-1].split(','):
                    line.append(int(item))
                ret_list.append(line.copy())
            else:
                for item in  lines[i].split(','):
                    line.append(int(item))
                ret_list.append(line.copy())
    return  ret_list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
def toarry(file_in,file_out):
    file = Path(file_in)
    lines = readlines(file)

    array =[]
    for line in lines:
        if line[:2] in template:
            array.append(line[:2])
    writelines(file_out,array)

    return array
#便参数函数
def merge_list2(one_list, *more_list):
    for i in range(len(more_list)):
        for item in more_list[i]:
            if item not in one_list:
                one_list.append(item)
    return one_list
def merge_list(listoflist):
    if listoflist==[]:
        ret = []
    else:
        ret = listoflist[0]

    for ls in listoflist[0:]:
        for item in ls:
            if item not in ret:
                ret.append(item)
    return  ret
def normalize(ls):
    min_=min(ls)
    max_ = max(ls)
    i=0
    ret = []
    for item in ls:
        ret .append( float(item - min_)/(max_ -min_))
    return ret

def recolor(ls):
    ret = []
    colors = ['lightskyblue','skyblue','deepskyblue','cornflowerblue','royalblue']
    step = len(colors)
    ls = normalize(ls)
    print(ls)
    for item in ls:
        n = 0.
        while n <step:
            if item >= n/step and item <=(n+1)/step:
                ret.append(colors[int(n)])
            n+=1

    return ret

def str2list(str):
    '''
        str = "['.0.1','.0.2']" -- >list=['.0.1','.0.2']
    :param str:
    :return:
    '''
    str = str.replace('[','')
    str = str.replace(']','')
    str = str.replace('\'','')
    str = str.replace(' ','')
    str = str.replace('\"','')


    ret = str.split(',')
    return  ret
def parents_format(strs):
    lists=[]
    for str in strs:
        ls = str2list(str)
        lists.append(ls.copy())
    return lists



#SeqSubSeq
def SeqSubSeq(file_in,file_out):
    '''
    将段内容前面的标题加上
    对数形状字符串,寻找所有顺序子序列
    所有叶子结点与其所有祖先由上到下输出值
    :param file_name:
    :return:
    '''
    file_name = Path(file_in)
    stack=[]
    lines=[]
    arr = readlines(file_name)
    #print(arr)
    cnt=0
    while(cnt<len(arr)):
        if arr[cnt]=='':
            cnt+=1
        elif cnt==0 :
            stack.append(cnt)
            cnt+=1
        elif len(stack)==0:
            stack.append(cnt)
            cnt+=1
        elif value[arr[cnt]]>value[arr[stack[-1]]]:
            if arr[cnt] == '.0':
                stack.append(cnt )
                lines.append(stack.copy())
                stack.pop()
                cnt += 1
            else:
                stack.append(cnt)
                cnt+=1
        elif value[arr[cnt]]<value[arr[stack[-1]]]:
                stack.pop()
            #stack.append(cnt+1)
                #nt+=1
        elif value[arr[cnt]]==value[arr[stack[-1]]]:
            stack.pop()
            stack.append(cnt)
            cnt+=1
    writelist(file_out,lines)





def main():
    return 0


if __name__ == '__main__':
    arr = toarry()
    preprocess('line_cluster.txt')

