# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flow-based-transcript-assembly/. The authors are listed in prov/9XQGWM.jsonl.

"""Transcript assembly by heaviest paths and max flow, in the style of StringTie.

The graph is a splice graph: a DAG on the nodes 0 to n - 1 with every edge
(u, v) having u < v. A fragment is a path of at least two nodes (the node path
of a read or of a read pair) with a weight, its number of reads. Fragments on
one node only are ignored here. The coverage W(v) of a node is the total
weight of the fragments that hold v.

Each round starts at the node of highest coverage, extends a path toward the
source and then toward the sink with the neighbour that has the most
compatible fragment weight, and computes the abundance of the path as a
maximum flow through the fragments that the path explains. The flow on each
fragment is subtracted, and the loop stops when no node has coverage c_min.

What this leaves out, compared with StringTie: coverage per base instead of
read counts, the bias factor on node capacities, super-reads from read pairs,
the filters on short and weak transcripts, and the strand and locus logic.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Sequence, Tuple

Path = Tuple[int, ...]


def edmonds_karp(n: int, cap: Dict[Tuple[int, int], float], s: int, t: int):
    """Maximum flow by shortest augmenting paths. Returns (value, flow on each edge of cap).

    The network must have no pair of opposite edges (u, v) and (v, u); N(P) has none.
    """
    res: Dict[int, Dict[int, float]] = {u: {} for u in range(n)}
    for (u, v), c in cap.items():
        if (v, u) in cap:
            raise ValueError("opposite edges are not supported")
        res[u][v] = c
        res[v][u] = 0
    value = 0
    while True:
        parent = {s: s}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v, c in res[u].items():
                if c > 1e-12 and v not in parent:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            break
        b, v = float("inf"), t
        while v != s:
            b = min(b, res[parent[v]][v])
            v = parent[v]
        v = t
        while v != s:
            u = parent[v]
            res[u][v] -= b
            res[v][u] += b
            v = u
        value += b
    return value, {(u, v): c - res[u][v] for (u, v), c in cap.items()}


def _part(f: Path, lo: int, hi: int) -> Path:
    return tuple(x for x in f if lo <= x <= hi)


def compatible(f: Path, q: Path) -> bool:
    """f and q overlap and agree on the node range they share, so one path can hold both."""
    lo, hi = max(f[0], q[0]), min(f[-1], q[-1])
    part = _part(f, lo, hi)
    return bool(part) and part == _part(q, lo, hi)


def _explained(f: Path, p: Path) -> int:
    """The index of f in p if f is a contiguous part of p, else -1."""
    if f[0] not in p:
        return -1
    i = p.index(f[0])
    return i if p[i:i + len(f)] == f else -1


def path_flow(p: Path, weight: Dict[Path, float]):
    """The max flow of the network N(p). Returns (value, flow of each explained fragment)."""
    m = len(p)
    big = sum(weight.values()) + 1
    explained = {}
    for f, w in weight.items():
        i = _explained(f, p)
        if w > 0 and i >= 0:
            explained[f] = (i, i + len(f) - 1)
    cap: Dict[Tuple[int, int], float] = {}
    for i, v in enumerate(p):
        c = sum(weight[f] for f, (a, b) in explained.items() if a <= i <= b)
        cap[(2 + 2 * i, 3 + 2 * i)] = c
    for f, (a, b) in explained.items():
        cap[(3 + 2 * a, 2 + 2 * b)] = weight[f]
    cap[(0, 2)] = big
    cap[(3 + 2 * (m - 1), 1)] = big
    value, flow = edmonds_karp(2 + 2 * m, cap, 0, 1)
    return value, {f: flow[(3 + 2 * a, 2 + 2 * b)] for f, (a, b) in explained.items()}


def assemble(n: int, edges: Sequence[Tuple[int, int]], fragments: Dict[Sequence[int], float],
             c_min: float = 1.0) -> List[Tuple[List[int], float]]:
    """Return a list of (transcript path, abundance in reads)."""
    succ: List[List[int]] = [[] for _ in range(n)]
    pred: List[List[int]] = [[] for _ in range(n)]
    for u, v in sorted(set(edges)):
        if not u < v:
            raise ValueError("edges must go from a smaller to a larger node id")
        succ[u].append(v)
        pred[v].append(u)
    weight: Dict[Path, float] = {}
    for f, w in fragments.items():
        f = tuple(f)
        if any(v not in succ[u] for u, v in zip(f, f[1:])):
            raise ValueError("each fragment must be a path of the graph")
        if len(f) >= 2 and w > 0:
            weight[f] = weight.get(f, 0) + w

    def coverage(v: int) -> float:
        return sum(w for f, w in weight.items() if v in f)

    def score(u: int, q: Path) -> float:
        return sum(w for f, w in weight.items() if w > 0 and u in f and compatible(f, q))

    out: List[Tuple[List[int], float]] = []  # @line L1
    while n and max(coverage(v) for v in range(n)) >= c_min:  # @line L2
        cov = [coverage(v) for v in range(n)]
        start = max(range(n), key=lambda v: (cov[v], -v))  # @line L3
        p: Path = (start,)  # @line L4
        while True:  # @line L5
            best = max(((score(u, (u,) + p), -u) for u in pred[p[0]]), default=(0, 0))
            if best[0] <= 0:
                break
            p = (-best[1],) + p
        while True:  # @line L6
            best = max(((score(u, p + (u,)), -u) for u in succ[p[-1]]), default=(0, 0))
            if best[0] <= 0:
                break
            p = p + (-best[1],)
        value, gflow = path_flow(p, weight)  # @line L7
        if value >= c_min:  # @line L8
            out.append((list(p), value))  # @line L9
            for f, g in gflow.items():
                weight[f] -= g
        else:
            for f in weight:  # @line L10
                if start in f:
                    weight[f] = 0
    return out  # @line L11
