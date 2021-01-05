import pandas as pd
import numpy as np

########################################################################################################################
"""This block includes all methods which are necessary to compute the canonical smallest code for a graph.
"""


def build_canonical_smallest_code(csp_graph: pd.DataFrame) -> str:
    """Method for building the canonical code of a graph.

    :param pd.DataFrame csp_graph: The csp_graph of the graph.
    :return: The canonical code for the graph
    :rtype: str
    """
    # todo: Code commenting
    canonical_code = ''
    node_codes = {}

    # iterate over all nodes in the csp_graph
    for i in range(0, len(csp_graph)):
        node = csp_graph.iloc[i]

        # get label, ind-/outdegree, in-/outgoing neighbours for the current_node
        node_label = str(int(node.label))
        node_indegree = str(int(len(node.ingoing_neighbours)))
        node_outdegree = str(int(len(node.outgoing_neighbours)))
        node_ingoing_neighbours: list[list] = node.ingoing_neighbours
        node_outgoing_neighbours: list[list] = node.outgoing_neighbours

        # compute the unique code for every node and append them to a dict
        node_code: str = node_label + node_indegree + node_outdegree

        for j in range(len(node_ingoing_neighbours)):
            node_code += str(int(node_ingoing_neighbours[j][0])) + str(int(node_ingoing_neighbours[j][1]))

        for j in range(len(node_outgoing_neighbours)):
            node_code += str(int(node_outgoing_neighbours[j][0])) + str(int(node_outgoing_neighbours[j][1]))

        if node_code in list(node_codes.keys()):
            node_codes.update({node_code: node_codes[node_code] + 1})

        else:
            node_codes.update({node_code: 1})

    # concatenate all node codes to get the final canonical code for the graph
    node_codes_keys = list(node_codes.keys())
    node_codes_list = []
    for key in node_codes_keys:
        node_name = key + '#' + str(node_codes[key]) + '#'
        node_codes_list.append(node_name)

    sorted_node_nodes_list = sorted(node_codes_list)

    for key in sorted_node_nodes_list:
        canonical_code += key

    return canonical_code


########################################################################################################################
"""This block computes just the labels of all nodes in the right most path
"""


def compute_right_most_path_labels(right_most_path: list, nodes: pd.DataFrame) -> list:
    """Method for computing the labels of all nodes on the right-most-path.

    :param list right_most_path: A list of all nodes on the right-most-path
    :param pd.DataFrame nodes: All nodes of the graph
    :return: A list with all labels of all nodes on the right-most-path
    :rtype: list
    """
    right_most_path_labels = []

    for i in range(0, len(right_most_path)):
        current_node_label = nodes.loc[right_most_path[i]]['label']
        right_most_path_labels.append(current_node_label)

    return right_most_path_labels


########################################################################################################################
"""This block includes all methods which are necessary to compute the csp graph representation. 
It's mostly used to generate the csp graph of the (large) input graph with a multiple of joins of different data sets.
To generate the csp graph of the initial patterns/new candidates other methods are used (due to performance reasons).
"""


