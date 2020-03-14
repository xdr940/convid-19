
from utils import recolor
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#a = [1,2,3,4,5]
#
def draw1():
    nodes = [56, 77, 128, 356, 691, 880]
    edges = [69, 97, 173, 540, 1298, 1721]

    nodes = np.array(nodes)
    edges = np.array(edges)
    R = edges / nodes

    #
    label = ['+.1.00', '+.1.02', '+.1.03', '+.1.07', '+.1.08', '+all']

    plt.subplot(2,1,1)
    plt.plot(label, nodes, 'r-o',label='nodes')
    plt.plot(label, edges, 'g-o',label='edges')
    plt.legend()
    plt.xlabel('key nodes add')
    plt.ylabel('number of nodes or edges')


    plt.subplot(2,1,2)

    plt.plot(label, R, 'b-o',label='R')
    plt.legend()
    plt.xlabel('key nodes number')
    plt.ylabel('R')

def main():
    draw1()
    plt.show()


if __name__ == '__main__':
    main()
