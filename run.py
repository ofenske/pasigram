import pandas as pd
from pasigram.model.graph import Graph
from pasigram.controller.pasigram import Pasigram
from timeit import default_timer as timer
from pyspark import SparkContext
from memory_monitor import get_size

if __name__ == '__main__':
    local_cluster = False
    spark_cluster = False
    local_distributed = False
    num_workers = 6

    nodes = pd.read_csv(r'data/nodes.csv', sep=';', index_col='id')
    edges = pd.read_csv(r'data/edges.csv', sep=';', index_col='id')
    start = timer()
    graph = Graph(nodes, edges)
    print('Compress graph!')
    graph.build_compressed_graph()
    print('Build csp graph!')
    graph.build_csp_graph()

    pasigram = Pasigram(graph, 2)

    if local_cluster is True:
        sc = SparkContext(appName="PaSiGraM", master="local")
        pasigram.execute(sc, num_workers, local_distributed)
        end = timer()
        print('Execution time:', end - start)
        print(len(pasigram.frequent_subgraphs), 'frequent subgraphs were found!')
        print('Stopping the SparkSession!')
        sc.stop()

    elif spark_cluster is True:
        sc = SparkContext(appName="PaSiGraM", master="spark://pgxlgtm:7077")
        sc.setLogLevel("ERROR")
        sc.addPyFile(r'pasigram.zip')
        pasigram.execute(sc, num_workers, local_distributed)
        end = timer()
        print('Execution time:', end - start)
        print(len(pasigram.frequent_subgraphs), 'frequent subgraphs were found!')
        print('Used memory for PaSiGraM: '+str(get_size(pasigram))+" byte")
        print('Stopping the SparkSession!')
        sc.stop()

    else:
        print('Execute PaSiGraM!')
        pasigram.execute(local_distributed=local_distributed)
        end = timer()
        print('Execution time: '+str(end - start)+' seconds')
        print(len(pasigram.frequent_subgraphs), 'frequent subgraphs were found!')
        print('Used memory for PaSiGraM: '+str(get_size(pasigram))+" byte")
