# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smalldb-mechanism/. The authors are listed in prov/3V0287.jsonl.
"""The SmallDB mechanism of Blum, Ligett and Roth (2008), in the form of
Dwork and Roth (2014, Algorithm 4), for a tiny universe.

The data is a histogram x over a universe X of size U, with n records, and
n is public. A query is a 0-1 vector f over X, and its normalized answer is
f(x) = (1/n) sum_j f[j] x[j], the fraction of records it counts. The
mechanism picks, with the exponential mechanism, a database y of only
m = ceil(ln |Q| / alpha^2) records whose answers are close to those of x.
Neighbors replace one record by another, so each f(x) moves by at most 1/n.

The mechanism lists every database of m records, so its cost is about
U^m. That is the point of the method for theory and the reason it is not
used at scale. The code uses random.Random so that the tests can be
repeated. A real release needs a cryptographic source of randomness and
exact sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).
"""

from __future__ import annotations

import math
import random
from typing import Sequence


def small_size(alpha: float, num_queries: int) -> int:
    """The size m = ceil(ln |Q| / alpha^2) of the small databases, at least 1. Precondition: alpha > 0."""
    if alpha <= 0:
        raise ValueError("alpha must be positive")
    return max(1, math.ceil(math.log(max(num_queries, 1)) / (alpha * alpha)))


def compositions(m: int, U: int) -> list[tuple[int, ...]]:
    """All histograms of m records over U cells, that is all U-tuples of non-negative integers with sum m.

    There are C(m + U - 1, U - 1) of them. Cost: linear in that number times U.
    """
    if U == 1:
        return [(m,)]
    out = []
    for first in range(m, -1, -1):
        for rest in compositions(m - first, U - 1):
            out.append((first,) + rest)
    return out


def answer(f: Sequence[int], hist: Sequence[int]) -> float:
    """The normalized answer of the counting query f on a histogram: the fraction of records it counts."""
    total = sum(hist)
    return sum(w * h for w, h in zip(f, hist)) / total


def utility(x: Sequence[int], y: Sequence[int], queries: Sequence[Sequence[int]]) -> float:
    """u(x, y) = -max over f of |f(x) - f(y)|. Its sensitivity in x is 1/n under replace. Cost: O(|Q| U)."""
    return -max(abs(answer(f, x) - answer(f, y)) for f in queries)


def smalldb_pmf(
    x: Sequence[int],
    queries: Sequence[Sequence[int]],
    epsilon: float,
    m: int,
) -> dict[tuple[int, ...], float]:
    """The exact output distribution of SmallDB over the databases of m records.

    P(y) is proportional to exp(epsilon * u(x, y) / (2 * (1/n))).
    Precondition: epsilon > 0, n = sum(x) >= 1, at least one query.
    Cost: O(|R| |Q| U) with |R| = C(m + U - 1, U - 1).
    """
    n = sum(x)
    R = compositions(m, len(x))  # @line L2
    u = [utility(x, y, queries) for y in R]  # @line L3
    top = max(u)
    w = [math.exp(epsilon * n * (v - top) / 2.0) for v in u]  # @line L4
    z = sum(w)
    return {y: v / z for y, v in zip(R, w)}


def smalldb(
    x: Sequence[int],
    queries: Sequence[Sequence[int]],
    epsilon: float,
    alpha: float,
    rng: random.Random,
) -> tuple[int, ...]:
    """Release a small synthetic database with SmallDB; it is epsilon-DP for replace neighbors.

    Precondition: epsilon > 0, alpha > 0, n = sum(x) >= 1, at least one query.
    Cost: O(|R| |Q| U) time and O(|R|) space, with |R| about U^m / m!.
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if sum(x) < 1 or not queries:
        raise ValueError("need a non-empty dataset and at least one query")
    m = small_size(alpha, len(queries))  # @line L1
    pmf = smalldb_pmf(x, queries, epsilon, m)
    u = rng.random()
    acc = 0.0
    last = None
    for y, p in pmf.items():
        acc += p
        last = y
        if u < acc:
            return y
    return last


def max_error(x: Sequence[int], y: Sequence[int], queries: Sequence[Sequence[int]]) -> float:
    """The largest error max over f of |f(x) - f(y)| of normalized answers."""
    return -utility(x, y, queries)
