from pasigram.datastructures.graph import Graph
import pandas as pd

nodes = pd.read_csv(r'D:\workspace\pasigram\data\nodes.csv', sep=';')
edges = pd.read_csv(r'D:\workspace\pasigram\data\edges.csv', sep=';')
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
print(data.get_adjacency_list.to_string())

