""" GinXCommon """
import random
import json

class GinXCommon:

    """Docstring for GinXCommon. """

    def __init__(self):
        """TODO: to be defined1. """

    @staticmethod
    def to_json(data):
        """to_json

        :param data
        """
        return json.dumps(data, indent=2)

    @staticmethod
    def random_hex_color(num):
        """random_hex_color

        :param num
        """
        return [hex(random.randrange(0, 16777215)) for x in range(num)]

    def sorted_dict(self, method, graph):
        """sorted_dict

        :param method
        :param graph
        """
        return self.to_json(sorted(method(graph).items(), key=lambda x: x[1], reverse=True))
