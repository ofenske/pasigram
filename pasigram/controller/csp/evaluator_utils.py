import pandas as pd
import numpy as np
import multiprocessing as mp
from pasigram.model.graph import Graph
from functools import partial
from toolz import curry
from pyspark import Broadcast
from typing import Union


@curry
def evaluate_candidates(input_csp_graph: Union[Broadcast, pd.DataFrame], min_support: int,
                        input_graph_edges: Union[Broadcast, pd.DataFrame],
                        local_distributed: bool, candidate_set: pd.DataFrame) -> pd.DataFrame:
    """Method to evaluate if candidates of a given set are frequent or not.

    :param pd.DataFrame input_csp_graph: The csp_graph representation of the input graph
    :param int min_support: The minimum support the candidates have to meet
    :param pd.DataFrame input_graph_edges: The edges set of the input graph
    :param bool local_distributed: Enable (=True) or disable (=False) local parallelization over multiple cpu cores
    :param pd.DataFrame candidate_set: The set of candidates
    :return: A set of frequent subgraphs
    :rtype: pd.DataFrame
    """
    # initialize 'new_frequent_subgraphs' set
    new_frequent_subgraphs = pd.DataFrame(columns=['graph', 'size', 'frequency'])

    # distribute the computation over all cpu cores of the machine
    if local_distributed is True:
        # get number of available cpu cores
        agents = mp.cpu_count()

        # if there are less candidates then cpu cores, set number of chunks equal 1 or the number of candidates
        if len(candidate_set) <= agents:
            if len(candidate_set) == 0:
                candidates_chunks = np.array_split(candidate_set, 1)
            else:
                candidates_chunks = np.array_split(candidate_set, len(candidate_set))
        # split the 'candidate_set' into equal sized chunks
        else:
            candidates_chunks = np.array_split(candidate_set, agents)

        # initialize Pool of processes (one for every cpu core)
        with mp.Pool(processes=agents) as pool:
            if type(input_csp_graph) == Broadcast:
                result: list[pd.DataFrame[Graph]] = pool.map(
                    partial(evaluate_candidates_chunk, min_support=min_support, input_csp_graph=input_csp_graph.value,
                            input_graph_edges=input_graph_edges.value), candidates_chunks)
            else:
                # compute the new candidates
                result: list[pd.DataFrame[Graph]] = pool.map(
                    partial(evaluate_candidates_chunk, min_support=min_support, input_csp_graph=input_csp_graph,
                            input_graph_edges=input_graph_edges), candidates_chunks)

        # iterate through DataFrames in 'result'
        for frequent_subgraphs in result:
            # append 'frequent_subgraphs' to 'new_frequent_subgraphs'
            new_frequent_subgraphs = new_frequent_subgraphs.append(frequent_subgraphs)

    # execute the computation on one single cpu core
    else:
        if type(input_csp_graph) == Broadcast:
            new_frequent_subgraphs = new_frequent_subgraphs.append(
                evaluate_candidates_chunk(candidate_set, min_support, input_csp_graph.value, input_graph_edges.value))
        else:
            new_frequent_subgraphs = new_frequent_subgraphs.append(
                evaluate_candidates_chunk(candidate_set, min_support, input_csp_graph, input_graph_edges))

    return new_frequent_subgraphs


def evaluate_candidates_chunk(candidates_chunk: pd.DataFrame, min_support: int,
                              input_csp_graph: pd.DataFrame, input_graph_edges: pd.DataFrame) -> pd.DataFrame:
    """Method to evaluate if graphs of a given set are frequent or not

    :param pd.DataFrame candidates_chunk: The set of candidates which one want to evaluate
    :param int min_support: The user defined min_support the candidates have to meet
    :param pd.DataFrame input_csp_graph: The csp graph of the input graph
    :param pd.DataFrame input_graph_edges: The set of all edges of the input graph
    :return: The set of all frequent subgraphs
    :rtype: pd.DataFrame
    """
    new_frequent_subgraphs = pd.DataFrame(columns=['graph', 'size', 'frequency'])
    for i in range(0, len(candidates_chunk)):
        # get the 'current_candidate' out of 'candidate_chunk'
        current_candidate: Graph = candidates_chunk.iloc[i]['graph']

        # calculate the frequency of the current candidate
        current_candidate_frequency: int = calculate_frequency(current_candidate, input_csp_graph, input_graph_edges)

        # check if 'current_candidate_frequency' is above 'min_support'
        if current_candidate_frequency >= min_support:
            # get the canonical code of 'current_candidate'
            current_candidate_canonical_code: str = current_candidate.canonical_code
            # get the size of 'current_candidate'
            size: int = current_candidate.size
            # append 'current_candidate' to 'new_frequent_subgraphs'
            new_frequent_subgraphs.at[current_candidate_canonical_code] = [current_candidate, size,
                                                                            current_candidate_frequency]
    return new_frequent_subgraphs


