import pandas as pd
import numpy as np
from local.pasigram.model.graph import Graph
from local.pasigram.controller.csp.evaluator_utils import evaluate_candidates
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

    def evaluate_candidates(self, candidate_set: pd.DataFrame, execution_mode: str,
                            input_csp_graph: Union[Broadcast, pd.DataFrame],
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


        new_frequent_subgraphs = evaluate_candidates(input_csp_graph, self.__min_support, input_graph_edges,
                                                         execution_mode, candidate_set)

        return new_frequent_subgraphs
