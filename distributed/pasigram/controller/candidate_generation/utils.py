import pandas as pd
import copy
import multiprocessing as mp
import numpy as np
from distributed.pasigram.model.graph import Graph
from distributed.pasigram.controller.candidate_generation.bfs import find_right_most_path
from functools import partial
from toolz import curry

########################################################################################################################
"""This block includes all methods to create the initial patterns (size-1 patterns). It includes two parts:
1. Method for locally distribute the generation process over multiple cpu cores of a machine.
2. The logic to generate such initial patterns.
"""


@curry
def create_initial_patterns(frequent_edges: pd.DataFrame) -> pd.DataFrame:
    new_candidates = pd.DataFrame(columns=['graph', 'size', 'frequency'])

    new_candidates = get_initial_patterns(frequent_edges)

    new_candidates = new_candidates.loc[~new_candidates.index.duplicated(keep='first')]

    return new_candidates


def get_initial_patterns(frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method to create the initial patterns

    :param pd.DataFrame frequent_edges:
    :return:
    """
    new_candidates = pd.DataFrame(columns=['graph', 'size', 'frequency'])
    for i in range(0, len(frequent_edges)):
        # get id and label of edges and nodes
        source_node_label = frequent_edges.iloc[i]['source']
        source_node_id = 0
        target_node_label = frequent_edges.iloc[i]['target']
        target_node_id = 1
        edge_label = frequent_edges.iloc[i]['label']

        # initialize DataFrames for the input nodes and edges
        nodes = pd.DataFrame(data=[source_node_label, target_node_label], columns=['label'],
                             index=[source_node_id, target_node_id])
        edges = pd.DataFrame.from_dict({0: [source_node_id, target_node_id, edge_label]}, orient='index',
                                       columns=['source', 'target', 'label'])

        # initialize graph object for every candidate
        current_candidate = Graph(nodes, edges)
        current_candidate.create_initial_csp_graph()
        current_candidate.build_canonical_smallest_code()

        # set root node, right most node and right most path for the graph
        current_candidate.root_node = source_node_id
        current_candidate.right_most_node = target_node_id
        current_candidate.right_most_path = [source_node_id, target_node_id]

        # add graph object (candidate) to the candidate DataFrame
        current_candidate_frequency = frequent_edges.iloc[i]['frequency']
        new_candidates.at[current_candidate.canonical_code] = [current_candidate, 1, current_candidate_frequency]

    return new_candidates


########################################################################################################################
"""This block includes all methods to generate new candidates. It includes two parts:
1. Method for locally distribute the generation process over multiple cpu cores of a machine.
2. The logic to generate the new candidates.
"""


@curry
def generate_new_subgraphs(frequent_edges: pd.DataFrame, candidates: pd.DataFrame) -> pd.DataFrame:

    new_candidates = generate_new_subgraph(candidates, frequent_edges)

    # eliminate duplicated candidates
    new_candidates = new_candidates.loc[~new_candidates.index.duplicated(keep='first')]

    return new_candidates


def generate_new_subgraph(candidates: pd.DataFrame, frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method to generate new subgraphs out of a given graph.

    :param candidates: The frequent subgraphs we want to expand
    :param frequent_edges: The set of all frequent edges of the input graph
    :return: List of the newly generated candidates
    :rtype: list
    """
    new_candidates = pd.DataFrame(columns=['graph', 'size'])
    for i in range(0, len(candidates)):
        current_candidate = candidates.iloc[i]['graph']

        # generate all forward-edge-candidates for current_candidate
        new_candidates = new_candidates.append(generate_new_forward_edge_candidates(current_candidate, frequent_edges))

        # generate all backward-edge-candidates for current_candidates
        new_candidates = new_candidates.append(generate_backward_edge_candidates(current_candidate, frequent_edges))

    return new_candidates


########################################################################################################################
"""This block includes all methods to create new candidates by the forward edge extension step, which is a part of
the right most extension approach to generate new candidates. It includes methods to compute all relevant edges 
and generate all possible candidates.
"""


def generate_new_forward_edge_candidates(current_candidate: Graph, frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method for generating all possible forward edge candidates out of a given frequent subgraph.

    :param Graph current_candidate: The candidate for which we want to add new backward edges
    :param pd.DataFrame frequent_edges: The set of all frequent edges of the input graph
    :return: A graph object of the newly generated candidate
    :rtype: Graph
    """

    forward_edge_candidates = pd.DataFrame(columns=['graph', 'size'])

    # get the right-most-path for current_candidate
    right_most_path = current_candidate.right_most_path

    # iterate over all nodes of right_most_path
    for j in range(0, len(right_most_path)):
        # get the id and label of the current_node
        current_node_id = right_most_path[j]
        current_node_label = current_candidate.nodes.loc[current_node_id]['label']

        # get the relevant forward edges for current_node
        relevant_foward_edges = compute_relevant_forward_edges(current_node_label, frequent_edges)

        # iterate over all edges of relevant_forward_edges
        for k in range(len(relevant_foward_edges)):
            # get the current_relevant_edge (pd.Series)
            current_relevant_forward_edge = relevant_foward_edges.iloc[k]

            # get the Graph object of the new candidate
            new_pattern = add_new_forward_edge(current_candidate, current_relevant_forward_edge, current_node_id)

            forward_edge_candidates.at[new_pattern.canonical_code] = [new_pattern, new_pattern.size]

    return forward_edge_candidates


def compute_relevant_forward_edges(node: str, frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method to find all edges which contains node as the source

    :param str node: The node which should be the source
    :param pd.DataFrame frequent_edges: DataFrame of frequent edges which could be relevant for node
    :return: A DataFrame with all relevant edges for the node.
    :rtype: pd.DataFrame
    """

    relevant_forward_edges = frequent_edges[(frequent_edges['source'] == node) | (frequent_edges['target'] == node)]
    return relevant_forward_edges


def add_new_forward_edge(candidate: Graph, new_edge: pd.Series, current_node_id: int) -> Graph:
    """Method to add a new forward edge to an existing graph, which connects a node in the existing graph to an new node
    which is not already in the existing graph. As a result you get an new graph object with the all edges and nodes of
    the existing graph + the new edge and node.

    :param Graph candidate: The existing graph to expand.
    :param pd.Series new_edge: The edge we want to add to the existing graph.
    :param int current_node_id: The id of the node where we want to add the new edge.
    :return: A Graph object of the new generated graph.
    :rtype: Graph
    """

    # get the nodes and edges of the existing subgraph
    candidate_nodes = candidate.nodes.copy()
    candidate_edges = candidate.edges.copy()
    candidate_csp_graph: pd.DataFrame = candidate.csp_graph.copy()

    current_node_label = candidate_nodes.loc[current_node_id]['label']

    if current_node_label == new_edge.at['source']:

        # get label,id of the target node of the new_edge
        target_node_label = new_edge.at['target']
        target_node_id = len(candidate_nodes)

        source_node_id = current_node_id

        # append the new node (target_node) to the existing nodes
        candidate_nodes.at[target_node_id] = [target_node_label]

    else:
        # get label,id of the target node of the new_edge
        target_node_id = current_node_id

        source_node_id = len(candidate_nodes)
        source_node_label = new_edge.at['source']

        # append the new node (target_node) to the existing nodes
        candidate_nodes.at[source_node_id] = [source_node_label]

    # get the label of new_edge
    new_edge_label = new_edge.at['label']

    # append new_edge to the existing edges
    candidate_edges.at[len(candidate_edges)] = [source_node_id, target_node_id, new_edge_label]

    # initialize the new_candidate as a graph
    new_candidate = Graph(candidate_nodes, candidate_edges, candidate_csp_graph)

    # set the right_most_node of new_candidate
    new_candidate.right_most_node = len(candidate_nodes) - 1

    # set the root_node of  new_candidate
    new_candidate.root_node = candidate.root_node

    # set the right most path for the new candidate
    new_candidate.right_most_path = find_right_most_path(new_candidate)

    # copy the valid instances of the parent subgraph
    new_candidate.instances = copy.deepcopy(candidate.instances)

    # set the new added edge for the new candidate
    new_candidate.new_added_edge = {'parent_node_id': source_node_id, 'child_node_id': target_node_id,
                                    'edge_label': new_edge_label, 'edge_type': 'forward'}

    # extend the csp graph by the new edge (and perhaps new node)
    new_candidate.extend_csp_graph()

    # build the new canonical code for the candidate
    new_candidate.build_canonical_smallest_code()

    return new_candidate


########################################################################################################################
"""This block includes all methods to create new candidates by the backward edge extension step, which is a part of
the right most extension approach to generate new candidates. It includes methods to compute all relevant edges 
and generate all possible candidates.
"""


def generate_backward_edge_candidates(current_candidate: Graph, frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method for generating all possible backward edge candidates out of a given frequent subgraph.

    :param Graph current_candidate: The candidate for which we want to add new backward edges
    :param pd.DataFrame frequent_edges: The set of all frequent edges of the input graph
    :return: A graph object of the newly generated candidate
    :rtype: Graph
    """

    backward_edge_candidates = pd.DataFrame(columns=['graph', 'size'])

    # get the right-most-node-label of current_candidate
    right_most_node_label = current_candidate.nodes.loc[current_candidate.right_most_node]['label']

    # get labels for all nodes in right-most-path of current_candidate
    right_most_path_labels = current_candidate.right_most_path_labels

    # get the relevant backward edges for current_candidate
    relevant_backward_edges = compute_relevant_backward_edges(right_most_node_label,
                                                              right_most_path_labels,
                                                              frequent_edges)

    # iterate over all edges in relevant_backward_edges
    for j in range(0, len(relevant_backward_edges)):
        # get the current relevant backward edge
        current_relevant_backward_edge = relevant_backward_edges.iloc[j]
        # add current_relevant_backward_edge to current_candidate and create a new pattern (Graph object)
        new_pattern = add_new_backward_edge(current_candidate, current_relevant_backward_edge)

        backward_edge_candidates.at[new_pattern.canonical_code] = [new_pattern, new_pattern.size]

    return backward_edge_candidates


def compute_relevant_backward_edges(right_most_node_label: str, right_most_path: list,
                                    frequent_edges: pd.DataFrame) -> pd.DataFrame:
    """Method to compute all relevant backward edges from the right-most-node to all nodes in the right-most-path.

    :param str right_most_node_label: The label of the right-most-node
    :param list right_most_path: A list of nodes which are part of the right-most-path
    :param pd.DataFrame frequent_edges: DataFrame of all frequent edges
    :return: Extends all relevant backward edges.
        Format : source|target|label|frequency
    :rtype: pd.DataFrame
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
            frequent_edges[(frequent_edges['source'] == right_most_node_label) &
                           (frequent_edges['target'] == right_most_path[i])])

        relevant_backward_edges = relevant_backward_edges.append(
            frequent_edges[(frequent_edges['target'] == right_most_node_label) &
                           (frequent_edges['source'] == right_most_path[i])])

    return relevant_backward_edges


def add_new_backward_edge(candidate: Graph, new_edge: pd.Series) -> Graph:
    """Method to add a new backward edge to an existing graph, which connects the right-most-node in the existing graph
    to an existing node which is part of the right-most-path. As a result you get an new graph object with the all
    edges and nodes of the existing graph + the new edge.

    :param Graph candidate: The existing graph to expand.
    :param pd.Series new_edge: The edge we want to add to the existing graph.
    :return: A Graph object of the new generated graph.
    :rtype: Graph
    """

    # get the nodes and edges of the existing subgraph
    candidate_nodes = candidate.nodes.copy()
    candidate_edges = candidate.edges.copy()
    candidate_csp_graph: pd.DataFrame = candidate.csp_graph.copy()

    right_most_path_nodes = candidate.right_most_path
    right_most_node_label = candidate_nodes.loc[candidate.right_most_node]['label']

    if right_most_node_label == new_edge.at['source']:
        # get label, id of the target node of the new_edge
        target_node_label = new_edge.loc['target']

        for i in range(0, len(right_most_path_nodes) - 1):
            current_right_most_path_node = candidate_nodes.loc[right_most_path_nodes[i]]
            label = current_right_most_path_node.loc['label']

            if label == target_node_label:
                target_node_id = right_most_path_nodes[i]

        # get the label of new_edge
        new_edge_label = new_edge.loc['label']

        # append new_edge to the existing edges
        candidate_edges.at[len(candidate_edges)] = [candidate.right_most_node, target_node_id, new_edge_label]

    elif right_most_node_label == new_edge.at['target']:
        # get label,id of the target node of the new_edge
        source_node_label = new_edge.loc['source']

        for i in range(0, len(right_most_path_nodes) - 1):
            current_right_most_path_node = candidate_nodes.loc[right_most_path_nodes[i]]
            label = current_right_most_path_node.loc['label']

            if label == source_node_label:
                source_node_id = right_most_path_nodes[i]

        # get the label of new_edge
        new_edge_label = new_edge.loc['label']

        # append new_edge to the existing edges
        candidate_edges.at[len(candidate_edges)] = [source_node_id, candidate.right_most_node, new_edge_label]

    # initialize the new_candidate as a graph
    new_candidate = Graph(candidate_nodes, candidate_edges, candidate_csp_graph)

    # set the right_most_node of new_candidate
    new_candidate.right_most_node = len(candidate_nodes) - 1

    # set the root_node of  new_candidate
    new_candidate.root_node = candidate.root_node

    # set the right most path for the new candidate
    new_candidate.right_most_path = find_right_most_path(new_candidate)

    # copy the valid instances of the parent subgraph
    new_candidate.instances = copy.deepcopy(candidate.instances)

    # set the new added edge for the new candidate
    new_candidate.new_added_edge = {'parent_node_id': candidate_edges.loc[len(candidate_edges) - 1].source,
                                    'child_node_id': candidate_edges.loc[len(candidate_edges) - 1].target,
                                    'edge_label': new_edge_label, 'edge_type': 'backward'}

    # extend the csp graph by the new edge (and perhaps new node)
    new_candidate.extend_csp_graph()

    # build the new canonical code for the candidate
    new_candidate.build_canonical_smallest_code()

    return new_candidate


########################################################################################################################
"""This block includes the method to compute the nodes of the right most path in a given graph.
"""


def compute_right_most_path_nodes(right_most_path: list, edges: pd.DataFrame) -> list:
    """Method for computing a list with all nodes which are part of the right-most-path.

    :param list right_most_path: A list with the ids of all edges of the right-most-path
    :param pd.DataFrame edges: DataFrame with all edges.
    :return: A list with ids of all nodes of the right-most-path.
    :rtype: list
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
        if source_node not in right_most_path_nodes:
            right_most_path_nodes.append(source_node)
        if target_node not in right_most_path_nodes:
            right_most_path_nodes.append(target_node)

    return right_most_path_nodes

########################################################################################################################
