import pandas as pd


def compute_adjacency_matrix(node_ids: list, edge_ids: list, edges: pd.DataFrame) -> pd.DataFrame:
    """Builds the adjacency matrix.

    Parameters
    ----------
    node_ids : list
        List with all node ids.
    edge_ids : list
        List with all edge ids.
    edges : pd.DataFrame
        DataFrame with all edges.

    Returns
    -------
    Matrix as DataFrame
    """
    # initialize the adjacency matrix
    graph = pd.DataFrame(index=node_ids, columns=node_ids)

    # iterate over all edges of the graph to build adjacency matrix
    for i in range(0, len(edge_ids)):
        # get source and target node of an edge
        edge_id = edge_ids[i]
        source_node = edges.loc[edge_id]['source']
        target_node = edges.loc[edge_id]['target']

        # insert entry to matrix
        graph.loc[source_node][target_node] = edge_id

    return graph