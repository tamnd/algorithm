# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gpsr/. The authors are listed in prov/8QEP75.jsonl.
"""GPSR: greedy forwarding with perimeter (face) routing on a planar subgraph.

Nodes are points in the plane; two nodes are neighbors when they are within the
radio range r (a unit disk graph). Each node computes, from its neighbors alone,
its edges in the Gabriel graph or the relative neighborhood graph.
"""

import math


def dist2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def unit_disk_graph(points, r):
    n = len(points)
    adj = [set() for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if dist2(points[u], points[v]) <= r * r:
                adj[u].add(v)
                adj[v].add(u)
    return adj


def gabriel_graph(points, adj):
    """Keep uv unless a common witness w lies strictly inside the circle with diameter uv."""
    out = [set() for _ in adj]
    for u in range(len(adj)):
        for v in adj[u]:
            d = dist2(points[u], points[v])
            if not any(dist2(points[u], points[w]) + dist2(points[v], points[w]) < d for w in adj[u] if w != v):
                out[u].add(v)
    return out


def relative_neighborhood_graph(points, adj):
    """Keep uv unless some w is closer to both u and v than they are to each other."""
    out = [set() for _ in adj]
    for u in range(len(adj)):
        for v in adj[u]:
            d = dist2(points[u], points[v])
            if not any(max(dist2(points[u], points[w]), dist2(points[v], points[w])) < d for w in adj[u] if w != v):
                out[u].add(v)
    return out


def angle(a, b):
    return math.atan2(b[1] - a[1], b[0] - a[0])


def next_ccw(points, planar, x, ref_angle, exclude_zero=True):
    """The neighbor of x in the planar graph that comes first counterclockwise from ref_angle."""
    best, best_d = None, None
    for z in planar[x]:
        d = (angle(points[x], points[z]) - ref_angle) % (2 * math.pi)
        if exclude_zero and d < 1e-12:
            d = 2 * math.pi
        if best_d is None or d < best_d:
            best, best_d = z, d
    return best


def crossing(p1, p2, q1, q2):
    """The point where segment p1p2 properly crosses segment q1q2, or None."""
    d = (p2[0] - p1[0]) * (q2[1] - q1[1]) - (p2[1] - p1[1]) * (q2[0] - q1[0])
    if abs(d) < 1e-15:
        return None
    t = ((q1[0] - p1[0]) * (q2[1] - q1[1]) - (q1[1] - p1[1]) * (q2[0] - q1[0])) / d
    s = ((q1[0] - p1[0]) * (p2[1] - p1[1]) - (q1[1] - p1[1]) * (p2[0] - p1[0])) / d
    if 1e-12 < t < 1 - 1e-12 and 1e-12 < s < 1 - 1e-12:
        return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
    return None


def gpsr(points, adj, planar, src, dst, max_hops=None):
    """Route one packet from src to dst. Returns (delivered, path, greedy hops, perimeter hops)."""
    D = points[dst]
    if max_hops is None:
        max_hops = 4 * len(points) * len(points)
    x, prev = src, None
    mode = "greedy"
    lp = lf = None
    e0 = None
    e0_used = False
    path = [src]
    greedy_hops = perimeter_hops = 0
    while len(path) <= max_hops:
        if x == dst:  # @line L1 arrived
            return True, path, greedy_hops, perimeter_hops
        if mode == "perimeter" and dist2(points[x], D) < dist2(lp, D):
            mode = "greedy"  # @line L2 closer than where perimeter mode began
        if mode == "greedy":  # @line L3
            y = min(adj[x], key=lambda z: (dist2(points[z], D), z), default=None)  # @line L4
            if y is not None and dist2(points[y], D) < dist2(points[x], D):
                prev, x = x, y  # @line L5 greedy step
                path.append(x)
                greedy_hops += 1
                continue
            mode = "perimeter"  # @line L6 local minimum: enter perimeter mode
            lp = lf = points[x]
            z = next_ccw(points, planar, x, angle(points[x], D), exclude_zero=False)
            new_face = True
        else:
            z = next_ccw(points, planar, x, angle(points[x], points[prev]))  # @line L7 right-hand rule
            new_face = False
        if z is None:
            return False, path, greedy_hops, perimeter_hops
        for _ in range(len(planar[x]) + 1):
            p = crossing(points[x], points[z], lp, D)  # @line L8 face change
            if p is None or dist2(p, D) >= dist2(lf, D):
                break
            lf = p
            z = next_ccw(points, planar, x, angle(points[x], points[z]))
            new_face = True
        if new_face:
            e0, e0_used = (x, z), False
        if (x, z) == e0:  # @line L9 the first edge of the face again: unreachable
            if e0_used:
                return False, path, greedy_hops, perimeter_hops
            e0_used = True
        prev, x = x, z  # @line L10 forward along the edge
        path.append(x)
        perimeter_hops += 1
    return False, path, greedy_hops, perimeter_hops


def components(adj):
    comp = [-1] * len(adj)
    c = 0
    for s in range(len(adj)):
        if comp[s] >= 0:
            continue
        comp[s] = c
        stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if comp[v] < 0:
                    comp[v] = c
                    stack.append(v)
        c += 1
    return comp
