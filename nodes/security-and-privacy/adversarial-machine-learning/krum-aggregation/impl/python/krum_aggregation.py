# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/krum-aggregation/. The authors are listed in prov/NQC1A8.jsonl.

"""Krum, the Byzantine-robust aggregation rule of Blanchard, El Mhamdi, Guerraoui and Stainer (2017).

The input is a list of n update vectors, of which at most f may be Byzantine. The tests
build every update from a fixed seed; nothing here talks to a client or a network.
"""

import math
from typing import Sequence

Vector = list[float]


def squared_distance(u: Sequence[float], v: Sequence[float]) -> float:
    """The squared Euclidean distance ||u - v||^2, correctly rounded by math.fsum. Cost O(d)."""
    return math.fsum((a - b) * (a - b) for a, b in zip(u, v, strict=True))


def check_sizes(n: int, f: int) -> None:
    """Raise ValueError unless f >= 0 and n > 2 f + 2, the condition under which Krum is defined."""
    if f < 0 or n <= 2 * f + 2:
        raise ValueError("Krum needs f >= 0 and n > 2 f + 2")


def krum_scores(updates: Sequence[Sequence[float]], f: int) -> list[float]:
    """The score s(i): the sum of the n - f - 2 smallest squared distances from V_i to the other updates.

    Precondition: n > 2 f + 2 and all updates have the same length d.
    Cost O(n^2 (d + log n)) time and O(n) extra space.
    """
    n = len(updates)
    check_sizes(n, f)
    m = n - f - 2
    scores: list[float] = []
    for i in range(n):
        dists = sorted(squared_distance(updates[i], updates[j]) for j in range(n) if j != i)
        scores.append(math.fsum(dists[:m]))
    return scores


def krum_index(updates: Sequence[Sequence[float]], f: int) -> int:
    """The index i* of the update with the smallest score; ties go to the smallest index.

    Precondition: n > 2 f + 2 and all updates have the same length d.
    Cost O(n^2 (d + log n)) time and O(n) extra space.
    """
    n = len(updates)
    if f < 0 or n <= 2 * f + 2:  # @line L1
        raise ValueError("Krum needs f >= 0 and n > 2 f + 2")
    m = n - f - 2
    best, best_score = -1, math.inf
    for i in range(n):  # @line L2
        dists = [squared_distance(updates[i], updates[j]) for j in range(n) if j != i]  # @line L3
        dists.sort()  # @line L4
        score = math.fsum(dists[:m])  # @line L5
        if score < best_score:  # @line L6
            best, best_score = i, score
    return best  # @line L7


def krum(updates: Sequence[Sequence[float]], f: int) -> Vector:
    """The update V_{i*} chosen by Krum, as a new list. Same precondition and cost as krum_index."""
    return list(updates[krum_index(updates, f)])


def multi_krum_indices(updates: Sequence[Sequence[float]], f: int, m: int) -> list[int]:
    """The m-Krum selection of arXiv:1703.02757v1, Section 6: pick by Krum, remove, repeat m times.

    Returns the original indices in the order they were picked. Precondition: 1 <= m and
    every round is valid, that is n - m + 1 > 2 f + 2. Cost O(m n^2 (d + log n)).
    """
    n = len(updates)
    if m < 1 or n - m + 1 <= 2 * f + 2 or f < 0:
        raise ValueError("m-Krum needs m >= 1 and n - m + 1 > 2 f + 2")
    left = list(range(n))
    picked: list[int] = []
    for _ in range(m):
        k = krum_index([updates[i] for i in left], f)
        picked.append(left.pop(k))
    return picked


def multi_krum(updates: Sequence[Sequence[float]], f: int, m: int) -> Vector:
    """The mean of the m updates chosen by multi_krum_indices. Same precondition; cost O(m n^2 (d + log n))."""
    chosen = multi_krum_indices(updates, f, m)
    d = len(updates[0])
    return [math.fsum(updates[i][j] for i in chosen) / m for j in range(d)]


def average(updates: Sequence[Sequence[float]]) -> Vector:
    """The plain coordinatewise mean, the rule that one Byzantine update can move anywhere. Cost O(n d)."""
    n = len(updates)
    return [math.fsum(u[j] for u in updates) / n for j in range(len(updates[0]))]
