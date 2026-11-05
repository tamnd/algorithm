# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hits-algorithm/. The authors are listed in prov/AJD47V.jsonl.

import math


def _normalize(x: list[float]) -> list[float]:
    s = math.sqrt(sum(v * v for v in x))
    return [v / s for v in x]


def hits_algorithm(
    n: int,
    arcs: list[tuple[int, int]],
    eps: float = 1e-12,
    max_rounds: int = 10_000,
) -> tuple[list[float], list[float]]:
    """Return (authority, hub) scores of a directed graph, each of Euclidean norm 1.

    The graph has nodes 0 .. n-1 and the arcs (u, v) of the list; a repeated arc
    counts as a weight. Each round computes a = A^T h and h = A a, then scales both
    to norm 1, as Kleinberg's I and O operations. The loop stops when the change
    of both vectors is at most eps, or after max_rounds rounds. A graph with no
    arcs gives two zero vectors.
    Time O(n + m) per round, extra space O(n).
    """
    a = [0.0] * n  # @line L1
    h = [1.0] * n
    h_scaled = _normalize(h) if n else []
    for _ in range(max_rounds):  # @line L2
        a_new = [0.0] * n
        for u, v in arcs:  # @line L3
            a_new[v] += h[u]
        h_new = [0.0] * n
        for u, v in arcs:  # @line L4
            h_new[u] += a_new[v]
        if not any(a_new):  # @line L5
            return a_new, h_new
        a_new = _normalize(a_new)  # @line L6
        h_new = _normalize(h_new)
        delta = math.dist(a_new, a) + math.dist(h_new, h_scaled)  # @line L7
        a, h, h_scaled = a_new, h_new, h_new  # @line L8
        if delta <= eps:  # @line L9
            return a, h
    return a, h  # @line L10
