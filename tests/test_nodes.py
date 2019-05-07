from unittest import TestCase
import pandas as pd
from pasigram.model.graph import Graph
from pasigram.service.nodes_service import compute_node_ids, compute_node_degrees


class TestNodes(TestCase):

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

        result = str(compute_node_ids(nodes))
        self.assertEqual(str(expected), result, msg="Test for the node ids")

    def test_node_degrees(self):
        expected = pd.DataFrame.from_dict({"1": ["1", "1"],
                                           "2": ["1", "1"]}, columns=["indegree", "outdegree"],
                                          orient="index").to_string()
        node_ids = [1, 2]

        edges = pd.DataFrame.from_dict({1: [1, 2, "a"],
                                        2: [2, 1, "b"]}, orient='index', columns=['source', 'target', 'label'])

        result = compute_node_degrees(node_ids, edges).to_string()
        self.assertEqual(expected, result, msg="Test for the node degrees")
