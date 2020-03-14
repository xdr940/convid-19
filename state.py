import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from path import Path
import seaborn as sns
import argparse

parser = argparse.ArgumentParser(description="precess tree file to a doc")
parser.add_argument('--node_edition_csv', default='./data/node_edition.csv')
parser.add_argument('--edge_edition_csv', default='./data/edge_edition.csv')

args = parser.parse_args()


def main(args):
    df_nodes = pd.read_csv(args.node_edition_csv)
    df_edges = pd.read_csv(args.edge_edition_csv)

    byxtd = df_edges['病原学特点']
    for colum in df_edges.columns:
        plt.plot(df_edges[colum])
    plt.show()

    pass


def heatmap_():
    sns.set()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题-设置字体为黑体
    df = pd.read_csv('./data/edge_edition.csv')
    df = pd.DataFrame(df, dtype=int)
    # Draw a heatmap with the numeric values in each cell
    df.index = ['2nd', '3rd', '4th', '5th', '6th', '7th']
    f, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.T, annot=True, fmt='d', linewidths=.5, ax=ax)
    #plt.title('结点数量变化')
    plt.title('边数量变化')

    plt.show()


if __name__ == '__main__':
    heatmap_()
    #main(args)
