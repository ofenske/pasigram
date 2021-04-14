import pandas as pd

from local.pasigram.service.edges_service import compute_edge_ids


class Edges:
    """A class to represent a set of directed edges with labels.
    """

    def __init__(self, edges: pd.DataFrame):
        """A class to represent a set of directed edges with labels.

        :param pd.DataFrame edges: Contains the edges of the graph
        """

        self.__edges = edges
        self.__edge_ids = compute_edge_ids(self.__edges)
        self.__new_added_edge = {}

    @property
    def edges(self) -> pd.DataFrame:
        """The edges of the graph (id, source, target)

        :return: edges
        :rtype: pd.DataFrame
        """
        return self.__edges

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

    @edges.setter
    def edges(self, new_edges: pd.DataFrame) -> None:
        self.__edges = new_edges
