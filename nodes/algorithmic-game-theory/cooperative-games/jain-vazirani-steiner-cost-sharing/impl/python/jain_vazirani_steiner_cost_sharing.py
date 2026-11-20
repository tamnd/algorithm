# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jain-vazirani-steiner-cost-sharing/. The authors are listed in prov/F0QV3E.jsonl.
"""Jain-Vazirani cost sharing for Steiner trees, in its threshold form.

The input is an undirected graph with nonnegative edge costs, a root r and a set S of
terminals (the players). Let d be the shortest path metric of the graph. Grow a time t from 0.
At time t, two points of S + {r} are joined when d(u, v) <= t. While the component of a
terminal does not contain the root, the terminal pays 1/|K| per unit of time, where K is its
component. The shares add up to the cost of a minimum spanning tree on S + {r} under d. This
is at least the optimal Steiner tree cost and at most twice it, and no share rises when S grows.

The same shares come out of the primal-dual algorithm of Jain and Vazirani (2001) on the
bidirected metric closure, where each active component raises its dual at rate 1 and splits
the increase equally among its terminals.
"""

from fractions import Fraction
from itertools import combinations


def metric_closure(n, edges):
    """All-pairs shortest path costs by Floyd-Warshall; None means unreachable."""
    d = [[None] * n for _ in range(n)]
    for v in range(n):
        d[v][v] = Fraction(0)
    for u, v, w in edges:
        w = Fraction(w)
        if d[u][v] is None or w < d[u][v]:
            d[u][v] = d[v][u] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik is None:
                continue
            di = d[i]
            for j in range(n):
                if dk[j] is not None and (di[j] is None or dik + dk[j] < di[j]):
                    di[j] = dik + dk[j]
    return d


def _check(n, edges, root, terminals):
    if not 0 <= root < n:
        raise ValueError("root out of range")
    for u, v, w in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge end out of range")
        if w < 0:
            raise ValueError("negative edge cost")
    terms = sorted(set(terminals))
    for i in terms:
        if not 0 <= i < n:
            raise ValueError("terminal out of range")
        if i == root:
            raise ValueError("the root is not a player")
    return terms


def jv_cost_shares(n, edges, root, terminals):
    """Return {terminal: share} as Fractions. Vertices are 0 .. n-1; edges are (u, v, cost)."""
    terminals = _check(n, edges, root, terminals)
    d = metric_closure(n, edges)  # @line L1
    points = [root] + terminals
    for p in terminals:
        if d[root][p] is None:
            raise ValueError("terminal not connected to the root")
    pairs = sorted((d[u][v], u, v) for u, v in combinations(points, 2))  # @line L2
    comp = {p: p for p in points}
    members = {p: [p] for p in points}
    share = {i: Fraction(0) for i in terminals}
    t = Fraction(0)  # @line L3
    for w, u, v in pairs:  # @line L4
        cu, cv = comp[u], comp[v]
        if cu == cv:
            continue
        for c, mem in members.items():  # @line L5
            if c != comp[root]:
                for i in mem:
                    share[i] += (w - t) / len(mem)
        t = w  # @line L6
        if len(members[cu]) < len(members[cv]):
            cu, cv = cv, cu
        for p in members[cv]:
            comp[p] = cu
        members[cu].extend(members.pop(cv))
    return share  # @line L7


def mst_cost(d, points):
    """Cost of a minimum spanning tree on points under the metric d (Prim, O(k^2))."""
    points = list(points)
    if len(points) <= 1:
        return Fraction(0)
    best = {p: d[points[0]][p] for p in points[1:]}
    total = Fraction(0)
    while best:
        p = min(best, key=lambda q: (best[q], q))
        total += best.pop(p)
        for q in best:
            if d[p][q] < best[q]:
                best[q] = d[p][q]
    return total