def calculate_frequency(candidate_graph: Graph, input_csp_graph: pd.DataFrame, input_graph_edges: pd.DataFrame) -> int:
    """Method to calculate the frequency of a single candidate in an input graph.

    :param Graph candidate_graph: The graph object of the candidate
    :param pd.DataFrame input_csp_graph: The csp graph of the input graph
    :param pd.DataFrame input_graph_edges: The set of all edges of the input graph
    :return: The frequency of the candidate
    :rtype: int
    """
    # initialize the potential occurrences and final instances of the candidate_graph
    frequency = 0
    valid_instances = []

    # get the potential assignments of all nodes of the candidate to the nodes of the input graph
    potential_assignments: dict[list] = compute_potential_assigments(candidate_graph.csp_graph,
                                                                     candidate_graph.instances,
                                                                     candidate_graph.new_added_edge, input_csp_graph)
    # if potential_assignments is empty then return 0-frequency
    if len(potential_assignments) == 0:
        return frequency

    potential_instances: list[dict] = find_valid_instances(potential_assignments, candidate_graph.edges,
                                                           candidate_graph.instances, input_graph_edges)
    # if valid_assignments is empty then return 0-frequency
    if len(potential_instances) == 0:
        return frequency

    # iterate over all lists in 'valid_instances'
    for i in range(len(potential_instances)):
        graph_size_nodes: int = len(candidate_graph.nodes)
        # if current instance contains the same number of valid assignments as the candidate contains nodes
        # -> current instance must be a valid instance
        if graph_size_nodes == len(potential_instances[i]):
            # increase frequency of candidate with 1
            frequency += 1
            # append current instance to 'valid_instances'
            valid_instances.append(potential_instances[i])

    candidate_graph.instances = valid_instances

    return frequency


def find_valid_instances(potential_assignments: dict, candidate_edges: pd.DataFrame, candidate_instances: pd.DataFrame,
                         input_graph_edges: pd.DataFrame) -> list:
    """Method to compute valid instances of a candidate in the input graph.

    :param dict potential_assignments: A dictionary with potential assignments to partner nodes in input graph
    :param pd.DataFrame candidate_edges: The set of all edges of the candidate
    :param pd.DataFrame input_graph_edges: The set of all edges of the input graph
    :return: A list of valid assignments for all nodes
    """
    valid_instances = []
    not_visited_nodes = list(potential_assignments.keys())
    assigment_iterator_list = potential_assignments

    # Dynamic evaluation: if the candidate inherits the valid instances from its parent, then we only have to compute
    # valid assignments for the nodes, which are connected by the 'new_added_edge'
    if len(candidate_instances) > 0:
        # set the 'valid_instances' to inherited instances of the parent graph
        valid_instances = candidate_instances
        # get the later added node of the nodes which are connected by the newly added edge
        assigment_iterator_list = sorted(potential_assignments)
        new_node = assigment_iterator_list[len(assigment_iterator_list) - 1]
        # iterate over all instances to delete the later added node
        for instance in valid_instances:
            if new_node in list(instance.keys()):
                del (instance[new_node])
            # if later added node not in an instance, then it have to be a newly added node
            # -> wen can't delete the node, because it can't be in any instance of the parent graph
            else:
                break

    # iterate through all nodes in 'potential_assignments'
    for node1 in assigment_iterator_list:
        # remove 'node1' from 'not_visited_nodes'
        not_visited_nodes.remove(node1)

        # iterate through all nodes in 'not_visited_nodes'
        for node2 in not_visited_nodes:
            # find valid instances for a pair of (node1, node2)
            new_instances: list[dict] = find_partner_nodes(node1, potential_assignments[node1], node2,
                                                           potential_assignments[node2],
                                                           candidate_edges, input_graph_edges)
            # if 'valid_instances' is empty -> overwrite it with 'new_instances'
            if len(valid_instances) == 0:
                valid_instances: list[dict] = new_instances.copy()
                continue

            # iterate over all instances in 'new_instances' (this are only the instances for node1 and node2 pairs)
            for i in range(len(new_instances)):
                # get current instance
                new_instance: dict = new_instances[i]
                # iterate over already identified instances
                for j in range(len(valid_instances)):
                    # get the assignment for 'node2'
                    new_node_assignment: int = new_instance[node2].copy()
                    # if 'new_node_assignment' is already in current instance of 'valid_instances'
                    # -> continue with next instance in 'valid_instances'
                    if new_node_assignment in list(valid_instances[j].values()):
                        # Info: one node of the input graph cannot be an assignment for two different nodes
                        # of the same candidate instance
                        continue
                    # if 'node2' is already in current instance of 'valid_instances'
                    # -> continue with next instance in 'valid_instances'
                    elif node2 in list(valid_instances[j].keys()):
                        continue

                    parent_node_instance = new_instance[node1]
                    # check if the instance of the parent node (node1) is already in current instance of 'valid_instances'
                    # Info: if that's not the case, there cant be an edge between the already identified assignments
                    # in ''valid_instances' and the new assignment -> an istance has to be a connected graph
                    if parent_node_instance in list(valid_instances[j].values()):
                        # update the current valid instance with the 'new_node_assignment' of 'node2'
                        valid_instances[j].update({node2.copy(): new_node_assignment})
                        # continue with next 'new_instance' (leave inner loop and continue in outer loop)
                        break

    return valid_instances


