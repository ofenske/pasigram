import pandas as pd
from pasigram.service.adjacency_matrix_service import *


class AdjacencyMatrix:

    def __init__(self, node_ids: list, edge_ids: list, edges: pd.DataFrame) -> object:
        self.__adjacency_matrix = compute_adjacency_matrix(node_ids, edge_ids, edges)

    @property
    def adjacency_matrix(self):
        return self.__adjacency_matrix
