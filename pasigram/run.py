from pasigram.datastructures.graph import graph
import pandas as pd

nodes = pd.read_csv(r'D:\workspace\pasigram\data\nodes.csv', sep=';')
edges = pd.read_csv(r'D:\workspace\pasigram\data\edges.csv', sep=';')
data = graph(nodes, edges)
print(data.get_matrix())
