from unittest import TestCase
import pandas as pd
from pasigram.model.graph import *


# adjacency_matrix, nodes, nodes_ids, edges, unique_edges, edges_ids, adjacency_list, node_degrees,
# clusters_by_label_and_degree, clusters_by_adjacency_list, canonical_code

class TestGraph(TestCase):

    def test_matrix(self):
        expected = pd.DataFrame.from_dict({"1": [float('nan'), "1"],
                                           "2": ["2", float('nan')]}, columns=["1", "2"], orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.adjacency_matrix.to_string()
        self.assertEqual(expected, result, msg="Test for the matrix")

    def test_nodes(self):
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.nodes.to_string()
        self.assertEqual(nodes.to_string(), result, msg="Test for the nodes")

    def test_nodes_ids(self):
        expected = ['1', '2']
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = str(graph.nodes_ids)
        self.assertEqual(str(expected), result, msg="Test for the edges ids")

    def test_edges(self):
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.edges.to_string()
        self.assertEqual(edges.to_string(), result, msg="Test for the edges")

    def test_unique_edges(self):
        expected = pd.DataFrame.from_dict({"node1node2a": ["node1", "node2", "a", "1"],
                                           "node2node1b": ["node2", "node1", "b", "1"]}, columns=['source', 'target', 'label', 'frequency'],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.unique_edges.to_string()
        self.assertEqual(expected, result, msg="Test for the unique edges")

    def test_edges_ids(self):
        expected = ['1', '2']
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = str(graph.edges_ids)
        self.assertEqual(str(expected), result, msg="Test for the edges ids")

    def test_adjacency_list(self):
        expected = pd.DataFrame.from_dict({"1": [[["a", "node2", 1, 1]]],
                                           "2": [[["b", "node1", 1, 1]]]}, columns=["neighbours"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.adjacency_list.to_string()

        self.assertEqual(expected, result, msg="Test for the adjacency list")

    def test_node_degrees(self):
        expected = pd.DataFrame.from_dict({"1": ['1', '1'],
                                           "2": ['1', '1']}, columns=["Indegree", "Outdegree"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.node_degrees.to_string()
        self.assertEqual(expected, result, msg="Test for the node degrees")

    def test_clusters_by_label_and_degree(self):
        # clustername of nodes = label of nodes+indegree of nodes+outdegree of nodes
        expected = pd.DataFrame.from_dict({"node111": ['node1', '1', '1', ['1']],
                                           "node211": ['node2', '1', '1', ['2']]},
                                          columns=["label", "indegree", "outdegree", "elements"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.clusters_by_label_and_degree.to_string()
        self.assertEqual(expected, result, msg="Test for the clusters by label and degree")

    def test_clusters_by_adjacency_list(self):
        # clustername of nodes = label of nodes+indegree of nodes+outdegree of nodes
        expected = pd.DataFrame.from_dict({"node111anode2": ['node1', '1', '1', [["a", "node2", 1, 1]], ['1']],
                                           "node211bnode1": ['node2', '1', '1', [["b", "node1", 1, 1]], ['2']]},
                                          columns=["label", "indegree", "outdegree", "neighbours", "elements"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.clusters_by_adjacency_list.to_string()
        self.assertEqual(expected, result, msg="Test for the clusters by label, degree and adjacency list")

    def test_canonical_code(self):
        nodes1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes.csv', sep=';', index_col='id')
        nodes2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes2.csv', sep=';', index_col='id')
        edges1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges.csv', sep=';', index_col='id')
        edges2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges2.csv', sep=';', index_col='id')

        graph1 = Graph(nodes1, edges1)
        graph2 = Graph(nodes2, edges2)
        code1 = graph1.canonical_code
        code2 = graph2.canonical_code
        self.assertEqual(code1, code2, msg="Test if the same graph in different order produces the same canonical code")

    def test_negative_canonical_code(self):
        nodes1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\nodes1.csv', sep=';',
                             index_col='id')
        nodes2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\nodes2.csv', sep=';',
                             index_col='id')
        edges1 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\edges1.csv', sep=';',
                             index_col='id')
        edges2 = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\cam_test_graphs\edges2.csv', sep=';',
                             index_col='id')

        graph1 = Graph(nodes1, edges1)
        graph2 = Graph(nodes2, edges2)
        code1 = graph1.canonical_code
        code2 = graph2.canonical_code
        self.assertIsNot(code1, code2, msg="Test if two different graphs produces different canonical codes")

