import pandas as pd
from pasigram.model.candidate_edges import *
from pasigram.model.candidate_nodes import *
from pasigram.model.graph import *


class Generator:

    def __init__(self, graph: Graph, min_support):
        self.__edges = CandidateEdges(graph.edges_ids, graph.edges, graph.nodes, min_support)
        self.__nodes = CandidateNodes
        self.__min_support = min_support
        print('')

    @property
    def edges(self) -> pd.DataFrame:
        return self.__edges.edges

    @property
    def nodes(self) -> pd.DataFrame:
        return self.__nodes.nodes

    @property
    def min_support(self) -> int:
        return self.__min_support

    @property
    def frequent_edges(self) -> pd.DataFrame:
        return self.__edges.frequent_edges
