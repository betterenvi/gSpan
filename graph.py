import collections
import itertools
VACANT_EDGE_ID = -1
VACANT_VERTEX_ID = -1
VACANT_EDGE_LABEL = -1
VACANT_VERTEX_LABEL = -1
VACANT_GRAPH_ID = -1
AUTO_EDGE_ID = -1


class Edge(object):

    def __init__(self,
                 eid=VACANT_EDGE_ID,
                 frm=VACANT_VERTEX_ID,
                 to=VACANT_VERTEX_ID,
                 elb=VACANT_EDGE_LABEL):

        self.eid = eid
        self.frm = frm
        self.to = to
        self.elb = elb


class Vertex(object):

    def __init__(self,
                 vid=VACANT_VERTEX_ID,
                 vlb=VACANT_VERTEX_LABEL):

        self.vid = vid
        self.vlb = vlb
        self.edges = dict()

    def add_edge(self, eid, frm, to, elb):
        self.edges[to] = Edge(eid, frm, to, elb)


class Graph(object):

    def __init__(self,
                 gid=VACANT_GRAPH_ID,
                 is_undirected=True,
                 eid_auto_increment=True):

        self.gid = gid
        self.is_undirected = is_undirected
        self.vertices = dict()
        self.set_of_elb = collections.defaultdict(set)
        self.set_of_vlb = collections.defaultdict(set)
        self.eid_auto_increment = eid_auto_increment
        self.counter = 0#itertools.count()

    def get_num_vertices(self):
        return len(self.vertices)

    def add_vertex(self, vid, vlb):
        if vid in self.vertices:
            return self
        self.vertices[vid] = Vertex(vid, vlb)
        self.set_of_vlb[vlb].add(vid)
        return self

    def add_edge(self, eid, frm, to, elb):
        if (frm is self.vertices and
            to in self.vertices and
            to in self.vertices[frm].edges):
            return self
        if self.eid_auto_increment:
            eid = self.counter#.next()
            self.counter+=1
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
                e = v.edges[to]  # (vid, to) and (to, vid) have same elb
                self.set_of_elb[e.elb].discard((to, vid))
                del self.vertices[to].edges[vid]
        else:
            for frm in self.vertices.keys():
                v = self.vertices[frm]
                if vid in v.edges.keys():
                    e = self.vertices[frm].edges[vid]
                    self.set_of_elb[e.elb].discard((frm, vid))
                    del self.vertices[frm].edges[vid]

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
        del self.vertices[frm].edges[to]
        if self.is_undirected:
            self.set_of_elb[elb].discard((to, frm))
            del self.vertices[to].edges[frm]
        return self

    def remove_edge_with_elb(self, elb):
        # use list. otherwise, 'Set changed size during iteration'
        for frm, to in list(self.set_of_elb[elb]):
            self.remove_edge(frm, to)
        return self

    def remove_vertex_with_vlb(self, vlb):
        for vid in list(self.set_of_vlb[vlb]):
            self.remove_vertex(vid)
        return self

    def remove_edge_with_vevlb(self, vevlb):
        vlb1, elb, vlb2 = vevlb
        for frm, to in list(self.set_of_elb[elb]):
            if frm in self.set_of_vlb[vlb1] and to in self.set_of_vlb[vlb2]:
                self.remove_edge(frm, to)
        return self

    def display(self):
        display_str=''
        print('t # {}'.format(self.gid))
        for vid in self.vertices:
            print('v {} {}'.format(vid, self.vertices[vid].vlb))
            display_str+='v {} {} '.format(vid, self.vertices[vid].vlb)
        for frm in self.vertices:
            edges = self.vertices[frm].edges
            for to in edges:
                if self.is_undirected:
                    if frm < to:
                        print('e {} {} {}'.format(frm, to, edges[to].elb))
                        display_str+='e {} {} {} '.format(frm, to, edges[to].elb)
                else:
                    print('e {} {} {}'.format(frm, to, edges[to].elb))
                    display_str+='e {} {} {}'.format(frm, to, edges[to].elb)
        return display_str

    def plot(self):
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except Exception as e:
            print('Can not plot graph: {}'.format(e))
            return
        gnx = nx.Graph() if self.is_undirected else nx.DiGraph()
        vlbs = {vid: v.vlb for vid, v in self.vertices.items()}
        elbs = {}
        for vid, v in self.vertices.items():
            gnx.add_node(vid, label=v.vlb)
        for vid, v in self.vertices.items():
            for to, e in v.edges.items():
                if (not self.is_undirected) or vid < to:
                    gnx.add_edge(vid, to, label=e.elb)
                    elbs[(vid, to)] = e.elb
        fsize = (min(16, 1 * len(self.vertices)),
                 min(16, 1 * len(self.vertices)))
        plt.figure(3, figsize=fsize)
        pos = nx.spectral_layout(gnx)
        nx.draw_networkx(gnx, pos, arrows=True, with_labels=True, labels=vlbs)
        # nx.draw_networkx_labels(gnx,pos)
        nx.draw_networkx_edge_labels(gnx, pos, edge_labels=elbs)
        plt.show()
