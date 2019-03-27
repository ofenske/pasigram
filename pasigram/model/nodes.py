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
    root_node : str
        The id of node whch is the root node of the graph
    right_most_node : str
        The id of the node which is the right-most-node of the graph
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
        self.__root_node = None
        self.__right_most_node = None

    @property
    def nodes(self) -> pd.DataFrame:
        return self.__nodes

    @property
    def nodes_ids(self) -> list:
        return self.__node_ids

    @property
    def node_degrees(self) -> pd.DataFrame:
        return self.__node_degrees

    @property
    def right_most_node(self):
        return self.__right_most_node

    @property
    def root_node(self):
        return self.__root_node

    @right_most_node.setter
    def set_right_most_node(self, node_id):
        self.__right_most_node = node_id

    @root_node.setter
    def set_root_node(self, node_id):
        self.__root_node = node_id
