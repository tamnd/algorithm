# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gomory-hu-algorithm/. The authors are listed in prov/PSCBG5.jsonl.

from collections import deque
from fractions import Fraction
from typing import Callable, Optional, Union

Number = Union[int, Fraction, float]


def _min_cut(k: int, arcs: list[tuple[int, int, Number]], s: int, t: int) -> tuple[Number, set[int]]:
    """Minimum s-t cut of a directed network on 0 .. k-1 by shortest augmenting paths.

    Returns (value, S) with S the vertices reachable from s in the final residual graph.
    """
    head: list[int] = []
    res: list[Number] = []
    adj: list[list[int]] = [[] for _ in range(k)]
    for u, v, cap in arcs:
        adj[u].append(len(head))
        head.append(v)
        res.append(cap)
        adj[v].append(len(head))
        head.append(u)
        res.append(0)
    value: Number = 0
    while True:
        parent = [-1] * k
        parent[s] = -2
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for a in adj[u]:
                v = head[a]
                if res[a] > 0 and parent[v] == -1:
                    parent[v] = a
                    queue.append(v)
        if parent[t] == -1:
            return value, {v for v in range(k) if parent[v] != -1}
        delta = None
        v = t
        while v != s:
            a = parent[v]
            delta = res[a] if delta is None else min(delta, res[a])
            v = head[a ^ 1]
        v = t
        while v != s:
            a = parent[v]
            res[a] -= delta
            res[a ^ 1] += delta
            v = head[a ^ 1]
        value += delta


def gomory_hu_algorithm(
    n: int,
    edges: list[tuple[int, int, Number]],
    on_split: Optional[Callable[[int, int, Number, list[int], list[int]], None]] = None,
) -> list[tuple[int, int, Number]]:
    """Gomory-Hu cut tree of an undirected graph by the original contraction method.

    The graph has the vertices 0 .. n-1 and the undirected edges (u, v, w), w >= 0
    (int, Fraction or float). Parallel and zero-weight edges are allowed; self-loops
    are ignored. Each undirected edge is sent to the flow routine as two arcs u->v
    and v->u of capacity w.
    Returns the n - 1 tree edges (a, b, lam) with a < b, sorted. For each pair u, v the
    least lam on the tree path is the minimum u-v cut value, and deleting that tree
    edge splits the vertices into a minimum u-v cut.
    on_split(s, t, lam, xs, xt) is called after each split, with xs and xt the two
    halves of the split tree node.
    n - 1 maximum flow computations on contracted graphs, O(n + m) space besides them.
    """
    for u, v, w in edges:
        if w < 0:
            raise ValueError("weights must be nonnegative")
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("vertex out of range")
    if n <= 1:
        return []
    nodes: list[list[int]] = [list(range(n))]  # @line L1
    tree: list[list[tuple[int, Number]]] = [[]]  # tree[i]: (neighbour node, weight)
    while True:
        x = next((i for i, X in enumerate(nodes) if len(X) >= 2), -1)  # @line L2
        if x == -1:
            break
        s, t = nodes[x][0], nodes[x][1]  # @line L3
        label = [-1] * n  # vertex of the contracted graph G_X for each vertex of G
        k = 0
        for v in nodes[x]:
            label[v] = k
            k += 1
        comp_of_nbr: dict[int, int] = {}
        for y, _ in tree[x]:  # @line L4
            comp = k
            k += 1
            comp_of_nbr[y] = comp
            seen = {x, y}
            stack = [y]
            while stack:
                z = stack.pop()
                for v in nodes[z]:
                    label[v] = comp
                for z2, _ in tree[z]:
                    if z2 not in seen:
                        seen.add(z2)
                        stack.append(z2)
        arcs: list[tuple[int, int, Number]] = []
        for u, v, w in edges:
            a, b = label[u], label[v]
            if a != b:
                arcs.append((a, b, w))
                arcs.append((b, a, w))
        lam, side = _min_cut(k, arcs, label[s], label[t])  # @line L5
        xs = [v for v in nodes[x] if label[v] in side]  # @line L6
        xt = [v for v in nodes[x] if label[v] not in side]
        nodes[x] = xs  # @line L7
        nodes.append(xt)
        y_new = len(nodes) - 1
        old = tree[x]
        tree[x] = [(y_new, lam)]
        tree.append([(x, lam)])
        for y, w in old:  # @line L8
            if comp_of_nbr[y] in side:
                tree[x].append((y, w))
            else:
                tree[y_new].append((y, w))
                tree[y] = [(y_new if z == x else z, w2) for z, w2 in tree[y]]
        if on_split is not None:
            on_split(s, t, lam, sorted(xs), sorted(xt))
    out = []  # @line L9
    for i, X in enumerate(nodes):
        for j, w in tree[i]:
            if i < j:
                a, b = X[0], nodes[j][0]
                out.append((min(a, b), max(a, b), w))
    out.sort(key=lambda e: (e[0], e[1]))
    return out
