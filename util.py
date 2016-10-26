from graph import *

def read_graphs(file_name):
    graphs = dict()
    with open(file_name) as f:
        lines = map(lambda x:x.strip(), f.readlines())
        nlines = len(lines)
        tgraph, graph_cnt, edge_cnt = None, 0, 0
        for i, line in enumerate(lines):
            cols = line.split(' ')
            if cols[0] == 't':
                if tgraph != None:
                    graphs[graph_cnt] = tgraph
                if cols[-1] == '-1':
                    break
                tgraph, edge_cnt = Graph(graph_cnt), 0
                graph_cnt += 1
            elif cols[0] == 'v':
                tgraph.add_vertex(cols[1], cols[2])
            elif cols[0] == 'e':
                tgraph.add_edge(edge_cnt, cols[1], cols[2], cols[3])
                edge_cnt += 1

    return graphs


