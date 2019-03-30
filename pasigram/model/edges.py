import pandas as pd
from pasigram.service.edges_service import *


class Edges:
    """A class to represent a set of directed edges with labels.

    ...

    Attributes
    ----------
    edges : pd.DataFrame
        The edges of the graph (id, source, target)
    edge_ids : list
        List of all ids of the edges
    edges_with_node_labels : pd.DataFrame
        Edges with labels for source and target instead of the ids
    unique_edges : pd.DataFrame
        All unique edges of the graph (labels for source and target nodes - not the ids)
    right_most_path : list
        List of all edge ids which are part of the right_most_path
    """

    def __init__(self, edges: pd.DataFrame):
        """A class to represent a set of directed edges with labels.

        Parameters
        ----------
        edges : pd.DataFrame
            Contains the edges of the graph
        """
        self.__edges = edges
        self.__edge_ids = compute_edge_ids(self.__edges)
        self.__edges_with_node_labels = pd.DataFrame()
        self.__unique_edges = pd.DataFrame

    def generate_edges_with_node_labels(self, nodes: pd.DataFrame):
        self.__edges_with_node_labels = compute_edges_with_node_labels(self.edges_ids, self.edges, nodes)

    def generate_unique_edges(self):
        self.__unique_edges = compute_unique_edges(self.edges_with_node_labels)

    @property
    def edges(self) -> pd.DataFrame:
        return self.__edges

    @property
    def edges_with_node_labels(self) -> pd.DataFrame:
        return self.__edges_with_node_labels

    @property
    def unique_edges(self) -> pd.DataFrame:
        return self.__unique_edges

    @property
    def edges_ids(self) -> list:
        return self.__edge_ids
