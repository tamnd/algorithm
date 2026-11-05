# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carraghan-pardalos-algorithm/. The authors are listed in prov/F3SXV2.jsonl.

from collections.abc import Sequence


def carraghan_pardalos_algorithm(adj: Sequence[Sequence[int]]) -> list[int]:
    """Return a maximum clique of a simple undirected graph, as a sorted list.

    adj[v] lists the neighbours of v (vertices 0 .. n-1, each edge in both lists,
    no self-loops). Vertices are ordered by non-decreasing degree, ties by index.
    The search takes the candidates in this order and cuts a branch as soon as
    the current clique plus all remaining candidates cannot beat the best clique.
    Among several maximum cliques it returns the first one found.
    """
    n = len(adj)
    nb = [set(adj[v]) for v in range(n)]
    order = sorted(range(n), key=lambda v: (len(nb[v]), v))  # @line L1
    best: list[int] = []  # @line L2

    def expand(c: list[int], p: list[int]) -> None:
        nonlocal best
        p = list(p)
        while p:  # @line L5
            if len(c) + len(p) <= len(best):  # @line L6
                return
            v = p.pop(0)  # @line L7
            q = [w for w in p if w in nb[v]]  # @line L8
            if not q:  # @line L9
                if len(c) + 1 > len(best):
                    best = c + [v]
            else:
                expand(c + [v], q)  # @line L10

    expand([], order)  # @line L3
    return sorted(best)  # @line L4
