import pandas as pd


class graph:
    def __init__(self, nodes, edges):
        self.__nodes = nodes
        self.__node_ids = self.__build_node_ids()
        self.__edges = edges
        self.__matrix = self.__build_graph()
        #self.__node_degrees = self.__calculate_node_degrees()
        #self.__adjacency_list = self.__build_adjacency_list()

    def __build_graph(self):
        graph = pd.DataFrame(index=self.__node_ids, columns=self.__node_ids)
        for i in range(0, len(self.__edges)):
            source_node = self.__edges.iloc[i][1]
            target_node = self.__edges.iloc[i][2]
            graph[target_node][source_node] = self.__edges.iloc[i][0]
        return graph

    def __build_adjacency_list(self):
        adjacency_list = pd.DataFrame(index=self.__node_ids, columns=['neighbours'])

        for i in range(0, len(self.__nodes)):
            current_node_id = self.__nodes.iloc[i]['id']
            adjacency_list['neighbours'][current_node_id] = pd.DataFrame(
                columns=['edge_label', 'neighbour_vertex_degree', 'neighbour_vertex_label'])
            for j in range(0, len(self.__edges)):
                if self.__edges.iloc[j]["source"] == adjacency_list.iloc[i]["id"]:
                    adjacency_list['neighbours'][i].append()

        return adjacency_list

    def __build_node_ids(self):
        node_ids = []
        for i in range(0, len(self.__nodes)):
            node_ids.append(self.__nodes.iloc[i]['id'])
        return node_ids

    def __calculate_node_degrees(self):
        node_degrees = pd.DataFrame(index=self.__node_ids, columns=['degree'])
        for i in range (0,len(self.__nodes)):
            current_node_id = self.__nodes.iloc[i]['id']
            current_node_degree = 0
            for j in range(0, len(self.__matrix.iloc[current_node_id])):
                if self.__matrix.iloc[current_node_id][j] != 'NaN':
                    current_node_degree += 1
            node_degrees['degree'][current_node_id] = current_node_degree

    def get_matrix(self):
        return self.__matrix

    def get_nodes(self):
        return self.__nodes

    def get_edges(self):
        return self.__edges

    def get_adjacency_list(self):
        return self.__adjacency_list

    def get_node_ids(self):
        return self.__node_ids, type(self.__node_ids)


# -----------------------------------------------------------------Tests-------------------------------------------------

edges = pd.read_csv('edges.csv', sep=';')
nodes = pd.read_csv('nodes.csv', sep=';')

graph = graph(nodes, edges)
print(graph.get_matrix())