def find_partner_nodes(candidate_node1: int, candidate_node1_assignments: list, candidate_node2: int,
                       candidate_node2_assignments: list, candidate_edges: pd.DataFrame,
                       input_graph_edges: pd.DataFrame) -> list:
    """Method to find valid assignments for two candidate nodes which are having an edge between them.

    :param int candidate_node1: The id of node1 (candidate node)
    :param list candidate_node1_assignments: All assignments for node1 (ids of input graph nodes)
    :param int candidate_node2: The id of node2 (candidate node)
    :param list candidate_node2_assignments: All assignments for node2 (ids of input graph nodes)
    :param pd.DataFrame candidate_edges: The set with all edges of the candidate
    :param pd.DataFrame input_graph_edges: The set with all edges of the input graph
    :return: List with valid assignments (dict) for both nodes
    :rtype: list[dict{candidate_node_id: assignment_id]
    """
    valid_instances = []
    # get all foward edges between 'node1' and 'node2'
    candidates_forward_edges: pd.DataFrame = candidate_edges[
        (candidate_edges['source'] == candidate_node1) & (candidate_edges['target'] == candidate_node2)]
    candidates_forward_edges_labels: list = sorted(list(candidates_forward_edges.label.unique()))

    # get all foward edges between 'node1' and 'node2'
    candidates_backward_edges: pd.DataFrame = candidate_edges[
        (candidate_edges['source'] == candidate_node2) & (candidate_edges['target'] == candidate_node1)]
    candidates_backward_edges_labels: list = sorted(list(candidates_backward_edges.label.unique()))

    # if there is no edge between 'node1' and 'node2' there can't be an valid instance for both together
    if len(candidates_forward_edges) == 0 and len(candidates_backward_edges) == 0:
        return valid_instances

    # iterate over all valid potential_assignments of node1
    for i in range(len(candidate_node1_assignments)):
        partner_node1 = candidate_node1_assignments[i]

        # iterate over all valid potential_assignments of node2
        for j in range(0, len(candidate_node2_assignments)):
            partner_node2 = candidate_node2_assignments[j]

            # if there is a forward edge between 'node1' and 'node2'
            if len(candidates_forward_edges) > 0:
                # compute all forward edges between the assignments of 'node1' and 'node2'
                partner_forward_edges = input_graph_edges[
                    (input_graph_edges['source'] == partner_node1) & (input_graph_edges['target'] == partner_node2)]
                partner_forward_edges_labels = sorted(list(partner_forward_edges.label.unique()))

                # compare the labels of forward candidate edges and the forward input graph edges
                # of node1 and node2 and there assignments
                # if label are unequal -> both assignments are not connected in the input graph
                # -> those they can't be part of the same instance
                if partner_forward_edges_labels != candidates_forward_edges_labels:
                    # continue with next assignment pair
                    continue
            # if there is a backward edge between 'node1' and 'node2'
            if len(candidates_backward_edges) > 0:
                # compute all backward edges between the assignments of 'node1' and 'node2'
                partner_backward_edges = input_graph_edges[
                    (input_graph_edges['source'] == partner_node2) & (input_graph_edges['target'] == partner_node1)]
                partner_backward_edges_labels = sorted(list(partner_backward_edges.label.unique()))

                # compare the labels of forward candidate edges and the forward input graph edges
                # of node1 and node2 and there assignments
                # if label are unequal -> both assignments are not connected in the input graph
                # -> those they can't be part of the same instance
                if partner_backward_edges_labels != candidates_backward_edges_labels:
                    # continue with next assignment pair
                    continue

            # build current instance with the current assignments for 'node1' and 'node2'
            instance = {candidate_node1: partner_node1,
                        candidate_node2: partner_node2}
            # append current instance to valid_instances
            valid_instances.append(instance)

    return valid_instances


