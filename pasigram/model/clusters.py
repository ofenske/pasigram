import pandas as pd
from pasigram.service.clusters_service import cluster_nodes_by_adjacency_list, cluster_nodes_by_label_and_degree


class Clusters:
    """A class to represent the clusters of nodes of a graph.
    """

    def __init__(self, nodes: pd.DataFrame, node_degrees: pd.DataFrame, adjacency_list: pd.DataFrame):
        """A class to represent the clusters of nodes of a graph.

        :param pd.DataFrame nodes: Contains all nodes of the graph
        :param pd.DataFrame node_degrees: Contains all node degrees of the graph
        :param pd.DataFrame adjacency_list: The adjacency list of the graph
        """

        self.__clusters_by_label_and_degree = cluster_nodes_by_label_and_degree(nodes, node_degrees)
        self.__clusters_by_adjacency_list = cluster_nodes_by_adjacency_list(self.clusters_by_label_and_degree,
                                                                            adjacency_list)

    @property
    def clusters_by_label_and_degree(self) -> pd.DataFrame:
        """Different clusters of nodes based on their labels, in-/outgoing degrees

        :return: clusters_by_label_and_degree
        :rtype: pd.DataFrame
        """
        return self.__clusters_by_label_and_degree

    @property
    def clusters_by_adjacency_list(self) -> pd.DataFrame:
        """Different clusters of nodes based on their labels, in-/outgoing degrees and adjacency lists

        :return: clusters_by_adjacency_list
        :rtype: pd.DataFrame
        """
        return self.__clusters_by_adjacency_list
