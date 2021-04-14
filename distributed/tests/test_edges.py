from unittest import TestCase
import pandas as pd
from pasigram.model.graph import Graph
from pasigram.service.edges_service import compute_unique_edges, compute_edge_ids, compute_frequent_edges


class TestEdges(TestCase):
    def test_edges(self):
        nodes = pd.DataFrame.from_dict({"1": ["node1"],
                                        "2": ["node2"]}, orient='index', columns=['label'])
        edges = pd.DataFrame.from_dict({"1": ["1", "2", "a"],
                                        "2": ["2", "1", "b"]}, orient='index', columns=['source', 'target', 'label'])

        graph = Graph(nodes, edges)
        result = graph.edges.to_string()
        self.assertEqual(edges.to_string(), result, msg="Test for the edges")

    def test_unique_edges(self):
        expected = pd.DataFrame.from_dict({"IRDBa": ["IR", "DB", "a", "1"],
                                           "DBIRb": ["DB", "IR", "b", "1"]},
                                          columns=['source', 'target', 'label', 'frequency'],
                                          orient="index").to_string()
        edges_with_node_labels = pd.DataFrame.from_dict({1: ['IR', 'DB', 'a', 'IRDBa'],
                                                         2: ['DB', 'IR', 'b', 'DBIRb']}, orient='index',
                                                        columns=['source', 'target', 'label', 'key'])

        result = compute_unique_edges(edges_with_node_labels).to_string()
        self.assertEqual(expected, result, msg="Test for the unique edges")

    def test_edges_ids(self):
        expected = [1, 2]

        edges = pd.DataFrame.from_dict({1: [1, 2, "a"],
                                        2: [2, 1, "b"]}, orient='index', columns=['source', 'target', 'label'])

        result = str(compute_edge_ids(edges))
        self.assertEqual(str(expected), result, msg="Test for the edges ids")

    def test_compute_frequent_edges(self):
        expected = pd.DataFrame.from_dict({"DBDMa": ["DB", "DM", "a", "2"],
                                           "DBIRb": ["DB", "IR", "b", "3"],
                                           "IRDMc": ["IR", "DM", "c", "2"],
                                           "IRIRe": ["IR", "IR", "e", "2"]},
                                          columns=['source', 'target', 'label', 'frequency'],
                                          orient="index").to_string()

        unique_edges = pd.DataFrame.from_dict({"DBDMa": ["DB", "DM", "a", 2],
                                               "DBIRb": ["DB", "IR", "b", 3],
                                               "IRDMc": ["IR", "DM", "c", 2],
                                               "IRIRe": ["IR", "IR", "e", 2],
                                               "IRDBx": ["IR", "DB", "x", 1],
                                               "DBDBf": ["DB", "DB", "f", 1]},
                                              columns=['source', 'target', 'label', 'frequency'],
                                              orient="index")

        result = compute_frequent_edges(unique_edges, 2).to_string()
        self.assertEqual(expected, result, msg="Test for frequent edges.")
