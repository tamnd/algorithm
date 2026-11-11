# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quorum-intersection/. The authors are listed in prov/6YJE35.jsonl.

"""Quorum systems on a small universe {0, ..., n-1}: intersection checks,
threshold and grid systems, load under a strategy, and failure probability.

A quorum is a frozenset of servers. Everything here is exact and brute force,
so keep n small (at most about 16).
"""

from fractions import Fraction
from itertools import combinations
from typing import Iterable


def threshold(n: int, q: int) -> list[frozenset]:
    """All sets of exactly q servers (larger sets add nothing for intersection)."""
    return [frozenset(c) for c in combinations(range(n), q)]


def min_intersection(a: Iterable[frozenset], b: Iterable[frozenset]) -> int:
    b = list(b)
    return min(len(x & y) for x in a for y in b)


def all_meet(a: Iterable[frozenset], b: Iterable[frozenset], k: int = 1) -> bool:
    """True if every quorum of a meets every quorum of b in at least k servers."""
    return min_intersection(a, b) >= k


def counting_bound(n: int, r: int, w: int) -> int:
    """|R & W| >= r + w - n for any r-set and w-set of an n-set."""
    return max(0, r + w - n)


def grid(k: int) -> list[frozenset]:
    """k x k grid; server i*k + j sits in row i, column j. A quorum is one full
    row and one full column."""
    out = []
    for i in range(k):
        for j in range(k):
            row = {i * k + c for c in range(k)}
            col = {r * k + j for r in range(k)}
            out.append(frozenset(row | col))
    return out


def load(n: int, quorums: list[frozenset], weights: list[Fraction] | None = None) -> Fraction:
    """The load of a strategy: the largest probability that a server is used,
    when a quorum is picked with the given weights (uniform by default).
    The load of the system is the minimum over strategies; for the symmetric
    systems here the uniform strategy reaches it."""
    if weights is None:
        weights = [Fraction(1, len(quorums))] * len(quorums)
    use = [Fraction(0)] * n
    for q, p in zip(quorums, weights):
        for s in q:
            use[s] += p
    return max(use)


def naor_wool_lower_bound(n: int, quorums: list[frozenset]) -> Fraction:
    """Naor and Wool: load >= max(1/c, c/n), c the size of the smallest quorum."""
    c = min(len(q) for q in quorums)
    return max(Fraction(1, c), Fraction(c, n))


def failure_probability(n: int, quorums: list[frozenset], p: Fraction) -> Fraction:
    """The probability that every quorum holds a failed server, when each server
    fails on its own with probability p. Exact by enumeration over 2^n sets."""
    total = Fraction(0)
    masks = [sum(1 << s for s in q) for q in quorums]
    for alive in range(1 << n):
        if any(m & alive == m for m in masks):
            continue
        up = bin(alive).count("1")
        total += (1 - p) ** up * p ** (n - up)
    return total


def masking_threshold(n: int, f: int) -> int | None:
    """The smallest q with 2q - n >= 2f + 1 (any two q-sets share 2f + 1 servers)
    and q <= n - f (a quorum of correct servers exists), or None."""
    for q in range(n + 1):
        if 2 * q - n >= 2 * f + 1 and q <= n - f:
            return q
    return None
