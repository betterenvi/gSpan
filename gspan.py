import collections
from graph import *
from util import *

class gSpan:
    def __init__(self, graphs, min_support, min_num_vertices = 1, max_num_vertices = float('inf'), is_undirected = True):
        self.graphs = graphs
        self.is_undirected = is_undirected
        self.min_support = min_support
        self.min_num_vertices = min_num_vertices
        self.max_num_vertices = max_num_vertices
        self.oldelb_to_newelb = dict()
        self.newelb_to_oldelb = dict()
        self.oldvlb_to_newvlb = dict()
        self.newvlb_to_oldvlb = dict()
        self.frequent_size1_subgraphs = list()
        self.frequent_subgraphs = list() # include subgraphs with any num(but >= 2, <= max_num_vertices) of vertices

        for g in graphs.values():
            if g.is_undirected != self.is_undirected:
                print '"is_undirected" does not match!'

    def xx():
        vlb_counter = collections.Counter()
        elb_counter = collections.Counter()
        edge_weight = 0.5 if self.is_undirected else 1
        for g in graphs.values():
            for v in g.vertices.values():
                vlb_counter[v.vlb] += 1
                for e in v.edges.values():
                    elb_counter[e.elb] += edge_weight
        vlb_cnt = sorted(vlb_counter.items(), key=lambda pair: pair[1], reverse=True)
        elb_cnt = sorted(elb_counter.items(), key=lambda pair: pair[1], reverse=True)

        def oldlb_newlb_map(lb_counter, lb_cnt, old2new, new2old):
            newlbs = sorted(lb_counter.keys())
            for i, (lb, _) in enumerate(lb_cnt):
                old2new[lb] = newlbs[i]
                new2old[newlbs[i]] = lb

        oldlb_newlb_map(vlb_counter, vlb_cnt, self.oldvlb_to_newvlb, self.newvlb_to_oldvlb)
        oldlb_newlb_map(elb_counter, elb_cnt, self.oldelb_to_newelb, self.newelb_to_oldelb)
        # remove infrequent edges
        for i in range(len(elb_cnt)):
            elb, cnt = elb_cnt[i]
            if cnt >= self.min_support:
                g = Graph(gid = INVALID_GRAPH_ID, is_undirected = self.is_undirected)
                g.add_vertex(0, )
            else:
                for g in graphs.values():
                    g.remove_edge_with_label(elb)

        # remove infrequent vertices
        for i in range(len(vlb_cnt)):
            vlb, cnt = vlb_cnt[i]
            if cnt >= self.min_support:
                g = Graph(gid = INVALID_GRAPH_ID, is_undirected = self.is_undirected)
                g.add_vertex(INVALID_VERTEX_ID, self.oldvlb_to_newvlb[vlb])
                self.frequent_size1_subgraphs(g)
            else:
                for g in graphs.values():
                    g.remove_vertex_with_label(vlb)


                self.frequent_subgraphs.append()

        # relabel vertices and edges
        _ = map(lambda g : g.relabel(self.oldvlb_to_newvlb, self.oldelb_to_newelb), graphs.values())

        if self.min_num_vertices == 1:




    def run(self):
        pass
