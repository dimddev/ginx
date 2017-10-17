#!/usr/bin/env python3.5
"""
Module name
"""
import os
import pathlib
import json
import random
from collections import OrderedDict

import click

# TODO
# 2. More segmented code, re-organaizing, refactoring, testing.
# 3. More commands and options to be provided


class GinXBuilder:
    """GinXBuilder"""

    def __init__(self):
        """__init__"""

        self.__new_project_data = None
        self.from_file = None

    @staticmethod
    def edges_mean(g_data, project_name):
        """edges_mean

        :param g_data
        :param project_name
        """

        if pathlib.Path('.ginx/{0}/.{0}.cache'.format(project_name)).is_file():
            with open('.ginx/{0}/.{0}.cache'.format(project_name)) as graph_read:
                return json.load(graph_read)

        g_data = [(key, g_data[key]) for key in sorted(g_data.keys())]
        g_data = OrderedDict(g_data)

        target_bag = []

        for key in g_data.keys():
            for item in g_data.items():
                for node in item[1]:

                    key_targets = []

                    if key == node[1]:

                        key_targets.append(node[0])
                        key_targets.append(node[1])
                        key_targets.append(node[2]['weight'])
                        target_bag.append(key_targets)

        for data in g_data.items():
            for node in data[1]:
                for bag in target_bag:

                    if node[0] == bag[1] and node[1] == bag[0]:
                        node[2]['weight'] = (bag[2] +  node[2]['weight']) / 2

        # make a cache file
        if not pathlib.Path('.ginx/{0}/.{0}.cache'.format(project_name)).is_file():
            with open('.ginx/{0}/.{0}.cache'.format(project_name), 'w') as graph:
                graph.write(json.dumps(g_data))

        return g_data


    def init_from_file(self, from_file, new_project=True):
        """init_from_file

        :param from_file
        :param new_project
        """
        with open('{}'.format(from_file)) as graph:

            extension = pathlib.PurePath(from_file).suffix

            if extension == '.json':
                # TODO
                # to be passed as argument to self.process_new_project()
                # self.from_file is used by self.process_new_project()
                self.from_file = json.load(graph)

            elif extension == '.csv':
                pass

            elif extension == 'txt':
                # extension == '.txt':
                self.from_file = [g for g in graph.read().split('\n') if g != '']

            else:
                click.echo('File format {} is not supported!'.format(extension))

            if new_project:
                self.process_new_project()

    def project_name(self):
        """project_name"""

        project_name = input('Project name: ')

        if not project_name:

            click.echo('Project name cannot be empty!')
            self.project_name()

        file_name = '.ginx/{}-init.graph'.format(project_name)

        if os.path.isfile(file_name):

            click.echo('Project with that name exist, please choose new one...')
            self.project_name()

        return project_name

    @staticmethod
    def write_graph_db(project_name, data, file_name):
        """write_graph_db

        :param project_name
        :param data
        :param file_name
        """

        if not isinstance(data, dict):
            click.echo('Data must be a dict')
            return False

        if not os.path.isdir('.ginx/{}'.format(project_name)):
            os.makedirs('.ginx/{}'.format(project_name))

        with open('.ginx/{}/{}-edges.graph'.format(project_name, file_name), 'w') as graph_file:
            graph_file.write(json.dumps(data, indent=2))

    def process_new_project(self, hello=True):
        """process_new_project

        :param hello
        """

        data = {}

        if hello:

            click.echo('Hello from FGraph detective.')
            click.echo('Please answering honestly on the next questions for best characteristic.')
            click.echo('The answers are numbers ( integer ) from 1 to 10.')
            click.echo('When you choose answer between 1 to 5, that means, you having this answer,')
            click.echo('as something close to you, but if you choose an answer bigger than 5,')
            click.echo('the answer have a small priority. So 1 is the best, 10 is the worst.')
            click.echo('Type 0 if there arn\'t connecion.')
            click.echo('\n')

        project_name = self.project_name()

        if os.path.isdir('.ginx/{}'.format(project_name)):

            click.echo('A project with this name exist, please choose new one...')
            self.process_new_project(False)
            return

        # self.from_file is set by self.init_from_file()
        for crew in self.from_file:

            data[crew] = []
            temp = []

            click.echo('Item: {}'.format(crew))

            for crew_fship in self.from_file:

                if crew == crew_fship:
                    continue

                try:

                    weight = int(input(
                        'What is the weight between {} and {} [0]: '.format(crew, crew_fship)
                    ))

                except ValueError:
                    weight = 0

                if weight == 0:
                    continue

                temp.append((crew, crew_fship, {'weight': weight}, ))
                # self.__graph.add_edge(crew, crew_fship, weight=int(weight))

            data[crew] += temp
            self.write_graph_db(project_name, {crew: data[crew]}, crew)

        self.write_graph_db(project_name, data, project_name)
        click.echo('Multi Graph for project {} was created'.format(project_name))
        self.__new_project_data = data

    def load_project(self, project_name=None):
        """load_project

        :param project_name
        """
        # self.__new_project_data is set by the process_new_project
        if self.__new_project_data and project_name is None:
            return self.edges_mean(self.__new_project_data, project_name)

        if project_name and pathlib.Path(
                '.ginx/{0}/{0}-edges.graph'.format(project_name)).is_file():

            with open('.ginx/{0}/{0}-edges.graph'.format(project_name)) as graph:
                return self.edges_mean(json.load(graph), project_name)

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

    def get_short_path(self, from_, to_):
        """get_short_path

        :param from_
        :param to
        """

        from networkx.exception import NetworkXNoPath
        from networkx.algorithms import all_shortest_paths

        try:
            return self.to_json(list(all_shortest_paths(self.__graph, from_, to_, 'weight')))
        except NetworkXNoPath:
            click.echo('No shortest paths between {} and {}'.format(from_, to_))

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
        self.__nx.draw_networkx_edges(self.__graph,
            pos, edge_color='k',
            arrows=True
        )
        plt.show()

