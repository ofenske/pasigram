# import pandas as pd
from pasigram.service.nodes_service import *


class Nodes:
    """A class to represent a set of nodes with labels.

       ...

       Attributes
       ----------
       nodes : pd.DataFrame
           All nodes (id, label)
       nodes_ids : list
           List of all ids of the nodes
       node_degrees : pd.DataFrame
           Degrees of all nodes

       """

    def __init__(self, nodes: pd.DataFrame, edges: pd.DataFrame) -> object:
        """A class to represent a set of nodes with labels.

        Parameters
        ----------
        nodes : pd.DataFrame
            Contains all nodes of the graph
        edges : pd.DataFrame
            Contains all edges of the graph
        """
        self.__nodes = nodes
        self.__node_ids = compute_node_ids(self.__nodes)
        self.__node_degrees = compute_node_degrees(self.__node_ids, edges)

    @property
    def nodes(self) -> pd.DataFrame:
        return self.__nodes

    @property
    def ids(self) -> list:
        return self.__node_ids

    @property
    def degrees(self) -> pd.DataFrame:
        return self.__node_degrees
