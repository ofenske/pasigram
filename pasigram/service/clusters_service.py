import pandas as pd


def cluster_nodes_by_label_and_degree(nodes: pd.DataFrame, node_degrees: pd.DataFrame) -> pd.DataFrame:
    """Method for cluster nodes by their labels and degrees.

    Parameters
    ----------
    nodes : DataFrame
        The DataFrame which contains the nodes of the graph.

    node_degrees : DataFrame
        The DataFrame which contains the degree for the single nodes of the graph.

    Returns
    -------
    DataFrame in following format:
    cluster_id | label | indegree | outdegree | elements
    """
    clusters = pd.DataFrame(columns=['label', 'indegree', 'outdegree', 'elements'])

    node_ids = nodes.index
    # iterate over all nodes to cluster them by degree and label
    for i in range(0, len(node_ids)):
        # label, id, degree of the current node
        current_node_id = node_ids[i]
        current_node_label = nodes.loc[current_node_id]['label']
        current_node_indegree = node_degrees.loc[current_node_id]['Indegree']
        current_node_outdegree = node_degrees.loc[current_node_id]['Outdegree']

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


def cluster_nodes_by_adjacency_list(pre_clusters: pd.DataFrame, adjacency_list: pd.DataFrame) -> pd.DataFrame:
    """Methode for cluster nodes based on their labels, degrees and adjacency list

    Parameters
    ----------
    pre_clusters : DataFrame
        The DataFrame with the clusters predefined by cluster_nodes_by_label_and_degree()

    adjacency_list : DataFrame
        The DataFrame which contains the adjacency list for every node.

    Returns
    -------
    DataFrame in following format:
    cluster_id | label | indegree | outdegree | neighbours | elements
    """
    final_clusters = pd.DataFrame(columns=['label', 'indegree', 'outdegree', 'neighbours', 'elements'])

    # iterate over all nodes of all clusters of the predefined clusters
    for i in range(0, len(pre_clusters)):
        # get all nodes of the cluster
        cluster_elements = pre_clusters.iloc[i]['elements']

        # get label, degree of the current cluster
        node_label = pre_clusters.iloc[i]['label']
        node_indegree = pre_clusters.iloc[i]['indegree']
        node_outdegree = pre_clusters.iloc[i]['outdegree']

        # iterate over all nodes of the current cluster
        for j in range(0, len(cluster_elements)):
            # get the current node of the current cluster (the id)
            element = cluster_elements[j]

            # get neighbours of the current node (call by node id)
            node_neighbours = adjacency_list.loc[element]['neighbours']

            # initialize cluster name (= label of node + degree of nodes + labels of edges + labels of neighbours
            cluster_name = str(node_label) + str(node_indegree) + str(node_outdegree)

            # Initialize lists for edge labels and neighbour labels for the current node
            edge_labels = []
            neighbour_labels = []

            # Iterate over all elements in adjacency list of current node
            for k in range(0, len(node_neighbours)):
                # append label of edge and label of neighbour node to existing lists
                edge_labels.append(node_neighbours[k][0])
                neighbour_labels.append(node_neighbours[k][1])

            # sort edge and neighbour labels
            # sorted_edge_labels = sorted(edge_labels)
            # sorted_neighbour_labels = sorted(neighbour_labels)

            # Iterate over all elements of the neighbour list to build incrementally the final cluster name
            for k in range(0, len(neighbour_labels)):
                # build final cluster name element by element
                cluster_name += str(edge_labels[k]) + str(neighbour_labels[k])

            # check if cluster name not already exists
            if cluster_name not in final_clusters.index:
                # define new cluster
                final_clusters.loc[cluster_name] = [node_label, node_indegree, node_outdegree, node_neighbours,
                                                    [element]]

            # cluster name already exists
            else:
                # assign node to existing cluster
                final_clusters.loc[cluster_name]['elements'].append(element)

    return final_clusters