@click.group()
@click.option('-q', is_flag=True, help='Remove the head line before the result')
def main(q):
    """Graph Inspector
    """
    pass

@click.command()
@click.argument('INIT_FILE', nargs=1)
def project(init_file):
    """Init new project from json or csv files"""

    if init_file:
        djb = GinXBuilder()
        djb.init_from_file(init_file)

@click.command()
@click.argument('project', type=click.STRING)
@click.option('-f', type=click.STRING, help='Used together with SP, select the start node')
@click.option('-t', type=click.STRING, help='Used together with SP, select the end node')
def gpath(project, f, t):
    """Get graph paths (SP) between nodeA and nodeB"""

    djb = GinXBuilder()

    if project:
        ginx_graph = GinXQuery(djb.load_project(project))

        if f and t:
            click.echo('Get shortest path between {} and {}'.format(f, t))
            click.echo(ginx_graph.get_short_path(f, t))

@click.command()
@click.argument('project', type=click.STRING)
@click.option('-c', is_flag=True, help='Print the current flow closeness centrality.\
Compute current-flow closeness centrality for nodes. Current-flow closeness centrality is variant of closeness \
centrality based on effective resistance between nodes in a network. This metric is also known as information centrality')
@click.option('-b', is_flag=True, help='''Communicability betweenness centrality. Return subgraph
communicability for all pairs of nodes in G. Communicability betweenness measure makes use of the number of walks \
connecting every pair of nodes as the basis of a betweenness centrality measure.''')
@click.option('-f', is_flag=True, help='''Print the current flow betweenness centrality. Current-flow betweenness \
centrality uses an electrical current model for information spreading in contrast to betweenness centrality which
uses shortest paths.''')
@click.option('-d', is_flag=True, help='Print distance measures center')
@click.option('-p', is_flag=True, help='Print distance measures periphery')
@click.option('-t', is_flag=True, help='Print the numbers of triangles that include a node as one vertex')
@click.option('-s', is_flag=True, help='Use matplotlib to draw the graph')
def gquery(project, c, b, f, s, d, p, t):
    """gquery - perform statistical operations"""

    djb = GinXBuilder()

    if project:
        ginx_graph = GinXQuery(djb.load_project(project))

        if c:
            click.echo('Current flow closeness centrality:')
            click.echo(ginx_graph.current_flow_closeness_centrality())

        if b:
            click.echo('Communicability betweenness centrality:')
            click.echo(ginx_graph.communicability_betweenness_centrality())

        if f:
            click.echo('Current flow betweenness centrality')
            click.echo(ginx_graph.current_flow_betweenness_centrality())

        if t:
            click.echo('Print the numbers of triangles that include a node as one vertex')
            click.echo(ginx_graph.triangles())

        if d:
            click.echo('Distance measures center:')
            click.echo(ginx_graph.d_central())

        if p:
            click.echo('Distance measures periphery')
            click.echo(ginx_graph.d_periphery())

        if s:
            ginx_graph.showme()

@click.command()
def docker():
    """GinX use docker container as computing machine.
    All dependecies are installed there."""
    pass

@click.command()
def aws():
    """GinX use AWS as computing architecture. Using S3, Lambdas and more"""
    pass

if __name__ == '__main__':
    main.add_command(project)
    main.add_command(gquery)
    main.add_command(gpath)
    main.add_command(aws)
    main.add_command(docker)
    main()
