import pandas as pd
from pasigram.service.candidate_edges_service import *


class CandidateEdges:

    def __init__(self, edge_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame, min_support: int):
        self.__edges = compute_edges_with_node_labels(edge_ids, edges, nodes)
        self.__edge_ids = compute_edge_ids(self.edges)
        self.__frequent_edges = compute_frequent_edges(min_support, self.edges)

    @property
    def edges(self) -> pd.DataFrame:
        return self.__edges

    @property
    def frequent_edges(self) -> pd.DataFrame:
        return self.__frequent_edges

    @property
    def edge_ids(self) -> list:
        return self.__edge_ids
