import pandas as pd
from pasigram.service.adjacency_list_service import *


class AdjacencyList:

    def __init__(self, node_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame, node_degrees: pd.DataFrame):
        self.__adjacency_list = compute_adjacency_list(node_ids, edges, nodes, node_degrees)

    @property
    def adjacency_list(self):
        return self.__adjacency_list
