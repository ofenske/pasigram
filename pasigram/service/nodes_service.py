import pandas as pd


def compute_node_ids(nodes: pd.DataFrame) -> list:
    """Method for computing the ids of all nodes

    Parameters
    ----------
    nodes : pd.DataFrame
        Contains all nodes.

    Returns
    -------
    list
        A list with all ids of the nodes
    """
    return list(nodes.index)


def compute_node_degrees(node_ids: list, edges: pd.DataFrame) -> pd.DataFrame:
    """Method for computing the indegree and outdegree for every node in a graph

    Parameters
    ----------
    node_ids : list
        Contains all ids of the nodes
    edges : pd.DataFrame
        Contains all edges

    Returns
    -------
    DataFrame
        Format: Indegree|Outdegree
        index = node_ids
    """
    node_degrees = pd.DataFrame(index=node_ids, columns=['Indegree', 'Outdegree'])
    for i in range(0, len(node_ids)):
        current_node_id = node_ids[i]
        current_node_indegree = 0
        current_node_outdegree = 0

        # calculate outgoing node degree
        current_node_outdegree += len(edges[edges['source'] == current_node_id])

        # calculate ingoing node degrees
        current_node_indegree += len(edges[edges['target'] == current_node_id])

        # assign node degree to node
        node_degrees.loc[current_node_id]['Indegree'] = current_node_indegree
        node_degrees.loc[current_node_id]['Outdegree'] = current_node_outdegree

    return node_degrees
