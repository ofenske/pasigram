import pandas as pd
from pasigram.service.adjacency_list_service import compute_adjacency_list


class AdjacencyList:
    """A class to represent the adjacency list of a graph.
    """

    def __init__(self, node_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame, node_degrees: pd.DataFrame):
        """A class to represent the adjacency list of a graph.

        :param list node_ids: Contains all node ids of the graph
        :param pd.DataFrame edges: Contains all edges of the graph
        :param pd.DataFrame nodes: Contains all nodes of the graph
        :param pd.DataFrame node_degrees: Contains all node degrees of the graph
        """

        self.__adjacency_list = compute_adjacency_list(node_ids, edges, nodes, node_degrees)

    @property
    def adjacency_list(self) -> pd.DataFrame:
        """Adjacency list of the graph

        :return: adjacency_list
        :rtype: pd.DataFrame
        """
        return self.__adjacency_list
