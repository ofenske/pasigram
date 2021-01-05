import pandas as pd
import multiprocessing as mp
import numpy as np
from functools import partial


def compute_edge_ids(edges: pd.DataFrame) -> list:
    """Method for computing a list with ids of all edges in it

    :param pd.DataFrame edges: Contains all edges
    :return: A list with all ids of the edges.
    :rtype: list
    """

    return list(edges.index)


def compute_frequent_edges(edges: pd.DataFrame, nodes: pd.DataFrame, min_support: int,
                           local_distributed: bool) -> pd.DataFrame:
    """Method to compute frequent edges that support a given 'min_support'

    :param pd.DataFrame edges: Set of all edges of a graph
    :param pd.DataFrame nodes: Set of all nodes of a graph
    :param int min_support: The predefined min_support for the algorithm
    :param bool local_distributed: Set to 'True' if the computation should be distributed over all multiple cpu cores
    :return: Set of all frequent edges
    :rtype: pd.DataFrame
    """
    frequent_edges = pd.DataFrame(columns=['source', 'target', 'label', 'frequency'])

    if local_distributed is True:
        # set the number of processes (one process for each cpu core)
        num_processes = mp.cpu_count()

        # divide edges into chunks, so that every processes has approximately the same number of edges
        if len(edges) <= num_processes:
            if len(edges) == 0:
                edges_chunks = np.array_split(edges, 1)
            else:
                edges_chunks = np.array_split(edges, len(edges))
        else:
            edges_chunks = np.array_split(edges, num_processes)

        # execute the parallel computation
        with mp.Pool(processes=num_processes) as pool:
            result = pool.map(partial(get_frequent_edges, nodes=nodes, min_support=min_support), edges_chunks)

        # collect all results in one DataFrame
        for candidates in result:
            for i in range(len(candidates)):
                if candidates.iloc[i].name in list(frequent_edges.index):
                    frequent_edges.loc[candidates.iloc[i].name].frequency += 1
                else:
                    frequent_edges.at[candidates.iloc[i].name] = candidates.iloc[i]

    # execute computation on one cpu core
    else:
        frequent_edges = get_frequent_edges(edges, nodes, min_support)

    return frequent_edges[frequent_edges['frequency'] >= min_support]


def get_frequent_edges(edges: pd.DataFrame, nodes: pd.DataFrame, min_support: int) -> pd.DataFrame:
    """Method to compute frequent edges that support a given 'min_support'

    :param pd.DataFrame edges: Set of all edges of a graph
    :param pd.DataFrame nodes: Set of all nodes of a graph
    :param int min_support: The predefined min_support for the algorithm
    :return: Set of all frequent edges
    :rtype: pd.DataFrame
    """
    # get list of labels of all nodes
    nodes_labels = list(nodes['label'].values)
    # get list of keys of all nodes
    nodes_keys = list(nodes.index)
    # initialize dict with values from 'nodes_keys' as keys and values from 'nodes_labels' as values
    nodes_dict = dict(zip(nodes_keys, nodes_labels))
    labeled_edges = edges.copy()
    # replace the values of the source and target column with the values of 'nodes_dict'
    labeled_edges['source'] = labeled_edges['source'].map(nodes_dict)
    labeled_edges['target'] = labeled_edges['target'].map(nodes_dict)
    # create dummy column to sum up the occurrence for every edge
    labeled_edges['dummy'] = 1
    # sum up occurrence for every edge in a new column 'frequency'
    labeled_edges['frequency'] = labeled_edges.groupby(['source', 'target', 'label'])['dummy'].transform('sum')
    # delete duplicates and the dummy column
    labeled_edges.drop_duplicates(subset=['source', 'target', 'label'], inplace=True)
    frequent_edges = labeled_edges.drop(columns=['dummy'])

    return frequent_edges[frequent_edges['frequency'] >= min_support]
