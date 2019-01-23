import pandas as pd
from pasigram.service.edges_service import *


class Edges:

    def __init__(self, edges: pd.DataFrame):
        self.__edges = edges
        self.__edge_ids = compute_edge_ids(self.__edges)

    @property
    def edges(self):
        return self.__edges

    @property
    def ids(self):
        return self.__edge_ids
