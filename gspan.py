import collections, itertools, copy
from graph import *
from util import *

class DFScode(list):
    def __init__(self):
        self.rmpath = list()

    def to_graph(self):
        pass

    def from_graph(self, g):
        pass

    def build_rmpath(self):
        pass

class PDFS(object):
    def __init__(self):
        self.gid = INVALID_GRAPH_ID
        self.edge = None
        self.prev = None

class Projected(list):
    """docstring for Projected
    Projected is a list of PDFS. Each element of Projected is a projection one frequent graph in one original graph.
    """
    def __init__(self):
        super(Projected, self).__init__()


class gSpan(object):
    def __init__(self, graphs, min_support, min_num_vertices = 1, max_num_vertices = float('inf'), is_undirected = True):
        self.graphs = graphs
        self.is_undirected = is_undirected
        self.min_support = min_support
        self.min_num_vertices = min_num_vertices
        self.max_num_vertices = max_num_vertices
        self.DFScode = DFScode()
        self.frequent_size1_subgraphs = list()
        self.frequent_subgraphs = list() # include subgraphs with any num(but >= 2, <= max_num_vertices) of vertices
        self.counter = itertools.count()

        for g in graphs.values():
            if g.is_undirected != self.is_undirected:
                print '"is_undirected" does not match!'

    def generate_1edge_frequent_subgraphs(self):
        vlb_counter = collections.Counter()
        vevlb_counter = collections.Counter()
        edge_weight = 0.5 if self.is_undirected else 1
        for g in graphs.values():
            for v in g.vertices.values():
                vlb_counter[v.vlb] += 1
                for to, e in v.edges.items():
                    vlb1, vlb2 = v.vlb, g.vertices[to].vlb
                    if self.is_undirected and vlb1 > vlb2:
                        vlb1, vlb2 = vlb2, vlb1
                    vevlb_counter[(vlb1, e.elb, vlb2)] += edge_weight
        # remove infrequent vertices or add frequent vertices
        for vlb, cnt in vlb_counter.items():
            if cnt >= self.min_support:
                g = FrequentGraph(gid = self.counter.next(), is_undirected = self.is_undirected)
                g.add_vertex(0, vlb)
                self.frequent_size1_subgraphs.append(g)
            else:
                for g in graphs.values():
                    g.remove_vertex_with_vlb(vlb)
        # remove edges of infrequent vev or ...
        for vevlb, cnt in vevlb_counter.item():
            if cnt >= self.min_support:
                g = FrequentGraph(gid = self.counter.next(), is_undirected = self.is_undirected)
                g.add_vertex(0, vevlb[0])
                g.add_vertex(1, vevlb[2])
                g.add_edge(0, 0, 1, vevlb[1])
                g.DFScode.append((0, 1, vevlb))
                self.frequent_subgraphs.append(g)
            else:
                for g in graphs.values():
                    g.remove_edge_with_vevlb(vevlb)

        return copy.copy(self.frequent_subgraphs)

    def run(self):
        one_edge_subgraphs = self.generate_1edge_frequent_subgraphs()
        for g in one_edge_subgraphs:

