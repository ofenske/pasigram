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


def compute_relevant_forward_edges(node: str, frequent_edges: pd.DataFrame) -> pd.DataFrame:
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
    relevant_forward_edges = frequent_edges[frequent_edges['source'] == node]
    return relevant_forward_edges


def compute_relevant_backward_edges(right_most_node_label: str, right_most_path: list,
                                    frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method to compute all relevant backward edges from the right-most-node to all nodes in the right-most-path.

    Parameters
    ----------
    right_most_node_label : str
        The label of the right-most-node
    right_most_path : list
        A list of nodes which are part of the right-most-path
    frequent_edges : pd.DataFrame
        DataFrame of all frequent edges

    Returns
    -------
    DataFrame
        Extends all relevant backward edges.
        Format : source|target|label|frequency
    """
    # get the columns of frequent_edges
    column_names = list(frequent_edges.columns.values)

    # initialize result DataFrame with column_names as columns
    relevant_backward_edges = pd.DataFrame(columns=column_names)

    # iterate over all nodes in right_most_path except the last one (right-most-node)
    for i in range(0, len(right_most_path) - 1):
        # get all edges out of frequent_edges which have the right-most-node as source and the current node as target
        # append all result edges to relevant_backward_edges
        relevant_backward_edges = relevant_backward_edges.append(
            frequent_edges[(frequent_edges['source'] == right_most_node_label) & (
                    frequent_edges['target'] ==
                    right_most_path[i])])

    return relevant_backward_edges


def compute_relevant_right_most_node_forward_edges(right_most_node_label: str,
                                                   frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """

    Parameters
    ----------
    right_most_node_label : str
        The label of the right_most_node of the graph
    frequent_edges : pd.DataFrame
        DataFrame which contains all frequent edges of the input graph

    Returns
    -------
    pd.DataFrame
        All relevant forward edges of the right-most-node
    """
    relevant_right_most_node_forward_edges = frequent_edges[frequent_edges['target'] == right_most_node_label]
    return relevant_right_most_node_forward_edges


def add_new_forward_edge(candidate: Graph, new_edge: pd.Series, current_node_id: int) -> Graph:
    """Method to add a new forward edge to an existing graph, which connects a node in the existing graph to an new node
    which is not already in the existing graph. As a result you get an new graph object with the all edges and nodes of
    the existing graph + the new edge and node.

    Parameters
    ----------
    candidate : Graph
        The existing graph to expand.
    new_edge : pd.Series
        The edge we want to add to the existing graph.
    current_node_id : str
        The id of the node where we want to add the new edge.

    Returns
    -------
    Graph
        A Graph object of the new generated graph.
    """
    # get the nodes and edges of the existing subgraph
    candidate_nodes = candidate.nodes.copy()
    candidate_edges = candidate.edges.copy()

    # get label,id of the target node of the new_edge
    target_node_label = new_edge.loc['target']
    target_node_id = len(candidate_nodes)

    # append the new node (target_node) to the existing nodes
    candidate_nodes.loc[target_node_id] = [target_node_label]

    # get the label of new_edge
    new_edge_label = new_edge.loc['label']

    # append new_edge to the existing edges
    candidate_edges.loc[len(candidate_edges)] = [current_node_id, target_node_id, new_edge_label]

    # initialize the new_candidate as a graph
    new_candidate = Graph(candidate_nodes, candidate_edges)

    # set the right_most_node of new_candidate
    new_candidate.right_most_node = len(candidate.nodes) - 1

    # set the root_node of  new_candidate
    new_candidate.root_node = candidate.root_node

    new_candidate.right_most_path = find_right_most_path(new_candidate)

    return new_candidate


def add_new_backward_edge(candidate: Graph, new_edge: pd.Series) -> Graph:
    """Method to add a new forward edge to an existing graph, which connects a node in the existing graph to an new node
    which is not already in the existing graph. As a result you get an new graph object with the all edges and nodes of
    the existing graph + the new edge and node.

    Parameters
    ----------
    candidate : Graph
        The existing graph to expand.
    new_edge : pd.Series
        The edge we want to add to the existing graph.
    current_node_id : str
        The id of the node where we want to add the new edge.

    Returns
    -------
    Graph
        A Graph object of the new generated graph.
    """
    # get the nodes and edges of the existing subgraph
    candidate_nodes = candidate.nodes.copy()
    candidate_edges = candidate.edges.copy()

    right_most_path_nodes = candidate.right_most_path
    # get label,id of the target node of the new_edge
    target_node_label = new_edge.loc['target']

    for i in range(0, len(right_most_path_nodes) - 1):
        current_right_most_path_node = candidate_nodes.loc[right_most_path_nodes[i]]
        label = current_right_most_path_node.loc['label']

        if label == target_node_label:
            target_node_id = right_most_path_nodes[i]

    # get the label of new_edge
    new_edge_label = new_edge.loc['label']

    # append new_edge to the existing edges
    candidate_edges.loc[len(candidate_edges)] = [candidate.right_most_node, target_node_id, new_edge_label]

    # initialize the new_candidate as a graph
    new_candidate = Graph(candidate_nodes, candidate_edges)

    # set the right_most_node of new_candidate
    new_candidate.right_most_node = len(candidate.nodes) - 1

    # set the root_node of  new_candidate
    new_candidate.root_node = candidate.root_node

    new_candidate.right_most_path = find_right_most_path(new_candidate)

    return new_candidate


def add_new_right_most_node_forward_edge(candidate: Graph, new_edge: pd.Series) -> Graph:
    """Method to add a new right-mos-node forward edge to an existing graph, which connects a node in the existing graph
    to an new node which is not already in the existing graph.
    As a result you get an new Graph object with the all edges and nodes of the existing graph + the new edge and node.

    Parameters
    ----------
    candidate : Graph
        The existing graph to expand
    new_edge : pd.Series
        The edge we want to add to the existing graph

    Returns
    -------

    """
    # get the nodes and edges of the existing subgraph
    candidate_nodes = candidate.nodes.copy()
    candidate_edges = candidate.edges.copy()

    # get label,id of the target node of the new_edge
    new_source_node_label = new_edge.loc['source']
    new_source_node_id = len(candidate_nodes)


    target_node_id = candidate.right_most_node

    # append the new node (new_source_node) to the existing nodes
    candidate_nodes.loc[new_source_node_id] = [new_source_node_label]

    # get the label of new_edge
    new_edge_label = new_edge.loc['label']

    # append new_edge to the existing edges
    candidate_edges.loc[len(candidate_edges)] = [new_source_node_id, target_node_id, new_edge_label]

    # initialize the new_candidate as a graph
    new_candidate = Graph(candidate_nodes, candidate_edges)

    # set the right_most_node of new_candidate
    new_candidate.right_most_node = len(candidate.nodes) - 1

    # set the root_node of  new_candidate
    new_candidate.root_node = candidate.root_node

    new_candidate.right_most_path = find_right_most_path(new_candidate)

    return new_candidate


def find_right_most_path(graph: Graph) -> list:
    """An implementation of BFS to find the right-most-path.

    Parameters
    ----------
    graph : Graph
        The graph for which to find the shortest path from the root node to the right-most-node

    Returns
    -------
    list
        A list of all nodes in the right-most-path.
    """
    # get the start and the end node for the shortest path
    start_node_id = graph.root_node
    end_node_id = graph.right_most_node

    # initialize DataFrame where all nodes an their parents are saved
    node_set = pd.DataFrame(columns=["parent"])

    # queue for all nodes for which we have to find the child nodes
    queue = [end_node_id]

    # list of all visited nodes
    visited_nodes = [end_node_id]

    # bool if we reach the start_node
    found = False

    # list for all nodes in the right-most-path
    right_most_path = []

    # search for next nodes until found == True
    # we start the search from the end_node
    while not found:
        # get the first element out of the queue
        current_node_id = queue.pop(0)

        # exceptional case for the end_node
        if current_node_id == end_node_id:
            node_set.loc[current_node_id] = None

        # get all edges that are containing current_node
        edge_list = graph.edges[(graph.edges['source'] == current_node_id) | (graph.edges['target'] == current_node_id)]

        # iterate over all edges to get the "child nodes" of current_node
        for i in range(0, len(edge_list)):
            # get the potential child node out of source of current edge
            potential_child_node = edge_list.iloc[i]['source']

            # proof if potential_child_node is the same as current_node or if it is already in visited_nodes
            if potential_child_node != current_node_id and potential_child_node not in visited_nodes:
                # save potential_child_node in the nodes DataFrame
                node_set.loc[potential_child_node] = current_node_id

                # append potential_child_node to queue and visited_nodes
                queue.append(potential_child_node)
                visited_nodes.append(potential_child_node)

                # proof if potential_child_node is the same as start_node -> then we found the shortest path
                if potential_child_node == start_node_id:
                    found = True
                    # get out of for-loop
                    break

                # get into next iteration of for-loop
                continue

            # get the potential child node out of target of current edge
            potential_child_node = edge_list.iloc[i]['target']

            # proof if potential_child_node is the same as current_node or if it is already in visited_nodes
            if potential_child_node != current_node_id and potential_child_node not in visited_nodes:
                # save potential_child_node in the nodes DataFrame
                node_set.loc[potential_child_node] = current_node_id

                # append potential_child_node to queue and visited_nodes
                queue.append(potential_child_node)
                visited_nodes.append(potential_child_node)

                # proof if potential_child_node is the same as start_node -> then we found the shortest path
                if potential_child_node == start_node_id:
                    found = True
                    # get out of for-loop
                    break

                # get into next iteration of for-loop
                continue

    # backtrack in the nodes DataFrame to add all nodes to right_most_path with
    # root_node is the first and right_most_node the last node in the right-most-path
    current_node = start_node_id
    while current_node != end_node_id:
        right_most_path.append(current_node)
        current_node = node_set.loc[current_node]['parent']

    right_most_path.append(current_node)

    return right_most_path
