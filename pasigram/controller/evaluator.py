from pasigram.model.graph import *


class Evaluator:
    """ A class to represent the evaluator component of the PaSiGraM algorithm.

            ...

            Attributes
            ----------
            min_support: Integer
                The minimum support the graphs have to meet
            input_graph : pd.DataFrame
                The input graph to use to compute the frequencies of the candidates
           """

    def __init__(self, graph: Graph, min_support: int) -> object:
        """

        Parameters
        ----------
        graph: pd.DataFrame
            The input graph to use to compute the frequencies of the candidates
        min_support : Integer
            The minimum support the graphs have to meet
        """
        self.__min_support = min_support
        self.__input_graph = graph

    def evaluate_candidate(self, candidate: pd.DataFrame) -> bool:
        candidate_frequency = 0
        input_graph_clusters = self.__input_graph.clusters_by_adjacency_list

        for i in range(0, len(candidate)):
            current_node = candidate.iloc[i]
            current_node_label = current_node.iloc['label']
            candidate_clusters = input_graph_clusters[input_graph_clusters['label'] == current_node_label]
            for j in range(0, len(candidate_clusters)):
                potential_partner_node = candidate_clusters.iloc[j]
