import pandas as pd
from pasigram.service.candidate_edges_service import *


class CandidateEdges:

    def __init__(self, edge_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame):
        self.__edges = compute_edges_with_node_labels(edge_ids, edges, nodes)

    @property
    def edges(self):
        return self.__edges
