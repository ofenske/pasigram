import pandas as pd
from pasigram.model.candidate_edges import *
from pasigram.model.candidate_nodes import *
from pasigram.model.graph import *


class Generator:
    """ A class to represent the generator component of the PaSiGraM algorithm.

        ...

        Attributes
        ----------
        nodes : pd.DataFrame
            The nodes of the graph (id, label)
        edges : pd.DataFrame
            The edges of the graph (id, source, target)
        min_support: Integer
            The minimum support the graphs have to meet
        frequent_edges : pd.DataFrame
            The frequent edges which were generated based on the min_support and edges of the graph
       """

    def __init__(self, graph: Graph, min_support):
        """

        Parameters
        ----------
        graph : Graph (Object)
            The graph which has to analyze
        min_support : Integer
            The mininum support the candidates have to meet
        """
        self.__edges = CandidateEdges(graph.edges_ids, graph.edges, graph.nodes, min_support)
        self.__nodes = CandidateNodes
        self.__min_support = min_support
        print('')

    @property
    def edges(self) -> pd.DataFrame:
        return self.__edges.edges

    @property
    def nodes(self) -> pd.DataFrame:
        return self.__nodes.nodes

    @property
    def min_support(self) -> int:
        return self.__min_support

    @property
    def frequent_edges(self) -> pd.DataFrame:
        return self.__edges.frequent_edges
