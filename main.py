# !/usr/bin/python
# coding=utf-8
import os
import sys
import getopt

from gspan import gSpan
from config import parser

FLAGS, unknown = parser.parse_known_args(args=sys.argv[1:])

def main():

    if not os.path.exists(FLAGS.database_file_name):
        print('{} does not exist.'.format(FLAGS.database_file_name))
        sys.exit()

    gs = gSpan(
        database_file_name=FLAGS.database_file_name,
        min_support=FLAGS.s,
        min_num_vertices=FLAGS.l,
        max_num_vertices=FLAGS.u,
        max_ngraphs=FLAGS.n,
        is_undirected=(FLAGS.d == 0),
        verbose=(FLAGS.v != 0),
        visualize=(FLAGS.p != 0),
        where=(FLAGS.w != 0)
    )

    gs.run()
    gs.time_stats()

if __name__ == '__main__':
    main()
