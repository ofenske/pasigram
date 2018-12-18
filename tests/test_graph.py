from unittest import TestCase
import pandas as pd
from pasigram.datastructures.graph import Graph


class TestGraph(TestCase):
    def test_get_matrix(self):
        expected = pd.DataFrame.from_dict({"1": [float('nan'), "1"],
                                           "2": ["2", float('nan')]}, columns=["1", "2"], orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"id": ["1", "2"],
                                        "label": ["node1", "node2"]})
        edges = pd.DataFrame.from_dict({"id": ["1", "2"],
                                        "source": ["1", "2"],
                                        "target": ["2", "1"],
                                        "label": ["a", "b"]})
        graph = Graph(nodes, edges)
        result = graph.get_matrix.to_string()
        self.assertEquals(expected, result, msg="Test1")

    def test_get_adjacency_list(self):
        expected = pd.DataFrame.from_dict({"1": [[["a", ["node2"], 1]]],
                                           "2": [[["b", ["node1"], 1]]]}, columns=["neighbours"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({"id": ["1", "2"],
                                        "label": ["node1", "node2"]})
        edges = pd.DataFrame.from_dict({"id": ["1", "2"],
                                        "source": ["1", "2"],
                                        "target": ["2", "1"],
                                        "label": ["a", "b"]})
        graph = Graph(nodes, edges)
        result = graph.get_adjacency_list.to_string()

        self.assertEqual(expected, result, msg="Test")

    """def test_get_node_degrees(self):
        self.fail()"""
