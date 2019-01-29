import pandas as pd
from pasigram.service.clusters_service import *


class Clusters:
    """A class to represent the clusters of nodes of a graph.

       Attributes
       ----------
       clusters_by_label_and_degree : pd.DataFrame
           Different clusters of nodes based on their labels, in-/outgoing degrees
       clusters_by_adjacency_list : pd.DataFrame
           Different clusters of nodes based on their labels, in-/outgoing degrees and adjacency lists
    """

    def __init__(self, nodes: pd.DataFrame, node_degrees: pd.DataFrame, adjacency_list: pd.DataFrame):
        """A class to represent the clusters of nodes of a graph.

        Parameters
        ----------
        nodes : pd.DataFrame
            Contains all nodes of the graph
        node_degrees : pd.DataFrame
            Contains all node degrees of the graph
        adjacency_list : pd.DataFrame
            The adjacency list of the graph
        """
        self.__clusters_by_label_and_degree = cluster_nodes_by_label_and_degree(nodes, node_degrees)
        self.__clusters_by_adjacency_list = cluster_nodes_by_adjacency_list(self.clusters_by_label_and_degree,
                                                                            adjacency_list)

    @property
    def clusters_by_label_and_degree(self) -> pd.DataFrame:
        return self.__clusters_by_label_and_degree

    @property
    def clusters_by_adjacency_list(self) -> pd.DataFrame:
        return self.__clusters_by_adjacency_list
