import pandas as pd
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

        # ids of all nodes of the graph (list)
        self.__node_ids = self.__build_node_ids()
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
        graph = pd.DataFrame(index=self.__node_ids, columns=self.__node_ids)

        # iterate over all edges of the graph to build adjacency matrix
        for i in range(0, len(self.__edges)):
            # get source and target node of an edge
            source_node = self.__edges.iloc[i][1]
            target_node = self.__edges.iloc[i][2]

            # insert entry to matrix
            graph.loc[source_node][target_node] = self.__edges.iloc[i]['id']

        return graph

    def __build_adjacency_list(self) -> pd.DataFrame:
        """ Method which build the adjacency lists of all nodes.
        Notation: index: nodeId, neighbours: [[edgelabel, neighbourVertexLabel, neighbourVertexDegree], ...]

        Returns
        -------
        pd.DataFrame
        """

        # initialize adjacency list
        adjacency_list = pd.DataFrame(index=self.__node_ids, columns=["neighbours"])

        # iterate over all nodes of the graph to build adjacency list
        for i in range(0, len(self.__nodes)):
            # get id of the current node
            current_node_id = self.__nodes.iloc[i]['id']

            # initialize new entry for the current node
            adjacency_list.loc[current_node_id]['neighbours'] = []

            # Todo: use df[df[source == current_node_id]] instead of for-loop (more efficient?)
            # iterate over all edges of the graph to get all neighbours of the current node
            for j in range(0, len(self.__edges)):
                # if node_id is source of current edge
                if self.__edges.iloc[j]["source"] == current_node_id:
                    # get label of the current edge
                    edge_label = self.__edges.iloc[j]["label"]

                    # get id, label, degree of the neighbour node of the current node for the current edge
                    neighbour_vertex_id = self.__edges.iloc[j]["target"]
                    neighbour_vertex_label_list = self.__nodes[self.__nodes["id"] == neighbour_vertex_id]["label"]
                    neighbour_vertex_label = neighbour_vertex_label_list.iloc[0]
                    neighbour_vertex_degree = self.__node_degrees.loc[neighbour_vertex_id]["degree"]

                    # append edge label, neighbour node label, neighbour node degree  to the neighbour list of the current node
                    adjacency_list['neighbours'][current_node_id].append(
                        [edge_label, neighbour_vertex_label, neighbour_vertex_degree])

        # sort neighbour_list for each node
        for i in range(0, len(adjacency_list)):
            sorted_list = sorted(adjacency_list.iloc[i]['neighbours'])
            adjacency_list.iloc[i]['neighbours'] = sorted_list

        return adjacency_list

    def __build_node_ids(self) -> list:
        """

        Returns
        -------
        list
        """
        node_ids = []
        for i in range(0, len(self.__nodes)):
            node_ids.append(self.__nodes.iloc[i]['id'])
        return node_ids

    def __calculate_node_degrees(self) -> pd.DataFrame:
        """

        Returns
        -------
        pd.DataFrame

        """
        node_degrees = pd.DataFrame(index=self.__node_ids, columns=['degree'])
        for i in range(0, len(self.__node_ids)):
            current_node_id = self.__nodes.iloc[i]['id']
            current_node_degree = 0
            current_node = self.__matrix.loc[current_node_id]
            for element in current_node:
                if pd.isnull(element) == False:
                    current_node_degree += 1
            node_degrees['degree'][current_node_id] = current_node_degree
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
    def get_node_ids(self) -> list:
        return self.__node_ids, type(self.__node_ids)

    @property
    def get_node_degrees(self) -> pd.DataFrame:
        return self.__node_degrees

    @property
    def get_canonical_code(self) -> str:
        return self.__canonical_code
