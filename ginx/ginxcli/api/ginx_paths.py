""" GinXPaths """
import click
from .ginx_shared import GinXBase

from networkx.exception import NetworkXNoPath
from networkx.algorithms import all_shortest_paths


class GinXPaths(GinXBase):
    """GinXQuery"""

    def __init__(self, graph_data):
        """__init__"""
        super().__init__(graph_data)

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

        try:
            return self.common.to_json(list(all_shortest_paths(self.graph, from_, to_, 'weight')))
        except NetworkXNoPath:
            click.echo('No shortest paths between {} and {}'.format(from_, to_))
