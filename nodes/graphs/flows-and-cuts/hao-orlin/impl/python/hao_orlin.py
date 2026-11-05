# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hao-orlin/. The authors are listed in prov/X5P88R.jsonl.

from collections import deque
from fractions import Fraction
from typing import Callable, Optional, Union

Number = Union[int, Fraction, float]


def _rooted_min_cut(
    n: int,
    edges: list[tuple[int, int, Number]],
    s: int,
    on_phase: Optional[Callable[[int, Number, list[int]], None]],
) -> tuple[Number, list[int]]:
    """Least c(X, V - X) over sets X with s in X and X != V, by one Hao-Orlin run."""
    head: list[int] = []
    res: list[Number] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, cap in edges:
        if u == v:
            continue
        adj[u].append(len(head))
        head.append(v)
        res.append(cap)
        adj[v].append(len(head))
        head.append(u)
        res.append(0)
    excess: list[Number] = [0] * n
    d = [0] * n  # @line L1
    d[s] = n
    in_s = [False] * n
    in_s[s] = True
    awake = [v != s for v in range(n)]  # membership of W
    dormant: list[list[int]] = []  # dormant sets other than S, oldest first
    count: dict[int, int] = {0: n - 1}  # number of awake vertices with each label

    def push(a: int, amount: Number) -> None:
        res[a] -= amount
        res[a ^ 1] += amount
        excess[head[a ^ 1]] -= amount
        excess[head[a]] += amount

    def put_to_sleep(group: list[int]) -> None:
        for w in group:
            awake[w] = False
            count[d[w]] -= 1
        dormant.append(group)

    for a in adj[s]:  # @line L2
        if res[a] > 0:
            push(a, res[a])
    best_value: Optional[Number] = None
    best_side: list[int] = []
    t = min((v for v in range(n) if awake[v]), key=lambda v: (d[v], v))  # @line L3
    for _ in range(n - 1):  # @line L4
        queue = deque(v for v in range(n) if awake[v] and v != t and excess[v] > 0)
        it = [0] * n
        while queue:  # @line L5
            v = queue.popleft()
            while awake[v] and v != t and excess[v] > 0:
                if it[v] < len(adj[v]):
                    a = adj[v][it[v]]
                    w = head[a]
                    if res[a] > 0 and awake[w] and d[v] == d[w] + 1:  # @line L6
                        amount = min(excess[v], res[a])
                        push(a, amount)
                        if w != t and excess[w] > 0 and excess[w] <= amount:
                            queue.append(w)
                    else:
                        it[v] += 1
                    continue
                it[v] = 0
                if count[d[v]] == 1:  # @line L7
                    put_to_sleep([w for w in range(n) if awake[w] and d[w] >= d[v]])
                else:
                    labels = [d[head[a]] for a in adj[v] if res[a] > 0 and awake[head[a]]]
                    if not labels:  # @line L8
                        put_to_sleep([v])
                    else:
                        count[d[v]] -= 1  # @line L9
                        d[v] = 1 + min(labels)
                        count[d[v]] = count.get(d[v], 0) + 1
        value: Number = 0  # @line L10
        for u, v, cap in edges:
            if not awake[u] and awake[v]:
                value += cap
        side = [v for v in range(n) if not awake[v]]
        if on_phase is not None:
            on_phase(t, value, side)
        if best_value is None or value < best_value:
            best_value, best_side = value, side
        in_s[t] = True  # @line L11
        awake[t] = False
        count[d[t]] -= 1
        d[t] = n
        for a in adj[t]:  # @line L12
            if res[a] > 0 and not in_s[head[a]]:
                push(a, res[a])
        if not any(awake):  # @line L13
            if not dormant:
                break
            for w in dormant.pop():
                awake[w] = True
                count[d[w]] = count.get(d[w], 0) + 1
        t = min((v for v in range(n) if awake[v]), key=lambda v: (d[v], v))  # @line L14
    assert best_value is not None
    return best_value, best_side


def hao_orlin(
    n: int,
    edges: list[tuple[int, int, Number]],
    on_phase: Optional[Callable[[str, int, Number, list[int]], None]] = None,
) -> tuple[Number, list[int]]:
    """Minimum cut of a directed graph: the least c(X, V - X) over X with X != {}, V.

    The graph has the vertices 0 .. n-1 (n >= 2) and the directed edges (u, v, cap),
    cap >= 0 (int, Fraction or float). Parallel, antiparallel and zero-capacity edges
    are allowed; self-loops are ignored. For an undirected graph give both directions.
    Returns (value, X) with X the sorted source side. Two Hao-Orlin runs from vertex 0,
    one on the graph and one on its reverse, each with n - 1 sink phases sharing one
    push-relabel state. on_phase(run, sink, value, side) reports each phase, with run
    "forward" or "reverse" and side the source side found in that run's graph.
    """
    if n < 2:
        raise ValueError("need at least two vertices")
    for u, v, cap in edges:
        if cap < 0:
            raise ValueError("capacities must be nonnegative")
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("vertex out of range")
    fwd = None if on_phase is None else (lambda t, val, side: on_phase("forward", t, val, side))
    rev = None if on_phase is None else (lambda t, val, side: on_phase("reverse", t, val, side))
    v1, x1 = _rooted_min_cut(n, edges, 0, fwd)  # @line L15
    v2, x2 = _rooted_min_cut(n, [(v, u, c) for u, v, c in edges], 0, rev)
    if v2 < v1:
        return v2, sorted(set(range(n)) - set(x2))
    return v1, x1
