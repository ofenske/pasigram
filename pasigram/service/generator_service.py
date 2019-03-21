import pandas as pd
from pasigram.model.graph import *


def generate_initial_candidates(frequent_edges: pd.DataFrame) -> pd.DataFrame:
    # get all frequent edges to initialize graph objects
    join_set = frequent_edges

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
        # self.__candidates.loc[current_candidate.canonical_code] = [iteration_step, current_candidate]
