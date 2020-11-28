"""Define some args."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse


def str2bool(s):
    """Convert str to bool."""
    return s.lower() not in ['false', 'f', '0', 'none', 'no', 'n']


parser = argparse.ArgumentParser()
parser.add_argument(
    '-s', '--min_support',
    type=int,
    default=5000,
    help='min support, default 5000'
)
parser.add_argument(
    '-n', '--num_graphs',
    type=float,
    default=float('inf'),
    help='only read the first n graphs in the given database, '
         'default inf, i.e. all graphs'
)
parser.add_argument(
    '-l', '--lower_bound_of_num_vertices',
    type=int,
    default=2,
    help='int, lower bound of number of vertices of output subgraph, default 2'
)
parser.add_argument(
    '-u', '--upper_bound_of_num_vertices',
    type=int,
    default=float('inf'),
    help='int, upper bound of number of vertices of output subgraph, '
         'default inf'
)
parser.add_argument(
    '-d', '--directed',
    type=str2bool,
    default=False,
    help='bool, run for directed graphs, default off, i.e. undirected graphs'
)
parser.add_argument(
    '-v', '--verbose',
    type=str2bool,
    default=False,
    help='bool, verbose output, default off'
)
parser.add_argument(
    'database_file_name',
    type=str,
    help='str, database file name'
)
parser.add_argument(
    '-p', '--plot',
    type=str2bool,
    default=False,
    help='bool, whether plot frequent subgraph, default off'
)
parser.add_argument(
    '-w', '--where',
    type=str2bool,
    default=False,
    help='bool, output where one frequent subgraph appears in database, '
         'default off'
)
