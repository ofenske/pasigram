import pandas as pd
from pasigram.service.adjacency_matrix_service import compute_adjacency_matrix


class AdjacencyMatrix:
    """A class to represent the adjacency matrix of a graph.
    """

    def __init__(self, node_ids: list, edge_ids: list, edges: pd.DataFrame) -> None:
        """A class to represent the adjacency matrix of a graph.

        :param list node_ids: Contains all ids of the nodes of the graph
        :param list edge_ids: Contains all ids of the edges of the graph
        :param d.DataFrame edges: Contains all edges of te graph
        """

        self.__adjacency_matrix = compute_adjacency_matrix(node_ids, edge_ids, edges)

    @property
    def adjacency_matrix(self) -> pd.DataFrame:
        """Adjacency matrix of the graph (ids of nodes and edges)

        :return: adjacency_matrix
        :rtype: pd.DataFrame
        """
        return self.__adjacency_matrix
