from unittest import TestCase
import pandas as pd
from local.pasigram.controller.csp.frequency_calculator import FrequencyCalculator
from local.pasigram.model.graph import Graph


class TestEvaluator(TestCase):

    def test_compute_candidate_frequency(self):
        """Test to test the correct funtionality of the 'compute_candidate_frequency'-method of the
        FrequencyCalculator-class.

        :return: True or False
        :rtype: bool
        """
        # build the input graph
        nodes = pd.read_csv(r'../data/nodes.csv', sep=';', index_col='id')
        edges = pd.read_csv(r'../data/edges.csv', sep=';', index_col='id')
        graph = Graph(nodes, edges)

        # build the csp graph of the candidate
        candidate_csp_graph = pd.DataFrame.from_dict({0: ['DB', 0, 2, [], [['a', 'DM', 1], ['b', 'IR', 2]]],
                                                      1: ['DM', 1, 0, [['a', 'DB', 0]], []],
                                                      2: ['IR', 1, 0, [['b', 'DB', 0]], []]
                                                      }, orient='index',
                                                     columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours',
                                                              'outgoing_neighbours'])

        new_added_edge = {'parent_node_id': 0, 'child_node_id': 2, 'edge_label': 'b'}
        frequency_calculator = FrequencyCalculator(graph.csp_graph, 2)

        candidate_frequency = frequency_calculator.compute_candidate_frequency(candidate_csp_graph, 2, new_added_edge)
        print(candidate_frequency)
        self.assertEqual(2, candidate_frequency[0], msg="Test of frequency calculation")

    def test_compute_candidate_frequency_with_given_instances(self):
        """Test to test the correct funtionality of the 'compute_candidate_frequency_with_given_instances'-method of the
        FrequencyCalculator-class.

        :return: True or False
        :rtype: bool
        """
        # build the input graph
        nodes = pd.read_csv(r'../data/nodes.csv', sep=';', index_col='id')
        edges = pd.read_csv(r'../data/edges.csv', sep=';', index_col='id')
        graph = Graph(nodes, edges)

        # build the csp graph of the candidate
        candidate_csp_graph = pd.DataFrame.from_dict({0: ['DB', 0, 2, [], [['a', 'DM', 1], ['b', 'IR', 2]]],
                                                      1: ['DM', 1, 0, [['a', 'DB', 0]], []],
                                                      2: ['IR', 1, 0, [['b', 'DB', 0]], []]
                                                      }, orient='index',
                                                     columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours',
                                                              'outgoing_neighbours'])

        new_added_edge = {'parent_node_id': 0, 'child_node_id': 2, 'edge_label': 'b'}
        candidate_instances = [{2: 0, 3: 1}, {7: 0, 10: 1}]
        frequency_calculator = FrequencyCalculator(graph.csp_graph, 2)

        candidate_frequency = frequency_calculator.compute_candidate_frequency_with_given_instances(candidate_csp_graph,
                                                                                                    candidate_instances,
                                                                                                    2, new_added_edge)
        print(candidate_frequency)
        self.assertEqual(2, candidate_frequency[0], msg="Test of frequency calculation with given instances")
