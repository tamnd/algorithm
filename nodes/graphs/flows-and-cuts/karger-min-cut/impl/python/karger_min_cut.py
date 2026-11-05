# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karger-min-cut/. The authors are listed in prov/981JCR.jsonl.

import random


def _find(parent: list[int], x: int) -> int:
    """Root of x in the union-find forest, with path halving."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def contract(n: int, edges: list[tuple[int, int]], rng: random.Random) -> tuple[set[int], int]:
    """One run of random contraction on an undirected multigraph.

    Vertices are 0 .. n-1 with n >= 2; edges is a list of pairs, where a
    repeated pair is a parallel edge and a pair (v, v) is a self-loop that is
    ignored. Returns (S, k): S is the side of the final cut that holds vertex 0,
    and k is the number of edges with one end in S and one end outside it.
    Time O(m alpha(n)) after an O(m) shuffle.
    """
    parent = list(range(n))  # @line L6
    comps = n
    order = list(edges)  # @line L7
    rng.shuffle(order)
    for u, v in order:  # @line L8
        if comps <= 2:
            break
        ru, rv = _find(parent, u), _find(parent, v)
        if ru != rv:  # @line L9
            parent[ru] = rv
            comps -= 1
    root = _find(parent, 0)  # @line L10
    side = {x for x in range(n) if _find(parent, x) == root}
    k = sum(1 for u, v in edges if (u in side) != (v in side))  # @line L11
    return side, k  # @line L12


def karger_min_cut(n: int, edges: list[tuple[int, int]], trials: int,
                   rng: random.Random | None = None) -> tuple[int, set[int]]:
    """Karger's algorithm: the best cut found by `trials` runs of contract.

    The graph is undirected and unweighted (parallel edges count separately).
    Returns (k, S) where S holds vertex 0 and k is the number of edges that
    cross S. The value k is always a real cut value, so k >= the minimum cut;
    it equals the minimum with probability at least 1 - (1 - 2/(n(n-1)))^trials.
    Requires n >= 2 and trials >= 1. Time O(trials * m alpha(n)).
    """
    if n < 2 or trials < 1:
        raise ValueError("need n >= 2 and trials >= 1")
    rng = rng or random.Random()
    best, best_side = -1, set()  # @line L1
    for _ in range(trials):  # @line L2
        side, k = contract(n, edges, rng)  # @line L3
        if best < 0 or k < best:  # @line L4
            best, best_side = k, side
    return best, best_side  # @line L5
