import collections
INVALID_EDGE_ID = -1
INVALID_VERTEX_ID = -1
INVALID_EDGE_LABEL = -1
INVALID_VERTX_LABEL = -1
INVALID_GRAPH_ID = -1

class Edge(object):
    def __init__(self, eid = INVALID_EDGE_ID, frm = INVALID_VERTEX_ID, to = INVALID_VERTEX_ID, elb = INVALID_EDGE_LABEL):
        self.eid = eid
        self.frm = frm
        self.to = to
        self.elb = elb

class Vertex(object):
    def __init__(self, vid = INVALID_VERTEX_ID, vlb = INVALID_VERTX_LABEL):
        self.vid = vid
        self.vlb = vlb
        self.edges = dict()

    def add_edge(self, eid, frm, to, elb):
        self.edges[to] = Edge(eid, frm, to, elb)

class Graph(object):
    def __init__(self, gid = INVALID_GRAPH_ID, is_undirected = True):
        self.gid = gid
        self.is_undirected = is_undirected
        self.vertices = dict()
        self.set_of_elb = collections.defaultdict(set)
        self.set_of_vlb = collections.defaultdict(set)

    def get_num_vertices(self):
        return len(self.vertices)

    def add_vertex(self, vid, vlb):
        self.vertices[vid] = Vertex(vid, vlb)
        self.set_of_vlb[vlb].add(vid)
        return self

    def add_edge(self, eid, frm, to, elb):
        self.vertices[frm].add_edge(eid, frm, to, elb)
        self.set_of_elb[elb].add((frm, to))
        if self.is_undirected:
            self.vertices[to].add_edge(eid, to, frm, elb)
            self.set_of_elb[elb].add((to, frm))
        return self


    def remove_vertex(self, vid):
        if self.is_undirected:
            v = self.vertices[vid]
            for to in v.edges.keys():
                e = v.edges[to] # (vid, to) and (to, vid) have same elb
                self.set_of_elb[e.elb].discard((to, vid))
                del self.vertices[to][vid]
        else:
            for frm in self.vertices.keys():
                v = self.vertices[frm]
                if vid in v.edges.keys():
                    e = self.vertices[frm].edges[vid]
                    self.set_of_elb[e.elb].discard((frm, vid))
                    del self.vertices[frm][vid]

        v = self.vertices[vid]
        for to in v.edges.keys():
            e = v.edges[to]
            self.set_of_elb[e.elb].discard((vid, to))

        self.set_of_vlb[v.vlb].discard(vid)
        del self.vertices[vid]
        return self

    def remove_edge(self, frm, to):
        elb = self.vertices[frm].edges[to].elb
        self.set_of_elb[elb].discard((frm, to))
        del self.vertices[frm][to]
        if self.is_undirected:
            self.set_of_elb[elb].discard((to, frm))
            del self.vertices[to][frm]
        return self

    def remove_edge_with_elb(self, elb):
        for frm, to in self.set_of_elb[elb]:
            self.remove_edge(frm, to)
        return self

    def remove_vertex_with_vlb(self, vlb):
        for vid in self.set_of_vlb[vlb]:
            self.remove_vertex(vid)
        return self

    def remove_edge_with_vevlb(self, vevlb):
        vlb1, elb, vlb2 = vevlb
        for frm, to in self.set_of_elb[elb]:
            if frm in self.set_of_vlb[vlb1] and to in self.set_of_vlb[vlb2]:
                self.remove_edge(frm, to)
        return self

class FrequentGraph(Graph):
    def __init__(self, gid = INVALID_GRAPH_ID, is_undirected = True):
        super(FrequentGraph, self).__init__(gid = gid, is_undirected = is_undirected)
        self.DFScode = []
        self.
