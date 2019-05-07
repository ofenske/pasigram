import pandas as pd
import copy


def compute_candidate_frequency(input_csp_graph: pd.DataFrame, candidate_csp_graph: pd.DataFrame,
                                candidate_right_most_node: int, new_added_edge: dict, min_support: int) -> [int, list]:
    # initialize the potential occurences and final instances if the candidate_graph
    potential_occurences = []
    instances = []

    # get all node ids of the candidate
    candidate_node_ids = list(candidate_csp_graph.index)

    # iterate over all nodes of the candidate_csp_graph
    for i in range(0, len(candidate_node_ids)):
        # get the id, label, indegree, outdegree of the current_candidate_node
        current_candidate_node_id = candidate_node_ids[i]
        current_candidate_node = candidate_csp_graph.loc[current_candidate_node_id]
        current_candidate_node_label = current_candidate_node.loc['label']
        current_candidate_node_indegree = current_candidate_node.loc['indegree']
        current_candidate_node_outdegree = current_candidate_node.loc['outdegree']

        # initialize the list of potential partner_nodes for the current_candidate_node
        current_candidate_node_partner_node_ids = []

        # get all nodes of the input graph which have the same label as current_candidate_node
        potential_partner_nodes_list = input_csp_graph[input_csp_graph['label'] == current_candidate_node_label]

        # get the ids of all nodes in potential_partner_nodes_list
        potential_partner_node_ids = list(potential_partner_nodes_list.index)

        # iterate over all nodes in potential_partner_nodes_list
        for j in range(0, len(potential_partner_node_ids)):
            # get the id of 'potential_partner_node'
            potential_parnter_node_id = potential_partner_node_ids[j]
            potential_partner_node = potential_partner_nodes_list.loc[potential_parnter_node_id]

            # get the indegree and outdegree of 'potential_partner_node'
            potential_partner_node_indegree = potential_partner_node.loc['indegree']
            potential_partner_node_outdegree = potential_partner_node.loc['outdegree']

            # check if node degree constraint is violated
            if (potential_partner_node_indegree >= current_candidate_node_indegree and
                    potential_partner_node_outdegree >= current_candidate_node_outdegree):
                # get the ingoing neighbour lists of the nodes
                current_candidate_node_ingoing_neighbour_list = current_candidate_node.loc['ingoing_neighbours'].copy()
                potential_partner_node_ingoing_neighbour_list = potential_partner_node.loc['ingoing_neighbours'].copy()

                # get the outgoing neighbour lists of the nodes
                current_candidate_node_outgoing_neighbour_list = current_candidate_node.loc[
                    'outgoing_neighbours'].copy()
                potential_partner_node_outgoing_neighbour_list = potential_partner_node.loc[
                    'outgoing_neighbours'].copy()

                # check if neighbour list constraint is violated
                # neighbour_list of 'current_node' has to be a subset of neighbour_list of 'potential_partner_node'
                if is_ingoing_subset(current_candidate_node_ingoing_neighbour_list,
                                     potential_partner_node_ingoing_neighbour_list):
                    if is_outgoing_subset(current_candidate_node_outgoing_neighbour_list,
                                          potential_partner_node_outgoing_neighbour_list):
                        # all constraints for the 'potential_partner_node' are full filed
                        # -> append to current_candidate_node_partner_node_ids
                        current_candidate_node_partner_node_ids.append(potential_parnter_node_id)

        # for every node in candidate_csp_graph do the following:
        # if their is no 'potential_partner_node' for 'current_node', then the frequency of candidate_graph is 0
        if len(current_candidate_node_partner_node_ids) == 0:
            return 0, instances

        # check if there are already elements (=occurences) in potential_occurences
        if len(potential_occurences) == 0:
            # if the list is empty append an key-value-pair for every potential_partner_node
            # key = current_candidate_node_partner_node_id
            # value = current_candidate_node_id
            for j in range(0, len(current_candidate_node_partner_node_ids)):
                potential_occurences.append({current_candidate_node_partner_node_ids[j]: current_candidate_node_id})

        # there are existing elements (=occurences) in potential_occurences
        else:
            potential_occurences, all_instances_updated = build_instances(input_csp_graph,
                                                                                  current_candidate_node_id,
                                                                                  current_candidate_node_partner_node_ids,
                                                                                  potential_occurences,
                                                                                  candidate_right_most_node,
                                                                                  new_added_edge, min_support)

    if all_instances_updated is False:
        return 0, instances

    candidate_frequency = 0

    for i in range(0, len(potential_occurences)):
        if len(potential_occurences[i]) == len(candidate_csp_graph):
            candidate_frequency += 1
            instances.append(potential_occurences[i])

    return candidate_frequency, instances


