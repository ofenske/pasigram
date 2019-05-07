import pandas as pd
from pasigram.controller.csp.utils import compute_candidate_frequency, compute_candidate_frequency_with_given_instances


class Evaluator:
    """A class to represent the evaluator component of the PaSiGraM algorithm.
    """

    def __init__(self, csp_graph: pd.DataFrame, min_support: int) -> None:
        """Constructor

        :param pd.DataFrame csp_graph: The csp graph representation of the input graph
        :param Integer min_support: The minimum support the candidates have to meet
        """

        self.__min_support = min_support
        self.__input_graph = csp_graph
        self.__frequent_subgraphs = pd.DataFrame(columns=['number_of_edges', 'graph'])

    def evaluate_candidates(self, candidate_set: pd.DataFrame) -> pd.DataFrame:
        """Method to evaluate the frequency of newly generated candidates.

        :param pd.DataFrame candidate_set: The set of candidates for which one want to evaluate the frequency
        :return: The set of all frequent subgraphs according to the minimum support
        :rtype: pd.DataFrame
        """

        new_frequent_subgraphs = pd.DataFrame(columns=['graph', 'size', 'frequency'])

        for i in range(0, len(candidate_set)):
            current_candidate_csp_graph = candidate_set.iloc[i]['graph'].csp_graph
            current_candidate = candidate_set.iloc[i]['graph']
            new_added_edge = current_candidate.new_added_edge
            candidate_instances = current_candidate.instances
            frequent_candidates_len = len(new_frequent_subgraphs)
            if len(current_candidate.instances) > 0:
                current_candidate_frequency, current_candidate_instances = compute_candidate_frequency_with_given_instances(
                    self.__input_graph, current_candidate_csp_graph, current_candidate.instances,
                    current_candidate.right_most_node, new_added_edge, self.__min_support)

            elif len(current_candidate.instances) is 0:
                current_candidate_frequency, current_candidate_instances = compute_candidate_frequency(
                    self.__input_graph, current_candidate_csp_graph, current_candidate.right_most_node, new_added_edge,
                    self.__min_support)

            if current_candidate_frequency >= self.__min_support:
                current_candidate.instances = current_candidate_instances
                current_candidate_canonical_code = candidate_set.iloc[i]['graph'].canonical_code
                size = current_candidate.size
                new_frequent_subgraphs.loc[current_candidate_canonical_code] = [current_candidate, size,
                                                                                current_candidate_frequency]

        return new_frequent_subgraphs
