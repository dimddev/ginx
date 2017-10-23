""" GinX Shared """
from networkx import nx
import matplotlib.pyplot as plt
from .ginx_common import GinXCommon


class GinXBase:
    """GinXQuery"""

    def __init__(self, graph_data):
        """__init__"""

        self.nx = nx
        self.graph = nx.Graph()
        self.common = GinXCommon()

        for edge in graph_data.keys():
            self.graph.add_edges_from(graph_data[edge])

    def showme(self, s_paths):
        """showme"""

        pos = self.nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, node_color='c')

        # self.nx.draw_networkx_nodes(
        #     self.graph, pos,
        #     node_color=['r'],
        #     node_size=2000
        # )

        path_edges = zip(s_paths[1:])
        print(s_paths)
        self.nx.draw_networkx_nodes(self.graph, pos, nodelist=s_paths, node_color='r')
        print(11111111111)
        self.nx.draw_networkx_labels(self.graph, pos)
        self.nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='r', arrows=True)
        plt.show()
