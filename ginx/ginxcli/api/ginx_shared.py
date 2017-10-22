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

    def showme(self):
        """showme"""

        pos = self.nx.spring_layout(self.graph)

        self.nx.draw_networkx_nodes(
            self.graph, pos,
            node_color=['c', 'b', 'g'],
            node_size=2000
        )
        self.nx.draw_networkx_labels(self.graph, pos)
        self.nx.draw_networkx_edges(self.graph, pos, edge_color='k', arrows=True)
        plt.show()
