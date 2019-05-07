import pandas as pd
from pasigram.service.nodes_service import compute_node_ids, compute_node_degrees


class Nodes:
    """A class to represent a set of nodes with labels.
    """

    def __init__(self, nodes: pd.DataFrame, edges: pd.DataFrame) -> None:
        """A class to represent a set of nodes with labels.

        :param pd.DataFrame nodes: Contains all nodes of the graph
        :param pd.DataFrame edges: Contains all edges of the graph
        """

        self.__nodes = nodes
        self.__node_ids = compute_node_ids(self.__nodes)
        self.__node_degrees = compute_node_degrees(self.__node_ids, edges)
        self.__root_node = None
        self.__right_most_node = None
        self.__right_most_path = []
        self.__instances = []

    @property
    def nodes(self) -> pd.DataFrame:
        """All nodes (id, label)

        :return: nodes
        :rtype: pd.DataFrame
        """
        return self.__nodes

    @property
    def nodes_ids(self) -> list:
        """List of all ids of the nodes

        :return: nodes_ids
        :rtype: list
        """
        return self.__node_ids

    @property
    def node_degrees(self) -> pd.DataFrame:
        """Degrees of all nodes

        :return: node_degrees
        :rtype: pd.DataFrame
        """
        return self.__node_degrees

    @property
    def right_most_node(self) -> str:
        """The id of the node which is the right-most-node of the graph

        :return: right_most_node
        :rtype: str
        """
        return self.__right_most_node

    @property
    def root_node(self) -> str:
        """The id of node which is the root node of the graph

        :return: root_node
        :rtype: str
        """
        return self.__root_node

    @property
    def instances(self) -> pd.DataFrame:
        """The instances of a candidate graph in his input graph

        :return: instances
        :rtype: pd.DataFrame
        """
        return self.__instances

    @property
    def right_most_path(self) -> list:
        """A list with the ids of all nodes which are part of the right-most-path.
        By default empty list.

        :return: right_most_path
        :rtype: list
        """
        return self.__right_most_path

    @right_most_node.setter
    def right_most_node(self, node_id):
        self.__right_most_node = node_id

    @root_node.setter
    def root_node(self, node_id):
        self.__root_node = node_id

    @right_most_path.setter
    def right_most_path(self, path: list):
        self.__right_most_path = path

    @instances.setter
    def instances(self, instances: list):
        self.__instances = instances
