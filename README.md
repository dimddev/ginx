----
## GinX

Ginx - acronym from Graph Inspector is a simple command line tool for creating and querying graphs.
GinX using NetworkX and it depends on numpy, scipy and matplotlib.

----
## Installation:

    # let's create some working directory
    $ mkdir test && cd test
	# then clone the ginx
    $ git clone https://github.com/dimddev/ginx

----
## Using of virtualenv

Virtualenv will keeping clear your global python ecosystem, if you prefer `docker` skip the next few lines.

In case `virtualenv` is not installed, you could type:

    $ sudo apt-get install python-virtualenv

now we creating a virtualenv with name ".env"

    $ virtualenv -p /usr/bin/python3.6 .env

next activate it with:

    $ source .env/bin/activate

and finally let's install ginx:

    $ cd ginx/ginx
    $ python setup install

----
## Using of docker

If you prefer to use docker, go one directory back, and run the script

    $ ./install_ginx_on_docker.sh

After setup is done, you could run and connect to docker ginx as usual.

----
## Usage:

    $ ginx --help

Currently only `project`, `gpath` and `gquery` commands are implemented.
