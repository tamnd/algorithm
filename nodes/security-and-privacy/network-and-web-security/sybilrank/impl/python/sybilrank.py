# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sybilrank/. The authors are listed in prov/S4HXC8.jsonl.

"""SybilRank (Cao, Sirivianos, Yang and Pregueiro, NSDI 2012, Section 4).

Early-terminated power iteration of trust from honest seeds on an undirected
social graph, then a ranking by degree-normalized trust. The graph is an
adjacency dict of a small synthetic graph; no real account data is used.
"""

from math import ceil, log2
from typing import Hashable, Mapping, Sequence

Node = Hashable


def default_iterations(n: int) -> int:
    """w = ceil(log2 n), the O(log n) early termination of Section 4.2."""
    return max(1, ceil(log2(n))) if n > 1 else 1


def propagate(adj: Mapping[Node, Sequence[Node]], seeds: Sequence[Node], total: float, w: int) -> dict[Node, float]:
    """Trust after w power iterations, starting with total split evenly on the seeds.

    Precondition: every node has at least one neighbor, adj is symmetric, and
    seeds is a nonempty list of distinct nodes. Cost: O(w (n + m)) time and
    O(n) extra space for n nodes and m edges.
    """
    share = total / len(seeds)
    seed_set = set(seeds)
    trust = {v: (share if v in seed_set else 0.0) for v in adj}  # @line L1
    for _ in range(w):  # @line L2
        nxt = {v: 0.0 for v in adj}  # @line L3
        for u, nbrs in adj.items():  # @line L4
            give = trust[u] / len(nbrs)
            for v in nbrs:
                nxt[v] += give
        trust = nxt  # @line L5
    return trust


def rank(adj: Mapping[Node, Sequence[Node]], trust: Mapping[Node, float]) -> list[Node]:
    """Nodes ordered by degree-normalized trust, lowest (most suspect) first.

    Ties are broken by the string form of the node, so the order is
    deterministic. Cost: O(n log n).
    """
    score = {v: trust[v] / len(adj[v]) for v in adj}  # @line L6
    return sorted(adj, key=lambda v: (score[v], str(v)))  # @line L7


def sybilrank(adj: Mapping[Node, Sequence[Node]], seeds: Sequence[Node], total: float = 1.0, w: int | None = None) -> list[Node]:
    """Propagate trust from the seeds for w iterations (default ceil(log2 n)) and rank."""
    if w is None:
        w = default_iterations(len(adj))
    return rank(adj, propagate(adj, seeds, total, w))
