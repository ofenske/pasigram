from pasigram.model.graph import *
from pasigram.controller.generator import *
from pasigram.controller.evaluator import *
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
print("\n_______csp_graph_______\n")
print(graph.csp_graph)


unique_edges = graph.count_edges()

generator = Generator(unique_edges, 2)

print("########GENERATOR_ATTRIBUTES########")
print("\n_______Unique_edges_______\n")
print(graph.unique_edges)
print("\n_______Frequent_edges_______\n")
print(generator.frequent_edges)

generator.generate(1)

print("\n_______Candidate#1_______\n")
print("_______Matrix_______\n")
print(generator.candidates.iloc[1]['graph'].adjacency_matrix)
print("\n_______Nodes_______\n")
print(generator.candidates.iloc[1]['graph'].nodes)
print("\n_______Edges_______\n")
print(generator.candidates.iloc[1]['graph'].edges)
print("\n_______Node_degrees_______\n")
print(generator.candidates.iloc[1]['graph'].node_degrees)
print("\n_______Adjacency_list_______\n")
print(generator.candidates.iloc[1]['graph'].adjacency_list)
print("\n_______Canonical_code_______\n")
print(generator.candidates.iloc[1]['graph'].canonical_code)
print("\n_______csp_graph_______\n")
print(generator.candidates.iloc[1]['graph'].csp_graph)

evaluator = Evaluator(graph.csp_graph, 2)
print("\nThe frequency of the current candidate is: ", evaluator.compute_candidate_frequency(generator.candidates.iloc[1]['graph'].csp_graph))



