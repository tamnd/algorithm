# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pwm-score-p-value/. The authors are listed in prov/YNZJ2F.jsonl.
"""The p-value of a weight matrix score, after Touzet and Varre (2007).

The score of a word w = w_1 .. w_L is sum_j M[j][w_j]. Under a background in
which the letters are independent with probabilities p(a), the p-value of a
threshold alpha is P(score >= alpha). The code rounds the matrix down to a
grid of step eps, computes the distribution of the rounded score by dynamic
programming, and gets a lower and an upper bound. When no rounded score falls
between alpha - E and alpha, where E is the largest total rounding error, the
two bounds are equal and the answer is exact. Otherwise eps is divided by 10.

Matrix entries and the threshold are turned into exact fractions (a float
becomes its exact binary value), and eps0 is read as a decimal, so the
rounding and the bounds have no floating-point error. The probabilities keep
the type of p: exact for Fraction, floating point for float.

Columns are 0-based in this code; the page numbers them from 1.
"""

import math
from fractions import Fraction
from typing import Dict, List, NamedTuple, Sequence

from bioseq import DNA


class PValueResult(NamedTuple):
    """lo <= P(score >= alpha) <= hi; exact is True when lo == hi is proved.
    eps is the last grid step, error the bound E of that round and rounds the
    number of rounds run."""

    lo: object
    hi: object
    exact: bool
    eps: Fraction
    error: Fraction
    rounds: int


def _fraction(x) -> Fraction:
    """The exact value of x as a Fraction (for a float, its exact binary value)."""
    if isinstance(x, float) and not math.isfinite(x):
        raise ValueError("matrix entries and the threshold must be finite")
    return Fraction(x)


def _check(M: Sequence[Sequence], p: Sequence) -> None:
    if not M:
        raise ValueError("the matrix needs at least one column")
    if any(len(row) != len(p) for row in M):
        raise ValueError("every column needs one entry per letter")
    if any(x < 0 for x in p) or abs(sum(p) - 1) > 1e-9:
        raise ValueError("the background must be a probability vector")


def score_distribution(M: Sequence[Sequence], p: Sequence) -> Dict[Fraction, object]:
    """The full distribution {score: probability} of sum_j M[j][w_j], with the
    scores as exact fractions. It has at most |alphabet|^L entries."""
    _check(M, p)
    Q: Dict[Fraction, object] = {Fraction(0): 1}
    for row in M:
        R: Dict[Fraction, object] = {}
        for s, q in Q.items():
            for a, w in enumerate(row):
                if p[a] > 0:
                    t = s + _fraction(w)
                    R[t] = R.get(t, 0) + q * p[a]
        Q = R
    return Q


def pvalue_round(N: Sequence[Sequence[int]], p: Sequence, A: int, B: int):
    """One round on an integer matrix N with B <= A.

    Returns (sure, middle): sure = P(sum N >= A) and middle = {s: P(sum N = s)}
    for the scores B <= s < A. Partial scores that reach A whatever the next
    letters are moved into sure; those that cannot reach B are dropped.
    """
    L = len(N)
    best = [0] * (L + 1)
    worst = [0] * (L + 1)
    for j in range(L - 1, -1, -1):
        allowed = [N[j][a] for a in range(len(p)) if p[a] > 0]
        best[j] = best[j + 1] + max(allowed)
        worst[j] = worst[j + 1] + min(allowed)
    sure = 0
    Q: Dict[int, object] = {0: 1}
    for j in range(L):
        R: Dict[int, object] = {}
        for s, q in Q.items():
            for a in range(len(p)):
                if p[a] == 0:
                    continue
                t = s + N[j][a]
                if t + worst[j + 1] >= A:
                    sure += q * p[a]
                elif t + best[j + 1] >= B:
                    R[t] = R.get(t, 0) + q * p[a]
        Q = R
    return sure, Q


def pwm_score_p_value(M: Sequence[Sequence], p: Sequence, alpha, eps0="0.1",
                      max_rounds: int = 8) -> PValueResult:
    """Bounds on P(score >= alpha) for a matrix M[j][a] and background p.

    eps starts at eps0 and is divided by 10 after each round that does not
    prove the answer exact, for at most max_rounds rounds.
    """
    _check(M, p)
    if max_rounds < 1:
        raise ValueError("max_rounds must be at least 1")
    F = [[_fraction(w) for w in row] for row in M]
    alpha = _fraction(alpha)
    eps = Fraction(repr(eps0)) if isinstance(eps0, float) else Fraction(eps0)  # @line L1
    if eps <= 0:
        raise ValueError("eps0 must be positive")
    rounds = 0
    while True:  # @line L2
        rounds += 1
        N = [[math.floor(w / eps) for w in row] for row in F]  # @line L3
        E = sum(max(w - eps * n for w, n, pa in zip(row, nrow, p) if pa > 0)  # @line L4
                for row, nrow in zip(F, N))
        A = math.ceil(alpha / eps)  # @line L5
        B = math.ceil((alpha - E) / eps)  # @line L6
        sure, middle = pvalue_round(N, p, A, B)  # @line L7
        lo = sure  # @line L8
        hi = sure + sum(middle.values())  # @line L9
        if not middle or rounds == max_rounds:  # @line L10
            return PValueResult(lo, hi, not middle, eps, E, rounds)  # @line L11
        eps /= 10  # @line L12


def log_odds_matrix(sites: Sequence[str], p: Sequence[float], pseudo: float = 1.0) -> List[List[float]]:
    """M[j][a] = log2(((count + pseudo p(a)) / (n + pseudo)) / p(a)) from aligned sites over ACGT."""
    if not sites or len({len(s) for s in sites}) != 1:
        raise ValueError("need aligned sites of one length")
    n = len(sites)
    M = []
    for j in range(len(sites[0])):
        col = [s[j] for s in sites]
        M.append([math.log2(((col.count(a) + pseudo * p[i]) / (n + pseudo)) / p[i]) for i, a in enumerate(DNA)])
    return M


def score(M: Sequence[Sequence], word: str):
    """The score sum_j M[j][word_j] of a word over ACGT."""
    if len(word) != len(M):
        raise ValueError("the word length must equal the number of columns")
    return sum(M[j][DNA.index(c)] for j, c in enumerate(word))