def compute_candidate_frequency_with_given_instances(input_csp_graph: pd.DataFrame, candidate_csp_graph: pd.DataFrame,
                                                     candidate_instances: list, candidate_right_most_node: int,
                                                     new_added_edge: dict, min_support: int) -> [int, list]:
    potential_occurences = candidate_instances.copy()
    updated_instances = []

    if len(candidate_csp_graph) is 3:
        a = 0

    current_candidate_node_id = candidate_right_most_node
    current_candidate_node = candidate_csp_graph.loc[current_candidate_node_id]
    current_candidate_node_label = current_candidate_node.loc['label']
    current_candidate_node_indegree = current_candidate_node.loc['indegree']
    current_candidate_node_outdegree = current_candidate_node.loc['outdegree']
    current_candidate_node_partner_node_ids = []

    potential_partner_nodes_list = input_csp_graph[input_csp_graph['label'] == current_candidate_node_label]

    potential_partner_node_ids = list(potential_partner_nodes_list.index)
    for j in range(0, len(potential_partner_node_ids)):
        potential_parnter_node_id = potential_partner_node_ids[j]
        potential_partner_node = potential_partner_nodes_list.loc[potential_parnter_node_id]

        # get the indegree and outdegree of 'potential_partner_node'
        potential_partner_node_indegree = potential_partner_node.loc['indegree']
        potential_partner_node_outdegree = potential_partner_node.loc['outdegree']

        # check if node degree constraint is violated
        if (potential_partner_node_indegree >= current_candidate_node_indegree and
                potential_partner_node_outdegree >= current_candidate_node_outdegree):
            # get the ingoing neighbour lists of the nodes
            current_candidate_node_ingoing_neighbour_list = current_candidate_node.loc['ingoing_neighbours'].copy()
            potential_partner_node_ingoing_neighbour_list = potential_partner_node.loc['ingoing_neighbours'].copy()

            # get the outgoing neighbour lists of the nodes
            current_candidate_node_outgoing_neighbour_list = current_candidate_node.loc[
                'outgoing_neighbours'].copy()
            potential_partner_node_outgoing_neighbour_list = potential_partner_node.loc[
                'outgoing_neighbours'].copy()

            # check if neighbour list constraint is violated
            # todo: check for alternatives with better performance
            #  (check if one list is subset of the other list)
            if is_ingoing_subset(current_candidate_node_ingoing_neighbour_list,
                                 potential_partner_node_ingoing_neighbour_list):
                if is_outgoing_subset(current_candidate_node_outgoing_neighbour_list,
                                      potential_partner_node_outgoing_neighbour_list):
                    current_candidate_node_partner_node_ids.append(potential_parnter_node_id)

    # if their is no potential partner node for current_node, then the frequency of candidate_graph is 0
    if len(current_candidate_node_partner_node_ids) == 0:
        return 0, updated_instances
    elif len(current_candidate_node_partner_node_ids) < min_support:
        return -1, updated_instances

    # check if there are already elements (=occurences) in potential_occurences
    '''if len(potential_occurences) == 0:
        # if the list is empty append an key-value-pair for every potential_partner_node
        # key = current_candidate_node_partner_node_id
        # value = current_candidate_node_id
        for j in range(0, len(current_candidate_node_partner_node_ids)):
            potential_occurences.append({current_candidate_node_partner_node_ids[j]: current_candidate_node_id})'''

    # there are existing elements (=occurences) in potential_occurences
    # else:

    updated_potential_occurences, all_instances_updated = build_instances(input_csp_graph, current_candidate_node_id,
                                                                          current_candidate_node_partner_node_ids,
                                                                          potential_occurences,
                                                                          candidate_right_most_node, new_added_edge,
                                                                          min_support)

    if all_instances_updated is False:
        return 0, updated_instances

    candidate_frequency = 0

    for i in range(0, len(updated_potential_occurences)):
        if len(updated_potential_occurences[i]) == len(candidate_csp_graph):
            candidate_frequency += 1
            updated_instances.append(updated_potential_occurences[i])

    return candidate_frequency, updated_instances


