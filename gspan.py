import collections, itertools, copy, time
import codecs
from graph import *
import pandas as pd

def record_timestamp(func):
    def deco(self):
        self.timestamps[func.__name__ + '_in'] = time.time()
        #self.timestamps[func.__name__ + '_c_in'] = time.clock()
        func(self)
        self.timestamps[func.__name__ + '_out'] = time.time()
        #self.timestamps[func.__name__ + '_c_out'] = time.clock()
    return deco

class DFSedge(object):
    def __init__(self, frm, to, vevlb):
        self.frm = frm
        self.to = to
        self.vevlb = vevlb

    def __eq__(self, other):
        return self.frm == other.frm and self.to == other.to and self.vevlb == other.vevlb

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '(frm={}, to={}, vevlb={})'.format(self.frm, self.to, self.vevlb)

class DFScode(list):
    """
    DFScode is a list of DFSedge.
    """
    def __init__(self):
        self.rmpath = list()

    def __eq__(self, other):
        la, lb = len(self), len(other)
        if la != lb:
            return False
        for i in range(la):
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return ''.join(['[', ','.join([str(dfsedge) for dfsedge in self]), ']'])

    def push_back(self, frm, to, vevlb):
        self.append(DFSedge(frm, to, vevlb))
        return self

    def to_graph(self, gid = VACANT_GRAPH_ID, is_undirected = True):
        g = Graph(gid, is_undirected = is_undirected, eid_auto_increment = True)
        for dfsedge in self:
            frm, to, (vlb1, elb, vlb2) = dfsedge.frm, dfsedge.to, dfsedge.vevlb
            if vlb1 != VACANT_VERTEX_LABEL:
                g.add_vertex(frm, vlb1)
            if vlb2 != VACANT_VERTEX_LABEL:
                g.add_vertex(to, vlb2)
            g.add_edge(AUTO_EDGE_ID, frm, to, elb)
        return g

    def from_graph(self, g):
        pass

    def build_rmpath(self):
        self.rmpath = list()
        old_frm = None
        for i in range(len(self) - 1, -1, -1):
            dfsedge = self[i]
            frm, to, vevlb = dfsedge.frm, dfsedge.to, dfsedge.vevlb
            if frm < to and (old_frm == None or to == old_frm):
                self.rmpath.append(i)
                old_frm = frm
        return self

    def get_num_vertices(self):
        return len(set([dfsedge.frm for dfsedge in self] + [dfsedge.to for dfsedge in self]))

class PDFS(object):
    def __init__(self, gid = VACANT_GRAPH_ID, edge = None, prev = None):
        self.gid = gid
        self.edge = edge
        self.prev = prev

class Projected(list):
    """docstring for Projected
    Projected is a list of PDFS. Each element of Projected is a projection one frequent graph in one original graph.
    """
    def __init__(self):
        super(Projected, self).__init__()

    def push_back(self, gid, edge, prev):
        self.append(PDFS(gid, edge, prev))
        return self

class History(object):
    """docstring for History"""
    def __init__(self, g, pdfs):
        super(History, self).__init__()
        self.edges = list()
        self.vertices_used = collections.defaultdict(int)
        self.edges_used = collections.defaultdict(int)
        if pdfs == None:
            return
        while pdfs:
            e = pdfs.edge
            self.edges.append(e)
            self.vertices_used[e.frm], self.vertices_used[e.to], self.edges_used[e.eid] = 1, 1, 1
            pdfs = pdfs.prev
        self.edges = self.edges[::-1]

    def has_vertex(self, vid):
        return self.vertices_used[vid] == 1

    def has_edge(self, eid):
        return self.edges_used[eid] == 1

