import pandas as pd
import numpy as np
from pasigram.model.graph import Graph
from pasigram.controller.csp.evaluator_utils import evaluate_candidates
from pyspark import SparkContext, Broadcast
from typing import Union


class Evaluator:
    """A class to represent the evaluator component of the PaSiGraM algorithm.
    """

    def __init__(self, min_support: int) -> None:
        """Constructor

        :param Integer min_support: The minimum support the candidates have to meet
        """

        self.__min_support = min_support

    def evaluate_candidates(self, candidate_set: pd.DataFrame, sc: SparkContext, num_workers: int,
                            local_distributed: bool, input_csp_graph: Union[Broadcast, pd.DataFrame],
                            input_graph_edges: Union[Broadcast, pd.DataFrame]) -> pd.DataFrame:
        """Method to evaluate the frequency of newly generated candidates.

        :param pd.DataFrame candidate_set: The set of candidates for which one want to evaluate the frequency
        :param SparkContext sc: The SparkContext to use.
        :param int num_workers: The number of workers which are used by Spark
        :param bool local_distributed: Enable (=True) or disable (=False) local distribution over the local cpu cores
        :param input_graph_edges: The edges of the input graph
        :return: The set of all frequent subgraphs according to the minimum support
        :rtype: pd.DataFrame
        """

        # initialize 'new_frequent_subgraphs'
        new_frequent_subgraphs = pd.DataFrame(columns=['graph', 'size', 'frequency'])

        # if SparkContext is enabled, distribute the calculation over the Spark cluster
        if sc is not None:
            # split the 'candidates_set' into even chunks -> every cluster node get's one chunk
            candidates_chunks: list = np.array_split(candidate_set, num_workers)
            # transform 'candidates_chunks' into an RDD
            candidates_rdd = sc.parallelize(candidates_chunks, num_workers)

            # distribute the candidate evaluation over the single cluster nodes
            new_frequent_subgraphs_list: list[pd.DataFrame[Graph]] = candidates_rdd.map(
                evaluate_candidates(input_csp_graph, self.__min_support,
                                    input_graph_edges, local_distributed)).collect()

            # iterate over all DataFrames in 'new_frequent_subgraphs_list'
            for item in new_frequent_subgraphs_list:
                # get the current DataFrame
                new_frequent_subgraphs = new_frequent_subgraphs.append(item)

        # execute 'evaluate_candidates()' without global parallelization on Spark cluster
        else:
            new_frequent_subgraphs = evaluate_candidates(input_csp_graph, self.__min_support, input_graph_edges,
                                                         local_distributed, candidate_set)

        return new_frequent_subgraphs
