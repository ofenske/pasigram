import pandas as pd
from pasigram.service.adjacency_list_service import *


class AdjacencyList:
    """A class to represent the adjacency list of a graph.

    ...

    Attributes
    ----------
    adjacency_list : pd.DataFrame
        Adjacency list of the graph
    """

    def __init__(self, node_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame, node_degrees: pd.DataFrame):
        """A class to represent the adjacency list of a graph.

        Parameters
        ----------
        node_ids : list
            Contains all node ids of the graph
        edges : pd.DataFrame
            Contains all edges of the graph
        nodes : pd.DataFrame
            Contains all nodes of the graph
        node_degrees : pd.DataFrame
            Contains all node degrees of the graph
        """
        self.__adjacency_list = compute_adjacency_list(node_ids, edges, nodes, node_degrees)

    @property
    def adjacency_list(self) -> pd.DataFrame:
        return self.__adjacency_list
