import pandas as pd
import numpy as np
from pasigram.model.graph import Graph
from pasigram.controller.pasigram import Pasigram
from timeit import default_timer as timer
from memory_monitor import get_size

if __name__ == '__main__':
    execution_mode = 'single_core'

    nodes = pd.read_csv(r'../data/nodes.csv', sep=';', index_col='id')
    edges = pd.read_csv(r'../data/edges.csv', sep=';', index_col='id')
    start = timer()
    graph = Graph(nodes, edges)
    print('Compress graph!')
    graph.build_compressed_graph()
    print('Build csp graph!')
    graph.build_csp_graph()

    pasigram = Pasigram(graph, 2)

    print('Execute PaSiGraM!')
    pasigram.execute(execution_mode=execution_mode)
    end = timer()
    print('Execution time: ' + str(end - start) + ' seconds')
    print(len(pasigram.frequent_subgraphs), 'frequent subgraphs were found!')
    print('Used memory for PaSiGraM: ' + str(get_size(pasigram)) + " byte")
