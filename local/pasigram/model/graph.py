import pandas as pd
from local.pasigram.model.edges import Edges
from local.pasigram.model.nodes import Nodes
from local.pasigram.service.graph_service import build_canonical_smallest_code, build_csp_graph, \
    compute_right_most_path_labels, extend_csp_graph, dictionary_compression, create_initial_csp_graph


class Graph:
    """A class to represent a directed graph with labels for the edges and nodes.
    """

    def __init__(self, nodes: pd.DataFrame, edges: pd.DataFrame, csp_graph: pd.DataFrame = None) -> None:
        """Constructor

        :param pd.DataFrame nodes: Contains all nodes of the graph. Should be in the following format: id|label
        :param pd.DataFrame edges: Contains all edges of the graph. Should be in the following format: id|source|target|label
        :param pd.DataFrame csp_graph: The csp graph for the graph (optionally)
        """

        # edges of the graph (pd.DataFrame)
        self.__edges: Edges = Edges(edges)

        # nodes of the graph (pd.DataFrame)
        self.__nodes: Nodes = Nodes(nodes)

        # the data structure needed to solve the csp problem
        self.__csp_graph: pd.DataFrame = csp_graph

        # canonical code of the graph build based on the final clusters
        self.__canonical_code: str = None

        # the dictionary of nodes used for compression
        self.__node_dict = {}

        # the dictionary of edges used for compression
        self.__edge_dict = {}

    def build_csp_graph(self) -> None:
        """Method to build the csp graph

        """
        self.__csp_graph = build_csp_graph(self.nodes, self.edges)

    def create_initial_csp_graph(self) -> None:
        self.__csp_graph = create_initial_csp_graph(self.nodes_ids, self.nodes, self.edges)

    def extend_csp_graph(self) -> None:
        """Method to extend an existing csp graph, with one edge (and the corresponding nodes).
        Mainly used to extend an existing frequent subgraph to generate new candidates.

        """
        self.__csp_graph = extend_csp_graph(self.csp_graph, self.new_added_edge, self.nodes)

    def build_canonical_smallest_code(self) -> None:
        """Method to build the canonical code based on the csp graph.

        """
        self.__canonical_code = build_canonical_smallest_code(self.csp_graph)

    def build_compressed_graph(self) -> None:
        """Method to do dictionary compression for the graph. Nodes and edges set will be compressed (labels will be
        replaced by numbers).

        """
        compressed_result = dictionary_compression(self.nodes, self.edges)

        self.__node_dict = compressed_result[0]
        self.__edge_dict = compressed_result[1]
        self.__nodes.nodes = compressed_result[2]
        self.__edges.edges = compressed_result[3]

    @property
    def size(self) -> int:
        """The size of the graph (number of edges)

        :return:
        """
        return len(self.edges)

    @property
    def nodes(self) -> pd.DataFrame:
        """The nodes of the graph (id, label)

        :return: nodes
        :rtype: pd.DataFrame
        """
        return self.__nodes.nodes

    @property
    def nodes_ids(self) -> list:
        """List of all ids of the nodes

        :return: nodes_id
        :rtype: list
        """
        return self.__nodes.nodes_ids

    @property
    def edges(self) -> pd.DataFrame:
        """The edges of the graph (id, source, target)

        :return: edges
        :rtype: pd.DataFrame
        """
        return self.__edges.edges

    @property
    def edges_ids(self) -> list:
        """List of all ids of the edges

        :return: edges_ids
        :rtype: list
        """
        return self.__edges.edges_ids

    @property
    def canonical_code(self) -> str:
        """The canonical code of the graph

        :return: canonical_code
        :rtype: str
        """
        return self.__canonical_code

    @property
    def csp_graph(self) -> pd.DataFrame:
        """The CSP representation of the graph

        :return: csp_graph
        :rtype: pd.DataFrame
        """
        return self.__csp_graph

    @property
    def root_node(self) -> int:
        """The root node of the graph.
        By default None.

        :return: root_node
        :rtype: int
        """
        return self.__nodes.root_node

    @property
    def right_most_node(self) -> int:
        """The right-most-node of the graph (last added node for the candidates).
        By default None.

        :return: right_most_node
        :rtype: int
        """
        return self.__nodes.right_most_node

    @property
    def right_most_path(self) -> list:
        """A list with the ids of all nodes which are part of the right-most-path.
        By default empty list.

        :return: right_most_path
        :rtype: list
        """
        return self.__nodes.right_most_path

    @property
    def instances(self) -> pd.DataFrame:
        """Instances of the candidates in the input graph.
        By default empty DataFrame.

        :return: instances
        :rtype: pd.DataFrame
        """
        return self.__nodes.instances

    @property
    def right_most_path_labels(self) -> list:
        """A list with the labels of all nodes which are part of the right-most-path

        :return: right_most_path_labels
        :rtype: list
        """
        return compute_right_most_path_labels(self.right_most_path, self.nodes)

    @property
    def new_added_edge(self) -> dict:
        """The last added edge of the graph

        :return: new_added_edge
        _rtype: dict
        """
        return self.__edges.new_added_edge

    @right_most_path.setter
    def right_most_path(self, edge_ids: list):
        self.__nodes.right_most_path = edge_ids

    @root_node.setter
    def root_node(self, node_id):
        self.__nodes.root_node = node_id

    @right_most_node.setter
    def right_most_node(self, node_id):
        self.__nodes.right_most_node = node_id

    @instances.setter
    def instances(self, instances: list):
        self.__nodes.instances = instances

    @new_added_edge.setter
    def new_added_edge(self, new_edge: dict):
        self.__edges.new_added_edge = new_edge
