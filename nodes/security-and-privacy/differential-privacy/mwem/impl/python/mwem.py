# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mwem/. The authors are listed in prov/R361Z0.jsonl.
"""MWEM, the multiplicative weights exponential mechanism (Hardt, Ligett and
McSherry 2012), for counting queries over a small finite domain.

The data is a histogram B over a domain D of size N: B[x] is the number of
records equal to x, and n = sum(B) is public. A counting query is a 0-1
vector q over D, and q(B) = sum_x q[x] B[x]. Neighbors replace one record
by another, so n stays fixed and each q(B) moves by at most 1.

The code uses random.Random so that the tests can be repeated, and float
noise. A real release needs a cryptographic source of randomness and exact
sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).
"""

from __future__ import annotations

import math
import random
from typing import Sequence


def laplace_noise(b: float, rng: random.Random) -> float:
    """One draw of Lap(b), the density (1/(2b)) exp(-|z|/b), by the inverse CDF.

    Precondition: b > 0. Cost: one uniform draw and O(1) time.
    """
    u = rng.random() - 0.5
    while u == -0.5:
        u = rng.random() - 0.5
    s = (u > 0) - (u < 0)
    return -b * s * math.log(1.0 - 2.0 * abs(u))


def evaluate(q: Sequence[int], hist: Sequence[float]) -> float:
    """The answer q(hist) = sum_x q[x] hist[x]. Cost: O(N)."""
    return sum(w * h for w, h in zip(q, hist))


def exponential_mechanism_pmf(scores: Sequence[float], epsilon0: float) -> list[float]:
    """The exponential mechanism for scores of sensitivity 1: P(r) is proportional to exp(epsilon0 * score_r / 2).

    Precondition: at least one score, epsilon0 > 0. Cost: O(len(scores)).
    """
    top = max(scores)
    w = [math.exp(epsilon0 * (s - top) / 2.0) for s in scores]
    z = sum(w)
    return [v / z for v in w]


def sample_index(pmf: Sequence[float], rng: random.Random) -> int:
    """Draw an index from a pmf with one uniform draw by the inverse CDF. Cost: O(len(pmf))."""
    u = rng.random()
    acc = 0.0
    for i, p in enumerate(pmf):
        acc += p
        if u < acc:
            return i
    return len(pmf) - 1


def mw_update(A: Sequence[float], q: Sequence[int], m: float, n: float) -> list[float]:
    """One multiplicative weights step: A(x) times exp(q[x] (m - q(A)) / (2n)), scaled back to total n.

    Precondition: A has total n > 0 and positive entries. Cost: O(N).
    """
    eta = (m - evaluate(q, A)) / (2.0 * n)
    logs = [math.log(a) + eta * w for a, w in zip(A, q)]
    top = max(logs)
    w = [math.exp(v - top) for v in logs]
    z = sum(w)
    return [n * v / z for v in w]


def mwem(
    B: Sequence[int],
    queries: Sequence[Sequence[int]],
    T: int,
    epsilon: float,
    rng: random.Random,
    return_last: bool = False,
) -> list[float]:
    """Run MWEM for T rounds and return a synthetic histogram.

    By default the output is the average of A_0, ..., A_{T-1}, the histograms
    that the T rounds start from, as in Figure 1 of Hardt, Ligett and
    McSherry; their error theorem is for this average. With return_last the
    output is A_T, which they use in their experiments. Both are
    post-processing of the same run. Each round spends epsilon/(2T) on the
    selection and epsilon/(2T) on the measurement, so the run is epsilon-DP
    for replace neighbors.
    Precondition: T >= 1, epsilon > 0, n = sum(B) >= 1, at least one query.
    Cost: O(T |Q| N) time and O(N + |Q|) extra space.
    """
    if T < 1 or epsilon <= 0:
        raise ValueError("need T >= 1 and epsilon > 0")
    if not queries:
        raise ValueError("need at least one query")
    n = float(sum(B))
    if n <= 0:
        raise ValueError("the dataset must not be empty")
    N = len(B)
    true = [evaluate(q, B) for q in queries]
    A = [n / N] * N  # @line L1
    total = [0.0] * N
    for _ in range(T):  # @line L2
        total = [s + a for s, a in zip(total, A)]
        scores = [abs(evaluate(q, A) - t) for q, t in zip(queries, true)]
        i = sample_index(exponential_mechanism_pmf(scores, epsilon / (2.0 * T)), rng)  # @line L3
        m = true[i] + laplace_noise(2.0 * T / epsilon, rng)  # @line L4
        A = mw_update(A, queries[i], m, n)  # @line L5
    if return_last:
        return A
    return [s / T for s in total]  # @line L6


def max_error(B: Sequence[int], A: Sequence[float], queries: Sequence[Sequence[int]]) -> float:
    """The largest error max_q |q(A) - q(B)| over the queries. Cost: O(|Q| N)."""
    return max(abs(evaluate(q, A) - evaluate(q, B)) for q in queries)
