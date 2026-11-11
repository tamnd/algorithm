# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinkless-orientation/. The authors are listed in prov/T5PX1A.jsonl.

"""Sinkless orientation: a checker, a random start, and a reference repair by path reversal.

An orientation maps each edge {u, v} (stored with u < v) to its head. It is
sinkless if every node of degree at least 3 has an outgoing edge. Nodes of
degree 1 or 2 are free.

random_orientation orients each edge by a fair coin; a node of degree d is
then a sink with probability 2^(-d). repair removes the sinks one at a time:
for a sink v it searches backwards along directed edges for a node w that is
free or has at least two outgoing edges, and reverses the directed path from
w to v. Then v gains an outgoing edge, w loses one (and keeps one, or is
free), and the inner nodes of the path keep their out-degree. Such a w always
exists, by a counting argument given on the page.

Precondition: adj is an undirected simple graph.
Cost: repair is a centralized reference; each sink costs one backward BFS, O(n + m).
"""

import random
from collections import deque

Orientation = dict[tuple[int, int], int]


def edges(adj: list[list[int]]) -> list[tuple[int, int]]:
    return [(u, v) for u in range(len(adj)) for v in adj[u] if u < v]


def out_degree(adj: list[list[int]], orient: Orientation) -> list[int]:
    out = [0] * len(adj)
    for (u, v), head in orient.items():
        out[u if head == v else v] += 1
    return out


def is_sinkless(adj: list[list[int]], orient: Orientation) -> bool:
    if set(orient) != set(edges(adj)):
        return False
    if any(head not in e for e, head in orient.items()):
        return False
    out = out_degree(adj, orient)
    return all(out[v] >= 1 for v in range(len(adj)) if len(adj[v]) >= 3)


def random_orientation(adj: list[list[int]], rng: random.Random) -> Orientation:
    return {(u, v): (v if rng.random() < 0.5 else u) for u, v in edges(adj)}


def sinks(adj: list[list[int]], orient: Orientation) -> list[int]:
    out = out_degree(adj, orient)
    return [v for v in range(len(adj)) if len(adj[v]) >= 3 and out[v] == 0]


def head_of(orient: Orientation, a: int, b: int) -> int:
    return orient[(min(a, b), max(a, b))]


def repair(adj: list[list[int]], orient: Orientation) -> tuple[Orientation, int]:
    """Return (sinkless orientation, total length of reversed paths)."""
    orient = dict(orient)
    out = out_degree(adj, orient)
    reversed_edges = 0
    for v in range(len(adj)):
        if len(adj[v]) < 3 or out[v] > 0:
            continue
        # backward BFS: x -> y is an edge with head y; walk from y to x
        parent = {v: -1}
        q = deque([v])
        w = -1
        while q and w < 0:
            y = q.popleft()
            for x in adj[y]:
                if x not in parent and head_of(orient, x, y) == y:
                    parent[x] = y
                    if len(adj[x]) < 3 or out[x] >= 2:
                        w = x
                        break
                    q.append(x)
        assert w >= 0, "no free or rich node reaches the sink"
        out[w] -= 1
        out[v] += 1
        x = w
        while x != v:
            y = parent[x]
            orient[(min(x, y), max(x, y))] = x
            reversed_edges += 1
            x = y
    return orient, reversed_edges
