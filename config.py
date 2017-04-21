import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-s',
    type=int,
    default=5000,
    help='min support, default 5000'
)
parser.add_argument(
    '-n',
    type=float,
    default=float('inf'),
    help='only read the first n graphs in the given database, '
    'default inf, i.e. all graphs'
)
parser.add_argument(
    '-l',
    type=int,
    default=2,
    help='lower bound of number of vertices of output subgraph, default 2'
)
parser.add_argument(
    '-u',
    type=int,
    default=float('inf'),
    help='upper bound of number of vertices of output subgraph, default inf'
)
parser.add_argument(
    '-d',
    type=int,
    default=0,
    help='run for directed graphs, default off, i.e. for undirected graphs'
)
parser.add_argument(
    '-v',
    type=int,
    default=0,
    help='verbose output, default off'
)
parser.add_argument(
    'database_file_name',
    type=str,
    help='database file name'
)
parser.add_argument(
    '-p',
    type=int,
    default=0,
    help='plot frequent subgraph, default off'
)
parser.add_argument(
    '-w',
    type=int,
    default=0,
    help='output where one frequent subgraph appears in database, default off'
)
