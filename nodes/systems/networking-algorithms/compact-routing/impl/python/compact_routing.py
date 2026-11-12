# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compact-routing/. The authors are listed in prov/CZ5P8G.jsonl.

"""The stretch-3 compact routing scheme of Thorup and Zwick (SPAA 2001).

Preprocessing picks a set A of landmarks with the procedure center(G, s):
sample landmarks, then sample again among the vertices whose cluster
C(w) = {v : d(w, v) < d(A, v)} is too large, until every cluster has at most
4n/s vertices. Then:

  table(u) = for each landmark l, the tree-routing record of u in the
             shortest-path tree T(l); and for each v in C(u), the next hop
             from u toward v.
  label(v) = (v, l_v, the tree-routing label of v in T(l_v)), where l_v is
             the landmark nearest to v.

To route from u to v: if v is in C(u), follow the stored next hops (every
vertex on the way also has v in its cluster). Otherwise route in T(l_v).
The route has length at most d(u, l_v) + d(l_v, v) <= 3 d(u, v).

Tree routing is the scheme of Thorup and Zwick for trees: depth-first
numbers with the heavy child first, so a vertex keeps O(1) words, and the
label of v lists the ports of the light edges on the path from the root to
v, at most log2(n) of them. Ports are neighbour names here.
"""

import heapq
import math


# ------------------------------------------------------------ shortest paths

def dijkstra(graph, s):
    """Distances from s and a shortest-path tree with tie-break by the
    parent's name. graph: dict v -> dict neighbour -> positive weight."""
    dist, par = {s: 0}, {s: None}
    pq, done = [(0, -1, s)], set()
    while pq:
        d, _, x = heapq.heappop(pq)
        if x in done:
            continue
        done.add(x)
        for y, w in graph[x].items():
            if y in done:
                continue
            nd = d + w
            if y not in dist or (nd, x) < (dist[y], par[y]):
                dist[y], par[y] = nd, x
                heapq.heappush(pq, (nd, x, y))
    return dist, par


def all_pairs(graph):
    out = {}
    for s in graph:
        out[s] = dijkstra(graph, s)
    return out


# --------------------------------------------------------------- landmarks

def clusters(graph, dist, A):
    """C(w) = {v : d(w, v) < d(A, v)} for every w."""
    inf = float("inf")
    dA = {v: min((dist[a][0].get(v, inf) for a in A), default=inf) for v in graph}
    return {w: {v for v, d in dist[w][0].items() if d < dA[v]} for w in graph}


def center(graph, dist, s, rng):
    """Thorup and Zwick's center(G, s): sample from W until every cluster
    has at most 4n/s vertices."""
    n = len(graph)
    A, W = set(), sorted(graph)
    while W:
        p = min(1.0, s / len(W))
        A |= {w for w in W if rng.random() < p}
        C = clusters(graph, dist, A)
        W = sorted(w for w in graph if len(C[w]) > 4 * n / s)
        if not W and not A:          # s <= 4: the bound holds already, but
            W = sorted(graph)        # the scheme needs one landmark
    return A, C


# ------------------------------------------------------------- tree routing

class TreeRouting:
    """Thorup-Zwick routing in one rooted tree, given by parent pointers."""

    def __init__(self, par, root):
        kids = {v: [] for v in par}
        for v, p in par.items():
            if p is not None:
                kids[p].append(v)
        size = {}
        order = [root]
        for v in order:
            order.extend(sorted(kids[v]))
        for v in reversed(order):
            size[v] = 1 + sum(size[c] for c in kids[v])
        heavy = {v: (max(kids[v], key=lambda c: (size[c], c)) if kids[v] else None)
                 for v in par}
        # depth-first numbering, heavy child first
        f, last, light_ports = {}, {}, {root: []}
        stack, k = [root], 0
        while stack:
            v = stack.pop()
            f[v] = k
            k += 1
            light = sorted(c for c in kids[v] if c != heavy[v])
            for c in reversed(light):
                light_ports[c] = light_ports[v] + [c]   # port of a light edge
                stack.append(c)
            if heavy[v] is not None:
                light_ports[heavy[v]] = light_ports[v]
                stack.append(heavy[v])
        for v in order:
            last[v] = f[v] + size[v] - 1
        # the O(1)-word record that each vertex keeps for this tree
        self.record = {v: (f[v], last[v], heavy[v],
                           last[heavy[v]] if heavy[v] is not None else None,
                           par[v], len(light_ports[v])) for v in par}
        # the label of each vertex: its number and its light-edge ports
        self.label = {v: (f[v], tuple(light_ports[v])) for v in par}

    def next_hop(self, x, label):
        """The neighbour of x toward the vertex with this label, or None
        if x is that vertex."""
        fx, lastx, h, hlast, parent, ldepth = self.record[x]
        fv, ports = label
        if fv == fx:
            return None
        if not fx < fv <= lastx:
            return parent
        if h is not None and fx + 1 <= fv <= hlast:
            return h
        return ports[ldepth]


# ------------------------------------------------------------- the scheme

class CompactRouting:
    def __init__(self, graph, rng, s=None):
        n = len(graph)
        self.graph = graph
        self.dist = all_pairs(graph)
        if s is None:
            s = max(1.0, math.sqrt(n / max(1.0, math.log(n))))
        self.A, C = center(graph, self.dist, s, rng)
        self.trees = {a: TreeRouting(self.dist[a][1], a) for a in sorted(self.A)}
        # tables
        self.direct = {u: {v: self.dist[v][1][u] for v in C[u]} for u in graph}
        # labels
        self.nearest = {}
        for v in graph:
            self.nearest[v] = min(sorted(self.A), key=lambda a: (self.dist[a][0][v], a))
        self.labels = {v: (v, self.nearest[v], self.trees[self.nearest[v]].label[v])
                       for v in graph}

    def table_words(self, u):
        """Words in u's table: a 6-word record per landmark, 2 per direct entry."""
        return 6 * len(self.A) + 2 * len(self.direct[u])

    def label_words(self, v):
        return 3 + len(self.labels[v][2][1])

    def route(self, u, v):
        """Forward a packet hop by hop, using only the local table and the
        header. Returns the list of vertices visited."""
        lab = self.labels[v]
        if v in self.direct[u]:
            header = ("direct", v)
        else:
            header = ("tree", lab[1], lab[2])
        path, x = [u], u
        while x != v:
            if header[0] == "direct":
                x = self.direct[x][v]
            else:
                x = self.trees[header[1]].next_hop(x, header[2])
            path.append(x)
            if len(path) > 4 * len(self.graph):
                raise RuntimeError("routing loop")
        return path

    def length(self, path):
        return sum(self.graph[a][b] for a, b in zip(path, path[1:]))
