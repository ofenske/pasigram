import pandas as pd
from pasigram.service.adjacency_matrix_service import *


class AdjacencyMatrix:
    """A class to represent the adjacency matrix of a graph.

    ...

    Attributes
    ----------
    adjacency_matrix : pd.DataFrame
        Adjacency matrix of the graph (ids of nodes and edges)
    """

    def __init__(self, node_ids: list, edge_ids: list, edges: pd.DataFrame) -> object:
        """A class to represent the adjacency matrix of a graph.

        Parameters
        ----------
        node_ids : list
            Contains all ids of the nodes of the graph
        edge_ids : list
            Contains all ids of the edges of the graph
        edges : pd.DataFrame
            Contains all edges of te graph
        """
        self.__adjacency_matrix = compute_adjacency_matrix(node_ids, edge_ids, edges)

    @property
    def adjacency_matrix(self) -> pd.DataFrame:
        return self.__adjacency_matrix
