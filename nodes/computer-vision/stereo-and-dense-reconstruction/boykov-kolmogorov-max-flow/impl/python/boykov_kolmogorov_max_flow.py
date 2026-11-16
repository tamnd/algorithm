# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boykov-kolmogorov-max-flow/. The authors are listed in prov/FXPM4P.jsonl.
"""The Boykov-Kolmogorov max-flow algorithm.

The graph has nodes 0 .. n - 1 and directed edges (u, v, capacity) with
nonnegative capacities. Each input edge k is stored as the residual edge
2k (u -> v) and its reverse 2k + 1 (v -> u, residual capacity 0 at the
start), so the reverse of edge e is e ^ 1.

Two search trees are kept: S grows from the source along edges with
residual capacity, T grows into the sink along edges with residual
capacity. parent[v] is the index of the tree edge that joins v to its
parent: the edge parent -> v in S, and the edge v -> parent in T.
"""

from __future__ import annotations

from collections import deque
from typing import List, Sequence, Tuple

FREE, SRC, SNK = 0, 1, 2
TERMINAL = -1  # parent value of s and t
NONE = -2  # parent value of an orphan or a free node


def bk_max_flow(n: int, edges: Sequence[Tuple[int, int, int]], s: int,
                t: int) -> Tuple[int, List[bool], List[int]]:
    """Return (flow value, source side of a minimum cut, flow on each edge).

    The source side is the final S tree, which is the set of nodes that
    the source reaches in the residual graph.
    """
    if s == t:
        raise ValueError("source and sink must differ")
    adj: List[List[int]] = [[] for _ in range(n)]
    to: List[int] = []
    cap: List[int] = []
    for (u, v, c) in edges:
        if c < 0:
            raise ValueError("capacities must be nonnegative")
        adj[u].append(len(to))
        to.append(v)
        cap.append(c)
        adj[v].append(len(to))
        to.append(u)
        cap.append(0)

    tree = [FREE] * n  # @line L1
    parent = [NONE] * n  # @line L1
    tree[s], tree[t] = SRC, SNK  # @line L1
    parent[s] = parent[t] = TERMINAL  # @line L1
    active = deque([s, t])  # @line L2
    in_active = [False] * n  # @line L2
    in_active[s] = in_active[t] = True  # @line L2
    orphans: deque = deque()  # @line L2
    flow = 0  # @line L2

    def make_active(v: int) -> None:
        if not in_active[v]:
            in_active[v] = True
            active.append(v)

    def grow() -> int:
        """Return an edge from a node of S to a node of T, or -1."""
        while active:  # @line L12
            p = active[0]  # @line L13
            if tree[p] == FREE:  # @line L13
                active.popleft()  # @line L13
                in_active[p] = False  # @line L13
                continue  # @line L13
            for e in adj[p]:  # @line L14
                q = to[e]
                if tree[p] == SRC:
                    if cap[e] <= 0:  # @line L14
                        continue
                    if tree[q] == FREE:  # @line L15
                        tree[q], parent[q] = SRC, e  # @line L15
                        make_active(q)  # @line L15
                    elif tree[q] == SNK:  # @line L16
                        return e  # @line L16
                else:
                    if cap[e ^ 1] <= 0:  # @line L14
                        continue
                    if tree[q] == FREE:  # @line L15
                        tree[q], parent[q] = SNK, e ^ 1  # @line L15
                        make_active(q)  # @line L15
                    elif tree[q] == SRC:  # @line L16
                        return e ^ 1  # @line L16
            active.popleft()  # @line L17
            in_active[p] = False  # @line L17
        return -1  # @line L18

    def has_terminal_origin(q: int) -> bool:
        while parent[q] != TERMINAL:
            if parent[q] == NONE:
                return False
            e = parent[q]
            q = to[e ^ 1] if tree[q] == SRC else to[e]
        return True

    def adopt(p: int) -> None:
        side = tree[p]
        for e in adj[p]:  # @line L19
            q = to[e]
            if tree[q] != side:
                continue
            # The candidate parent edge: q -> p in S, p -> q in T.
            pe = e ^ 1 if side == SRC else e
            if cap[pe] > 0 and has_terminal_origin(q):  # @line L20
                parent[p] = pe  # @line L20
                return  # @line L20
        for e in adj[p]:  # @line L21
            q = to[e]
            if tree[q] != side:
                continue
            pe = e ^ 1 if side == SRC else e
            if cap[pe] > 0:  # @line L22
                make_active(q)  # @line L22
            child_edge = e if side == SRC else e ^ 1
            if parent[q] == child_edge:  # @line L23
                parent[q] = NONE  # @line L23
                orphans.append(q)  # @line L23
        tree[p] = FREE  # @line L24

    while True:  # @line L3
        bridge = grow()  # @line L4
        if bridge < 0:  # @line L5
            break  # @line L5
        path = [bridge]  # @line L6
        a = to[bridge ^ 1]  # @line L6
        while parent[a] != TERMINAL:  # @line L6
            path.append(parent[a])  # @line L6
            a = to[parent[a] ^ 1]  # @line L6
        c = to[bridge]  # @line L6
        while parent[c] != TERMINAL:  # @line L6
            path.append(parent[c])  # @line L6
            c = to[parent[c]]  # @line L6
        delta = min(cap[e] for e in path)  # @line L7
        for e in path:  # @line L7
            cap[e] -= delta  # @line L7
            cap[e ^ 1] += delta  # @line L7
        flow += delta  # @line L7
        for e in path[1:]:  # @line L8
            if cap[e] == 0:  # @line L8
                head, tail = to[e], to[e ^ 1]
                if tree[head] == SRC and tree[tail] == SRC:  # @line L9
                    parent[head] = NONE  # @line L9
                    orphans.append(head)  # @line L9
                elif tree[head] == SNK and tree[tail] == SNK:  # @line L10
                    parent[tail] = NONE  # @line L10
                    orphans.append(tail)  # @line L10
        while orphans:  # @line L11
            adopt(orphans.popleft())  # @line L11

    source_side = [tree[v] == SRC for v in range(n)]
    edge_flow = [cap[2 * k + 1] for k in range(len(edges))]
    return flow, source_side, edge_flow


def cut_capacity(n: int, edges: Sequence[Tuple[int, int, int]],
                 source_side: Sequence[bool]) -> int:
    """The total capacity of the edges from the source side to the rest."""
    return sum(c for (u, v, c) in edges if source_side[u] and not source_side[v])


def grid_graph(w: int, h: int, terminal_caps, pair_caps) -> Tuple[int, list, int, int]:
    """A 4-connected grid of w x h pixels in the form used in vision.

    terminal_caps[v][u] = (a, b) gives the edges s -> pixel of capacity a and
    pixel -> t of capacity b. pair_caps(u1, v1, u2, v2) gives the capacity of
    each of the two edges between 4-neighbors. Returns (n, edges, s, t).
    """
    s, t = w * h, w * h + 1
    edges = []
    for v in range(h):
        for u in range(w):
            p = v * w + u
            a, b = terminal_caps[v][u]
            if a:
                edges.append((s, p, a))
            if b:
                edges.append((p, t, b))
            for (du, dv) in ((1, 0), (0, 1)):
                uu, vv = u + du, v + dv
                if uu < w and vv < h:
                    q = vv * w + uu
                    c = pair_caps(u, v, uu, vv)
                    if c:
                        edges.append((p, q, c))
                        edges.append((q, p, c))
    return w * h + 2, edges, s, t
