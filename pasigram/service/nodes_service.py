import pandas as pd


def compute_node_ids(nodes: pd.DataFrame) -> list:
    """Method for computing the ids of all nodes

    :param pd.DataFrame nodes: Contains all nodes of the graph
    :return: A list with all ids of the nodes
    :rtype: list
    """

    return list(nodes.index)


def compute_node_degrees(node_ids: list, edges: pd.DataFrame) -> pd.DataFrame:
    """Method for computing the indegree and outdegree for every node in a graph

    :param list node_ids: Contains all ids of the nodes
    :param pd.DataFrame edges: Contains all edges
    :return: Format: indegree|outdegree
        index = node_ids
    :rtype: pd.DataFrame
    """

    node_degrees = pd.DataFrame(index=node_ids, columns=['indegree', 'outdegree'])
    for i in range(0, len(node_ids)):
        current_node_id = node_ids[i]
        current_node_indegree = 0
        current_node_outdegree = 0

        # calculate outgoing node degree
        current_node_outdegree += len(edges[edges['source'] == current_node_id])

        # calculate ingoing node degrees
        current_node_indegree += len(edges[edges['target'] == current_node_id])

        # assign node degree to node
        node_degrees.loc[current_node_id]['indegree'] = current_node_indegree
        node_degrees.loc[current_node_id]['outdegree'] = current_node_outdegree

    return node_degrees
