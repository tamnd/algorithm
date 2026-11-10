# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sidney-decomposition/. The authors are listed in prov/YXCAK6.jsonl.

"""Sidney decomposition for 1|prec|sum w_j C_j, and the 2-approximation that
runs the pieces in order (Chekuri and Motwani 1999; Margot, Queyranne and Wang 2003).

Jobs are 0 .. n-1 with p_j > 0 and w_j >= 0. A pair (i, j) in prec means that
job i must complete before job j starts. An initial set is a set of jobs that
contains every predecessor of each of its jobs.
"""

from collections import deque
from fractions import Fraction
from typing import Iterable, Sequence


def _max_closure(jobs: list[int], c: dict[int, Fraction], prec: list[tuple[int, int]]) -> set[int]:
    """An initial set I of `jobs` with the largest sum of c over I, by a minimum cut.

    Edges: s -> j with capacity c_j if c_j > 0, j -> t with capacity -c_j if c_j < 0,
    and j -> i with infinite capacity for each pair (i, j), so that a source side
    that holds j also holds i. The source side of a minimum cut is a maximum closure.
    """
    s, t = "s", "t"
    inf = sum(abs(v) for v in c.values()) + 1
    cap: dict = {}
    adj: dict = {s: set(), t: set()}
    for j in jobs:
        adj[j] = set()

    def add(u, v, x):
        cap[(u, v)] = cap.get((u, v), 0) + x
        cap.setdefault((v, u), 0)
        adj[u].add(v)
        adj[v].add(u)

    for j in jobs:
        if c[j] > 0:
            add(s, j, c[j])
        elif c[j] < 0:
            add(j, t, -c[j])
    inside = set(jobs)
    for i, j in prec:
        if i in inside and j in inside:
            add(j, i, inf)
    while True:  # Edmonds-Karp: augment along shortest paths
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v in adj[u]:
                if v not in parent and cap[(u, v)] > 0:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            return {v for v in parent if v != s}
        f, v = inf, t
        while parent[v] is not None:
            f = min(f, cap[(parent[v], v)])
            v = parent[v]
        v = t
        while parent[v] is not None:
            cap[(parent[v], v)] -= f
            cap[(v, parent[v])] += f
            v = parent[v]


def ratio(p: Sequence[int], w: Sequence[int], S: Iterable[int]) -> Fraction:
    S = list(S)
    return Fraction(sum(w[j] for j in S), sum(p[j] for j in S))


def max_ratio_initial_set(p, w, prec, jobs: list[int]) -> set[int]:
    """A nonempty initial set of `jobs` with the largest w(I)/p(I), by Dinkelbach's method."""
    S = set(jobs)
    while True:
        rho = ratio(p, w, S)
        c = {j: w[j] - rho * p[j] for j in jobs}
        I = _max_closure(jobs, c, prec)
        if sum(c[j] for j in I) <= 0:
            return S
        S = I  # ratio(I) > rho, so the loop ends after finitely many steps


def sidney_decomposition(p: Sequence[int], w: Sequence[int], prec: Sequence[tuple[int, int]]) -> list[list[int]]:
    """Pieces S_1, S_2, ...: each S_k is a max-ratio initial set of the jobs not yet taken."""
    n = len(p)
    if len(w) != n or any(x <= 0 for x in p) or any(x < 0 for x in w):
        raise ValueError("need p_j > 0 and w_j >= 0 for every job")
    prec = list(prec)
    rest = list(range(n))  # @line L1
    pieces = []
    while rest:  # @line L2
        S = max_ratio_initial_set(p, w, prec, rest)  # @line L3
        pieces.append(sorted(S))  # @line L4
        rest = [j for j in rest if j not in S]  # @line L5
    return pieces  # @line L6


def topological_order(jobs: list[int], prec) -> list[int]:
    """Kahn's algorithm on the order induced on `jobs`, smallest index first."""
    inside = set(jobs)
    indeg = {j: 0 for j in jobs}
    succ: dict[int, list[int]] = {j: [] for j in jobs}
    for i, j in prec:
        if i in inside and j in inside:
            indeg[j] += 1
            succ[i].append(j)
    ready = sorted(j for j in jobs if indeg[j] == 0)
    out = []
    while ready:
        j = ready.pop(0)
        out.append(j)
        for k in succ[j]:
            indeg[k] -= 1
            if indeg[k] == 0:
                ready.append(k)
        ready.sort()
    if len(out) != len(jobs):
        raise ValueError("the precedence pairs contain a cycle")
    return out


def sidney_order(p, w, prec) -> list[int]:
    """The pieces in order, each in some order that respects prec: a 2-approximation."""
    return [j for S in sidney_decomposition(p, w, prec) for j in topological_order(S, prec)]


def cost(p, w, order) -> int:
    t, s = 0, 0
    for j in order:
        t += p[j]
        s += w[j] * t
    return s