def compute_potential_assigments(candidate_csp_graph: pd.DataFrame, candidate_instances: pd.DataFrame,
                                 new_added_edge: dict, input_csp_graph: pd.DataFrame) -> dict:
    """Method to compute potential assignments for all nodes of the candidate in the input graph.
    An input graph node is called potential assigment to a candidate node, iff the node labels are equal,
    in- and outdegree of input graph node are greater equals in- and outdegree of the candidate node
    and the neighbour lists of the candidate node are subsets of the neighbour lists of the input node.

    Dynamic programming approach: if the candidate inherits the valid instances from its parent, then the method only
    computes potential assigments for the nodes which are conncected by the newly added edge.

    :param pd.DataFrame candidate_csp_graph: The csp_graph representation of the candidate graph
    :param pd.DataFrame candidate_instances: Instances of the nodes of the candidate
    :param pd.DataFrame input_csp_graph: The csp_graph representation of the input graph
    :return: A dict which contains a list (value) of potential assignments for every candidate node (key)
    :rtype: dict[candidate_node_id: [assignment_ids]]
    """
    potential_assignments = {}

    # Dynamic evaluation: if the candidate inherits the valid instances from its parent, then we only have to compute
    # new potential assignments for the nodes, which are connected by the 'new_added_edge'
    if len(candidate_instances) == 0:
        candidate_node_ids = list(candidate_csp_graph.index)
    else:
        candidate_node_ids = [new_added_edge['parent_node_id'], new_added_edge['child_node_id']]

    # iterate over all candidate nodes in 'candidate_node_ids' to compute their potential_assignments
    for node_index in candidate_node_ids:
        # get id, label, in- and outdegree of the candidate_node
        candidate_node = candidate_csp_graph.loc[node_index]
        candidate_node_label = candidate_csp_graph.loc[candidate_node.name]['label']
        candidate_node_indegree = candidate_csp_graph.loc[candidate_node.name]['indegree']
        candidate_node_outdegree = candidate_csp_graph.loc[candidate_node.name]['outdegree']

        # initialize empty list for potential assignments for candidate_node in the input graph
        candidate_node_potential_assignments_ids = []

        # compute all nodes of input graph which have the same label and in-/outdegree as candidate_node
        potential_assignment_nodes: pd.DataFrame = input_csp_graph[
            (input_csp_graph['indegree'] >= candidate_node_indegree) &
            (input_csp_graph['outdegree'] >= candidate_node_outdegree) &
            (input_csp_graph['label'] == candidate_node_label)]

        # iterate over all potential_assignments (nodes of input graph)
        for j in range(len(potential_assignment_nodes)):
            # get the ingoing and outgoing neighbour lists for candidate and input graph node
            potential_partner_node_ingoing_neighbours: list[list] = potential_assignment_nodes.iloc[j][
                'ingoing_neighbours'].copy()
            potential_partner_node_outgoing_neighbours: list[list] = potential_assignment_nodes.iloc[j][
                'outgoing_neighbours'].copy()
            candidate_node_ingoing_neighbours: list[list] = candidate_csp_graph.loc[candidate_node.name][
                'ingoing_neighbours'].copy()
            candidate_node_outgoing_neighbours: list[list] = candidate_csp_graph.loc[candidate_node.name][
                'outgoing_neighbours'].copy()

            # check the constraint that the ingoing and outgoing neighbours of assigment are super sets
            # of the ingoing and outgoing neighbours of candidate_node
            if is_subset(candidate_node_ingoing_neighbours, potential_partner_node_ingoing_neighbours):
                if is_subset(candidate_node_outgoing_neighbours, potential_partner_node_outgoing_neighbours):
                    # append id of potential_assigment to candidate_node_partner_node_ids
                    candidate_node_potential_assignments_ids.append(potential_assignment_nodes.iloc[j].name)

        potential_assignments.update({candidate_node.name: candidate_node_potential_assignments_ids})

    # else:
    #     new_nodes = [new_added_edge['parent_node_id'], new_added_edge['child_node_id']]

    return potential_assignments


def is_subset(list1: list, list2: list) -> bool:
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
    # this is because an empty list should be an sublist of an not empty list
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
