import pandas as pd
from pasigram.service.candidate_edges_service import *


class CandidateEdges:
    """A class to represent a directed graph with labels for the edges and nodes.

        ...

        Attributes
        ----------
        edges : pd.DataFrame
            The edges of the graph (id, source, target)
        edges_ids : list
            List of all ids of the edges
        frequent_edges : pd.DataFrame
            The frequent edges which were generated based on the min_support and the edges of the input graph
        """
    def __init__(self, edge_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame, min_support: int):
        """

        Parameters
        ----------
        edge_ids : list
            List which contains the ids of all edges
        edges : pd.DataFrame
            All edges of the input graph
        nodes : pd.DataFrame
            All nodes of the input graph
        min_support : int
            The minimum support the candidates have to meet

        Returns
        -------
        object
        """
        self.__edges = compute_edges_with_node_labels(edge_ids, edges, nodes)
        self.__edge_ids = compute_edge_ids(self.edges)
        self.__frequent_edges = compute_frequent_edges(min_support, self.edges)

    @property
    def edges(self) -> pd.DataFrame:
        return self.__edges

    @property
    def frequent_edges(self) -> pd.DataFrame:
        return self.__frequent_edges

    @property
    def edge_ids(self) -> list:
        return self.__edge_ids
