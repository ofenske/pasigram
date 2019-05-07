from unittest import TestCase
import pandas as pd
from pasigram.service.clusters_service import cluster_nodes_by_label_and_degree, cluster_nodes_by_adjacency_list


class TestClusters(TestCase):
    def test_cluster_nodes_by_label_and_degree(self):
        # clustername of nodes = label of nodes+indegree of nodes+outdegree of nodes
        expected = pd.DataFrame.from_dict({"IR11": ['IR', '1', '1', ['1']],
                                           "DB11": ['DB', '1', '1', ['2']]},
                                          columns=["label", "indegree", "outdegree", "elements"],
                                          orient="index").to_string()
        nodes = pd.DataFrame.from_dict({1: ["IR"],
                                        2: ["DB"]}, orient='index', columns=['label'])

        node_degrees = pd.DataFrame.from_dict({1: [1, 1],
                                               2: [1, 1]}, orient='index', columns=['indegree', 'outdegree'])

        result = cluster_nodes_by_label_and_degree(nodes, node_degrees).to_string()
        self.assertEqual(expected, result, msg="Test for the clusters by label and degree")

    def test_clusters_by_adjacency_list(self):
        # clustername of nodes = label of nodes+indegree of nodes+outdegree of nodes
        expected = pd.DataFrame.from_dict(
            {"IR11bDBaDB": ['IR', '1', '1', [["b", "DB", "2", "1", "1"]], [["a", "DB", "2", "1", "1"]], ['1']],
             "DB11aIRbIR": ['DB', '1', '1', [["a", "IR", "1", "1", "1"]], [["b", "IR", "1", "1", "1"]], ['2']]},
            columns=["label", "indegree", "outdegree", "ingoing_neighbours", "outgoing_neighbours", "elements"],
            orient="index").to_string()
        cluster_by_label_and_degree = pd.DataFrame.from_dict({"IR11": ['IR', 1, 1, [1]],
                                                              "DB11": ['DB', 1, 1, [2]]},
                                                             columns=["label", "indegree", "outdegree", "elements"],
                                                             orient="index")

        adjacency_list = pd.DataFrame.from_dict({1: [[["b", "DB", 2, 1, 1]], [["a", "DB", 2, 1, 1]]],
                                                 2: [[["a", "IR", 1, 1, 1]], [["b", "IR", 1, 1, 1]]]},
                                                columns=["ingoing_neighbours", "outgoing_neighbours"],
                                                orient="index")

        result = cluster_nodes_by_adjacency_list(cluster_by_label_and_degree, adjacency_list).to_string()
        self.assertEqual(expected, result, msg="Test for the clusters by label, degree and adjacency list")
