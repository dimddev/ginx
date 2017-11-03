""" GinX Shared """
from networkx import nx
import matplotlib.pyplot as plt
from .ginx_common import GinXCommon
import numpy as np
import pandas as pd


class GinXBase:
    """GinXQuery"""

    def __init__(self, graph_data):
        """__init__"""

        self.nx = nx
        self.graph = nx.Graph()
        self.common = GinXCommon()

        self.graph.add_nodes_from(graph_data['nodes'])

        for edge in graph_data['edges'].keys():
            self.graph.add_edges_from(graph_data['edges'][edge])

        self.nodes_colors = ['#DC143C', '#FF4500', '#DB7093', '#C0AFEC']
        self.edges_colors = ['#98FB98', '#3CB371', '#F5CC13', '#EE745E']

        self.nodes_centrality_colors = [
            '#E6E6FA', # 0 POWDERBLUE
            '#87CEEB', # 1 sky blue
            '#00FA9A', # 2 LIMEGREEN
            '#DDA0DD', # 3 green
            '#FFD700', # 4 gold
            '#FF6347', # 5 orange
            '#FF0000'  # 6 red
        ]

    def showbar(self, data: list, title: str, ylabel: str):

        labels = [d[0] for d in data]
        y_data = [d[1] for d in data]

        x_data = list(np.arange(1, len(y_data) + 1))

        fig, ax = plt.subplots()
        plt.bar(labels, y_data)

        # ax.set_xticklabels(labels)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        plt.show()

    def showme_centrality(self, nodes, title):
        """showme_centrality

        :param data
        :param title
        """
        nodes = pd.DataFrame(nodes)
        nodes.set_index(0)
        bins = np.arange(0, 1.0, 0.001)
        nodes_group = nodes.groupby(np.digitize(nodes[1], bins)).ngroup()

        pos = self.nx.spring_layout(self.graph)

        self.nx.draw_networkx_labels(self.graph, pos, font_color='#58584F')

        for index, node_group in enumerate(nodes_group):
            # print(nodes[0][index], node_group)

            if node_group > len(self.nodes_centrality_colors):
                color = self.nodes_centrality_colors[-1]
            else:
                color = self.nodes_centrality_colors[node_group]

            self.nx.draw_networkx_nodes(
                self.graph, pos,
                node_color=[color],
                nodelist=[nodes[0][index]],
                node_size=2400
            )

        self.nx.draw_networkx_edges(
            self.graph,
            pos,
            edge_color='#F1F1CE',
            arrows=True,
            width=2.0
        )

        plt.show()

    def showme_center_periphery(self, center, periphery):
        """showme"""
        pos = self.nx.spring_layout(self.graph)

        # n_color= '#{}'.format(hex(np.random.randint(2458208, 4855479))[2:])
        n_color_center = '#F5807B'
        n_color_periphery = '#88DB99'

        # first draw center
        self.nx.draw_networkx_nodes(
            self.graph, pos,
            node_color=[n_color_center],
            nodelist=center,
            node_size=2400,
            linewidths=2.0
        )

        self.nx.draw_networkx_labels(self.graph, pos, font_color='#58584F')
        # first draw periphery
        self.nx.draw_networkx_nodes(
            self.graph, pos,
            node_color=[n_color_periphery],
            nodelist=periphery,
            node_size=1900
        )

        # self.nx.draw_networkx_labels(self.graph, pos, font_color='#F1F1CE')

        self.nx.draw_networkx_edges(
            self.graph,
            pos,
            edge_color='#F1F1CE',
            arrows=True,
            width=2.0
        )

        plt.show()

    def draw_graph(self, s_paths, pos, path_edges):

        self.nx.draw_networkx_nodes(
            self.graph,
            pos,
            nodelist=s_paths,
            node_color=self.nodes_colors.pop(),
            node_size=2400,
            label='Short paths between ...'
        )

        self.nx.draw_networkx_labels(self.graph, pos, font_color='#5F4C90')

        self.nx.draw_networkx_edges(
            self.graph,
            pos,
            edgelist=path_edges,
            edge_color=self.edges_colors.pop(),
            arrows=True,
            width=3.0
        )

    def showme_path(self, s_paths=None):
        """showme"""

        pos = self.nx.spring_layout(self.graph)
        self.nx.draw(
            self.graph,
            pos,
            node_color='#ACDA74',
            edge_color='#EED9B6',
            node_size=1550,
            width=2.0
        )

        # multipaths
        if isinstance(s_paths[0], list):

            for key, _ in enumerate(s_paths):
                path_edges = list(zip(s_paths[key], s_paths[key][1:]))
                self.draw_graph(s_paths[key], pos, path_edges)

        else:
            path_edges = list(zip(s_paths, s_paths[1:]))
            self.draw_graph(s_paths, pos, path_edges)

        plt.show()
