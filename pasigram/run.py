from pasigram.controller.csp.evaluator import *
from pasigram.controller.candidate_generation.generator import *
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
print("\n_______Edges_with_node_labels_______\n")
print(graph.edges_with_node_labels)
print("\n_______Node_degrees_______\n")
print(graph.node_degrees)
print("\n_______Adjacency_list_______\n")
print(graph.adjacency_list)
print("\n_______Canonical_code_______\n")
print(graph.canonical_code)
print("\n_______csp_graph_______\n")
print(graph.csp_graph)

generator = Generator(graph.unique_edges, 2)

print("########GENERATOR_ATTRIBUTES########")
print("\n_______Unique_edges_______\n")
print(graph.unique_edges)
print("\n_______Frequent_edges_______\n")
print(generator.frequent_edges)

generator.generate_initial_candidates()

print("\n_______Candidate#1_______\n")
print("_______Matrix_______\n")
print(generator.candidates.iloc[1]['graph'].adjacency_matrix)
print("\n_______Nodes_______\n")
print(generator.candidates.iloc[1]['graph'].nodes)
print("Root node: ", generator.candidates.iloc[1]['graph'].root_node)
print("right most node: ", generator.candidates.iloc[1]['graph'].right_most_node)
print("\n_______Edges_______\n")
print(generator.candidates.iloc[1]['graph'].edges)
print("right most path: ", generator.candidates.iloc[1]['graph'].right_most_path)
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



