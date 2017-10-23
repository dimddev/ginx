""" GinXPaths """
from typing import Callable
import json
import click
from networkx.exception import NetworkXNoPath
from networkx.algorithms import all_shortest_paths, shortest_path

from .ginx_shared import GinXBase


class GinXPaths(GinXBase):
    """GinXQuery"""

    def get_path(self, path_method: Callable, from_: str, to_: str, weight: str) -> json:
        """get_path

        :param path_method:
        :type path_method: Callable
        :param from_:
        :type from_: str
        :param to_:
        :type to_: str
        :param weight:
        :type weight: str

        :rtype: json
        """
        try:
            return self.common.to_json(list(path_method(self.graph, from_, to_, weight)))
        except NetworkXNoPath:
            click.echo('No shortest path(s) between {} and {}'.format(from_, to_))
            return []

    def get_shortest_path(self, from_: str, to_: str) -> json:
        """get_shortest_path

        :param from_:
        :type from_: str
        :param to_:
        :type to_: str

        :rtype: json
        """
        return self.get_path(shortest_path, from_, to_, 'weight')

    def get_shortest_paths(self, from_: str, to_: str) -> json:
        """get_shortest_paths

        :param from_:
        :type from_: str
        :param to_:
        :type to_: str

        :rtype: json
        """
        return self.get_path(all_shortest_paths, from_, to_, 'weight')
