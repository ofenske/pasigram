import pandas as pd


def build_canonical_smallest_code(final_clusters: pd.DataFrame) -> str:
    """Method for building the canonical code of a graph.

    Parameters
    ----------
    final_clusters : pd.DataFrame
        The DataFrame which contains the final clusters of the nodes.

    Returns
    -------
    String
    """

    # get all keys from final clusters
    keyset = list(final_clusters.index)

    # append number of elements to every clustername (clustername+"#1#")
    for i in range(0, len(keyset)):
        number_of_elements = len(final_clusters.loc[keyset[i]]['elements'])
        keyset[i] = keyset[i] + '#' + str(number_of_elements) + '#'

    # sort the keyset
    sorted_keyset = sorted(keyset)

    # Initialize the final label for the graph
    label = ""

    # Iterate over all elements in sorted_keyset
    for i in range(0, len(sorted_keyset)):
        # build label element by element
        label += sorted_keyset[i]

    return label
