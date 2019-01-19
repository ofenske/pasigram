import pandas as pd
import numpy as np
from pasigram.datastructures.cam import cluster_nodes_by_adjacency_list, cluster_nodes_by_label_and_degree, \
    build_canonical_smallest_code


class Graph:
    """A class to represent a directed graph with labels for the edges and nodes.

    ...

    Attributes
    ----------
        nodes : pd.DataFrame
            The nodes of the graph (id, label)
        node_ids : List
            contains all node ids
        edges : pd.DataFrame
            The edges of the graph (id, source, target)
        matrix : pd.DataFrame
            adjacency matrix of the graph (ids of nodes and edges)


    Methods
    -------
        build_graph(self)
            Method for building the adjacency  matrix of the graph
        build_adjacency_list(self)
            Method for building the adjacency list of the nodes
        build_node_ids(self)
            Method for building a list of node ids
        calculate_node_degrees(self)
            Method for calculating the outgoing degrees of all nodes

    """

    def __init__(self, nodes: pd.DataFrame, edges: pd.DataFrame) -> object:
        """

        Parameters
        ----------
        nodes : DataFrame
            Contains all nodes of the graph.
        edges : DataFrame
            Contains all edges of the graph.

        Returns
        -------
        object
        """
        # nodes of the graph (pd.DataFrame)
        self.__nodes = nodes

        # edges of the graph (pd.DataFrame)
        self.__edges = edges

        # adjacency matrix of the graph (pd.DataFrame)
        self.__matrix = self.__build_graph()

        # degrees of all nodes of the graph (pd.DataFrame)
        self.__node_degrees = self.__calculate_node_degrees()

        # adjacency list of the graph (pd.DataFrame)
        self.__adjacency_list = self.__build_adjacency_list()

        # initial clusters: nodes clustered by label and degrees (pd.DataFrame)
        self.__inital_clusters = cluster_nodes_by_label_and_degree(self.__nodes, self.__node_degrees)

        # final clusters: nodes clustered by labels, degrees and adjacency list (pd.DataFrame)
        self.__final_clusters = cluster_nodes_by_adjacency_list(self.__inital_clusters, self.__adjacency_list)

        # canonical code of the graph build based on the final clusters
        self.__canonical_code = build_canonical_smallest_code(self.__final_clusters)

    def __build_graph(self) -> pd.DataFrame:
        """Builds the adjacency matrix.

        Returns
        -------
        DataFrame
        """
        # get the ids of all nodes
        node_ids = list(self.__nodes.index)

        # initialize the adjacency matrix
        graph = pd.DataFrame(index=node_ids, columns=node_ids)

        # get the ids of all edges
        edge_ids = list(self.__edges.index)

        # iterate over all edges of the graph to build adjacency matrix
        for i in range(0, len(edge_ids)):
            # get source and target node of an edge
            edge_id = edge_ids[i]
            source_node = self.__edges.loc[edge_id]['source']
            target_node = self.__edges.loc[edge_id]['target']

            # insert entry to matrix
            graph.loc[source_node][target_node] = edge_id

        return graph

    def __build_adjacency_list(self) -> pd.DataFrame:
        """ Method which build the adjacency lists of all nodes.
        Notation: index: nodeId, neighbours: [[edgelabel, neighbourVertexLabel, neighbourVertexDegree], ...]

        Returns
        -------
        pd.DataFrame
        """
        # get ids of all nodes
        node_ids = list(self.__nodes.index)

        # initialize adjacency list
        adjacency_list = pd.DataFrame(index=node_ids, columns=["neighbours"])

        # iterate over all nodes of the graph to build adjacency list
        for i in range(0, len(node_ids)):
            # get id of the current node
            current_node_id = node_ids[i]

            # initialize new entry for the current node
            adjacency_list.loc[current_node_id]['neighbours'] = []

            # get all outgoing edges for the current node as pd.DataFrame (id|source|target|label)
            outgoing_edges = self.__edges[self.__edges['source'] == current_node_id]

            # iterate over all edges of the list 'outgoing_edges' to build the adjacency list for the current node
            for j in range(0, len(outgoing_edges)):
                # get label of the current edge
                edge_label = outgoing_edges.iloc[j]["label"]

                # get id, label, degree of the neighbour node of the current node for the current edge
                neighbour_vertex_id = outgoing_edges.iloc[j]["target"]
                neighbour_vertex_label = self.__nodes.loc[neighbour_vertex_id]["label"]
                neighbour_vertex_indegree = self.__node_degrees.loc[neighbour_vertex_id]["Indegree"]
                neighbour_vertex_outdegree = self.__node_degrees.loc[neighbour_vertex_id]["Outdegree"]

                # append edge label, neighbour node label, neighbour node degree  to the neighbour list of the current node
                adjacency_list['neighbours'][current_node_id].append(
                    [edge_label, neighbour_vertex_label, neighbour_vertex_indegree, neighbour_vertex_outdegree])

        # sort neighbour_list for each node
        for i in range(0, len(adjacency_list)):
            sorted_list = sorted(adjacency_list.iloc[i]['neighbours'])
            adjacency_list.iloc[i]['neighbours'] = sorted_list

        return adjacency_list

    def __calculate_node_degrees(self) -> pd.DataFrame:
        """

        Returns
        -------
        pd.DataFrame

        """

        node_ids = list(self.__nodes.index)
        node_degrees = pd.DataFrame(index=node_ids, columns=['Indegree', 'Outdegree'])
        for i in range(0, len(node_ids)):
            current_node_id = node_ids[i]
            current_node_indegree = 0
            current_node_outdegree = 0

            # calculate outgoing node degree
            current_node_outdegree += len(self.__edges[self.__edges['source'] == current_node_id])

            # calculate ingoing node degrees
            current_node_indegree += len(self.__edges[self.__edges['target'] == current_node_id])

            # assign node degree to node
            node_degrees.loc[current_node_id]['Indegree'] = current_node_indegree
            node_degrees.loc[current_node_id]['Outdegree'] = current_node_outdegree

        return node_degrees

    @property
    def get_matrix(self) -> pd.DataFrame:
        return self.__matrix

    @property
    def get_nodes(self) -> pd.DataFrame:
        return self.__nodes

    @property
    def get_edges(self) -> pd.DataFrame:
        return self.__edges

    @property
    def get_adjacency_list(self) -> pd.DataFrame:
        return self.__adjacency_list

    @property
    def get_node_degrees(self) -> pd.DataFrame:
        return self.__node_degrees

    @property
    def get_canonical_code(self) -> str:
        return self.__canonical_code
