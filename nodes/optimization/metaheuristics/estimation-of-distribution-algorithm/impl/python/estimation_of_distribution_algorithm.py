# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/estimation-of-distribution-algorithm/. The authors are listed in prov/MH6JW4.jsonl.

"""Univariate estimation of distribution algorithms on bit strings: UMDA and the compact GA."""

import random
from typing import Callable, Sequence

Bits = list[int]


def sample(p: Sequence[float], rng: random.Random) -> Bits:
    return [1 if rng.random() < pj else 0 for pj in p]


def umda(
    score: Callable[[Sequence[int]], float],
    n: int,
    lam: int,
    mu: int,
    generations: int,
    rng: random.Random,
    margins: bool = True,
    trace: list | None = None,
) -> tuple[Bits, float, list[float]]:
    """Maximize score over {0, 1}^n with UMDA and truncation selection.

    Each generation samples lam strings, keeps the mu best (ties keep the earlier
    sample), and sets p_j to the frequency of 1 at position j among them. With
    margins, p_j is then clamped to [1/n, 1 - 1/n]. Stop early when the best score
    stops changing because p has no free entries left. Return (best, its score, p).
    If trace is a list, append a copy of p after each generation.
    """
    lo, hi = (1 / n, 1 - 1 / n) if margins else (0.0, 1.0)
    p = [0.5] * n  # @line L1
    best, best_s = None, float("-inf")
    for _ in range(generations):  # @line L2
        xs = [sample(p, rng) for _ in range(lam)]  # @line L3
        ss = [score(x) for x in xs]
        chosen = sorted(range(lam), key=lambda i: -ss[i])[:mu]  # @line L4
        if ss[chosen[0]] > best_s:
            best, best_s = xs[chosen[0]], ss[chosen[0]]
        freq = [sum(xs[i][j] for i in chosen) / mu for j in range(n)]  # @line L5
        p = [min(hi, max(lo, q)) for q in freq]  # @line L6
        if trace is not None:
            trace.append(p[:])
    return best, best_s, p  # @line L7


def compact_ga(
    score: Callable[[Sequence[int]], float],
    n: int,
    K: int,
    iterations: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[Bits, float, list[float]]:
    """The compact GA of Harik, Lobo and Goldberg with the margins [1/n, 1 - 1/n].

    Each iteration samples two strings, and where they differ moves p_j by 1/K
    toward the bit of the better one. Return (best, its score, p).
    """
    p = [0.5] * n
    best, best_s = None, float("-inf")
    for _ in range(iterations):
        x, y = sample(p, rng), sample(p, rng)
        sx, sy = score(x), score(y)
        if sy > sx:
            x, y, sx, sy = y, x, sy, sx
        if sx > best_s:
            best, best_s = x, sx
        for j in range(n):
            if x[j] != y[j]:
                q = p[j] + (1 / K if x[j] == 1 else -1 / K)
                p[j] = min(1 - 1 / n, max(1 / n, q))
        if trace is not None:
            trace.append(p[:])
    return best, best_s, p


def onemax(x: Sequence[int]) -> int:
    return sum(x)


def trap(x: Sequence[int], k: int = 5) -> int:
    """Concatenated deceptive traps: a block with u ones scores k if u = k, else k - 1 - u."""
    total = 0
    for b in range(0, len(x), k):
        u = sum(x[b : b + k])
        total += k if u == k else k - 1 - u
    return total
