from unittest import TestCase
import pandas as pd
from pasigram.model.graph import Graph
from pasigram.service.graph_service import build_csp_graph


class TestGraph(TestCase):

    def test_canonical_code(self):
        nodes1 = pd.read_csv(r'../data/nodes.csv', sep=';', index_col='id')
        nodes2 = pd.read_csv(r'../data/nodes2.csv', sep=';', index_col='id')
        edges1 = pd.read_csv(r'../data/edges.csv', sep=';', index_col='id')
        edges2 = pd.read_csv(r'../data/edges2.csv', sep=';', index_col='id')

        graph1 = Graph(nodes1, edges1)
        graph2 = Graph(nodes2, edges2)
        code1 = graph1.canonical_code
        code2 = graph2.canonical_code
        self.assertEqual(code1, code2, msg="Test if the same graph in different order produces the same canonical code")

    def test_negative_canonical_code(self):
        nodes1 = pd.read_csv(r'../data/cam_test_graphs/nodes1.csv', sep=';', index_col='id')
        nodes2 = pd.read_csv(r'../data/cam_test_graphs/nodes2.csv', sep=';', index_col='id')
        edges1 = pd.read_csv(r'../data/cam_test_graphs/edges1.csv', sep=';', index_col='id')
        edges2 = pd.read_csv(r'../data/cam_test_graphs/edges2.csv', sep=';', index_col='id')

        graph1 = Graph(nodes1, edges1)
        graph2 = Graph(nodes2, edges2)
        code1 = graph1.canonical_code
        code2 = graph2.canonical_code
        self.assertIsNot(code1, code2, msg="Test if two different graphs produces different canonical codes")

    def test_build_csp_graph(self):
        expected = pd.DataFrame.from_dict({1: ['node1', "1", "1", [["b", "node2", 2]], [["a", "node2", 2]]],
                                           2: ['node2', "1", "1", [["a", "node1", 1]], [["b", "node1", 1]]]},
                                          columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours',
                                                   'outgoing_neighbours'],
                                          orient="index").to_string()

        node_degrees = pd.DataFrame.from_dict({1: [1, 1],
                                               2: [1, 1]}, orient='index', columns=['indegree', 'outdegree'])

        nodes = pd.DataFrame.from_dict({1: ["node1"],
                                        2: ["node2"]}, orient='index', columns=['label'])

        node_ids = [1, 2]

        adjacency_list = pd.DataFrame.from_dict({1: [[["b", "node2", 2, 1, 1]], [["a", "node2", 2, 1, 1]]],
                                                 2: [[["a", "node1", 1, 1, 1]], [["b", "node1", 1, 1, 1]]]},
                                                columns=["ingoing_neighbours", "outgoing_neighbours"],
                                                orient="index")

        result = build_csp_graph(nodes, node_ids, node_degrees, adjacency_list).to_string()
        print(result)
        print(expected)

        self.assertEqual(expected, result, msg="Test for the adjacency list")


""""def test_matrix(self):
        expected = pd.DataFrame.from_dict({"1": [float('nan'), "1"],
                                           "2": ["2", float('nan')]}, columns=["1", "2"], orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.adjacency_matrix.to_string()
        self.assertEqual(expected, result, msg="Test for the matrix")"""



