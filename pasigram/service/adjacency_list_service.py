import pandas as pd


def compute_adjacency_list(node_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame,
                           node_degrees: pd.DataFrame) -> pd.DataFrame:
    """

    Parameters
    ----------
    node_ids : list
        List with all node ids.
    edges : pd.DataFrame
        DataFrame with all edges.
    nodes : pd.DataFrame
        DataFrame with all nodes.
    node_degrees : pd.DataFrame
        DataFrame with all node degrees.

    Returns
    -------
    DataFrame in following format:
    node_id | neighbours
    neighbours = [edge_label, neighbour_vertex_label, neighbour_vertex_indegree, neighbour_vertex_outdegree]
    """
    # initialize adjacency list
    adjacency_list = pd.DataFrame(index=node_ids, columns=["neighbours"])

    # iterate over all nodes of the graph to build adjacency list
    for i in range(0, len(node_ids)):
        # get id of the current node
        current_node_id = node_ids[i]

        # initialize new entry for the current node
        adjacency_list.loc[current_node_id]['neighbours'] = []

        # get all outgoing edges for the current node as pd.DataFrame (id|source|target|label)
        outgoing_edges = edges[edges['source'] == current_node_id]

        # iterate over all edges of the list 'outgoing_edges' to build the adjacency list for the current node
        for j in range(0, len(outgoing_edges)):
            # get label of the current edge
            edge_label = outgoing_edges.iloc[j]["label"]

            # get id, label, degree of the neighbour node of the current node for the current edge
            neighbour_vertex_id = outgoing_edges.iloc[j]["target"]
            neighbour_vertex_label = nodes.loc[neighbour_vertex_id]["label"]
            neighbour_vertex_indegree = node_degrees.loc[neighbour_vertex_id]["Indegree"]
            neighbour_vertex_outdegree = node_degrees.loc[neighbour_vertex_id]["Outdegree"]

            # append edge label, neighbour node label, neighbour node degree  to the neighbour list of the current node
            adjacency_list['neighbours'][current_node_id].append(
                [edge_label, neighbour_vertex_label, neighbour_vertex_indegree, neighbour_vertex_outdegree])

    # sort neighbour_list for each node
    for i in range(0, len(adjacency_list)):
        sorted_list = sorted(adjacency_list.iloc[i]['neighbours'])
        adjacency_list.iloc[i]['neighbours'] = sorted_list

    return adjacency_list
