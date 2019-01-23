import pandas as pd
from pasigram.candidate_generation.candidate_edges import *


class Generator:

    def __init__(self, data, min_support):
        self.__edges = data.get_edges
        self.__nodes = data.get_nodes
        self.__min_support = min_support
        self.__most_edges = get_edges_with_node_labels(self.__edges, self.__nodes)


