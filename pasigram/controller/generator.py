import pandas as pd
from pasigram.model.candidate_edges import *
from pasigram.model.graph import *

class Generator:

    def __init__(self, graph: Graph, min_support):
        self.__edges = CandidateEdges(graph.edges_ids, graph.edges, graph.nodes)
        self.__nodes = graph.
        self.__min_support = min_support
        self.__most_edges = self.__get_edges_with_node_labels()
        print('')


