import pandas as pd
from pasigram.model.edges import Edges
from pasigram.model.nodes import Nodes
from pasigram.model.adjacency_list import AdjacencyList
from pasigram.model.adjacency_matrix import AdjacencyMatrix
from pasigram.model.clusters import Clusters
from pasigram.service.graph_service import build_canonical_smallest_code, build_csp_graph, \
    compute_right_most_path_labels


class Graph(Edges, Nodes, AdjacencyList, AdjacencyMatrix, Clusters):
    """A class to represent a directed graph with labels for the edges and nodes.
    """

    def __init__(self, nodes: pd.DataFrame, edges: pd.DataFrame) -> None:
        """Constructor

        :param pd.DataFrame nodes: Contains all nodes of the graph. Should be in the following format: id|label
        :param pd.DataFrame edges: Contains all edges of the graph. Should be in the following format: id|source|target|label
        """

        # edges of the graph (pd.DataFrame)
        self.__edges = Edges(edges)

        # nodes of the graph (pd.DataFrame)
        self.__nodes = Nodes(nodes, self.edges)

        # generate edges with node labels and all unique edges for the graph
        self.__edges.generate_edges_with_node_labels(self.nodes)
        self.__edges.generate_unique_edges()

        # adjacency matrix of the graph (pd.DataFrame)
        self.__adjacency_matrix = AdjacencyMatrix(self.nodes_ids, self.edges_ids, self.edges)

        # adjacency list of the graph (pd.DataFrame)
        self.__adjacency_list = AdjacencyList(self.nodes_ids, self.edges, self.nodes,
                                              self.node_degrees)

        # initial clusters: nodes clustered by label and degrees (pd.DataFrame)
        self.__clusters = Clusters(self.nodes, self.node_degrees, self.adjacency_list)

        # canonical code of the graph build based on the final clusters
        self.__canonical_code = build_canonical_smallest_code(self.clusters_by_adjacency_list)

        # the data structure needed to solve the csp problem
        self.__csp_graph = build_csp_graph(self.nodes, self.nodes_ids, self.node_degrees, self.adjacency_list)

    @property
    def adjacency_matrix(self) -> pd.DataFrame:
        """Adjacency matrix of the graph (ids of nodes and edges)

        :return: adjacency_matrix
        :rtype: pd.DataFrame
        """
        return self.__adjacency_matrix.adjacency_matrix

    @property
    def size(self) -> int:
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
    def unique_edges(self):
        return self.__edges.unique_edges

    @property
    def edges_ids(self) -> list:
        """List of all ids of the edges

        :return: edges_ids
        :rtype: list
        """
        return self.__edges.edges_ids

    @property
    def edges_with_node_labels(self) -> pd.DataFrame:
        """All edges of the graph with labels for the source and target node

        :return: edges_with_node_labels
        :rtype: pd.DataFrame
        """
        return self.__edges.edges_with_node_labels

    @property
    def adjacency_list(self) -> pd.DataFrame:
        """Adjacency list of the graph

        :return: adjacency_list
        :rtype: pd.DataFrame
        """
        return self.__adjacency_list.adjacency_list

    @property
    def node_degrees(self) -> pd.DataFrame:
        """Degrees of all nodes

        :return: node_degrees
        :rtype: pd.DataFrame
        """
        return self.__nodes.node_degrees

    @property
    def clusters_by_label_and_degree(self) -> pd.DataFrame:
        """Different clusters of nodes based on their labels, in-/outgoing degrees

        :return: clusters_by_label_and_degree
        :rtype: pd.DataFrame
        """
        return self.__clusters.clusters_by_label_and_degree

    @property
    def clusters_by_adjacency_list(self) -> pd.DataFrame:
        """Different clusters of nodes based on their labels, in-/outgoing degrees and adjacency lists

        :return: clusters_by_adjacency_list
        :rtype: pd.DataFrame
        """
        return self.__clusters.clusters_by_adjacency_list

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
