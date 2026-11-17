# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-projection-motif-finding/. The authors are listed in prov/24V46J.jsonl.
"""PROJECTION of Buhler and Tompa (2002): hash every window by k random
positions, refine each bucket that holds windows of at least s sequences with
EM under the one occurrence per sequence (OOPS) model, and keep the best
refined model. The planted-model formulas for the number of trials are here
as well.

Positions are 0-based in this code; the page numbers them from 1.
"""

import math
import random
from fractions import Fraction
from math import comb
from typing import Dict, List, NamedTuple, Sequence, Tuple

from bioseq import DNA, kmers

_INDEX = {a: k for k, a in enumerate(DNA)}


class ProjectionResult(NamedTuple):
    """The best refined model: theta[j][a], its consensus, its 0-based site in
    each sequence and its OOPS log likelihood ratio; also the number of buckets
    refined and the projections drawn (0-based positions, sorted)."""

    theta: Tuple[Tuple[float, ...], ...]
    consensus: str
    sites: Tuple[int, ...]
    score: float
    buckets_refined: int
    projections: Tuple[Tuple[int, ...], ...]


def hit_probability(L: int, d: int, k: int) -> Fraction:
    """P(a planted copy with exactly d changes at uniform positions hashes with the motif) = C(L-d, k) / C(L, k)."""
    if not 0 <= d <= L or not 0 <= k <= L:
        raise ValueError("need 0 <= d <= L and 0 <= k <= L")
    return Fraction(comb(L - d, k), comb(L, k))


def binomial_tail(n: int, p, s: int):
    """P(Bin(n, p) >= s), exact when p is a Fraction."""
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(s, n + 1))


def trials_needed(n: int, L: int, d: int, k: int, s: int, q: float) -> int:
    """The least m with 1 - (1 - P)^m >= q, where P = P(Bin(n, p) >= s) is the
    chance that one trial puts at least s planted copies in the motif bucket."""
    if not 0 < q < 1:
        raise ValueError("q must be in (0, 1)")
    P = float(binomial_tail(n, hit_probability(L, d, k), s))
    if P <= 0:
        raise ValueError("a trial can never succeed with these parameters")
    if P >= 1:
        return 1
    m = math.ceil(math.log(1 - q) / math.log(1 - P))
    while m > 1 and 1 - (1 - P) ** (m - 1) >= q:
        m -= 1
    while 1 - (1 - P) ** m < q:
        m += 1
    return m


def letter_frequencies(seqs: Sequence[str]) -> List[float]:
    total = sum(len(s) for s in seqs)
    return [sum(s.count(a) for s in seqs) / total for a in DNA]


def _encode(seqs, L):
    return [[tuple(_INDEX[a] for a in w) for w in kmers(s, L)] for s in seqs]


def oops_score(X, theta, mu) -> float:
    """The OOPS log likelihood ratio: sum over sequences of log((1/W_i) sum_q prod_j theta_j(x_j) / mu(x_j))."""
    lr = [[math.log(theta[j][a] / mu[a]) for a in range(4)] for j in range(len(theta))]
    total = 0.0
    for rows in X:
        v = [sum(lr[j][c] for j, c in enumerate(x)) for x in rows]
        m = max(v)
        total += m + math.log(sum(math.exp(t - m) for t in v) / len(v))
    return total


def oops_em(X, theta, mu, beta: float, iterations: int) -> Tuple[List[List[float]], List[float]]:
    """EM for the OOPS model with fixed background mu; returns theta and the score after each iteration.

    E step: z_iq proportional to prod_j theta_j(x_j) / mu(x_j) within each sequence.
    M step: theta_j(a) = (sum z [x_j = a] + beta mu(a)) / (n + beta).
    """
    L = len(theta)
    n = len(X)
    history = []
    for _ in range(iterations):
        lr = [[math.log(theta[j][a] / mu[a]) for a in range(4)] for j in range(L)]
        c = [[0.0] * 4 for _ in range(L)]
        for rows in X:
            v = [sum(lr[j][a] for j, a in enumerate(x)) for x in rows]
            m = max(v)
            w = [math.exp(t - m) for t in v]
            z = sum(w)
            for x, wk in zip(rows, w):
                for j, a in enumerate(x):
                    c[j][a] += wk / z
        theta = [[(c[j][a] + beta * mu[a]) / (n + beta) for a in range(4)] for j in range(L)]
        history.append(oops_score(X, theta, mu))
    return theta, history


def projection(seqs: Sequence[str], L: int, k: int, trials: int, s: int = 3, seed: int = 0,
               beta: float = 1.0, em_iterations: int = 10) -> ProjectionResult:
    """Run PROJECTION and return the best refined model.

    Draw order: random.Random(seed); one rng.sample(range(L), k) per trial.
    A bucket is refined when its windows come from at least s different
    sequences. The start model of a bucket is its letter counts plus beta mu(a).
    Among equal scores the first refined bucket wins.
    """
    if L <= 0 or not 1 <= k <= L:
        raise ValueError("need L >= 1 and 1 <= k <= L")
    if not seqs:
        raise ValueError("need at least one sequence")
    for x in seqs:
        if len(x) < L or set(x) - set(DNA):
            raise ValueError("sequences must be over ACGT with length at least L")
    if trials < 1 or s < 1 or beta <= 0 or em_iterations < 1:
        raise ValueError("trials, s and em_iterations must be at least 1, beta positive")
    mu = letter_frequencies(seqs)
    if min(mu) == 0:
        raise ValueError("every letter must occur in the input")
    rng = random.Random(seed)
    X = _encode(seqs, L)
    best = None  # @line L1
    refined = 0
    projections = []
    for _ in range(trials):  # @line L2
        pos = sorted(rng.sample(range(L), k))  # @line L3
        projections.append(tuple(pos))
        buckets: Dict[Tuple[int, ...], List[Tuple[int, int]]] = {}
        for i, rows in enumerate(X):  # @line L4
            for q, x in enumerate(rows):
                buckets.setdefault(tuple(x[p] for p in pos), []).append((i, q))
        for key in sorted(buckets):  # @line L5
            members = buckets[key]
            if len({i for i, _ in members}) < s:
                continue
            refined += 1
            counts = [[beta * mu[a] for a in range(4)] for _ in range(L)]  # @line L6
            for i, q in members:
                for j, a in enumerate(X[i][q]):
                    counts[j][a] += 1
            theta = [[c / sum(row) for c in row] for row in counts]
            theta, history = oops_em(X, theta, mu, beta, em_iterations)  # @line L7
            if best is None or history[-1] > best[0]:  # @line L8
                best = (history[-1], theta)
    if best is None:
        raise ValueError("no bucket reached the threshold s; use more trials, a smaller k or a smaller s")
    score, theta = best
    lr = [[math.log(theta[j][a] / mu[a]) for a in range(4)] for j in range(L)]
    sites = []
    for rows in X:
        v = [sum(lr[j][a] for j, a in enumerate(x)) for x in rows]
        sites.append(v.index(max(v)))
    cons = "".join(DNA[max(range(4), key=lambda a: (row[a], -a))] for row in theta)
    return ProjectionResult(tuple(map(tuple, theta)), cons, tuple(sites), score, refined,
                            tuple(projections))  # @line L9
