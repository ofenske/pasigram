import pandas as pd
from pasigram.service.edges_service import *
from pasigram.model.graph import *


class Generator:
    """ A class to represent the generator component of the PaSiGraM algorithm.

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
        self.__candidates = pd.DataFrame(columns=['number_of_edges', 'graph'])

    def generate(self, iteration_step: int):

        # generate initial candidates with one edge
        if iteration_step == 1:

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

                # add graph object (candidate) to the candidate DataFrame
                self.__candidates.loc[current_candidate.canonical_code] = [iteration_step, current_candidate]



    @property
    def min_support(self) -> int:
        return self.__min_support

    @property
    def frequent_edges(self) -> pd.DataFrame:
        return self.__frequent_edges

    @property
    def candidates(self) -> pd.DataFrame:
        return self.__candidates
