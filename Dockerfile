from python:3.6
RUN apt-get update
RUN apt-get upgrade --yes

ADD ./ginx ./ginx
WORKDIR ./ginx
RUN python setup.py install
