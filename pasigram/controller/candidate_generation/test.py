import pandas as pd
from pasigram.model.graph import *

nodes = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\nodes.csv', sep=';', index_col='id')
edges = pd.read_csv(r'C:\Users\OleFe\workspace\pasigram\data\edges.csv', sep=';', index_col='id')
graph = Graph(nodes, edges)

graph.root_node = 1
graph.right_most_node = 10


def find_shortest_path(graph: Graph):
    start_node_id = graph.root_node
    end_node_id = graph.right_most_node

    node_set = pd.DataFrame(columns=["parent"])
    queue = [end_node_id]
    visited_nodes = [end_node_id]
    found = False

    right_most_nodes = []

    while not found:
        current_node_id = queue.pop(0)
        if current_node_id == end_node_id:
            node_set.loc[current_node_id] = None
        edge_list = graph.edges[(graph.edges['source'] == current_node_id) | (graph.edges['target'] == current_node_id)]

        for i in range(0, len(edge_list)):
            potential_child_node = edge_list.iloc[i]['source']
            if potential_child_node != current_node_id and potential_child_node not in visited_nodes:
                node_set.loc[potential_child_node] = current_node_id
                queue.append(potential_child_node)
                visited_nodes.append(potential_child_node)
                if potential_child_node == start_node_id:
                    found = True
                    break
                continue

            potential_child_node = edge_list.iloc[i]['target']
            if potential_child_node != current_node_id and potential_child_node not in visited_nodes:
                node_set.loc[potential_child_node] = current_node_id
                queue.append(potential_child_node)
                visited_nodes.append(potential_child_node)
                if potential_child_node == start_node_id:
                    found = True
                    break
                continue
    current_node = start_node_id
    while current_node != end_node_id:
        right_most_nodes.append(current_node)
        current_node = node_set.loc[current_node]['parent']

    right_most_nodes.append(current_node)

    return right_most_nodes


print(find_shortest_path(graph))
