from pasigram.model.graph import *


class Evaluator:
    """ A class to represent the evaluator component of the PaSiGraM algorithm.

    ...

    Attributes
    ----------
    min_support: Integer
        The minimum support the graphs have to meet
    input_graph : pd.DataFrame
        The input graph to use to compute the frequencies of the candidates
    """

    def __init__(self, csp_graph: pd.DataFrame, min_support: int) -> object:
        """

        Parameters
        ----------
        csp_graph: pd.DataFrame
            The csp graph representation of the input graph
        min_support : Integer
            The minimum support the candidates have to meet
        """
        self.__min_support = min_support
        self.__input_graph = csp_graph
        self.__frequent_subgraphs = pd.DataFrame(columns=['number_of_edges', 'graph'])

    def compute_candidate_frequency(self, candidate_csp_graph: pd.DataFrame) -> int:
        """Method to compute the frequency of one candidate in the input graph.

        Parameters
        ----------
        candidate_csp_graph : pd.DataFrame
            The csp graph representation of the candidate

        Returns
        -------
        The frequency of the candidate in the input graph.
        """

        # initialize candidate frequency
        candidate_frequency = -1

        # iterate over all nodes of the candidate to check what frequency every node in the input graph has
        for i in range(0, len(candidate_csp_graph)):
            # get the current node (result = pd.Series -> Access to entries with loc-method)
            current_node = candidate_csp_graph.iloc[i]
            current_node_label = current_node.loc['label']
            current_node_indegree = current_node.loc['indegree']
            current_node_outdegree = current_node.loc['outdegree']
            current_node_frequency = 0

            # get all nodes from 'input_graph' with the same label as 'current_node'
            candidate_clusters = self.__input_graph[self.__input_graph['label'] == current_node_label]

            # iterate over all nodes in 'candidate_clusters'
            for j in range(0, len(candidate_clusters)):
                # get the current node out of 'candidate_clusters' (result = pd.Series)
                potential_partner_node = candidate_clusters.iloc[j]

                # get the indegree and outdegree of 'potential_partner_node'
                potential_partner_node_indegree = potential_partner_node.loc['indegree']
                potential_partner_node_outdegree = potential_partner_node.loc['outdegree']

                # check if node degree constraint is violated
                if (potential_partner_node_indegree >= current_node_indegree and
                        potential_partner_node_outdegree >= current_node_outdegree):
                    # get the neighbour lists of the nodes
                    current_node_neighbour_list = current_node.loc['neighbours']
                    potential_partner_node_neighbour_list = potential_partner_node.loc['neighbours']

                    # check if neighbour list constraint is violated
                    # todo: check for alternatives with better performance
                    #  (check if one list is subset of the other list)
                    if all([element in potential_partner_node_neighbour_list for element in
                            current_node_neighbour_list]):
                        potential_partner_node_frequency = potential_partner_node.loc['frequency']
                        current_node_frequency += potential_partner_node_frequency

            # check if the frequency of current candidate node is lower then min_frequency of already evaluated nodes
            if current_node_frequency < candidate_frequency or candidate_frequency < 0:
                candidate_frequency = current_node_frequency

        return candidate_frequency
