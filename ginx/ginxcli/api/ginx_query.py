""" GinX Query Module"""
import json
import click


class GinXQuery:
    """GinXQuery"""

    def __init__(self, graph_data):
        """__init__"""

        from networkx import nx
        self.__nx = nx
        self.__graph = nx.Graph()

        for edge in graph_data.keys():
            self.__graph.add_edges_from(graph_data[edge])

    @staticmethod
    def to_json(data):
        """to_json

        :param data
        """
        return json.dumps(data, indent=2)

    @staticmethod
    def random_hex_color(num):
        return [hex(random.randrange(0, 16777215)) for x in range(num)]

    def get_shortest_path(self, from_, to_):
        """get_shortest_path

        :param from_
        :param to_
        """
        pass

    def get_shortest_paths(self, from_, to_):
        """get_shortest_paths

        :param from_
        :param to
        """

        from networkx.exception import NetworkXNoPath
        from networkx.algorithms import all_shortest_paths

        try:
            return self.to_json(list(all_shortest_paths(self.__graph, from_, to_, 'weight')))
        except NetworkXNoPath:
            click.echo('No shortest paths between {} and {}'.format(from_, to_))

    def girvan_newman(self):
        """Finds communities in a graph using the Girvan–Newman method."""
        # https://github.com/networkx/networkx/blob/master/networkx/algorithms/community/centrality.py
        pass

    def betweeness_centrality(self, node):
        """Compute the shortest-path betweenness centrality for nodes.
           Betweenness centrality of a node $node$ is the sum of the
           fraction of all-pairs shortest paths that pass through $node$
        """
        pass

    def current_flow_closeness_centrality(self):
        """Compute current-flow closeness centrality for nodes.
           Current-flow closeness centrality is variant of closeness
           centrality based on effective resistance between nodes in
           a network. This metric is also known as information centrality
        """
        from networkx.algorithms import current_flow_closeness_centrality
        return self.to_json(sorted(
            current_flow_closeness_centrality(self.__graph).items(),
            key=lambda x: x[1], reverse=True
        ))

    def current_flow_betweenness_centrality(self):
        """Current-flow betweenness centrality uses an electrical current
           model for information spreading in contrast to betweenness
           centrality which uses shortest paths.
        """
        from networkx.algorithms import current_flow_betweenness_centrality
        return self.to_json(sorted(
            current_flow_betweenness_centrality(self.__graph).items(),
            key=lambda x: x[1], reverse=True
        ))

    def communicability_betweenness_centrality(self):
        """Communicability betweenness centrality
           Return subgraph communicability for all pairs of nodes in G.
           Communicability betweenness measure makes use of the number of walks
           connecting every pair of nodes as the basis of a betweenness centrality measure.
        """
        from networkx.algorithms.centrality import communicability_betweenness_centrality
        return self.to_json(sorted(
            communicability_betweenness_centrality(self.__graph).items(),
            key=lambda x: x[1], reverse=True
        ))

    def d_central(self):
        """d_center"""
        from networkx.algorithms import distance_measures
        return self.to_json(distance_measures.center(self.__graph))

    def d_periphery(self):
        """d_periphery"""
        from networkx.algorithms import distance_measures
        return self.to_json(distance_measures.periphery(self.__graph))

    def d_cluster(self):
        """d_cluster"""
        from networkx.algorithms import clustering
        return clustering(self.__graph)

    def triangles(self):
        """Triangles
        Finds the number of triangles that include a node as one vertex
        """
        from networkx.algorithms import triangles
        return triangles(self.__graph)

    def showme(self):
        """showme"""

        import matplotlib.pyplot as plt

        pos = self.__nx.spring_layout(self.__graph)

        self.__nx.draw_networkx_nodes(
            self.__graph, pos,
            node_color=['c', 'b', 'g'],
            node_size=2000
        )
        self.__nx.draw_networkx_labels(self.__graph, pos)
        self.__nx.draw_networkx_edges(self.__graph, pos, edge_color='k', arrows=True)
        plt.show()