class gSpan(object):
    def __init__(self, database_file_name, min_support = 10, min_num_vertices = 1, max_num_vertices = float('inf'),
        max_ngraphs = float('inf'), is_undirected = True, verbose = False, visualize = False, where = False):
        self.database_file_name = database_file_name
        self.graphs = dict()
        self.max_ngraphs = max_ngraphs
        self.is_undirected = is_undirected
        self.min_support = min_support
        self.min_num_vertices = min_num_vertices
        self.max_num_vertices = max_num_vertices
        self.DFScode = DFScode()
        self.support = 0
        self.frequent_size1_subgraphs = list()
        self.frequent_subgraphs = list() # include subgraphs with any num(but >= 2, <= max_num_vertices) of vertices
        self.counter = 0#itertools.count()
        self.verbose = verbose
        self.visualize = visualize
        self.where = where
        self.timestamps = dict()
        if self.max_num_vertices < self.min_num_vertices:
            print('Max number of vertices can not be smaller than min number of that.\nSet max_num_vertices = min_num_vertices.')
            self.max_num_vertices = self.min_num_vertices
        self.report_df=pd.DataFrame()

    def time_stats(self):
        func_names = ['read_graphs', 'run']
        time_deltas = collections.defaultdict(float)
        for fn in func_names:
            time_deltas[fn] = round(self.timestamps[fn + '_out'] - self.timestamps[fn + '_in'], 2)
            #time_deltas[fn + '_c'] = round(self.timestamps[fn + '_c_out'] - self.timestamps[fn + '_c_in'], 2)
        print('Read:\t{} s'.format(time_deltas['read_graphs']))#, time_deltas['read_graphs_c'])
        print('Mine:\t{} s'.format(time_deltas['run'] - time_deltas['read_graphs']))#, time_deltas['run_c'] - time_deltas['read_graphs_c'])
        print('Total:\t{} s'.format(time_deltas['run']))#, time_deltas['run_c'])
        return self

    @record_timestamp
    def read_graphs(self):
        self.graphs = dict()
        with codecs.open(self.database_file_name, 'r', 'utf-8') as f:
            lines=[line.strip() for line in f.readlines()]
            nlines = len(lines)
            tgraph, graph_cnt, edge_cnt = None, 0, 0
            for i, line in enumerate(lines):
                cols = line.split(' ')
                if cols[0] == 't':
                    if tgraph != None:
                        self.graphs[graph_cnt] = tgraph
                        graph_cnt += 1
                        tgraph = None
                    if cols[-1] == '-1' or graph_cnt >= self.max_ngraphs:
                        break
                    tgraph = Graph(graph_cnt, is_undirected = self.is_undirected, eid_auto_increment = True)
                elif cols[0] == 'v':
                    tgraph.add_vertex(cols[1], cols[2])
                elif cols[0] == 'e':
                    tgraph.add_edge(AUTO_EDGE_ID, cols[1], cols[2], cols[3])
            if tgraph != None: # adapt to input files that do not end with 't # -1'
                self.graphs[graph_cnt] = tgraph
        return self

    @record_timestamp
    def generate_1edge_frequent_subgraphs(self):
        vlb_counter = collections.Counter()
        vevlb_counter = collections.Counter()
        vlb_counted = set()
        vevlb_counted = set()
        for g in self.graphs.values():
            for v in g.vertices.values():
                vlb_counter[v.vlb] += 1 if (g.gid, v.vlb) not in vlb_counted else 0
                vlb_counted.add((g.gid, v.vlb))
                for to, e in v.edges.items():
                    vlb1, vlb2 = v.vlb, g.vertices[to].vlb
                    if self.is_undirected and vlb1 > vlb2:
                        vlb1, vlb2 = vlb2, vlb1
                    vevlb_counter[(vlb1, e.elb, vlb2)] += 1 if (g.gid, (vlb1, e.elb, vlb2)) not in vevlb_counter else 0
                    vevlb_counted.add((g.gid, (vlb1, e.elb, vlb2)))
        # remove infrequent vertices or add frequent vertices
        for vlb, cnt in vlb_counter.items():
            if cnt >= self.min_support:
                g = Graph(gid = self.counter, is_undirected = self.is_undirected)
                self.counter+=1
                g.add_vertex(0, vlb)
                self.frequent_size1_subgraphs.append(g)
                if self.min_num_vertices <= 1:
                    self.report_size1(g, support = cnt)
            else:
                continue
                for g in self.graphs.values():
                    g.remove_vertex_with_vlb(vlb)
        if self.min_num_vertices > 1:
            self.counter = 0#itertools.count()
        # remove edges of infrequent vev or ...
        for vevlb, cnt in vevlb_counter.items():
            if cnt >= self.min_support:
                continue
                # g = Graph(gid = self.counter.next(), is_undirected = self.is_undirected)
                # g.add_vertex(0, vevlb[0])
                # g.add_vertex(1, vevlb[2])
                # g.add_edge(0, 0, 1, vevlb[1])
                # self.frequent_subgraphs.append(g)
            else:
                continue
                for g in self.graphs.values():
                    g.remove_edge_with_vevlb(vevlb)
        #return copy.copy(self.frequent_subgraphs)

    @record_timestamp
    def run(self):
        self.read_graphs()
        self.generate_1edge_frequent_subgraphs()
        if self.max_num_vertices < 2:
            return
        root = collections.defaultdict(Projected)
        for gid, g in self.graphs.items():
            for vid, v in g.vertices.items():
                edges = self.get_forward_root_edges(g, vid)
                for e in edges:
                    root[(v.vlb, e.elb, g.vertices[e.to].vlb)].append(PDFS(gid, e, None))

        #if self.verbose: print 'run:', root.keys()
        for vevlb, projected in root.items():
            self.DFScode.append(DFSedge(0, 1, vevlb))
            self.subgraph_mining(projected)
            self.DFScode.pop()

    def get_support(self, projected):
        return len(set([pdfs.gid for pdfs in projected]))

    def report_size1(self, g, support):
        g.display()
        print('\nSupport: {}'.format(support))
        print('\n-----------------\n')

    def report(self, projected):
        self.frequent_subgraphs.append(copy.copy(self.DFScode))
        if self.DFScode.get_num_vertices() < self.min_num_vertices:
            return
        g = self.DFScode.to_graph(gid = self.counter, is_undirected = self.is_undirected)#.next()
        self.counter+=1
        display_str=g.display()
        print('\nSupport: {}'.format(self.support))

        ######Add some report info to pandas dataframe "self.report_df"#####
        #max_eg=max([tupl[0] for tupl in g.set_of_elb[1]])
        self.report_df=self.report_df.append(pd.DataFrame(
            {'support':[self.support],'description':[display_str], 'num_vert':self.DFScode.get_num_vertices()},#, 'max_eg_vert': max_eg,},
            index=[self.counter-1]))
        ############################
        if self.visualize:
            g.plot()
        if self.where:
            print('where:', list(set([p.gid for p in projected])))
        print('\n-----------------\n')

    def get_forward_root_edges(self, g, frm):
        result = []
        v_frm = g.vertices[frm]
        for to, e in v_frm.edges.items():
            if (not self.is_undirected) or v_frm.vlb <= g.vertices[to].vlb:
                result.append(e)
        return result

    def get_backward_edge(self, g, e1, e2, history):
        if self.is_undirected and e1 == e2:
            return None
        gsize = g.get_num_vertices()
        # assert e1.frm >= 0 and e1.frm < gsize
        # assert e1.to >= 0 and e1.to < gsize
        # assert e2.to >= 0 and e2.to < gsize
        for to, e in g.vertices[e2.to].edges.items():
            if history.has_edge(e.eid) or e.to != e1.frm:
                continue
            # return e # ok? if reture here, then self.DFScodep[0] != DFScode_min[0] should be checked in is_min(). or:
            if self.is_undirected:
                if e1.elb < e.elb or (e1.elb == e.elb and g.vertices[e1.to].vlb <= g.vertices[e2.to].vlb):
                    return e
            else:
                if g.vertices[e1.frm].vlb < g.vertices[e2.to] or (g.vertices[e1.frm].vlb == g.vertices[e2.to] and  e1.elb <= e.elb):
                    return e
            # if e1.elb < e.elb or (e1.elb == e.elb and g.vertices[e1.to].vlb <= g.vertices[e2.to].vlb):
            #     return e
        return None

    def get_forward_pure_edges(self, g, rm_edge, min_vlb, history):
        result = []
        gsize = g.get_num_vertices()
        # assert rm_edge.to >= 0 and rm_edge.to < gsize
        for to, e in g.vertices[rm_edge.to].edges.items():
            # assert e.to >= 0 and e.to < gsize
            if min_vlb <= g.vertices[e.to].vlb and (not history.has_vertex(e.to)):
                result.append(e)
        return result

    def get_forward_rmpath_edges(self, g, rm_edge, min_vlb, history):
        result = []
        gsize = g.get_num_vertices()
        # assert rm_edge.to >= 0 and rm_edge.to < gsize
        # assert rm_edge.frm >= 0 and rm_edge.frm < gsize
        to_vlb = g.vertices[rm_edge.to].vlb
        for to, e in g.vertices[rm_edge.frm].edges.items():
            new_to_vlb = g.vertices[to].vlb
            if rm_edge.to == e.to or min_vlb > new_to_vlb or history.has_vertex(e.to):
                continue
            # result.append(e) # ok? or:
            # if self.is_undirected:
            #     if rm_edge.elb < e.elb or (rm_edge.elb == e.elb and to_vlb <= new_to_vlb):
            #         return e
            # else:
            #     return e
            if rm_edge.elb < e.elb or (rm_edge.elb == e.elb and to_vlb <= new_to_vlb):
                result.append(e)
        return result

    def is_min(self):
        if self.verbose:print('is_min: checking', self.DFScode)
        if len(self.DFScode) == 1:
            return True
        g = self.DFScode.to_graph(gid = VACANT_GRAPH_ID, is_undirected = self.is_undirected)
        DFScode_min = DFScode()
        root = collections.defaultdict(Projected)
        for vid, v in g.vertices.items():
            edges = self.get_forward_root_edges(g, vid)
            for e in edges:
                root[(v.vlb, e.elb, g.vertices[e.to].vlb)].append(PDFS(g.gid, e, None))
        min_vevlb = min(root.keys())
        #if self.verbose: print 'is_min: bef p_is_min', min_vevlb, self.DFScode.get_num_vertices(), len(self.DFScode)
        DFScode_min.append(DFSedge(0, 1, min_vevlb))
        # if self.DFScode[0] != DFScode_min[0]: # no need to check because of pruning in get_*_edge*
        #     return False

        def project_is_min(projected):
            DFScode_min.build_rmpath()
            rmpath = DFScode_min.rmpath
            min_vlb = DFScode_min[0].vevlb[0]
            maxtoc = DFScode_min[rmpath[0]].to

            backward_root = collections.defaultdict(Projected)
            flag, newto = False, 0,
            for i in range(len(rmpath) - 1, 0 if self.is_undirected else -1, -1):
                if flag:
                    break
                for p in projected:
                    history = History(g, p)
                    e = self.get_backward_edge(g, history.edges[rmpath[i]], history.edges[rmpath[0]], history)
                    if e != None:
                        #if self.verbose: print 'project_is_min: 6', e.frm, e.to
                        backward_root[e.elb].append(PDFS(g.gid, e, p))
                        newto = DFScode_min[rmpath[i]].frm
                        flag = True
            #if self.verbose: print 'project_is_min: 1', flag, DFScode_min.get_num_vertices(), len(DFScode_min)
            if flag:
                backward_min_elb = min(backward_root.keys())
                DFScode_min.append(DFSedge(maxtoc, newto, (VACANT_VERTEX_LABEL, backward_min_elb, VACANT_VERTEX_LABEL)))
                idx = len(DFScode_min) - 1
                #if self.verbose: print 'project_is_min: 5', idx, len(self.DFScode)
                if self.DFScode[idx] != DFScode_min[idx]:
                    return False
                return project_is_min(backward_root[backward_min_elb])

            forward_root = collections.defaultdict(Projected)
            flag, newfrm = False, 0
            for p in projected:
                history = History(g, p)
                edges = self.get_forward_pure_edges(g, history.edges[rmpath[0]], min_vlb, history)
                if len(edges) > 0:
                    flag = True
                    newfrm = maxtoc
                    for e in edges:
                        forward_root[(e.elb, g.vertices[e.to].vlb)].append(PDFS(g.gid, e, p))
            #if self.verbose: print 'project_is_min: 2', flag
            for rmpath_i in rmpath:
                if flag:
                    break
                for p in projected:
                    history = History(g, p)
                    edges = self.get_forward_rmpath_edges(g, history.edges[rmpath_i], min_vlb, history)
                    if len(edges) > 0:
                        flag = True
                        newfrm = DFScode_min[rmpath_i].frm
                        for e in edges:
                            forward_root[(e.elb, g.vertices[e.to].vlb)].append(PDFS(g.gid, e, p))
            #if self.verbose: print 'project_is_min: 3', flag

            if not flag:
                return True

            forward_min_evlb = min(forward_root.keys())
            #if self.verbose: print 'project_is_min: 4', forward_min_evlb, newfrm
            DFScode_min.append(DFSedge(newfrm, maxtoc + 1, (VACANT_VERTEX_LABEL, forward_min_evlb[0], forward_min_evlb[1])))
            idx = len(DFScode_min) - 1
            if self.DFScode[idx] != DFScode_min[idx]:
                return False
            return project_is_min(forward_root[forward_min_evlb])

        res = project_is_min(root[min_vevlb])
        #if self.verbose: print 'is_min: leave'
        return res

    def subgraph_mining(self, projected):
        self.support = self.get_support(projected)
        if self.support < self.min_support:
            #if self.verbose: print 'subgraph_mining: < min_support', self.DFScode
            return
        if not self.is_min():
            #if self.verbose: print 'subgraph_mining: not min'
            return
        self.report(projected)

        num_vertices = self.DFScode.get_num_vertices()
        self.DFScode.build_rmpath()
        rmpath = self.DFScode.rmpath
        maxtoc = self.DFScode[rmpath[0]].to
        min_vlb = self.DFScode[0].vevlb[0]

        forward_root = collections.defaultdict(Projected)
        backward_root = collections.defaultdict(Projected)
        for p in projected:
            g = self.graphs[p.gid]
            history = History(g, p)
            # backward
            for rmpath_i in rmpath[::-1]:
                e = self.get_backward_edge(g, history.edges[rmpath_i], history.edges[rmpath[0]], history)
                if e != None:
                    backward_root[(self.DFScode[rmpath_i].frm, e.elb)].append(PDFS(g.gid, e, p))
            # pure forward
            if num_vertices >= self.max_num_vertices:
                continue
            edges = self.get_forward_pure_edges(g, history.edges[rmpath[0]], min_vlb, history)
            for e in edges:
                forward_root[(maxtoc, e.elb, g.vertices[e.to].vlb)].append(PDFS(g.gid, e, p))
            # rmpath forward
            for rmpath_i in rmpath:
                edges = self.get_forward_rmpath_edges(g, history.edges[rmpath_i], min_vlb, history)
                for e in edges:
                    forward_root[(self.DFScode[rmpath_i].frm, e.elb, g.vertices[e.to].vlb)].append(PDFS(g.gid, e, p))

        # backward
        for to, elb in backward_root:
            self.DFScode.append(DFSedge(maxtoc, to, (VACANT_VERTEX_LABEL, elb, VACANT_VERTEX_LABEL)))
            self.subgraph_mining(backward_root[(to, elb)])
            self.DFScode.pop()
        # forward
        # if num_vertices >= self.max_num_vertices: # no need. because forward_root has no element.
        #     return
        for frm, elb, vlb2 in forward_root:
            self.DFScode.append(DFSedge(frm, maxtoc + 1, (VACANT_VERTEX_LABEL, elb, vlb2)))
            self.subgraph_mining(forward_root[(frm, elb, vlb2)])
            self.DFScode.pop()

        return self
