import pandas as pd


def cluster_nodes_by_label_and_degree(nodes: pd.DataFrame, node_degrees: pd.DataFrame) -> pd.DataFrame:
    """Method for clustering nodes by their labels and degrees.

    :param pd.DataFrame nodes: The DataFrame which contains the nodes of the graph.
    :param pd.DataFrame node_degrees: The DataFrame which contains the in- and outdegree for every node of the graph
    :return: Format: label | indegree | outdegree | elements
        index = node_label + node_indegree + node_outdegree
    :rtype: pd.DataFrame
    """
    clusters = pd.DataFrame(columns=['label', 'indegree', 'outdegree', 'elements'])

    node_ids = nodes.index
    # iterate over all nodes to cluster them by degree and label
    for i in range(0, len(node_ids)):
        # label, id, degree of the current node
        current_node_id = node_ids[i]
        current_node_label = nodes.loc[current_node_id]['label']
        current_node_indegree = node_degrees.loc[current_node_id]['indegree']
        current_node_outdegree = node_degrees.loc[current_node_id]['outdegree']

        # clustername of nodes = label of nodes+indegree of nodes+outdegree of nodes
        # can be used to search if there is already a cluster to which a node can be assigned
        cluster_name = str(current_node_label) + str(current_node_indegree) + str(current_node_outdegree)

        # check if the clustername for the current node already exists
        # (yes = assign node to cluster, no = define new cluster)
        if cluster_name not in clusters.index:
            clusters.loc[cluster_name] = [current_node_label, current_node_indegree, current_node_outdegree,
                                          [current_node_id]]
        else:
            clusters.loc[cluster_name]['elements'].append(current_node_id)

    return clusters


def cluster_nodes_by_adjacency_list(cluster_by_label_and_degree: pd.DataFrame,
                                    adjacency_list: pd.DataFrame) -> pd.DataFrame:
    """Method for clustering nodes based on their labels, degrees and adjacency list

    :param pd.DataFrame cluster_by_label_and_degree: The DataFrame with the clusters predefined by cluster_nodes_by_label_and_degree()
    :param pd.DataFrame adjacency_list: The DataFrame which contains the adjacency list for every node
    :return: Format: cluster_id | label | indegree | outdegree | ingoing_neighbours | outgoing_neighbours | elements
        index = node_label + node_indegree + node_outdegree + ingoing_neighbours + outgoing_neighbours
    :rtype: pd.DataFrame
    """

    final_clusters = pd.DataFrame(
        columns=['label', 'indegree', 'outdegree', 'ingoing_neighbours', 'outgoing_neighbours', 'elements'])

    # iterate over all nodes of all clusters of the predefined clusters
    for i in range(0, len(cluster_by_label_and_degree)):
        # get all nodes of the cluster
        cluster_elements = cluster_by_label_and_degree.iloc[i]['elements']

        # get label, degree of the current cluster
        node_label = cluster_by_label_and_degree.iloc[i]['label']
        node_indegree = cluster_by_label_and_degree.iloc[i]['indegree']
        node_outdegree = cluster_by_label_and_degree.iloc[i]['outdegree']

        # iterate over all nodes of the current cluster
        for j in range(0, len(cluster_elements)):
            # get the current node of the current cluster (the id)
            element = cluster_elements[j]

            # get ingoing neighbours of the current node (call by node id)
            node_ingoing_neighbours = adjacency_list.loc[element]['ingoing_neighbours']

            # get outgoing neighbours of the current node (call by node id)
            node_outgoing_neighbours = adjacency_list.loc[element]['outgoing_neighbours']

            # initialize cluster name (= label of node + degree of nodes + labels of edges + labels of neighbours
            cluster_name = str(node_label) + str(node_indegree) + str(node_outdegree)

            # Initialize lists for ingoing edge labels and ingoing neighbour labels for the current node
            ingoing_edge_labels = []
            ingoing_neighbour_labels = []

            # Initialize lists for outgoing edge labels and outgoing neighbour labels for the current node
            outgoing_edge_labels = []
            outgoing_neighbour_labels = []

            # test which of the both lists is longer
            if len(node_ingoing_neighbours) > len(node_outgoing_neighbours):
                iteration_length = len(node_ingoing_neighbours)
            else:
                iteration_length = len(node_outgoing_neighbours)

            # Iterate over all elements in ingoing and outgoing adjacency list of current node
            for k in range(0, iteration_length):
                # check if list_index is out of range
                if k <= len(node_ingoing_neighbours) - 1:
                    # append label of edge and label of neighbour node to existing lists
                    ingoing_edge_labels.append(node_ingoing_neighbours[k][0])
                    ingoing_neighbour_labels.append(node_ingoing_neighbours[k][1])

                # check if list_index is out of range
                if k <= len(node_outgoing_neighbours) - 1:
                    # append label of edge and label of neighbour node to existing lists
                    outgoing_edge_labels.append(node_outgoing_neighbours[k][0])
                    outgoing_neighbour_labels.append(node_outgoing_neighbours[k][1])

            # sort edge and neighbour labels
            # sorted_edge_labels = sorted(edge_labels)
            # sorted_neighbour_labels = sorted(neighbour_labels)

            # Iterate over all elements of the ingoing neighbour list to build incrementally the final cluster name
            for k in range(0, len(ingoing_neighbour_labels)):
                # build final cluster name element by element
                cluster_name += str(ingoing_edge_labels[k]) + str(ingoing_neighbour_labels[k])

            # Iterate over all elements of the outgoing neighbour list to build incrementally the final cluster name
            for k in range(0, len(outgoing_neighbour_labels)):
                # build final cluster name element by element
                cluster_name += str(outgoing_edge_labels[k]) + str(outgoing_neighbour_labels[k])

            # check if cluster name not already exists
            if cluster_name not in final_clusters.index:
                # define new cluster
                final_clusters.loc[cluster_name] = [node_label, node_indegree, node_outdegree, node_ingoing_neighbours,
                                                    node_outgoing_neighbours, [element]]

            # cluster name already exists
            else:
                # assign node to existing cluster
                final_clusters.loc[cluster_name]['elements'].append(element)

    return final_clusters
