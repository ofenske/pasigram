from pasigram.datastructures.graph import Graph
import pandas as pd

nodes = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes.csv', sep=';', index_col='id')
edges = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges.csv', sep=';', index_col='id')
data = Graph(nodes, edges)

print("_______Matrix_______\n")
print(data.get_matrix)
print("\n_______Nodes_______\n")
print(data.get_nodes)
print("\n_______Edges_______\n")
print(data.get_edges)
print("\n_______Node_degrees_______\n")
print(data.get_node_degrees)
print("\n_______Adjacency_list_______\n")
print(data.get_adjacency_list)
print("\n_______Canonical_code_______\n")
print(data.get_canonical_code)

