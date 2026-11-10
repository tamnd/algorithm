# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-dfs/. The authors are listed in prov/A3D0QP.jsonl.

"""Lexicographic DFS by synchronous path relaxation, simulated one PRAM round at a time.

Each vertex v holds a label P[v]: a sequence of edge indices that spells a walk
from s to v. In one round, every vertex v other than s takes the
lexicographic minimum of its old label and the labels P[u] + (i,) of its
in-edges (u, v), where v is the i-th entry of adj[u]. All reads see the
labels from before the round. At the fixed point, P[v] is the path from s to v
in the DFS tree that the sequential DFS builds when it scans each adjacency
list in order, and sorting by P gives the DFS preorder.

Precondition: adj is a list of adjacency lists over 0 .. n - 1 (directed; an
undirected graph lists each edge at both ends) and 0 <= s < n.
Cost: h + 1 rounds, where h is the height of the DFS tree. A round costs
O(m h) work and O(log^2 n) span (O(log n) span for one comparison, and a
tournament of O(log n) levels over the in-edges). The final sort costs
O(n h log n) work and O(log^2 n) span.
"""


class Cost:
    """Counters for work, span and rounds."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0


def log2_ceil(k: int) -> int:
    """The number of tree levels that a reduction over k items needs."""
    return max(1, (k - 1).bit_length()) if k > 1 else 1


def parallel_dfs(
    adj: list[list[int]], s: int, cost: Cost | None = None
) -> tuple[list[int], list[int | None]]:
    """Return (preorder, parent) of the lexicographic DFS from s."""
    c = cost if cost is not None else Cost()
    n = len(adj)
    radj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u in range(n):
        for i, v in enumerate(adj[u]):
            radj[v].append((u, i))
    P: list[tuple[int, ...] | None] = [None] * n  # @line L1
    parent: list[int | None] = [None] * n
    P[s], parent[s] = (), s  # @line L2
    changed = True
    while changed:  # @line L3
        c.rounds += 1
        Q = P[:]
        Qpar = parent[:]
        longest = 0
        for v in range(n):  # @line L4
            if v == s:
                continue
            for u, i in radj[v]:  # @line L5
                if P[u] is None:
                    continue
                cand = P[u] + (i,)  # the old label of u, read before any write of this round
                c.work += len(cand)
                longest = max(longest, len(cand))
                if Q[v] is None or cand < Q[v]:
                    Q[v], Qpar[v] = cand, u
        changed = Q != P  # @line L6
        P, parent = Q, Qpar  # @line L7
        c.work += 2 * n
        c.span += log2_ceil(longest + 1) * log2_ceil(n + 1) + log2_ceil(n + 1) + 2
    reached = [v for v in range(n) if P[v] is not None]  # @line L8
    order = sorted(reached, key=lambda v: P[v])  # @line L9
    k = len(reached)
    c.work += k * log2_ceil(k + 1) * (max(len(P[v]) for v in reached) + 1)
    c.span += log2_ceil(k + 1) * log2_ceil(n + 1)
    return order, parent  # @line L10
