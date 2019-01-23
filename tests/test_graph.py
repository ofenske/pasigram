from unittest import TestCase
import pandas as pd
from pasigram.model.graph import *


class TestGraph(TestCase):
    def test_get_matrix(self):
        expected = pd.DataFrame.from_dict({"1": [float('nan'), "1"],
                                           "2": ["2", float('nan')]}, columns=["1", "2"], orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.adjacency_matrix.to_string()
        self.assertEqual(expected, result, msg="Test1")

    def test_get_adjacency_list(self):
        expected = pd.DataFrame.from_dict({"1": [[["a", "node2", 1, 1]]],
                                           "2": [[["b", "node1", 1, 1]]]}, columns=["neighbours"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.adjacency_list.to_string()

        self.assertEqual(expected, result, msg="Test")

    """def test_get_node_degrees(self):
        self.fail()"""
