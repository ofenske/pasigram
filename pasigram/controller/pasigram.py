from pasigram.controller.evaluator import *
from pasigram.controller.generator import *


class Pasigram:
    """ Interface of the PaSiGraM algorithm.

        ...

        Attributes
        ----------
        min_support: Integer
            The minimum support the graphs have to meet
        input_graph : pd.DataFrame
            The input graph to use to compute the frequencies of the candidates
        frequent_subgraphs : pd.DataFrame
            The set which contains all frequent subgraphs of the input graph.
        """

    def __init__(self, input_graph: Graph, min_support: int) -> object:
        """

        Parameters
        ----------
        input_graph: pd.DataFrame
            The input graph for PaSiGraM algorithm
        min_support : Integer
            The minimum support the candidates have to meet
        """
        self.__min_support = min_support
        self.__input_graph = input_graph
        self.__frequent_subgraphs = pd.DataFrame(columns=['iteration_step', 'number_of_edges', 'graph', 'frequency'])

    def execute(self):
        generator = Generator(self.input_graph.unique_edges, self.min_support)
        evaluator = Evaluator(self.input_graph.csp_graph, self.min_support)

    @property
    def input_graph(self):
        return self.__input_graph

    @property
    def frequent_subgraphs(self):
        return self.__frequent_subgraphs

    @property
    def min_support(self):
        return self.__min_support
