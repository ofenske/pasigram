import pandas as pd


def compute_edges_with_node_labels(edge_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame) -> pd.DataFrame:
    """Method for computing a DataFrame with node labels as entries for the source and target columns.

    :param list edge_ids: List with all ids for the edges of the input graph
    :param pd.DataFrame edges: Contains all edges of the input graph
    :param pd.DataFrame nodes: Contains all nodes of the input graph
    :return: Contains all edges with labels for source and target nodes.
        Format: source|target|label|key
        index = numerical
    :rtype: pd.DataFrame
    """

    edges_with_node_labels = pd.DataFrame(columns=['source', 'target', 'label', 'key'], index=edge_ids)

    # iterate over all edges
    for i in range(0, len(edge_ids)):
        # get the current edge id
        current_edge_id = edge_ids[i]
        # get the current edge label
        current_edge_label = edges.loc[current_edge_id]['label']

        # get the current edge source and target node id
        current_edge_source_node_id = edges.loc[current_edge_id]['source']
        current_edge_target_node_id = edges.loc[current_edge_id]['target']

        # get the current edge source and target node label
        current_edge_source_node_label = nodes.loc[current_edge_source_node_id]['label']
        current_edge_target_node_label = nodes.loc[current_edge_target_node_id]['label']

        # get the current edge key
        current_edge_key = str(current_edge_source_node_label) + str(current_edge_target_node_label) + str(
            current_edge_label)

        # append the current edge to the final DataFrame
        edges_with_node_labels.loc[current_edge_id] = [current_edge_source_node_label,
                                                       current_edge_target_node_label, current_edge_label,
                                                       current_edge_key]

    return edges_with_node_labels


def compute_unique_edges(edges_with_node_labels: pd.DataFrame) -> pd.DataFrame:
    """Method for computing the unique edges of a graph.

    :param pd.DataFrame edges_with_node_labels: Contains all edges with node labels as entries for the source and target columns of the input graph
    :return: Contains all unique edges in the following format: source|target|label|frequency
        index = entry of 'key'-column of edges_with_node_labels (=source_node_label+target_node_label+edge_label)
    :rtype:pd.DataFrame
    """

    # todo: refactor column names: source -> source_node_label, target->target_node_label, label->edge_label
    frequent_edges = pd.DataFrame(columns=['source', 'target', 'label', 'frequency'])
    # get the unique keys from all edges
    edges_keys = edges_with_node_labels['key'].unique()

    # iterate over all unique edge keys
    for i in range(0, len(edges_keys)):
        current_edge_key = edges_keys[i]
        # get all edges with current_edge_key
        candidates = edges_with_node_labels[edges_with_node_labels['key'] == current_edge_key]

        # get label of source node
        source_node = candidates.iloc[0]['source']
        # get label of target node
        target_node = candidates.iloc[0]['target']
        # get label of edge
        edge_label = candidates.iloc[0]['label']
        # get frequency of current edge
        frequency = len(candidates)
        # new entry in final dataframe
        frequent_edges.loc[current_edge_key] = [source_node, target_node, edge_label, frequency]

    return frequent_edges


def compute_edge_ids(edges: pd.DataFrame) -> list:
    """Method for computing a list with ids of all edges in it

    :param pd.DataFrame edges: Contains all edges
    :return: A list with all ids of the edges.
    :rtype: list
    """

    return list(edges.index)


def compute_frequent_edges(unique_edges: pd.DataFrame, min_support: int) -> pd.DataFrame:
    """Method for computing all frequent edges of the graph

    :param pd.DataFrame unique_edges: Conatins all uniqie edges
    :param int min_support: The minimum support the edges have to meet
    :return: Format: source|target|label|frequency
        index = index of unique_edges (=source_node_label+target_node_label+edge_label)
    :rtype: pd.DataFrame
    """

    # todo: refactor column names: source -> source_node_label, target->target_node_label, label->edge_label
    frequent_edges = pd.DataFrame(columns=['source', 'target', 'label', 'frequency'])
    key_set = list(unique_edges.index)

    for i in range(0, len(key_set)):
        current_key = key_set[i]
        if unique_edges.loc[current_key]['frequency'] >= min_support:
            frequent_edges.loc[current_key] = unique_edges.loc[current_key]

    return frequent_edges
