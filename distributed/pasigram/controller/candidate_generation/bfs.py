import pandas as pd
from distributed.pasigram.model.graph import Graph


def find_right_most_path(graph: Graph) -> list:
    """An implementation of BFS to find the right-most-path.

    :param Graph graph: The graph for which to find the shortest path from the root node to the right-most-node
    :return: A list of all nodes in the right-most-path.
    :rtype: list
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
        edge_list = graph.edges[
            (graph.edges['source'] == current_node_id) | (graph.edges['target'] == current_node_id)]

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