def is_outgoing_subset(list1: list, list2: list) -> bool:
    """Method to check if a list of lists is a subset of another list of lists.

    :param list1: The list for which to check if it is a subset of list2
    :param list2: The list for which to check if it is a superset of list1
    :return: True if list1 is subset of list2, else False
    :rtype: bool
    """
    # if both lists are identical return True
    if list1 == list2:
        return True
    # if list1 is empty and list2 not, then return True
    # this is because an empty list shouldn't be an sublist of an not empty list
    if len(list1) == 0 and len(list2) > 0:
        return True

    for i in range(0, len(list1)):
        found = False
        for j in range(0, len(list2)):
            if list1[i][:2] == list2[j][:2]:
                list2.pop(j)
                found = True
                break
        if found is False:
            return False

    return True


def is_ingoing_subset(list1: list, list2: list) -> bool:
    """Method to check if a list of lists is a subset of another list of lists.

    :param list1: The list for which to check if it is a subset of list2
    :param list2: The list for which to check if it is a superset of list1
    :return: True if list1 is subset of list2, else False
    :rtype: bool
    """
    # if both lists are identical return True
    if list1 == list2:
        return True
    # if list1 is empty and list2 not, then return false
    # this is because an empty list shouldn't be an sublist of an not empty list
    if len(list1) == 0 and len(list2) > 0:
        return True

    for i in range(0, len(list1)):
        found = False
        for j in range(0, len(list2)):
            if list1[i][:2] == list2[j][:2]:
                list2.pop(j)
                found = True
                break
        if found is False:
            return False

    return True


def has_child(outgoing_neighbours: list, ingoing_neighbours: list, child_node_id: int) -> [bool, str]:
    """Check which direction the edge has, which connects the neighbour node to the current one.

    :param list outgoing_neighbours: All outgoing neighbours of the current node
    :param list ingoing_neighbours: All ingoing neighbours of the current node
    :param child_node_id: The id of the child node for which one want to check the edge direction
    :return: 'outgoing_neighbour' if it is a forward edge and 'ingoing_neighbour' if it is a backward edge
    :rtype: str
    """
    child = False
    edge_direction = None
    if len(outgoing_neighbours) > len(ingoing_neighbours):
        iteration_length = len(outgoing_neighbours)
    else:
        iteration_length = len(ingoing_neighbours)

    for i in range(0, iteration_length):
        if i < len(outgoing_neighbours):
            outgoing_neighbour_node_id = outgoing_neighbours[i][2]
            if outgoing_neighbour_node_id == child_node_id:
                child = True
                edge_direction = "outgoing_neighbours"

        if i < len(ingoing_neighbours):
            ingoing_neighbour_node_id = ingoing_neighbours[i][2]
            if ingoing_neighbour_node_id == child_node_id:
                child = True
                edge_direction = "ingoing_neighbours"
    return child, edge_direction


