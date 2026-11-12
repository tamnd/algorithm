# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karlin-altschul-statistics/. The authors are listed in prov/TJVQ07.jsonl.

"""Karlin-Altschul parameters for ungapped local alignment scores.

A scoring scheme is given as a score distribution: a dict that maps each
pair score s to its probability P(X = s) = sum of p_i p'_j over the residue
pairs (i, j) with s_ij = s. The functions below compute the expected score,
the parameter lambda, the relative entropy H, the constant K (for integer
scores), E-values, P-values and bit scores.
"""

import math
from functools import reduce
from typing import Callable, Mapping, Sequence


def score_distribution(
    freqs1: Mapping[str, float],
    freqs2: Mapping[str, float],
    score: Callable[[str, str], int],
) -> dict[int, float]:
    """Distribution of the score of one aligned pair of random letters."""
    dist: dict[int, float] = {}
    for a, pa in freqs1.items():
        for b, pb in freqs2.items():
            s = score(a, b)
            dist[s] = dist.get(s, 0.0) + pa * pb
    return {s: p for s, p in dist.items() if p > 0}


def expected_score(dist: Mapping[int, float]) -> float:
    return sum(s * p for s, p in dist.items())


def _f(dist: Mapping[int, float], lam: float) -> float:
    """f(lam) = E[exp(lam X)] - 1."""
    return sum(p * math.exp(lam * s) for s, p in dist.items()) - 1.0


def check_conditions(dist: Mapping[int, float]) -> None:
    """Raise ValueError unless E[X] < 0 and P(X > 0) > 0."""
    if expected_score(dist) >= 0:
        raise ValueError("the expected score must be negative")
    if not any(s > 0 and p > 0 for s, p in dist.items()):
        raise ValueError("some positive score must have positive probability")


def solve_lambda(dist: Mapping[int, float], tol: float = 1e-13) -> float:
    """The unique positive root of E[exp(lam X)] = 1, by bisection.

    f is convex with f(0) = 0 and f'(0) = E[X] < 0, and f grows without
    bound, so f < 0 on (0, lam*) and f >= 0 on [lam*, infinity). The loop
    keeps lo < lam* <= hi.
    """
    check_conditions(dist)
    lo, hi = 0.0, 1.0
    while _f(dist, hi) < 0:
        lo, hi = hi, 2.0 * hi
    while hi - lo > tol * max(1.0, hi):
        mid = (lo + hi) / 2.0
        if _f(dist, mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def relative_entropy(dist: Mapping[int, float], lam: float) -> float:
    """H = sum over pairs of q_ij * lam * s_ij, with q_ij = p_i p'_j exp(lam s_ij), in nats."""
    return lam * sum(p * s * math.exp(lam * s) for s, p in dist.items())


def karlin_k(dist: Mapping[int, int | float], max_terms: int = 400, eps: float = 1e-15) -> float:
    """The constant K for integer scores, by the Karlin-Altschul series.

    Scores are first divided by their greatest common divisor d; lambda
    scales by d and K does not change. With gcd 1,

        K = exp(-2 sum_{k>=1} (1/k) [E(exp(lam S_k); S_k < 0) + P(S_k >= 0)])
            / (E[X exp(lam X)] * (1 - exp(-lam)))

    where S_k is the sum of k independent scores. This is the form that the
    NCBI BLAST code evaluates. The terms decay geometrically, but slowly
    when E[X] is close to 0; raise max_terms in that case.
    """
    d = reduce(math.gcd, (abs(int(s)) for s in dist if s != 0))
    red = {int(s) // d: p for s, p in dist.items()}
    lam = solve_lambda(red)
    first = sum(p * s * math.exp(lam * s) for s, p in red.items())
    walk: dict[int, float] = {0: 1.0}
    outer = 0.0
    for k in range(1, max_terms + 1):
        nxt: dict[int, float] = {}
        for a, pa in walk.items():
            for s, p in red.items():
                nxt[a + s] = nxt.get(a + s, 0.0) + pa * p
        walk = {a: v for a, v in nxt.items() if v > 1e-300}
        inner = sum(v * (math.exp(lam * a) if a < 0 else 1.0) for a, v in walk.items())
        outer += inner / k
        if inner < eps:
            break
    return math.exp(-2.0 * outer) / (first * (1.0 - math.exp(-lam)))


def evalue(score: float, m: float, n: float, lam: float, k: float) -> float:
    """E = K m n exp(-lam S): expected number of HSPs with score at least S."""
    return k * m * n * math.exp(-lam * score)


def pvalue(e: float) -> float:
    """P = 1 - exp(-E): probability of at least one such HSP (Poisson)."""
    return -math.expm1(-e)


def bit_score(score: float, lam: float, k: float) -> float:
    """S' = (lam S - ln K) / ln 2."""
    return (lam * score - math.log(k)) / math.log(2.0)


def evalue_from_bits(bits: float, m: float, n: float) -> float:
    """E = m n 2^(-S')."""
    return m * n * 2.0 ** (-bits)


def count_hsps(x: Sequence[str], y: Sequence[str], score: Callable[[str, str], int], cutoff: int) -> int:
    """Number of ungapped excursions with peak score >= cutoff, over all diagonals.

    On each diagonal the running score h = max(0, h + s) starts at 0. An
    excursion runs from a step that leaves 0 to the step that returns to 0
    (or to the end of the diagonal); its peak is the score of the best
    segment pair in it.
    """
    m, n = len(x), len(y)
    count = 0
    for d in range(-(m - 1), n):
        i, j = max(0, -d), max(0, d)
        h = peak = 0
        while i < m and j < n:
            h += score(x[i], y[j])
            if h <= 0:
                if peak >= cutoff:
                    count += 1
                h = peak = 0
            elif h > peak:
                peak = h
            i += 1
            j += 1
        if peak >= cutoff:
            count += 1
    return count
