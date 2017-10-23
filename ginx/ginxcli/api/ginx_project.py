""" Builder Class """
import os
import sys
import pathlib
import json
from collections import OrderedDict
import click


class GinXBuilder:
    """GinXBuilder"""

    def __init__(self):
        """__init__"""

        self.from_file = None

        self.__new_project_data = None
        self.__user_home = pathlib.Path.home()

    def get_cache_file(self, project_name: str) -> str:
        """get_cache_file

        :param project_name:
        :type project_name: str

        :rtype: str
        """
        return '{0}/.ginx/{1}/.{1}.cache'.format(self.__user_home, project_name)

    def edges_mean(self, g_data: dict, project_name: str) -> dict:
        """edges_mean

        :param g_data:
        :type g_data: dict
        :param project_name:
        :type project_name: str

        :rtype: dict
        """

        if pathlib.Path(self.get_cache_file(project_name)).is_file():
            with open(self.get_cache_file(project_name)) as graph_read:
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
        if not pathlib.Path(self.get_cache_file(project_name)).is_file():
            with open(self.get_cache_file(project_name), 'w') as graph:
                graph.write(json.dumps(g_data))

        return g_data

    def init_from_file(self, from_file: str, new_project: bool = True):
        """init_from_file

        :param from_file
        :param new_project
        """
        if not pathlib.Path(from_file).is_file():
            click.echo('File {} not found'.format(from_file))
            return

        with open('{}'.format(from_file)) as graph:

            extension = pathlib.PurePath(from_file).suffix

            if extension == '.json':
                self.from_file = json.load(graph)

            elif extension == '.csv':
                pass

            elif extension == '.txt':
                # extension == '.txt':
                self.from_file = [g for g in graph.read().split('\n') if g != '']

            else:
                click.echo('File format {} is not supported!'.format(extension))

            if new_project:
                self.process_new_project(from_file=self.from_file)

    def project_name(self):
        """project_name"""

        project_name = input('Project name: ')

        if not project_name:

            click.echo('Project name cannot be empty!')
            self.project_name()

        file_name = '{}/.ginx/{}-init.graph'.format(self.__user_home, project_name)

        if os.path.isfile(file_name):

            click.echo('Project with that name exist, please choose new one...')
            self.project_name()

        return project_name

    def write_graph_db(self, project_name: str, data: dict, file_name: str) -> bool:
        """write_graph_db

        :param project_name:
        :type project_name: str
        :param data:
        :type data: dict
        :param file_name:
        :type file_name: str

        :rtype: bool
        """

        if not isinstance(data, dict):
            click.echo('Data must be a dict')
            return False

        if not os.path.isdir('{}/.ginx/{}'.format(self.__user_home, project_name)):
            os.makedirs('{}/.ginx/{}'.format(self.__user_home, project_name))

        with open('{}/.ginx/{}/{}-edges.graph'.format(self.__user_home, project_name, file_name), 'w') as graph_file:
            graph_file.write(json.dumps(data, indent=2))

        return True

    def process_new_project(self, **kwargs: dict) -> bool:
        """process_new_project

        :param **kwargs:
        :type **kwargs: dict

        :rtype: bool
        """

        data = {}
        from_file = kwargs.get('from_file')

        if not from_file:

            click.echo('From file is missing')
            return False

        if kwargs.get('hello'):

            click.echo('Hello from GinX - an Graph Inspector!.')
            click.echo('Please answering on the next questions for best characteristic.')
            click.echo('The answers are numbers ( integer ) from 1 to 10.')
            click.echo('When you choose answer between 1 to 5, that means,')
            click.echo('better connections between these nodes, bigger than 5 is the opposite.')
            click.echo('So 1 is the best, 10 is the worst.')
            click.echo('Type 0 if there arn\'t connecion.')
            click.echo('\n')

        project_name = self.project_name()

        if os.path.isdir('{}/.ginx/{}'.format(self.__user_home, project_name)):

            click.echo('A project with name {} already exist, please choose new one...'.format(project_name))
            self.process_new_project(hello=False)

            return False

        for crew in from_file:

            data[crew] = []
            temp = []

            click.echo('Item: {}'.format(crew))

            for crew_fship in from_file:

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

            data[crew] += temp
            self.write_graph_db(project_name, {crew: data[crew]}, crew)

        result = self.write_graph_db(project_name, data, project_name)

        if result is True:
            click.echo('Graph for project {} was created'.format(project_name))
            return True
        return False

    def load_project(self, project_name: str = '') -> dict:
        """load_project

        :param project_name:
        :type project_name: str

        :rtype: dict
        """
        if project_name and pathlib.Path('{0}/.ginx/{1}/{1}-edges.graph'.format(self.__user_home, project_name)).is_file():
            with open('{0}/.ginx/{1}/{1}-edges.graph'.format(self.__user_home, project_name)) as graph:
                return self.edges_mean(json.load(graph), project_name)
        else:
            click.echo('Project {} does not exists'.format(project_name))
            sys.exit()
