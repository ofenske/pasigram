import pandas as pd
from local.pasigram.controller.candidate_generation.generator import Generator
from local.pasigram.controller.csp.evaluator import Evaluator
from local.pasigram.model.graph import Graph
from local.pasigram.service.edges_service import compute_frequent_edges, get_frequent_edges
from pyspark import SparkContext


class Pasigram:
    """Class to represent the PaSiGraM algorithm.
    """

    def __init__(self, input_graph: Graph, min_support: int) -> None:
        """Constructor

        :param Graph input_graph: The input graph for PaSiGraM algorithm
        :param int min_support: The minimum support the candidates have to meet
        """

        self.__min_support = min_support
        self.__input_graph = input_graph
        self.__frequent_subgraphs = pd.DataFrame(columns=['graph', 'size', 'frequency'])
        self.__current_max_size = 0

    def execute(self, execution_mode: str = 'single_core') -> None:
        """Method to execute the PaSiGraM algorithm

        :return:
        """

        input_csp_graph = self.__input_graph.csp_graph
        input_graph_edges = self.__input_graph.edges

        print('Compute frequent edges!')
        frequent_edges = get_frequent_edges(self.__input_graph.edges, self.__input_graph.nodes, self.min_support)

        # intialize the generator, which generates the new candidates
        generator = Generator(frequent_edges)

        # initialize the evaluator, which evaluates if the candidates are above the predefined min_support
        evaluator = Evaluator(self.min_support)

        # generate the initial size 1 candidates
        print('Generate initial candidates:')
        initial_candidates = generator.generate_initial_candidates(execution_mode)
        print('\t '+str(len(initial_candidates))+' initial candidates were found!')

        # append initial_candidates to frequent_subgraphs
        self.__frequent_subgraphs = self.__frequent_subgraphs.append(initial_candidates)
        self.__current_max_size += 1

        # set new_candidates_found boolean to True
        new_candidates_found = True

        # execute while-loop until no more frequent candidates can't be found
        while new_candidates_found:

            print('Size '+str(self.__current_max_size + 1)+' patterns:')
            # set new_candidates_found boolean to False
            new_candidates_found = False

            # generate the next n+1-size candidates
            print('\t Generate patterns:')
            new_subgraphs = generator.generate_new_subgraphs(
                self.frequent_subgraphs[self.frequent_subgraphs['size'] == self.__current_max_size], execution_mode)
            print('\t\t ' + str(len(new_subgraphs)) + ' new patterns were found!')

            # evaluate which of the newly generated candidates are frequent/above the predefined min_support
            print('\t Compute frequent candidates:')
            new_frequent_subgraphs = evaluator.evaluate_candidates(new_subgraphs, execution_mode,
                                                                   input_csp_graph, input_graph_edges)
            print('\t\t '+str(len(new_frequent_subgraphs))+' frequent subgraphs were found!')

            # if there are some new frequent subgraphs, execute if statements
            if len(new_frequent_subgraphs) > 0:
                # append the new frequent subgraphs to frequent_subgraphs
                self.__frequent_subgraphs = self.__frequent_subgraphs.append(new_frequent_subgraphs)

                # set new_candidates_found boolean to True, to stay inside while-loop
                new_candidates_found = True

                # increase current_max_size with 1
                self.__current_max_size += 1

        print('Finished')

    @property
    def input_graph(self) -> Graph:
        """The input graph for PaSiGraM algorithm

        :return: input_graph
        :rtype: Graph
        """
        return self.__input_graph

    @property
    def frequent_subgraphs(self) -> pd.DataFrame:
        """The set which contains all frequent subgraphs of the input graph.

        :return: frequent_subgraphs
        :rtype: pd.DataFrame
        """
        return self.__frequent_subgraphs

    @property
    def min_support(self) -> int:
        """The minimum support the candidates have to meet

        :return: min_support
        :rtype: int
        """
        return self.__min_support
