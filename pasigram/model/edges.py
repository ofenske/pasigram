import pandas as pd
from pasigram.service.edges_service import *


class Edges:
    """A class to represent a set of directed edges with labels.

       ...

       Attributes
       ----------
           edges : pd.DataFrame
               The edges of the graph (id, source, target)
           ids : list
               List of all ids of the edges

       """

    def __init__(self, edges: pd.DataFrame):
        self.__edges = edges
        self.__edge_ids = compute_edge_ids(self.__edges)

    @property
    def edges(self) -> pd.DataFrame:
        return self.__edges

    @property
    def ids(self) -> list:
        return self.__edge_ids
