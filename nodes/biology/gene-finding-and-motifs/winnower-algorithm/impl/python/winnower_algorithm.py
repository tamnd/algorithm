# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winnower-algorithm/. The authors are listed in prov/561KFN.jsonl.
"""WINNOWER of Pevzner and Sze (2000) in its basic form: build the n-partite
graph of windows joined when their Hamming distance is at most 2d, remove
every edge that has no common neighbor in some other sequence until no such
edge is left, and list the n-cliques of what remains.

Positions are 0-based in this code; the page numbers them from 1. A vertex is
a pair (sequence index, start).
"""

from typing import Dict, List, NamedTuple, Sequence, Set, Tuple

from bioseq import DNA, hamming

Vertex = Tuple[int, int]


class WinnowerResult(NamedTuple):
    """Edge counts before and after, the number of passes of the pruning loop,
    the surviving edges, and the n-cliques as tuples of 0-based starts."""

    edges_before: int
    edges_after: int
    passes: int
    edges: frozenset
    cliques: Tuple[Tuple[int, ...], ...]


def build_graph(seqs: Sequence[str], L: int, d: int) -> Dict[Vertex, List[Set[Vertex]]]:
    """adj[v][p] = the windows of sequence p within Hamming distance 2d of v (p != part of v)."""
    n = len(seqs)
    wins = [[(i, q) for q in range(len(s) - L + 1)] for i, s in enumerate(seqs)]
    adj = {v: [set() for _ in range(n)] for part in wins for v in part}
    for i in range(n):
        for k in range(i + 1, n):
            for u in wins[i]:
                a = seqs[i][u[1]:u[1] + L]
                for v in wins[k]:
                    if hamming(a, seqs[k][v[1]:v[1] + L]) <= 2 * d:
                        adj[u][k].add(v)
                        adj[v][i].add(u)
    return adj


def edge_set(adj) -> frozenset:
    return frozenset((u, v) for u in adj for part in adj[u] for v in part if u < v)


def winnow(adj, n: int) -> int:
    """Remove edges with no common neighbor in some other part, in place, until
    none is left. Returns the number of passes over the edges."""
    passes = 0
    while True:  # @line L2
        passes += 1
        removed = False
        for u, v in sorted(edge_set(adj)):  # @line L3
            if v not in adj[u][v[0]]:
                continue
            if any(adj[u][p].isdisjoint(adj[v][p]) for p in range(n) if p != u[0] and p != v[0]):  # @line L4
                adj[u][v[0]].discard(v)  # @line L5
                adj[v][u[0]].discard(u)
                removed = True
        if not removed:  # @line L6
            return passes


def cliques(adj, n: int) -> List[Tuple[int, ...]]:
    """All n-cliques with one vertex per part, by backtracking in the order of the parts."""
    out = []

    def extend(chosen: List[Vertex]) -> None:
        p = len(chosen)
        if p == n:
            out.append(tuple(q for _, q in chosen))
            return
        cand = set(adj[chosen[0]][p])
        for w in chosen[1:]:
            cand &= adj[w][p]
        for v in sorted(cand):
            extend(chosen + [v])

    for v in sorted(x for x in adj if x[0] == 0):
        extend([v])
    return out


def winnower(seqs: Sequence[str], L: int, d: int) -> WinnowerResult:
    """Run WINNOWER: build the graph, prune edges that are not extendable, list the n-cliques.

    Cost: O(n^2 W^2 L) to build the graph; each pass of the pruning loop costs
    O(|E| n W) with set intersections; listing the cliques is exponential in
    the worst case.
    """
    if L <= 0 or d < 0:
        raise ValueError("L must be positive and d at least 0")
    if len(seqs) < 2:
        raise ValueError("need at least two sequences")
    for s in seqs:
        if len(s) < L or set(s) - set(DNA):
            raise ValueError("sequences must be over ACGT with length at least L")
    n = len(seqs)
    adj = build_graph(seqs, L, d)  # @line L1
    before = len(edge_set(adj))
    passes = winnow(adj, n)
    found = cliques(adj, n)  # @line L7
    edges = edge_set(adj)
    return WinnowerResult(before, len(edges), passes, edges, tuple(found))  # @line L8


def consensus(windows: Sequence[str]) -> str:
    """The most common letter of each column (the first in ACGT order on a tie)."""
    return "".join(max(DNA, key=lambda a: (col.count(a), -DNA.index(a))) for col in zip(*windows))
