import jieba
import jieba.analyse
from gensim.test.utils import  get_tmpfile
import gensim.models.word2vec as word2vec
from  path import Path
import argparse
from utils import readlines,SeqSubSeq,toarry
#文件位置需要改为自己的存放路径
#将文本分词

parser = argparse.ArgumentParser(description="precess tree file to a doc")
parser.add_argument('--doc', default='./doc6.txt', help="Input file")
parser.add_argument('--doc_post',default='./doc_post.txt',help='output an txt to descripe file_in')
parser.add_argument('--seged_file',default='./conv19_segments.txt')
parser.add_argument('--stop_words_file',default='./stopwords.txt')
parser.add_argument('--model_file',default='./word2vec.model')

parser.add_argument('--node_list_file',default='./array.txt',help='output an txt to descripe file_in')
parser.add_argument('--seq_sub_seq_file',default='./seqsubseq.txt',help='output an txt to descripe file_in')


args = parser.parse_args()


file = Path('./doc_post.txt')
topn = 10

save_model=True
load_model=True
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords



def preprocess(args):
    '''

    :param file_name:  line_cluster file
    :return:
    '''
    toarry(file_in=args.doc,file_out=args.node_list_file)
    SeqSubSeq(file_in = args.node_list_file,file_out=args.seq_sub_seq_file)
    file_name = Path(args.seq_sub_seq_file)
    if not file_name.exists():
        return
    seq_sub_seq_file = Path(args.seq_sub_seq_file)
    seq_sub_seq = readlines(seq_sub_seq_file)


    src_file = Path(args.doc)
    lines = readlines(src_file)

    ret_line=[]
    for line in lines:
        ret_line.append(line[2:])
    print(ret_line)

    post_process_txt=[]
    post_pcoess_line=[]
    for line_arr in seq_sub_seq:
        if line_arr!='':
            for num_line in line_arr.split(','):
                post_pcoess_line.append(ret_line[int(num_line)])
        post_process_txt.append(post_pcoess_line.copy())
        post_pcoess_line=[]


    doc_post = 'doc_post.txt'
    with open(doc_post,'w',encoding='UTF-8') as txt:
        txt.write(str(post_process_txt[0] )[1:-1])
        for item in post_process_txt[1:]:
            txt.write('\n'+str(item)[1:-1])


def Segment(args):
    '''
    根据停词表, 利用jieba对源文档进行分词
    :return: none, 生成txt文件 seg_file
    '''
    stop_words_file = Path(args.stop_words_file)
    seged_file = Path(args.seged_file)
    stopwords = stopwordslist(stop_words_file)
    outstr=''
    with open(file,encoding='utf-8') as f:
        document = f.read()
        document_cut = jieba.cut_for_search(document)

        for word in document_cut:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "

        with open(seged_file, 'w',encoding="utf-8") as f2:
            f2.write(outstr)
def run(args):
    seged_file = Path(args.seged_file)

    sentences = word2vec.LineSentence(seged_file)
    model_file = Path(args.model_file)
    if load_model==True and model_file.exists():
        model = word2vec.Word2Vec.load("word2vec.model")
    else:
        model = word2vec.Word2Vec(sentences, hs=3, min_count=5, window=10, size=100)

    if save_model == True:
            #path = get_tmpfile("word2vec.model")  # 创建临时文件
            model.save(model_file)

    vocabulary = model.wv.similar_by_word('治疗', topn=100)
    for key in vocabulary:

            print(key)

if __name__=='__main__':
    preprocess(args)
    Segment(args)
    #run(args)
