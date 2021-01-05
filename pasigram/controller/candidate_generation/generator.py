import pandas as pd
import numpy as np
from pasigram.service.edges_service import get_frequent_edges
from pasigram.controller.candidate_generation.utils import create_initial_patterns, generate_new_subgraphs
from pasigram.model.graph import Graph
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

    def generate_initial_candidates(self, sc: SparkContext, num_workers: int, local_distributed: bool) -> pd.DataFrame:
        """Method for generating the initial candidates for the given input graph

        :param SparkContext sc: The SparkContext to use
        :param int num_workers: The number of workers which are used by Spark
        :return: The set of initial candidates of size 1
        :param local_distributed:
        :rtype: pd.DataFrame
        """
        # initialize 'initial_patterns'
        initial_patterns = pd.DataFrame(columns=['graph', 'size', 'frequency'])

        # if SparkContext is enabled, distribute the calculation over the Spark cluster
        if sc is not None:
            # split the 'frequent_edges' into even chunks -> every cluster node get's one chunk
            edges_chunks: list = np.array_split(self.frequent_edges, num_workers)
            # transform 'edges_chunks' into an RDD
            edges_rdd = sc.parallelize(edges_chunks, num_workers)

            # distribute the pattern generation over the single cluster nodes
            initial_patterns_list: list[pd.DataFrame[Graph]] = edges_rdd.map(
                create_initial_patterns(local_distributed)).collect()

            # iterate over all DataFrames in 'initial_patterns'
            for i in range(0, len(initial_patterns_list)):
                # get current pattern
                initial_pattern: pd.DataFrame = initial_patterns_list[i]
                # append 'df' to 'initial_patterns'
                initial_patterns = initial_patterns.append(initial_pattern)

        # execute initial pattern generation on single machine
        else:
            initial_patterns = create_initial_patterns(local_distributed, self.frequent_edges)

        # increase the current maximum size of patterns
        self.__current_max_size += 1

        return initial_patterns

    def generate_new_subgraphs(self, candidates: pd.DataFrame, sc: SparkContext, num_workers: int,
                               local_distributed) -> pd.DataFrame:
        """Method for generating new n+1-size graphs out of n-size frequent graphs

        :param candidates:
        :param sc:
        :param num_workers:
        :param local_distributed:
        :return: The set of n+1 size candidate graphs
        :rtype: pd.DataFrame
        """
        # initialize a DataFrame to save all new candidates
        new_candidates = pd.DataFrame(columns=['graph', 'size'])

        if sc is not None:
            # get all frequent edges to initialize graph objects
            candidates_chunks: list = np.array_split(candidates, num_workers)
            candidates_rdd = sc.parallelize(candidates_chunks, num_workers)
            new_candidates_list: list = candidates_rdd.map(
                generate_new_subgraphs(self.frequent_edges, local_distributed)).collect()

            for i in range(0, len(new_candidates_list)):
                new_candidates = new_candidates.append(new_candidates_list[i])

            # eliminate duplicated candidates
            new_candidates = new_candidates.loc[~new_candidates.index.duplicated(keep='first')]

        else:
            new_candidates = generate_new_subgraphs(self.frequent_edges, local_distributed, candidates)

        self.__current_max_size += 1

        return new_candidates
