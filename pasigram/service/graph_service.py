import pandas as pd
from pasigram.model.nodes import Nodes


def build_canonical_smallest_code(final_clusters: pd.DataFrame) -> str:
    """Method for building the canonical code of a graph.

    :param pd.DataFrame final_clusters: The DataFrame which contains the final clusters of the nodes.
    :return: The canonical code for the graph
    :rtype: str
    """

    # get all keys from final clusters
    keyset = list(final_clusters.index)

    # append number of elements to every clustername (clustername+"#1#")
    for i in range(0, len(keyset)):
        number_of_elements = len(final_clusters.loc[keyset[i]]['elements'])
        keyset[i] = keyset[i] + '#' + str(number_of_elements) + '#'

    # sort the keyset
    sorted_keyset = sorted(keyset)

    # Initialize the final label for the graph
    label = ""

    # Iterate over all elements in sorted_keyset
    for i in range(0, len(sorted_keyset)):
        # build label element by element
        label += sorted_keyset[i]

    return label


def build_csp_graph(nodes: pd.DataFrame, node_ids: list, node_degrees: pd.DataFrame, adjacency_list: pd.DataFrame) -> pd.DataFrame:
    """Method for building the CSP representation of the graph.

    :param pd.DataFrame adjacency_list: Clusters of all nodes in the graph by their adjacency list
    :return: Format: label|indegree|outdegree|ingoing_neighbours|outgoing_neighbours|frequency
        index = node_index
    :rtype: pd.DataFrame
    """

    # get keyset of all nodeids
    keyset = node_ids

    # build the initial DataFrame
    csp_graph = pd.DataFrame(
        columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours', 'outgoing_neighbours'])

    # iterate over all elements of 'clusters_by_adjacency_list'
    for i in range(0, len(keyset)):
        # get node id of the current node
        node_id = keyset[i]

        # get label, indegree, outdegree and frequency out of 'node'
        node_label = nodes.loc[node_id]['label']
        node_indegree = node_degrees.loc[node_id]['indegree']
        node_outdegree = node_degrees.loc[node_id]['outdegree']

        # get neighbour list out of 'node'
        ingoing_neighbour_list = adjacency_list.loc[node_id]['ingoing_neighbours']
        # initialize final neighbour list
        final_ingoing_neighbour_list = []

        # get neighbour list out of 'node'
        outgoing_neighbour_list = adjacency_list.loc[node_id]['outgoing_neighbours']
        # initialize final neighbour list
        final_outgoing_neighbour_list = []

        # test which of the both lists is longer
        if len(ingoing_neighbour_list) > len(outgoing_neighbour_list):
            iteration_length = len(ingoing_neighbour_list)
        else:
            iteration_length = len(outgoing_neighbour_list)

        # iterate over all entries (neighbour nodes) of 'neighbour_list'
        for j in range(0, iteration_length):
            # check if list_index is out of range
            if j <= len(ingoing_neighbour_list) - 1:
                # get only the first two entries of the current neighbour
                current_ingoing_neighbour = ingoing_neighbour_list[j][0:3]
                # append these entries to 'final_neighbour_list'
                final_ingoing_neighbour_list.append(current_ingoing_neighbour)

            # check if list_index is out of range
            if j <= len(outgoing_neighbour_list) - 1:
                # get only the first two entries of the current neighbour
                current_outgoing_neighbour = outgoing_neighbour_list[j][0:3]
                # append these entries to 'final_neighbour_list'
                final_outgoing_neighbour_list.append(current_outgoing_neighbour)

        # insert all entries for the current node into 'csp_graph'
        csp_graph.loc[node_id] = [node_label, node_indegree, node_outdegree, final_ingoing_neighbour_list,
                                  final_outgoing_neighbour_list]

    return csp_graph


def compute_right_most_path_labels(right_most_path: list, nodes: pd.DataFrame) -> list:
    """Method for computing the labels of all nodes on the right-most-path.

    :param list right_most_path: A list of all nodes on the right-most-path
    :param pd.DataFrame nodes: All nodes of the graph
    :return: A list with all labels of all nodes on the right-most-path
    :rtype: list
    """
    right_most_path_labels = []

    for i in range(0, len(right_most_path)):
        current_node_label = nodes.loc[right_most_path[i]]['label']
        right_most_path_labels.append(current_node_label)

    return right_most_path_labels
