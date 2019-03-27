import pandas as pd
from pasigram.service.edges_service import *
from pasigram.controller.candidate_generation.utils import *
from pasigram.model.graph import *


class Generator:
    """ A class to represent the candidate_generation component of the PaSiGraM algorithm.

    ...

    Attributes
    ----------
    nodes : pd.DataFrame
        The nodes of the graph (id, label)
    edges : pd.DataFrame
        The edges of the graph (id, source, target)
    min_support: Integer
        The minimum support the graphs have to meet
    frequent_edges : pd.DataFrame
        The frequent edges which were generated based on the min_support and edges of the graph
    """

    def __init__(self, unique_edges: pd.DataFrame, min_support: int) -> object:
        """A class to represent the generator component of the PaSiGraM algorithm.

        Parameters
        ----------
        unique_edges : DataFrame
            All unique edges of the input graph
        min_support : int
            The mininum support the candidates have to meet
        """
        self.__frequent_edges = compute_frequent_edges(unique_edges, min_support)
        self.__min_support = min_support
        self.__candidates = pd.DataFrame(columns=['size', 'graph'])
        self.__current_max_size = 0

    def generate_initial_candidates(self):
        """Method for generating the initial candidates for the given input graph

        """
        # get all frequent edges to initialize graph objects
        join_set = self.frequent_edges

        # iterate over all edges to build the graphs
        for i in range(0, len(join_set)):
            # get id and label of edges and nodes
            source_node_label = join_set.iloc[i]['source']
            source_node_id = 0
            target_node_label = join_set.iloc[i]['target']
            target_node_id = 1
            edge_label = join_set.iloc[i]['label']

            # initialize DataFrames for the input nodes and edges
            nodes = pd.DataFrame(data=[source_node_label, target_node_label], columns=['label'],
                                 index=[source_node_id, target_node_id])
            edges = pd.DataFrame.from_dict({"0": [source_node_id, target_node_id, edge_label]}, orient='index',
                                           columns=['source', 'target', 'label'])

            # initialize graph object for every candidate
            current_candidate = Graph(nodes, edges)

            # set root node, right most node and right most path for the graph
            current_candidate.set_root_node = source_node_id
            current_candidate.set_right_most_node = target_node_id
            current_candidate.set_right_most_path = ["0"]

            # add graph object (candidate) to the candidate DataFrame
            self.__candidates.loc[current_candidate.canonical_code] = [1, current_candidate]
        self.__current_max_size += 1

    def generate_new_subgraphs(self, candidates: pd.DataFrame) -> pd.DataFrame:
        """Method for generating new n+1-size graphs out of n-size frequent graphs

        Parameters
        ----------
        candidates : pd.DataFrame
            Contains all frequent graphs of size n
        """

        # reset the candidates DataFrame
        self.__candidates.drop(self.__candidates.index, inplace=True)
        # new_subgraphs = pd.DataFrame(columns=['size', 'graph'])

        # iterate over all graphs in candidates
        for i in range(0, len(candidates)):
            # get the Graph object of the current_candidate
            current_candidate = candidates.iloc[i]['graph']

            # get the ids of all nodes on the right_most_path of current_candidate
            right_most_path_nodes = compute_right_most_path_nodes(current_candidate.right_most_path,
                                                                  current_candidate.edges)

            # iterate over all nodes of right_most_path_nodes
            for j in range(0, len(right_most_path_nodes)):
                # get the id and label of the current_node
                current_node_id = right_most_path_nodes[j]
                current_node_label = current_candidate.nodes.loc[current_node_id]['label']

                # get the relevant edges for current_node
                relevant_edges = compute_relevant_edges(current_node_label, self.frequent_edges)

                # iterate over all edges of relevant_edges
                for k in range(0, len(relevant_edges)):
                    # get the current_relevant_edge (pd.Series)
                    current_relevant_edge = relevant_edges.iloc[k]

                    # get the Graph object of the new candidate
                    new_candidate = generate_new_candidate(current_candidate, current_relevant_edge, current_node_id)

    @property
    def min_support(self) -> int:
        return self.__min_support

    @property
    def frequent_edges(self) -> pd.DataFrame:
        return self.__frequent_edges

    @property
    def candidates(self) -> pd.DataFrame:
        return self.__candidates

    @property
    def current_max_size(self):
        return self.__current_max_size

    """def generate_candidates(self):
        if self.current_max_size == 1:
            candidate_set = self.candidates[self.candidates['size'] == 1]

            key_set = list(candidate_set.index)
            for i in range(0, len(key_set)):
                candidate1 = candidate_set.loc[key_set[i]]['graph']
                nodes_candidate1 = candidate1.nodes.values.tolist()
                for j in range(i, len(key_set)):
                    if i == j:
                        continue
                    candidate2 = candidate_set.loc[key_set[j]]['graph']
                    nodes_candidate2 = candidate2.nodes.values.tolist()

                    common_nodes = set(map(tuple, nodes_candidate1)) & set(map(tuple, nodes_candidate2))
                    res_list = list(map(list, common_nodes))

                    if len(res_list) == len(nodes_candidate1) - 1:
                        # todo: merge the two n-size candidates to one n+1-size candidate

                        print("\ncommon graphs")
                        print("\nGraph1\n")
                        print(candidate1.csp_graph)
                        print("\nGraph2\n")
                        print(candidate2.csp_graph)

        self.__current_max_size += 1"""
