# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anf-algorithm/. The authors are listed in prov/MDNVAV.jsonl.

import random

PHI = 0.77351  # the Flajolet-Martin correction constant


def random_ranks(n: int, r: int, seed: int) -> list[list[int]]:
    """For each vertex and each of r copies, a bit index i with probability 2^-(i+1)."""
    rng = random.Random(seed)
    ranks: list[list[int]] = []
    for _ in range(n):
        row = []
        for _ in range(r):
            i = 0
            while rng.random() < 0.5 and i < 62:
                i += 1
            row.append(i)
        ranks.append(row)
    return ranks


def lowest_zero(mask: int) -> int:
    """The index of the lowest bit of mask that is 0."""
    return ((mask + 1) & ~mask).bit_length() - 1


def fm_estimate(masks: list[int]) -> float:
    """The Flajolet-Martin estimate of a set size from r bitmasks of the set."""
    mean = sum(lowest_zero(x) for x in masks) / len(masks)
    return 2.0 ** mean / PHI


def anf_algorithm(adj: list[list[int]], h_max: int, ranks: list[list[int]]) -> tuple[list[float], list[list[int]]]:
    """Estimate the neighbourhood function N(0), ..., N(h_max) of a graph.

    adj[v] lists the out-neighbours of v (both directions for an undirected graph);
    N(h) is the number of ordered pairs (v, u) with u reachable from v by at most h
    arcs, v = u included. ranks[v][j] is the random bit of v in copy j (see
    random_ranks). Returns the estimates and the final bitmasks of each vertex.
    Time O(h_max * r * (n + m)), space O(n * r) machine words.
    """
    n = len(adj)
    r = len(ranks[0]) if n else 0
    masks = [[1 << ranks[v][j] for j in range(r)] for v in range(n)]  # @line L1
    est = [sum(fm_estimate(masks[v]) for v in range(n))]  # @line L2
    for _ in range(h_max):  # @line L3
        new = [list(masks[v]) for v in range(n)]  # @line L4
        for v in range(n):  # @line L5
            row = new[v]
            for u in adj[v]:
                other = masks[u]
                for j in range(r):
                    row[j] |= other[j]
        masks = new  # @line L6
        est.append(sum(fm_estimate(masks[v]) for v in range(n)))  # @line L7
    return est, masks  # @line L8
