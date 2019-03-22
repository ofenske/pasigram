import pandas as pd


def build_canonical_smallest_code(final_clusters: pd.DataFrame) -> str:
    """Method for building the canonical code of a graph.

    Parameters
    ----------
    final_clusters : pd.DataFrame
        The DataFrame which contains the final clusters of the nodes.

    Returns
    -------
    String
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


def build_csp_graph(clusters_by_adjacency_list: pd.DataFrame) -> pd.DataFrame:
    """
    Method for building the CSP representation of the graph.

    Parameters
    ----------
    clusters_by_adjacency_list : pd.DataFrame
        Clusters of all nodes in the graph by their adjacency list

    Returns
    -------
    DataFrame in following format:
    nodeid|label|indegree|outdegree|neighbours|frequency
    """

    # get keyset of all nodeids
    keyset = list(clusters_by_adjacency_list.index)

    # build the initial DataFrame
    csp_graph = pd.DataFrame(columns=['label', 'indegree', 'outdegree', 'neighbours', 'frequency'])

    # iterate over all elements of 'clusters_by_adjacency_list'
    for i in range(0, len(keyset)):
        # get node id of the current node
        node_id = keyset[i]
        # get current node out of 'clusters_by_adjacency_list' (pd.Series -> Access to single entries with loc method)
        node = clusters_by_adjacency_list.loc[node_id]

        # get label, indegree, outdegree and frequency out of 'node'
        node_label = node.loc['label']
        node_indegree = node.loc['indegree']
        node_outdegree = node.loc['outdegree']
        node_frequency = len(node.loc['elements'])

        # get neighbour list out of 'node'
        neighbour_list = node.loc['neighbours']
        # initialize final neighbour list
        final_neighbour_list = []

        # iterate over all entries (neighbour nodes) of 'neighbour_list'
        for j in range(0, len(neighbour_list)):
            # get only the first two entries of the current neighbour
            current_neighbour = neighbour_list[j][0:2]
            # append these entries to 'final_neighbour_list'
            final_neighbour_list.append(current_neighbour)

        # insert all entries for the current node into 'csp_graph'
        csp_graph.loc[node_id] = [node_label, node_indegree, node_outdegree, final_neighbour_list, node_frequency]

    return csp_graph
