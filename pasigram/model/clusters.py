import pandas as pd
from pasigram.service.clusters_service import *


class Clusters:
    def __init__(self, nodes: pd.DataFrame, node_degrees: pd.DataFrame, adjacency_list: pd.DataFrame):
        self.__clusters_by_label_and_degree = cluster_nodes_by_label_and_degree(nodes, node_degrees)
        self.__clusters_by_adjacency_list = cluster_nodes_by_adjacency_list(self.clusters_by_label_and_degree,
                                                                            adjacency_list)

    @property
    def clusters_by_label_and_degree(self):
        return self.__clusters_by_label_and_degree

    @property
    def clusters_by_adjacency_list(self):
        return self.__clusters_by_adjacency_list


