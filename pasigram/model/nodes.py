# import pandas as pd
from pasigram.service.nodes_service import *


class Nodes:

    def __init__(self, nodes: pd.DataFrame, edges: pd.DataFrame) -> object:
        self.__nodes = nodes
        self.__node_ids = compute_node_ids(self.__nodes)
        self.__node_degrees = compute_node_degrees(self.__node_ids, edges)

    @property
    def nodes(self):
        return self.__nodes

    @property
    def ids(self):
        return self.__node_ids

    @property
    def degrees(self):
        return self.__node_degrees
