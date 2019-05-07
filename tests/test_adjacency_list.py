from unittest import TestCase
import pandas as pd
from pasigram.service.adjacency_list_service import compute_adjacency_list


class TestAdjacencyList(TestCase):
    def test_compute_adjacency_list(self):
        expected = pd.DataFrame.from_dict({1: [[["b", "node2", 2, 1, 1]], [["a", "node2", 2, 1, 1]]],
                                           2: [[["a", "node1", 1, 1, 1]], [["b", "node1", 1, 1, 1]]]},
                                          columns=["ingoing_neighbours", "outgoing_neighbours"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({1: ["node1"],
                                        2: ["node2"]}, orient='index', columns=['label'])
        node_ids = [1, 2]
        node_degrees = pd.DataFrame.from_dict({1: [1, 1],
                                               2: [1, 1]}, orient='index', columns=['indegree', 'outdegree'])
        edges = pd.DataFrame.from_dict({1: [1, 2, "a"],
                                        2: [2, 1, "b"]}, orient='index', columns=['source', 'target', 'label'])

        result = compute_adjacency_list(node_ids, edges, nodes, node_degrees).to_string()

        self.assertEqual(expected, result, msg="Test for the adjacency list")
