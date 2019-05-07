import pandas as pd
from pasigram.service.edges_service import compute_frequent_edges
from pasigram.controller.candidate_generation.utils import add_new_forward_edge, compute_relevant_backward_edges, \
    add_new_backward_edge, compute_relevant_forward_edges, compute_relevant_right_most_node_forward_edges, \
    add_new_right_most_node_forward_edge
from pasigram.model.graph import Graph


class Generator:
    """A class to represent the candidate_generation component of the PaSiGraM algorithm.
    """

    def __init__(self, unique_edges: pd.DataFrame, min_support: int) -> None:
        """Constructor

        :param pd.DataFrame unique_edges:  All unique edges of the input graph
        :param int min_support: The mininum support the candidates have to meet
        """

        self.__frequent_edges = compute_frequent_edges(unique_edges, min_support)
        self.__min_support = min_support
        self.__candidates = pd.DataFrame(columns=['size', 'graph'])
        self.__current_max_size = 1

    def generate_initial_candidates(self) -> pd.DataFrame:
        """Method for generating the initial candidates for the given input graph

        :return: Initial candidates of size 1
        :rtype: pd.DataFrame
        """

        initial_patterns = pd.DataFrame(columns=['graph', 'size', 'frequency'])

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
            edges = pd.DataFrame.from_dict({0: [source_node_id, target_node_id, edge_label]}, orient='index',
                                           columns=['source', 'target', 'label'])

            # initialize graph object for every candidate
            current_candidate = Graph(nodes, edges)

            # set root node, right most node and right most path for the graph
            current_candidate.root_node = source_node_id
            current_candidate.right_most_node = target_node_id
            current_candidate.right_most_path = [source_node_id, target_node_id]

            # add graph object (candidate) to the candidate DataFrame
            current_candidate_frequency = join_set.iloc[i]['frequency']
            initial_patterns.loc[current_candidate.canonical_code] = [current_candidate, 1, current_candidate_frequency]
        self.__current_max_size += 1

        return initial_patterns

    def generate_new_subgraphs(self, candidates: pd.DataFrame) -> pd.DataFrame:
        """Method for generating new n+1-size graphs out of n-size frequent graphs

        :param pd.DataFrame candidates: Contains all frequent graphs of size n
        :return: All frequent graphs of size n
        :rtype: pd.DataFrame
        """

        # initialize a DataFrame to save all new candidates
        new_candidates = pd.DataFrame(columns=['graph', 'size'])

        # iterate over all graphs in candidates
        for i in range(0, len(candidates)):
            # get the Graph object of the current_candidate
            current_candidate = candidates.iloc[i]['graph']

            # generate all forward-edge-candidates for current_candidate
            self.__generate_new_forward_edge_candidates(current_candidate, new_candidates)

            # generate all backward-edge-candidates for current_candidate
            self.__generate_backward_edge_candidates(current_candidate, new_candidates)

            # generate all right-most-node-forward-edge-candidates for current_candidate
            self.__generate_new_right_most_node_forward_edge_candidates(current_candidate, new_candidates)

        return new_candidates

    def __generate_backward_edge_candidates(self, current_candidate: Graph, new_candidates: pd.DataFrame):
        """Method for generating all possible backward edge candidates out of a given frequent subgraph.

        :param Graph current_candidate: The candidate for which we want to add new backward edges
        :param pd.DataFrame new_candidates: The DataFrame where we save all candidates of size n
        """

        # get the right-most-node-label of current_candidate
        right_most_node_label = current_candidate.nodes.loc[current_candidate.right_most_node]['label']

        # get labels for all nodes in right-most-path of current_candidate
        right_most_path_labels = current_candidate.right_most_path_labels

        # get the relevant backward edges for current_candidate
        relevant_backward_edges = compute_relevant_backward_edges(right_most_node_label,
                                                                  right_most_path_labels,
                                                                  self.frequent_edges)

        # iterate over all edges in relevant_backward_edges
        for j in range(0, len(relevant_backward_edges)):
            # get the current relevant backward edge
            current_relevant_backward_edge = relevant_backward_edges.iloc[j]

            # add current_relevant_backward_edge to current_candidate and create a new pattern (Graph object)
            new_pattern = add_new_backward_edge(current_candidate, current_relevant_backward_edge)

            # get the canonical code of new_pattern
            new_pattern_code = new_pattern.canonical_code

            # check if new_pattern is already in new_candidates (if new_pattern already exists)
            if new_pattern_code not in new_candidates.index:
                new_candidates.loc[new_pattern_code] = [new_pattern, new_pattern.size]

    def __generate_new_forward_edge_candidates(self, current_candidate: Graph, new_candidates: pd.DataFrame):
        """Method for generating all possible forward edge candidates out of a given frequent subgraph.

        :param Graph current_candidate: The candidate for which we want to add new backward edges
        :param pd.DataFrame new_candidates: The DataFrame where we save all candidates of size n
        """

        # get the right-most-path for current_candidate
        right_most_path = current_candidate.right_most_path

        # iterate over all nodes of right_most_path
        for j in range(0, len(right_most_path)):
            # get the id and label of the current_node
            current_node_id = right_most_path[j]
            current_node_label = current_candidate.nodes.loc[current_node_id]['label']

            # get the relevant forward edges for current_node
            relevant_foward_edges = compute_relevant_forward_edges(current_node_label, self.frequent_edges)

            # iterate over all edges of relevant_forward_edges
            for k in range(0, len(relevant_foward_edges)):
                # get the current_relevant_edge (pd.Series)
                current_relevant_forward_edge = relevant_foward_edges.iloc[k]

                # get the Graph object of the new candidate
                new_pattern = add_new_forward_edge(current_candidate, current_relevant_forward_edge, current_node_id)

                # get the canonical_code of new_pattern
                new_pattern_code = new_pattern.canonical_code

                # check if new_pattern is already in new_candidates (if new_pattern already exists)
                if new_pattern_code not in new_candidates.index:
                    new_candidates.loc[new_pattern_code] = [new_pattern, new_pattern.size]

    def __generate_new_right_most_node_forward_edge_candidates(self, current_candidate: Graph,
                                                               new_candidates: pd.DataFrame):
        """

        :param Graph current_candidate: The current candidate to build new candidates
        :param pd.DataFrame new_candidates: The set of already newly generated candidates.
        """

        right_most_node_label = current_candidate.nodes.loc[current_candidate.right_most_node]['label']

        relevant_right_most_node_forward_edges = compute_relevant_right_most_node_forward_edges(right_most_node_label,
                                                                                                self.frequent_edges)

        for i in range(0, len(relevant_right_most_node_forward_edges)):
            current_relevant_right_most_node_forward_edge = relevant_right_most_node_forward_edges.iloc[i]

            # add current_relevant_right_most_node_forward_edge to current_candidate and create a new pattern
            new_pattern = add_new_right_most_node_forward_edge(current_candidate,
                                                               current_relevant_right_most_node_forward_edge)

            # get the canonical code of new_pattern
            new_pattern_code = new_pattern.canonical_code

            # check if new_pattern is already in new_candidates (if new_pattern already exists)
            if new_pattern_code not in new_candidates.index:
                new_candidates.loc[new_pattern_code] = [new_pattern, new_pattern.size]

    @property
    def min_support(self) -> int:
        """The minimum support the candidates have to meet

        :return: The minimum support
        :rtype: int
        """

        return self.__min_support

    @property
    def frequent_edges(self) -> pd.DataFrame:
        """ The frequent edges to use to build new subgraphs/patterns.

        :return: All frequent edges of the input graph.
        :rtype: pd.DataFrame
        """

        return self.__frequent_edges

    @property
    def candidates(self) -> pd.DataFrame:
        """The set of candidates which were build by the generator

        :return: All candidates which were build by the generator
        :rtype: pd.DataFrame
        """

        return self.__candidates

    @property
    def current_max_size(self) -> int:
        """The current maximum size of the candidates which were build by the generator

        :return: The current maximum size of the candidates
        :rtype: int
        """

        return self.__current_max_size
