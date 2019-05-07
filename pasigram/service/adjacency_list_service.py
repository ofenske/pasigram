import pandas as pd


def compute_adjacency_list(node_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame,
                           node_degrees: pd.DataFrame) -> pd.DataFrame:
    """

    :param list node_ids: List with all node ids.
    :param pd.DataFrame edges: DataFrame with all edges
    :param pd.DataFrame nodes: DataFrame with all nodes
    :param pd.DataFrame node_degrees: DataFrame with all node degrees
    :return: adjacency_list for all nodes of the graph
        Format: node_id | ingoing_neighbours | outgoing_neighbours
        *_neighbours = [edge_label, neighbour_vertex_label, neighbour_vertex_index, neighbour_vertex_indegree, neighbour_vertex_outdegree]
    :rtype: pd.DataFrame
    """

    # initialize adjacency list
    adjacency_list = pd.DataFrame(index=node_ids, columns=["ingoing_neighbours", "outgoing_neighbours"])

    # iterate over all nodes of the graph to build adjacency list
    for i in range(0, len(node_ids)):
        # get id of the current node
        current_node_id = node_ids[i]

        # initialize new entry for the current node
        adjacency_list.loc[current_node_id]['outgoing_neighbours'] = []

        # get all outgoing edges for the current node as pd.DataFrame (id|source|target|label)
        outgoing_edges = edges[edges['source'] == current_node_id]

        # iterate over all edges of the list 'outgoing_edges' to build the adjacency list for the current node
        for j in range(0, len(outgoing_edges)):
            # get label of the current edge
            edge_label = outgoing_edges.iloc[j]["label"]

            # get id, label, degree of the neighbour node of the current node for the current edge
            neighbour_vertex_id = outgoing_edges.iloc[j]["target"]
            neighbour_vertex_label = nodes.loc[neighbour_vertex_id]["label"]
            neighbour_vertex_indegree = node_degrees.loc[neighbour_vertex_id]["indegree"]
            neighbour_vertex_outdegree = node_degrees.loc[neighbour_vertex_id]["outdegree"]

            # append edge label, neighbour node label, neighbour node degree  to the neighbour list of the current node
            adjacency_list['outgoing_neighbours'][current_node_id].append(
                [edge_label, neighbour_vertex_label, neighbour_vertex_id, neighbour_vertex_indegree, neighbour_vertex_outdegree])

        # do the same stuff for ingoing_edges

        # initialize new entry for the current node
        adjacency_list.loc[current_node_id]['ingoing_neighbours'] = []

        # get all ingoing edges for the current node as pd.DataFrame (id|source|target|label)
        ingoing_edges = edges[edges['target'] == current_node_id]

        # iterate over all edges of the list 'ingoing_edges' to build the adjacency list for the current node
        for j in range(0, len(ingoing_edges)):
            # get label of the current edge
            edge_label = ingoing_edges.iloc[j]["label"]

            # get id, label, degree of the neighbour node of the current node for the current edge
            neighbour_vertex_id = ingoing_edges.iloc[j]["source"]
            neighbour_vertex_label = nodes.loc[neighbour_vertex_id]["label"]
            neighbour_vertex_indegree = node_degrees.loc[neighbour_vertex_id]["indegree"]
            neighbour_vertex_outdegree = node_degrees.loc[neighbour_vertex_id]["outdegree"]

            # append edge label, neighbour node label, neighbour node degree  to the neighbour list of the current node
            adjacency_list['ingoing_neighbours'][current_node_id].append(
                [edge_label, neighbour_vertex_label, neighbour_vertex_id, neighbour_vertex_indegree,
                 neighbour_vertex_outdegree])

    # sort neighbour_list for each node
    for i in range(0, len(adjacency_list)):
        sorted_outgoing_list = sorted(adjacency_list.iloc[i]['outgoing_neighbours'])
        adjacency_list.iloc[i]['outgoing_neighbours'] = sorted_outgoing_list
        sorted_ingoing_list = sorted(adjacency_list.iloc[i]['ingoing_neighbours'])
        adjacency_list.iloc[i]['ingoing_neighbours'] = sorted_ingoing_list

    return adjacency_list
