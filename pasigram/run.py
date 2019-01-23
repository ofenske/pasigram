from pasigram.model.graph import *
import pandas as pd

nodes = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes.csv', sep=';', index_col='id')
edges = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges.csv', sep=';', index_col='id')
graph = Graph(nodes, edges)

print("_______Matrix_______\n")
print(graph.adjacency_matrix)
print("\n_______Nodes_______\n")
print(graph.nodes)
print("\n_______Edges_______\n")
print(graph.edges)
print("\n_______Node_degrees_______\n")
print(graph.node_degrees)
print("\n_______Adjacency_list_______\n")
print(graph.adjacency_list)
print("\n_______Canonical_code_______\n")
print(graph.canonical_code)