def build_csp_graph(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Method to compute the csp graph.

    :param pd.DataFrame nodes: The set of nodes of the graph
    :param pd.DataFrame edges: The set of edges of the graph
    :return: CSP graph
    :rtype: pd.DataFrame
    """
    print('Build outgoing neighbour list!')
    # merge nodes with edges to get neighbour edges/nodes
    outgoing_nl = nodes.merge(edges, left_index=True, right_on='source', how='left').set_index(['source']).dropna(
        axis='index')
    # merge outgoing_nl with nodes to get the labels of the neighbour nodes
    outgoing_nl = outgoing_nl.merge(nodes, left_on='target', right_index=True, how='left')
    # append new column to outgoing_nl which includes a list [edge_label, neighbour_node_label, neighbour_node_id]
    outgoing_nl['outgoing_neighbours'] = outgoing_nl[['label_y', 'label', 'target']].values.tolist()
    # drop all unnecessary columns (label of neighbour node, id of neighbour node, label of source node)
    outgoing_nl.drop(axis='columns', labels=['target', 'label_y', 'label'], inplace=True)
    # group all nodes with the same id and join their 'outgoing_neighbours' columns with each other
    outgoing_nl = outgoing_nl.groupby(outgoing_nl.index)['outgoing_neighbours'].apply(list).apply(sorted)

    print('Build ingoing neighbour list!')
    # merge nodes with edges to get neighbour edges/nodes
    ingoing_nl = nodes.merge(edges, left_index=True, right_on='target', how='left').set_index(['target']).dropna(
        axis='index')
    # merge ingoing_nl with nodes to get the labels of the neighbour nodes
    ingoing_nl = ingoing_nl.merge(nodes, left_on='source', right_index=True, how='left')
    # append new column to ingoing_nl which includes a list [edge_label, neighbour_node_label, neighbour_node_id]
    ingoing_nl['ingoing_neighbours'] = ingoing_nl[['label_y', 'label', 'source']].values.tolist()
    # drop all unnecessary columns (label of neighbour node, id of neighbour node, label of source node)
    ingoing_nl.drop(axis='columns', labels=['source', 'label_y', 'label'], inplace=True)
    # group all nodes with the same id and join their 'ingoing_neighbours' columns with each other
    ingoing_nl = ingoing_nl.groupby(ingoing_nl.index)['ingoing_neighbours'].apply(list).apply(sorted)

    print('Merge ingoing and outgoing neighbours into csp graph!')
    csp_graph = pd.DataFrame(nodes.label, columns=['label'], index=list(nodes.index))
    csp_graph = csp_graph.merge(ingoing_nl, left_index=True, right_index=True, how='left')
    csp_graph = csp_graph.merge(outgoing_nl, left_index=True, right_index=True, how='left')
    print('Replace NaN values in neighbour columns!')
    csp_graph[['ingoing_neighbours', 'outgoing_neighbours']] = csp_graph[
        ['ingoing_neighbours', 'outgoing_neighbours']].applymap(replace_nan)
    print('Compute in- and outdegree of nodes!')
    csp_graph[['indegree', 'outdegree']] = csp_graph[['ingoing_neighbours', 'outgoing_neighbours']].applymap(len)
    csp_graph = csp_graph[['label', 'indegree', 'outdegree', 'ingoing_neighbours', 'outgoing_neighbours']]

    return csp_graph


def replace_nan(x) -> list:
    """Helper method to replace all NaN values in a dataframe. Is used by applymap method for the respective dataframe.

    :param x: The value of the respective column which one ant to proof of NaN
    :return: A list with the values (empty list for NaN values)
    :rtype: list
    """
    if x is np.nan:
        return []
    else:
        return x


########################################################################################################################
"""This block includes all methods which are used to compute the csp graph for the initial candidates.
WARNING: this approach to build the csp graph is very slow for big graphs, but faster than the join-based approach for
building the csp graph for small graphs (with only one edge). 
"""


def create_initial_csp_graph(keyset: list, nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Method to compute the csp graph for a given set of edges and nodes

    :param keyset: Keys of all nodes
    :param nodes: Set of all nodes of the graph
    :param edges: Set of all edges of the graph
    :return: Csp graph
    :rtype: pd.DataFrame
    """
    csp_graph = pd.DataFrame(
        columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours', 'outgoing_neighbours'])

    # iterate over all elements of 'clusters_by_adjacency_list'
    for i in range(0, len(keyset)):
        # get node id of the current node
        node_id = keyset[i]

        # get label, indegree, outdegree and frequency out of 'node'
        node_label = nodes.at[node_id, 'label']
        # get adjacency_list of node
        node_adjacency_list: dict = compute_adjacency_lists(node_id, nodes, edges)
        # get neighbour list out of 'node'
        ingoing_neighbour_list = sorted(node_adjacency_list['ingoing_neighbours'])
        node_indegree = len(ingoing_neighbour_list)
        # get neighbour list out of 'node'
        outgoing_neighbour_list = sorted(node_adjacency_list['outgoing_neighbours'])
        node_outdegree = len(outgoing_neighbour_list)

        # insert all entries for the current node into 'csp_graph'
        csp_graph.at[node_id] = [node_label, node_indegree, node_outdegree, ingoing_neighbour_list,
                                 outgoing_neighbour_list]

    return csp_graph


def compute_adjacency_lists(current_node_id: int, nodes: pd.DataFrame, edges: pd.DataFrame) -> dict:
    """Method to compute the adjacency list for a node.

    :param int current_node_id: The id of the node for which one want to compute the adjacency list
    :param pd.DataFrame nodes: The set of all nodes of the graph
    :param pd.DataFrame edges: The set of all edges of the graph
    :return: A dictionary with the ingoing and outgoing neighbours of the node
    :rtype: dict
    """
    adjacency_list = {}
    outgoing_neighbours = []
    ingoing_neighbours = []

    # compute ingoing and outgoing edges for the node
    outgoing_edges: pd.DataFrame = edges[edges['source'] == current_node_id]
    ingoing_edges: pd.DataFrame = edges[edges['target'] == current_node_id]

    # set the iteration length
    if len(outgoing_edges) > len(ingoing_edges):
        iterator = len(outgoing_edges)
    else:
        iterator = len(ingoing_edges)

    # iterate over all ingoing and outgoing edges
    for i in range(iterator):
        if i < len(outgoing_edges):
            # get label of the current edge
            edge_label = outgoing_edges.iloc[i]["label"]

            # get id, label of the neighbour node of the current node for the current edge
            neighbour_vertex_id = outgoing_edges.iloc[i]["target"]
            neighbour_vertex_label = nodes.loc[neighbour_vertex_id]["label"]
            outgoing_neighbours.append([edge_label, neighbour_vertex_label, neighbour_vertex_id])

        if i < len(ingoing_edges):
            # get label of the current edge
            edge_label = ingoing_edges.iloc[i]["label"]

            # get id, label of the neighbour node of the current node for the current edge
            neighbour_vertex_id = ingoing_edges.iloc[i]["source"]
            neighbour_vertex_label = nodes.loc[neighbour_vertex_id]["label"]
            ingoing_neighbours.append([edge_label, neighbour_vertex_label, neighbour_vertex_id])

    # append everything to the adjacency list of the node
    adjacency_list.update({'outgoing_neighbours': outgoing_neighbours,
                           'ingoing_neighbours': ingoing_neighbours})

    return adjacency_list


########################################################################################################################
"""This block includes all methods which are used to extend an existing csp graph of a graph object, if a new edge 
is added. It's unimportant if the edges comes with one or zero new nodes. Logic for all cases are encapsulated 
in the methods. This approach follows an dynamic programming approach, where one don't have to compute everything new,
but just add the new pieces (in that case the new edge (and perhaps the new node)). 
"""


def extend_csp_graph(csp_graph: pd.DataFrame, new_added_edge: dict, nodes: pd.DataFrame) -> pd.DataFrame:
    """Method to extend an existing csp graph with a new edge (and the corresponding nodes)

    :param pd.DataFrame csp_graph: The csp graph of the respective graph object
    :param dict new_added_edge: The newly added edge
    :param pd.DataFrame nodes: The set of all nodes of the graph
    :return: Extended csp graph
    :rtype: pd.DataFrame
    """
    # get the source and target node of the new edge
    source_node = int(new_added_edge['parent_node_id'])
    target_node = int(new_added_edge['child_node_id'])

    # if the source node is already in csp graph included -> edit it's 'outdegree' and 'outgoing_neighbours'
    if source_node in list(csp_graph.index):
        csp_graph.loc[source_node, 'outdegree'] += 1
        outgoing_neighbours = csp_graph.loc[source_node]['outgoing_neighbours'].copy()
        outgoing_neighbours.append([new_added_edge['edge_label'], nodes.loc[target_node]['label'], target_node])
        new_outgoing_neighbours = sorted(outgoing_neighbours)
        csp_graph.at[source_node, 'outgoing_neighbours'] = new_outgoing_neighbours

    # if source node isn't already in the csp graph included -> add it completely new to the csp graph
    else:
        source_node_label = nodes.at[source_node, 'label']
        outgoing_neighbours = [[new_added_edge['edge_label'], nodes.loc[target_node]['label'], target_node]]
        csp_graph.at[source_node] = [source_node_label, 0, 1, [], outgoing_neighbours]

    # if the target node is already in csp graph included -> edit it's 'indegree' and 'ingoing_neighbours'
    if target_node in list(csp_graph.index):
        csp_graph.loc[target_node, 'indegree'] += 1
        ingoing_neighbours = csp_graph.loc[target_node]['ingoing_neighbours'].copy()
        ingoing_neighbours.append([new_added_edge['edge_label'], nodes.loc[source_node]['label'], source_node])
        new_ingoing_neighbours = sorted(ingoing_neighbours)
        csp_graph.at[target_node, 'ingoing_neighbours'] = new_ingoing_neighbours

    # if target node isn't already in the csp graph included -> add it completely new to the csp graph
    else:
        target_node_label = nodes.loc[target_node]['label']
        ingoing_neighbours = [[new_added_edge['edge_label'], nodes.loc[source_node]['label'], source_node]]
        csp_graph.at[target_node] = [target_node_label, 1, 0, ingoing_neighbours, []]

    return csp_graph


########################################################################################################################
"""This block includes all methods which are necessary to do a dictionary compression for the nodes and edges set 
of a graph. There labels will be replaced by numbers and the mappings are saved in a dictionary (for both - edges 
and nodes). This will compress the graph in size and will lead to a better performance of the whole algorithm. 
This is mainly used to compress the input graph, because all subgraphs will be generated out of the input graph. 
"""


def dictionary_compression(nodes: pd.DataFrame, edges: pd.DataFrame) -> list:
    """Method to apply a dictionary compression on the edges and nodes DataFrames

    :param pd.DataFrame nodes: Set of all nodes of the graph
    :param pd.DataFrame edges: Set of all edges of the graph
    :return: A set with dictionaries for the node and edges labels, and the new compressed nodes and edges sets.
    :rtype: list[dict, dict, pd.DataFrame, pd.DataFrame]
    """
    # get the unique node and edge labels
    unique_node_labels: list = list(nodes.label.unique()).copy()
    unique_edge_labels: list = list(edges.label.unique()).copy()

    # create dictionaries for the node and edge labels
    # key = node/edge label
    # value = random number (int)
    node_dict: dict = dict(zip(unique_node_labels, range(0, len(unique_node_labels))))
    edge_dict: dict = dict(zip(unique_edge_labels, range(0, len(unique_edge_labels))))

    # replace the values of edge/node labels with the corresponding in the dictionary
    nodes['label'] = nodes['label'].map(node_dict)
    edges['label'] = edges['label'].map(edge_dict)

    return [node_dict, edge_dict, nodes, edges]