def build_instances(input_csp_graph: pd.DataFrame, current_candidate_node_id: int,
                    current_candidate_node_partner_node_ids: list, potential_occurences: list,
                    candidate_right_most_node: int, new_added_edge: dict, min_support: int):
    updated_potential_occurences = copy.deepcopy(potential_occurences)
    all_instances_updated = False
    number_of_updated_instances = 0
    # iterate over all nodes in current_candidate_node_partner_node_ids
    for j in range(0, len(current_candidate_node_partner_node_ids)):

        # iterate over all occurences in potential_occurences
        for k in range(0, len(updated_potential_occurences)):
            # get the current_partner_node_id
            current_partner_node_id = current_candidate_node_partner_node_ids[j]

            # get all values of potential_occurences[k]
            current_occurence_ids = list(updated_potential_occurences[k].values())

            if current_candidate_node_id == candidate_right_most_node:
                if len(new_added_edge) > 0:
                    # check if current_partner_node_id is already in potential_occurences[k] included
                    if current_partner_node_id in updated_potential_occurences[k]:
                        if new_added_edge['edge_type'] is "forward":
                            # todo
                            continue
                        elif updated_potential_occurences[k][current_partner_node_id] is not candidate_right_most_node:
                            continue

                    current_candidate_node_parent_node_id = new_added_edge['parent_node_id']
                    # check if the parent of current_candidate_node is already in the current_occurence_ids
                    if current_candidate_node_parent_node_id in current_occurence_ids:
                        # get the key out of potential_occurences[k] for parent of current_candidate_node
                        current_partner_node_parent_id = list(updated_potential_occurences[k].keys())[
                            list(updated_potential_occurences[k].values()).index(current_candidate_node_parent_node_id)]

                        # get the ingoing and outgoing neighbours of current_partner_node_parent
                        current_partner_node_parent_node_ingoing_neighbours = \
                            input_csp_graph.loc[current_partner_node_parent_id]['ingoing_neighbours']
                        current_partner_node_parent_node_outgoing_neighbours = \
                            input_csp_graph.loc[current_partner_node_parent_id]['outgoing_neighbours']

                        # check if current_partner_node is really a child node of current_partner_node_parent (in input_graph)
                        is_child, edge_direction = has_child(current_partner_node_parent_node_outgoing_neighbours,
                                                             current_partner_node_parent_node_ingoing_neighbours,
                                                             current_partner_node_id)
                        if is_child is True:
                            if edge_direction is "ingoing_neighbours":
                                for l in range(0, len(current_partner_node_parent_node_ingoing_neighbours)):
                                    current_child = current_partner_node_parent_node_ingoing_neighbours[l][2]

                                    if current_child == current_partner_node_id:
                                        updated_potential_occurences[k][
                                            current_partner_node_id] = current_candidate_node_id
                                        number_of_updated_instances += 1

                            else:
                                for l in range(0, len(current_partner_node_parent_node_outgoing_neighbours)):
                                    current_child = current_partner_node_parent_node_outgoing_neighbours[l][2]

                                    if current_child == current_partner_node_id:
                                        updated_potential_occurences[k][
                                            current_partner_node_id] = current_candidate_node_id
                                        number_of_updated_instances += 1


            else:
                # check if current_partner_node_id is already in potential_occurences[k] included
                if current_partner_node_id in updated_potential_occurences[k]:
                    continue

                current_candidate_node_parent_node_id = new_added_edge['parent_node_id']
                # check if the parent of current_candidate_node is already in the current_occurence_ids
                if current_candidate_node_id - 1 in current_occurence_ids:
                    # get the key out of potential_occurences[k] for parent of current_candidate_node
                    current_partner_node_parent_id = list(updated_potential_occurences[k].keys())[
                        list(updated_potential_occurences[k].values()).index(current_candidate_node_id - 1)]

                    # get the ingoing and outgoing neighbours of current_partner_node_parent
                    current_partner_node_parent_node_ingoing_neighbours = \
                        input_csp_graph.loc[current_partner_node_parent_id]['ingoing_neighbours']
                    current_partner_node_parent_node_outgoing_neighbours = \
                        input_csp_graph.loc[current_partner_node_parent_id]['outgoing_neighbours']

                    # check if current_partner_node is really a child node of current_partner_node_parent (in input_graph)
                    is_child, edge_direction = has_child(current_partner_node_parent_node_outgoing_neighbours,
                                                         current_partner_node_parent_node_ingoing_neighbours,
                                                         current_partner_node_id)
                    if is_child is True:
                        if edge_direction is "ingoing_neighbours":
                            for l in range(0, len(current_partner_node_parent_node_ingoing_neighbours)):
                                current_child = current_partner_node_parent_node_ingoing_neighbours[l][2]

                                if current_child == current_partner_node_id:
                                    updated_potential_occurences[k].update(
                                        {current_partner_node_id: current_candidate_node_id})
                                    number_of_updated_instances += 1

                        else:
                            for l in range(0, len(current_partner_node_parent_node_outgoing_neighbours)):
                                current_child = current_partner_node_parent_node_outgoing_neighbours[l][2]

                                if current_child == current_partner_node_id:
                                    updated_potential_occurences[k].update(
                                        {current_partner_node_id: current_candidate_node_id})
                                    number_of_updated_instances += 1

    if number_of_updated_instances >= min_support:
        all_instances_updated = True

    return updated_potential_occurences, all_instances_updated
