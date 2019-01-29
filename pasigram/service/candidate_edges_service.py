import pandas as pd


def compute_edges_with_node_labels(edge_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame) -> pd.DataFrame:
    edges_with_node_labels = pd.DataFrame(columns=['source', 'target', 'label', 'key'], index=edge_ids)

    for i in range(0, len(edge_ids)):
        current_edge_id = edge_ids[i]
        current_edge_label = edges.loc[current_edge_id]['label']
        current_edge_source_node_id = edges.loc[current_edge_id]['source']
        current_edge_target_node_id = edges.loc[current_edge_id]['target']
        current_edge_source_node_label = nodes.loc[current_edge_source_node_id]['label']
        current_edge_target_node_label = nodes.loc[current_edge_target_node_id]['label']
        current_edge_key = str(current_edge_source_node_label) + str(current_edge_target_node_label) + str(
            current_edge_label)

        edges_with_node_labels.loc[current_edge_id] = [current_edge_source_node_label,
                                                       current_edge_target_node_label, current_edge_label,
                                                       current_edge_key]

    return edges_with_node_labels


def compute_frequent_edges(min_support: int, edges: pd.DataFrame) -> pd.DataFrame:
    frequent_edges = pd.DataFrame(columns=['source', 'target', 'label', 'frequency'])
    # get the unique keys from all edges
    edges_keys = edges['key'].unique()

    # iterate over all unique edge keys
    for i in range(0, len(edges_keys)):
        current_edge_key = edges_keys[i]
        # get all edges with current_edge_key
        candidates = edges[edges['key'] == current_edge_key]

        # check if candidates meet the min_support
        if len(candidates) >= min_support:
            # get label of source node
            source_node = edges.iloc[0]['source']
            # get label of target node
            target_node = edges.iloc[0]['target']
            # get label of edge
            edge_label = edges.iloc[0]['label']
            # get frequency of current edge
            frequency = len(candidates)
            # new entry in final dataframe
            frequent_edges.loc[current_edge_key] = [source_node, target_node, edge_label, frequency]

    return frequent_edges


def compute_edge_ids(edges: pd.DataFrame) -> list:
    return list(edges.index)
