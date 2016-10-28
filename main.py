# !/usr/bin/python
# coding=utf-8
import os, sys, getopt
from gspan import gSpan

default_args = {'-n':float('inf'), '-s':10, '-l':2, '-u':float('inf'), '-d':0, 'database_file_name':'graph.data'}

def usage():
    pass

def parse_args(args, default_args):
    optlist, args = getopt.getopt(args, 'n:s:l:u:d')
    opt_dict = {k:v for k, v in optlist}
    opt_dict['-d'] = 0 if '-d' not in opt_dict else 1
    try:
        for k in opt_dict:
            opt_dict[k] = default_args[k] if k not in opt_dict else int(opt_dict[k])
        opt_dict['database_file_name'] = default_args['database_file_name'] if len(args) == 0 else args[0]
        return opt_dict
    except Exception:
        usage()
        exit()

def main():
    opt_dict = parse_args(sys.args[1:], default_args)
    if not os.path.exists(opt_dict['database_file_name']):
        print '{} does not exist.'.format(opt_dict['database_file_name'])
        exit()
    gs = gSpan(database_file_name = opt_dict['database_file_name'], min_support = opt_dict['-s'],
        min_num_vertices = opt_dict['-l'], max_num_vertices = opt_dict['-u'], is_undirected = opt_dict['-d'] == 0)
    gs.run()





