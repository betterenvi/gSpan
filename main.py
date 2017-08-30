# !/usr/bin/python
# coding=utf-8
import os
import sys

from config import parser
from gspan import gSpan


FLAGS, _ = parser.parse_known_args(args=sys.argv[1:])


def main():
    """Run gSpan."""
    if not os.path.exists(FLAGS.database_file_name):
        print('{} does not exist.'.format(FLAGS.database_file_name))
        sys.exit()

    gs = gSpan(
        database_file_name=FLAGS.database_file_name,
        min_support=FLAGS.min_support,
        min_num_vertices=FLAGS.lower_bound_of_num_vertices,
        max_num_vertices=FLAGS.upper_bound_of_num_vertices,
        max_ngraphs=FLAGS.num_graphs,
        is_undirected=(not FLAGS.directed),
        verbose=FLAGS.verbose,
        visualize=FLAGS.plot,
        where=FLAGS.where
    )

    gs.run()
    gs.time_stats()

if __name__ == '__main__':
    main()
