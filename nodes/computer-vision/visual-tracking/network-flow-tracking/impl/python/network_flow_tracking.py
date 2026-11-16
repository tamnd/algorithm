# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-flow-tracking/. The authors are listed in prov/4Z2N0P.jsonl.
"""Network flow data association (Zhang, Li and Nevatia, 2008).

All detections of a video are linked into tracks at once. Each detection i
becomes two nodes u_i and v_i joined by an edge of capacity 1 and cost c_i
(negative for a likely true detection). The source s connects to every u_i
(entry cost), every v_i connects to the sink t (exit cost), and v_i connects
to u_j when detection j may follow detection i in a track (link cost). A flow
of k units is a set of k disjoint tracks, and its cost is the cost of the
tracks. The flow of least cost over all k is found by successive shortest
paths: augment one unit along a shortest s-t path of the residual graph,
found with Bellman-Ford because costs can be negative, until the shortest
path costs 0 or more.
"""

import math

INF = float("inf")


class FlowGraph:
    """A directed graph with unit capacities and a residual edge for each edge."""

    def __init__(self, n_nodes):
        self.n = n_nodes
        self.to, self.cap, self.cost, self.adj = [], [], [], [[] for _ in range(n_nodes)]

    def add_edge(self, a, b, cost, cap=1):
        self.adj[a].append(len(self.to))
        self.to.append(b)
        self.cap.append(cap)
        self.cost.append(cost)
        self.adj[b].append(len(self.to))
        self.to.append(a)
        self.cap.append(0)
        self.cost.append(-cost)

    def shortest_path(self, s, t):
        """Bellman-Ford on the edges with residual capacity. Returns (distance, list of edge ids) or (INF, None)."""
        dist = [INF] * self.n
        prev = [-1] * self.n
        dist[s] = 0.0
        for _ in range(self.n - 1):
            changed = False
            for a in range(self.n):
                if dist[a] == INF:
                    continue
                for e in self.adj[a]:
                    if self.cap[e] > 0 and dist[a] + self.cost[e] < dist[self.to[e]] - 1e-12:
                        dist[self.to[e]] = dist[a] + self.cost[e]
                        prev[self.to[e]] = e
                        changed = True
            if not changed:
                break
        if dist[t] == INF:
            return INF, None
        path, node = [], t
        while node != s:
            e = prev[node]
            path.append(e)
            node = self.to[e ^ 1]
        return dist[t], path[::-1]


def track_by_flow(n_det, det_cost, entry_cost, exit_cost, links):
    """Least-cost set of disjoint tracks.

    n_det: the number of detections. det_cost[i], entry_cost[i], exit_cost[i]:
    the costs of using detection i, of starting a track at i, of ending a track
    at i. links: a dict {(i, j): cost} of the allowed links from detection i to
    a later detection j. Returns (tracks, total cost, the costs of the
    augmenting paths in order), with each track a list of detections.
    """
    s, t = 2 * n_det, 2 * n_det + 1
    g = FlowGraph(2 * n_det + 2)  # u_i = 2i, v_i = 2i + 1
    for i in range(n_det):  # @line L1
        g.add_edge(2 * i, 2 * i + 1, det_cost[i])
        g.add_edge(s, 2 * i, entry_cost[i])  # @line L2
        g.add_edge(2 * i + 1, t, exit_cost[i])
    for (i, j), c in sorted(links.items()):
        g.add_edge(2 * i + 1, 2 * j, c)
    total, path_costs = 0.0, []  # @line L3
    while True:
        d, path = g.shortest_path(s, t)  # @line L4
        if path is None or d >= 0:  # @line L5
            break
        for e in path:  # @line L6
            g.cap[e] -= 1
            g.cap[e ^ 1] += 1
        total += d
        path_costs.append(d)
    tracks = []  # @line L7
    for e in g.adj[s]:
        if e % 2 == 0 and g.cap[e] == 0:  # an edge s -> u_i that carries flow
            node, track = g.to[e], []
            while node != t:
                track.append(node // 2)
                v = node + 1
                nxt = None
                for f in g.adj[v]:
                    if f % 2 == 0 and g.cap[f] == 0:
                        nxt = g.to[f]
                        break
                node = nxt
            tracks.append(track)
    tracks.sort()
    return tracks, total, path_costs


def tracks_cost(tracks, det_cost, entry_cost, exit_cost, links):
    """The cost of a set of tracks under the model of track_by_flow."""
    total = 0.0
    for tr in tracks:
        total += entry_cost[tr[0]] + exit_cost[tr[-1]] + sum(det_cost[i] for i in tr)
        total += sum(links[(a, b)] for a, b in zip(tr, tr[1:]))
    return total


def detection_costs(frames, sigma=1.0, max_gap=2, gap_cost=1.0, enter=2.0, leave=2.0, speed=None):
    """Costs of a simple tracking model from detections (frame, x, y, score).

    det_cost = ln((1 - score) / score), negative for a score above 0.5.
    A link i -> j with 1 <= gap <= max_gap frames costs |p_j - p_i - gap v|^2
    / (2 gap sigma^2) + (gap - 1) gap_cost, with v a known mean velocity or
    zero, and is allowed only below 9.21 / 2 + (gap - 1) gap_cost.
    """
    n = len(frames)
    det = [math.log((1.0 - f[3]) / f[3]) for f in frames]
    vx, vy = speed if speed else (0.0, 0.0)
    links = {}
    for i in range(n):
        for j in range(n):
            gap = frames[j][0] - frames[i][0]
            if 1 <= gap <= max_gap:
                dx = frames[j][1] - frames[i][1] - gap * vx
                dy = frames[j][2] - frames[i][2] - gap * vy
                c = (dx * dx + dy * dy) / (2 * gap * sigma * sigma)
                if c <= 9.21 / 2:
                    links[(i, j)] = c + (gap - 1) * gap_cost
    return det, [enter] * n, [leave] * n, links
