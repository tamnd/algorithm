# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dimension-order-routing/. The authors are listed in prov/RHGNKB.jsonl.

"""Dimension-order routing on meshes, hypercubes and tori, and channel dependency graphs.

A node is a tuple of coordinates. A channel is (node, dim, direction, vc):
the link that leaves node along dimension dim in direction +1 or -1, on
virtual channel vc. A hypercube is the mesh with k = 2 in every dimension.

The channel dependency graph (Dally and Seitz, 1987) has an edge c1 -> c2 when
some packet can hold c1 and ask for c2 next. A deterministic routing function
is deadlock-free when this graph has no cycle.
"""

import itertools


def next_hop_mesh(cur: tuple, dst: tuple):
    """XY routing (e-cube on a hypercube): fix dimension 0 first, then 1, and so on."""
    for d in range(len(cur)):  # @line L1
        if cur[d] != dst[d]:  # @line L2
            if cur[d] < dst[d]:  # @line L3
                return d, +1
            return d, -1  # @line L4
    return None  # @line L5


def next_hop_torus(k: int):
    """Minimal dimension-order routing on a k-ary torus; ties go in the + direction."""

    def hop(cur: tuple, dst: tuple):
        for d in range(len(cur)):
            if cur[d] != dst[d]:
                ahead = (dst[d] - cur[d]) % k
                return (d, +1) if 2 * ahead <= k else (d, -1)
        return None

    return hop


def route(cur: tuple, dst: tuple, hop, k: int, torus: bool = False, dateline: bool = False) -> list:
    """The channels used from cur to dst.

    With dateline=True, a packet uses VC 0 in each dimension until it crosses
    the wrap-around link of that ring, and VC 1 after it.
    """
    channels = []
    cur = list(cur)
    vc, last_dim = 0, None
    while True:
        step = hop(tuple(cur), dst)
        if step is None:
            return channels
        d, s = step
        if d != last_dim:
            vc, last_dim = 0, d
        channels.append((tuple(cur), d, s, vc if dateline else 0))
        nxt = cur[d] + s
        if torus:
            wrapped = nxt in (-1, k)
            nxt %= k
            if wrapped and dateline:
                vc = 1
        elif not 0 <= nxt < k:
            raise AssertionError("mesh route left the mesh")
        cur[d] = nxt


def nodes(k: int, n: int) -> list:
    return list(itertools.product(range(k), repeat=n))


def dependency_graph(k: int, n: int, hop, torus: bool = False, dateline: bool = False) -> dict:
    """Channel dependency graph induced by the routes between all pairs of nodes."""
    graph: dict = {}
    for src in nodes(k, n):
        for dst in nodes(k, n):
            chans = route(src, dst, hop, k, torus, dateline)
            for c in chans:
                graph.setdefault(c, set())
            for a, b in zip(chans, chans[1:]):
                graph[a].add(b)
    return graph


def union(g1: dict, g2: dict) -> dict:
    out = {c: set(s) for c, s in g1.items()}
    for c, s in g2.items():
        out.setdefault(c, set()).update(s)
    return out


def find_cycle(graph: dict):
    """Return a list of channels on a cycle, or None. Iterative DFS."""
    color = {c: 0 for c in graph}  # 0 new, 1 on stack, 2 done
    for root in graph:
        if color[root]:
            continue
        stack = [(root, iter(sorted(graph[root])))]
        path = [root]
        color[root] = 1
        while stack:
            c, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                path.pop()
                color[c] = 2
            elif color.get(nxt, 0) == 1:
                return path[path.index(nxt):]
            elif color.get(nxt, 0) == 0:
                color[nxt] = 1
                path.append(nxt)
                stack.append((nxt, iter(sorted(graph.get(nxt, ())))))
    return None


def channel_number(c: tuple, k: int) -> int:
    """A numbering that increases along every XY route on a k-ary n-dimensional mesh."""
    node, d, s, _ = c
    x = node[d]
    return 2 * k * d + (x if s > 0 else k + (k - 1 - x))
