import pandas as pd
from pasigram.service.edges_service import compute_edge_ids, compute_edges_with_node_labels, compute_unique_edges


class Edges:
    """A class to represent a set of directed edges with labels.
    """

    def __init__(self, edges: pd.DataFrame):
        """A class to represent a set of directed edges with labels.

        :param pd.DataFrame edges: Contains the edges of the graph
        """

        self.__edges = edges
        self.__edge_ids = compute_edge_ids(self.__edges)
        self.__edges_with_node_labels = pd.DataFrame()
        self.__unique_edges = pd.DataFrame()
        self.__new_added_edge = {}

    def generate_edges_with_node_labels(self, nodes: pd.DataFrame):
        self.__edges_with_node_labels = compute_edges_with_node_labels(self.edges_ids, self.edges, nodes)

    def generate_unique_edges(self):
        self.__unique_edges = compute_unique_edges(self.edges_with_node_labels)

    @property
    def edges(self) -> pd.DataFrame:
        """The edges of the graph (id, source, target)

        :return: edges
        :rtype: pd.DataFrame
        """
        return self.__edges

    @property
    def edges_with_node_labels(self) -> pd.DataFrame:
        """Edges with labels for source and target instead of the ids

        :return: edges_with_node_labels
        :rtype: pd.DataFrame
        """
        return self.__edges_with_node_labels

    @property
    def unique_edges(self) -> pd.DataFrame:
        """All unique edges of the graph (labels for source and target nodes - not the ids)

        :return: unique_edges
        :rtype: pd.DataFrame
        """
        return self.__unique_edges

    @property
    def edges_ids(self) -> list:
        """List of all ids of the edges

        :return: edges_ids
        :rtype: list
        """
        return self.__edge_ids

    @property
    def new_added_edge(self) -> dict:
        """The edge which has been added at last

        :return: new_added_edge
        :rtype: dict
        """
        return self.__new_added_edge

    @new_added_edge.setter
    def new_added_edge(self, new_edge: dict):
        self.__new_added_edge = new_edge
