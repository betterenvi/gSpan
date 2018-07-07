"""Definitions of Edge, Vertex and Graph."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import itertools


VACANT_EDGE_ID = -1
VACANT_VERTEX_ID = -1
VACANT_EDGE_LABEL = -1
VACANT_VERTEX_LABEL = -1
VACANT_GRAPH_ID = -1
AUTO_EDGE_ID = -1


class Edge(object):
    """Edge class."""

    def __init__(self,
                 eid=VACANT_EDGE_ID,
                 frm=VACANT_VERTEX_ID,
                 to=VACANT_VERTEX_ID,
                 elb=VACANT_EDGE_LABEL):
        """Initialize Edge instance.

        Args:
            eid: edge id.
            frm: source vertex id.
            to: destination vertex id.
            elb: edge label.
        """
        self.eid = eid
        self.frm = frm
        self.to = to
        self.elb = elb


class Vertex(object):
    """Vertex class."""

    def __init__(self,
                 vid=VACANT_VERTEX_ID,
                 vlb=VACANT_VERTEX_LABEL):
        """Initialize Vertex instance.

        Args:
            vid: id of this vertex.
            vlb: label of this vertex.
        """
        self.vid = vid
        self.vlb = vlb
        self.edges = dict()

    def add_edge(self, eid, frm, to, elb):
        """Add an outgoing edge."""
        self.edges[to] = Edge(eid, frm, to, elb)


class Graph(object):
    """Graph class."""

    def __init__(self,
                 gid=VACANT_GRAPH_ID,
                 is_undirected=True,
                 eid_auto_increment=True):
        """Initialize Graph instance.

        Args:
            gid: id of this graph.
            is_undirected: whether this graph is directed or not.
            eid_auto_increment: whether to increment edge ids automatically.
        """
        self.gid = gid
        self.is_undirected = is_undirected
        self.vertices = dict()
        self.set_of_elb = collections.defaultdict(set)
        self.set_of_vlb = collections.defaultdict(set)
        self.eid_auto_increment = eid_auto_increment
        self.counter = itertools.count()

    def get_num_vertices(self):
        """Return number of vertices in the graph."""
        return len(self.vertices)

    def add_vertex(self, vid, vlb):
        """Add a vertex to the graph."""
        if vid in self.vertices:
            return self
        self.vertices[vid] = Vertex(vid, vlb)
        self.set_of_vlb[vlb].add(vid)
        return self

    def add_edge(self, eid, frm, to, elb):
        """Add an edge to the graph."""
        if (frm is self.vertices and
                to in self.vertices and
                to in self.vertices[frm].edges):
            return self
        if self.eid_auto_increment:
            eid = next(self.counter)
        self.vertices[frm].add_edge(eid, frm, to, elb)
        self.set_of_elb[elb].add((frm, to))
        if self.is_undirected:
            self.vertices[to].add_edge(eid, to, frm, elb)
            self.set_of_elb[elb].add((to, frm))
        return self

    def display(self):
        """Display the graph as text."""
        display_str = ''
        print('t # {}'.format(self.gid))
        for vid in self.vertices:
            print('v {} {}'.format(vid, self.vertices[vid].vlb))
            display_str += 'v {} {} '.format(vid, self.vertices[vid].vlb)
        for frm in self.vertices:
            edges = self.vertices[frm].edges
            for to in edges:
                if self.is_undirected:
                    if frm < to:
                        print('e {} {} {}'.format(frm, to, edges[to].elb))
                        display_str += 'e {} {} {} '.format(
                            frm, to, edges[to].elb)
                else:
                    print('e {} {} {}'.format(frm, to, edges[to].elb))
                    display_str += 'e {} {} {}'.format(frm, to, edges[to].elb)
        return display_str

    def plot(self):
        """Visualize the graph."""
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
        nx.draw_networkx_edge_labels(gnx, pos, edge_labels=elbs)
        plt.show()
