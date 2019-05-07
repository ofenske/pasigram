import pandas as pd
from pasigram.controller.csp.evaluator import Evaluator
from pasigram.controller.candidate_generation.generator import Generator
from pasigram.model.graph import Graph


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

    def execute(self):
        """Method to execute the PaSiGraM algorithm

        :return:
        """
        # intialize the generator, which generates the new candidates
        generator = Generator(self.input_graph.unique_edges, self.min_support)

        # initialize the evaluator, which evaluates if the candidates are above the predefined min_support
        evaluator = Evaluator(self.input_graph.csp_graph, self.min_support)

        # generate the initial size 1 candidates
        initial_candidates = generator.generate_initial_candidates()

        # append initial_candidates to frequent_subgraphs
        self.__frequent_subgraphs = self.__frequent_subgraphs.append(initial_candidates)
        self.__current_max_size += 1

        # set new_candidates_found boolean to True
        new_candidates_found = True

        # execute while-loop until no more frequent candidates can't be found
        while new_candidates_found:

            # set new_candidates_found boolean to False
            new_candidates_found = False

            # generate the next n+1-size candidates
            new_subgraphs = generator.generate_new_subgraphs(
                self.frequent_subgraphs[self.frequent_subgraphs['size'] == self.__current_max_size])

            # evaluate which of the newly generated candidates are frequent/above the predefined min_support
            new_frequent_subgraphs = evaluator.evaluate_candidates(new_subgraphs)

            # if there are some new frequent subgraphs, execute if statements
            if len(new_frequent_subgraphs) > 0:

                # append the new frequent subgraphs to frequent_subgraphs
                self.__frequent_subgraphs = self.__frequent_subgraphs.append(new_frequent_subgraphs)

                # # set new_candidates_found boolean to True, to stay inside while-loop
                new_candidates_found = True

                # increase current_max_size with 1
                self.__current_max_size += 1
                print(self.__current_max_size)

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
