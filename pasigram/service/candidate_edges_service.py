import pandas as pd


def compute_edges_with_node_labels(edge_ids: list, edges: pd.DataFrame, nodes: pd.DataFrame) -> pd.DataFrame:
    edges_with_node_labels = pd.DataFrame(columns=['source', 'target', 'label'], index=edge_ids)

    for i in range(0, len(edge_ids)):
        current_edge_id = edge_ids[i]
        current_edge_label = edges.loc[current_edge_id]['label']
        current_edge_source_node_id = edges.loc[current_edge_id]['source']
        current_edge_target_node_id = edges.loc[current_edge_id]['target']
        current_edge_source_node_label = nodes.loc[current_edge_source_node_id]['label']
        current_edge_target_node_label = nodes.loc[current_edge_target_node_id]['label']

        edges_with_node_labels.loc[current_edge_id] = [current_edge_source_node_label,
                                                       current_edge_target_node_label, current_edge_label]

    return edges_with_node_labels
