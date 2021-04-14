import pandas as pd


def compute_node_ids(nodes: pd.DataFrame) -> list:
    """Method for computing the ids of all nodes

    :param pd.DataFrame nodes: Contains all nodes of the graph
    :return: A list with all ids of the nodes
    :rtype: list
    """

    return list(nodes.index)
