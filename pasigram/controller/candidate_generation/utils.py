import pandas as pd
from pasigram.model.graph import *


def compute_right_most_path_nodes(right_most_path: list, edges: pd.DataFrame) -> list:
    """Method for computing a list with all nodes which are part of the right-most-path.

    Parameters
    ----------
    right_most_path : list
        A list with the ids of all edges of the right-most-path
    edges : pd.DataFrame
        DataFrame with all edges.

    Returns
    -------
    list
        A list with ids of all nodes of the right-most-path.
    """
    right_most_path_nodes = []

    # iterating over all edges of the right-most-path
    for i in range(0, len(right_most_path)):

        # get current edge id
        current_edge_id = right_most_path[i]

        # get source and target node ids
        source_node = edges.loc[current_edge_id]['source']
        target_node = edges.loc[current_edge_id]['target']

        # check if source or target node are already in the result list
        # todo: use map()-method instead of "not in" to check the above constraints -> better performance
        if source_node not in right_most_path_nodes:
            right_most_path_nodes.append(source_node)
        if target_node not in right_most_path_nodes:
            right_most_path_nodes.append(target_node)

    return right_most_path_nodes


def compute_relevant_edges(node: str, frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method to find all edges which contains node as the source

    Parameters
    ----------
    node : str
        The node which should be the source
    frequent_edges : pd.DataFrame
        DataFrame of frequent edges which could be relevant for node

    Returns
    -------
    DataFrame
        A DataFrame with all relevant edges for the node.
    """
    relevant_edges = frequent_edges[frequent_edges['source'] == node]
    return relevant_edges


def generate_new_candidate(candidate: Graph, new_edge: pd.Series, current_node_id: str) -> Graph:
    """Method for generating a new graph out of an existing graph and a new edge

    Parameters
    ----------
    candidate : Graph
        The frequent subgraph to use to generate the new candidate
    new_edge : pd.Series
        The edge we want to add to the existing subgraph.
    current_node_id : str
        The id of the node where we want to add the new edge.

    Returns
    -------
    Graph
        A Graph object of the new generated candidate.
    """
    # get the nodes and edges of the existing subgraph
    candidate_nodes = candidate.nodes
    candidate_edges = candidate.edges

    # get label,id of the target node of the new_edge
    target_node_label = new_edge.loc['target']
    target_node_id = str(len(candidate_nodes))

    # append the new node (target_node) to the existing nodes
    candidate_nodes.loc[target_node_id] = [target_node_label]

    # get the label of new_edge
    new_edge_label = new_edge.loc['label']

    # append new_edge to the existing edges
    candidate_edges.loc[len(candidate_edges)] = [current_node_id, target_node_id, new_edge_label]

    # initialize the new_candidate as a graph
    new_candidate = Graph(candidate_nodes, candidate_edges)

    # set the right_most_node of new_candidate
    new_candidate.set_right_most_node = str(len(candidate.nodes) - 1)

    # set the root_node of  new_candidate
    new_candidate.set_root_node = candidate.root_node

    # todo: set right_most_path -> implement method to compute right_most_path from right_most_node to root_node

    return new_candidate
