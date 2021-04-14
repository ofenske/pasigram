import pandas as pd
import numpy as np
from local.pasigram.service.edges_service import get_frequent_edges
from local.pasigram.controller.candidate_generation.utils import create_initial_patterns, generate_new_subgraphs
from local.pasigram.model.graph import Graph
from pyspark import SparkContext


class Generator:
    """A class to represent the candidate_generation component of the PaSiGraM algorithm.
    """

    def __init__(self, frequent_edges: pd.DataFrame) -> None:
        """Constructor

        :param pd.DataFrame frequent_edges:  All frequent edges of the input graph
        """

        self.__frequent_edges = frequent_edges
        self.__current_max_size: int = 1

    @property
    def frequent_edges(self) -> pd.DataFrame:
        """ The frequent edges to use to build new subgraphs/patterns.

        :return: All frequent edges of the input graph.
        :rtype: pd.DataFrame
        """

        return self.__frequent_edges

    @property
    def current_max_size(self) -> int:
        """The current maximum size of the candidates which were build by the generator

        :return: The current maximum size of the candidates
        :rtype: int
        """

        return self.__current_max_size

    def generate_initial_candidates(self, execution_mode: str) -> pd.DataFrame:
        """Method for generating the initial candidates for the given input graph

        :param SparkContext sc: The SparkContext to use
        :param int num_workers: The number of workers which are used by Spark
        :return: The set of initial candidates of size 1
        :param execution_mode:
        :rtype: pd.DataFrame
        """
        # initialize 'initial_patterns'
        initial_patterns = pd.DataFrame(columns=['graph', 'size', 'frequency'])

        initial_patterns = create_initial_patterns(execution_mode, self.frequent_edges)

        # increase the current maximum size of patterns
        self.__current_max_size += 1

        return initial_patterns

    def generate_new_subgraphs(self, candidates: pd.DataFrame, execution_mode: str) -> pd.DataFrame:
        """Method for generating new n+1-size graphs out of n-size frequent graphs

        :param candidates: The candidates which
        :param str execution_mode: Flag if we use single or multicore
        :return: The set of n+1 size candidate graphs
        :rtype: pd.DataFrame
        """
        # initialize a DataFrame to save all new candidates
        new_candidates = pd.DataFrame(columns=['graph', 'size'])


        new_candidates = generate_new_subgraphs(self.frequent_edges, execution_mode, candidates)

        self.__current_max_size += 1

        return new_candidates
