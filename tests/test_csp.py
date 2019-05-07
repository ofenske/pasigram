from unittest import TestCase
import pandas as pd
from pasigram.controller.csp.utils import compute_candidate_frequency, is_ingoing_subset, has_child, compute_candidate_frequency_with_given_instances
from pasigram.model.graph import Graph


class TestEvaluator(TestCase):

    def test_compute_candidate_frequency(self):
        nodes = pd.read_csv(r'../data/nodes.csv', sep=';', index_col='id')
        edges = pd.read_csv(r'../data/edges.csv', sep=';', index_col='id')
        graph = Graph(nodes, edges)
        graph.right_most_node = 3
        graph.new_added_edge = {'parent_node_id': 1, 'child_node_id': 2, 'edge_label': 'c'}


        input_csp_graph = graph.csp_graph

        """candidate_csp_graph = pd.DataFrame.from_dict({0: ['DB', 0, 2, [], [['b', 'IR', 2], ['a', 'DM', 1]]],
                                                      1: ['DM', 2, 0, [['a', 'DB', 0]], []],
                                                      2: ['IR', 1, 1, [['b', 'DB', 0]], []]}, orient='index',
                                                     columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours',
                                                              'outgoing_neighbours'])"""

        candidate_csp_graph = pd.DataFrame.from_dict({0: ['DB', 0, 2, [], [['a', 'DM', 1], ['b', 'IR', 2]]],
                                                      1: ['DM', 1, 0, [['a', 'DB', 0]], []],
                                                      2: ['IR', 1, 0, [['b', 'DB', 0]], []]
                                                      }, orient='index',
                                                     columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours',
                                                              'outgoing_neighbours'])

        print(compute_candidate_frequency(input_csp_graph, candidate_csp_graph, graph.right_most_node, graph.new_added_edge))

    def test_is_subset(self):
        # list1 = [['b', 'IR', 1], ['a', 'DM', 2]]
        list1 = []
        list2 = [['a', 'DM', 3], ['b', 'IR', 4]]

        print(is_ingoing_subset(list1, list2))

    def test_has_child(self):
        ingoing_neighbour_list = []
        outgoing_neighbour_list = [['b', 'IR', 2], ['a', 'DM', 1]]
        child_node_id = 1

        print(has_child(outgoing_neighbour_list, ingoing_neighbour_list, child_node_id))
