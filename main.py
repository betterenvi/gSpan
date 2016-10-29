# !/usr/bin/python
# coding=utf-8
import os, sys, getopt
from gspan import gSpan

default_args = {'-n':float('inf'), '-s':5000, '-l':2, '-u':float('inf'), '-d':0, '-v':0, 'database_file_name':'graphdata/graph.data'}

def usage():
    print '\nUsage: python main.py [-s min_support] [-n num_graph] [-l min_num_vertices] [-u max_num_vertices] [-d] [-v] [-h] database_file_name'
    print '''\nOptions:\n
    -s, min support, default 5000\n
    -n, only read the first n graphs in the given database, default inf, i.e. all graphs\n
    -l, lower bound of number of vertices of output subgraph, default 2\n
    -u, upper bound of number of vertices of output subgraph, default inf\n
    -d, run for directed graphs, default off, i.e. for undirected graphs\n
    -v, verbose output, default off\n
    -h, help\n
    '''

def parse_args(args, default_args):
    optlist, args = getopt.getopt(args, 'n:s:l:u:dv')
    opt_dict = {k:v for k, v in optlist}
    opt_dict['-d'] = 0 if '-d' not in opt_dict else 1
    opt_dict['-v'] = 0 if '-v' not in opt_dict else 1
    try:
        for k in default_args:
            opt_dict[k] = default_args[k] if k not in opt_dict else int(opt_dict[k])
        opt_dict['database_file_name'] = default_args['database_file_name'] if len(args) == 0 else args[0]
        return opt_dict
    except Exception:
        usage()
        exit()

def main():
    if len(sys.argv) == 1 or '-h' in sys.argv:
        usage()
        exit()
    if '-t' in sys.argv:
        opt_dict = parse_args('-n 2 -s 2 -l 2 -u 3 -v'.split(), default_args)
    else:
        opt_dict = parse_args(sys.argv[1:], default_args)
    if not os.path.exists(opt_dict['database_file_name']):
        print '{} does not exist.'.format(opt_dict['database_file_name'])
        exit()
    gs = gSpan(database_file_name = opt_dict['database_file_name'], min_support = opt_dict['-s'],
        min_num_vertices = opt_dict['-l'], max_num_vertices = opt_dict['-u'],
        max_ngraphs = opt_dict['-n'], is_undirected = opt_dict['-d'] == 0, verbose = opt_dict['-v'] == 1)
    gs.run()
    gs.time_stats()

if __name__ == '__main__':
    main()
