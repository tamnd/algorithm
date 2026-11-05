# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bron-kerbosch/. The authors are listed in prov/SFJ221.jsonl.

from collections.abc import Sequence


def bron_kerbosch(adj: Sequence[Sequence[int]]) -> list[list[int]]:
    """List all maximal cliques of a simple undirected graph (Bron-Kerbosch with pivot).

    adj[v] lists the neighbours of v (vertices 0 .. n-1, each edge in both lists,
    no self-loops). Uses the pivot rule of Tomita, Tanaka and Takahashi: the pivot
    u in P | X has the most neighbours in P (ties to the smallest index), and only
    the vertices of P outside N(u) are branched on, in increasing order.
    Returns each maximal clique once, as a sorted list, in the order found.
    The empty graph has one maximal clique, the empty set.
    Time O(3^(n/3)) set operations of O(n) each in the worst case.
    """
    n = len(adj)
    nb = [set(adj[v]) for v in range(n)]
    out: list[list[int]] = []  # @line L1

    def expand(r: list[int], p: set[int], x: set[int]) -> None:
        if not p and not x:  # @line L4
            out.append(sorted(r))
            return
        u = max(sorted(p | x), key=lambda w: len(p & nb[w]))  # @line L5
        for v in sorted(p - nb[u]):  # @line L6
            expand(r + [v], p & nb[v], x & nb[v])  # @line L7
            p.discard(v)  # @line L8
            x.add(v)

    expand([], set(range(n)), set())  # @line L2
    return out  # @line L3
