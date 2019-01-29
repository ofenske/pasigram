import pandas as pd


def compute_edge_ids(edges: pd.DataFrame) -> list:
    """

    Parameters
    ----------
    edges : pd.DataFrame
        Contains all edges

    Returns
    -------
    A list with all ids of the edges.
    """
    return list(edges.index)
