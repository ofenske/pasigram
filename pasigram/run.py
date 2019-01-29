from pasigram.model.graph import *
from pasigram.controller.generator import *
import pandas as pd

nodes = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes.csv', sep=';', index_col='id')
edges = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges.csv', sep=';', index_col='id')
graph = Graph(nodes, edges)

print("########GRAPH_ATTRIBUTES########")
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


generator = Generator(graph, 2)

print("########GENERATOR_ATTRIBUTES########")
print("\n_______Edges_with_labels_______\n")
print(generator.edges)
print("\n_______Frequent_edges_______\n")
print(generator.frequent_edges)

