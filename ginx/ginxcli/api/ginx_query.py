""" GinX Query Module"""

import itertools

from networkx.algorithms import current_flow_closeness_centrality
from networkx.algorithms import current_flow_betweenness_centrality
from networkx.algorithms.centrality import communicability_betweenness_centrality
from networkx.algorithms.centrality.betweenness import betweenness_centrality
from networkx.algorithms.community import centrality
from networkx.algorithms import distance_measures
from networkx.algorithms import clustering
from networkx.algorithms import triangles
from networkx.algorithms.connectivity import local_edge_connectivity

from .ginx_shared import GinXBase


class GinXQuery(GinXBase):
    """GinXQuery"""

    def girvan_newman(self):
        """Finds communities in a graph using the Girvan–Newman method."""
        # https://github.com/networkx/networkx/blob/master/networkx/algorithms/community/centrality.py
        return [x for x in itertools.islice(centrality.girvan_newman(self.graph), 4)]

    def betweeness_centrality(self, k=None):
        """Compute the shortest-path betweenness centrality for nodes.
           Betweenness centrality of a node V is the sum of the
           fraction of all-pairs shortest paths that pass through V.
           A node with higher betweenness centrality would have more
           control over the network, because more information will pass through that node.
        """
        return self.common.sorted_dict(betweenness_centrality, self.graph)

    def current_flow_closeness_centrality(self):
        """Compute current-flow closeness centrality for nodes.
           Current-flow closeness centrality is variant of closeness
           centrality based on effective resistance between nodes in
           a network. This metric is also known as information centrality
        """
        return self.common.sorted_dict(current_flow_closeness_centrality, self.graph)

    def current_flow_betweenness_centrality(self):
        """Current-flow betweenness centrality uses an electrical current
           model for information spreading in contrast to betweenness
           centrality which uses shortest paths.
        """
        return self.common.sorted_dict(current_flow_betweenness_centrality, self.graph)

    def communicability_betweenness_centrality(self):
        """Communicability betweenness centrality
           Return subgraph communicability for all pairs of nodes in G.
           Communicability betweenness measure makes use of the number of walks
           connecting every pair of nodes as the basis of a betweenness centrality measure.
        """
        return self.common.sorted_dict(communicability_betweenness_centrality, self.graph)

    def d_central(self):
        """d_center"""
        return self.common.to_json(distance_measures.center(self.graph))

    def d_periphery(self):
        """d_periphery"""
        return self.common.to_json(distance_measures.periphery(self.graph))

    def d_cluster(self):
        """d_cluster"""
        return self.common.to_json(clustering(self.graph))

    def triangles(self):
        """Triangles
        Finds the number of triangles that include a node as one vertex
        """
        return self.common.to_json(triangles(self.graph))
