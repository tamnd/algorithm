# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wright-fisher-model/. The authors are listed in prov/ZKD5QR.jsonl.
"""The Wright-Fisher model of one biallelic locus: a simulator and the exact
Markov chain.

The population has N diploid individuals, so 2N gene copies, in discrete
generations. X_t is the number of copies of allele A in generation t. Each
copy of generation t + 1 picks a parent copy independently. Without
selection the parent is uniform, so X_(t+1) given X_t = i is
Binomial(2N, i / (2N)). With selection the genotypes AA, Aa and aa have
fitnesses 1 + s, 1 + h s and 1, and the copies are drawn with the frequency
after selection.

The functions take the number of copies two_n = 2N. With Fraction values of
s and h (or s = 0) and exact=True, the chain is computed in exact rational
arithmetic.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, List, Sequence

from biostoch import binom_pmf, binomial


def selected_frequency(p, s=0, h=Fraction(1, 2)):
    """The frequency of A after selection with fitnesses 1 + s, 1 + h s, 1
    for AA, Aa, aa, given the frequency p before selection."""
    q = 1 - p
    w_A = p * (1 + s) + q * (1 + h * s)  # mean fitness of a copy of A
    w_bar = p * p * (1 + s) + 2 * p * q * (1 + h * s) + q * q
    return p * w_A / w_bar


def simulate(rng, i0: int, two_n: int, generations: int, s: float = 0.0,
             h: float = 0.5) -> List[int]:
    """The counts X_0, ..., X_T of allele A for T = generations steps.

    Each step makes one draw from Binomial(2N, p') by biostoch.binomial, where
    p' is the frequency after selection. The run stops early when the
    allele is lost or fixed, because the chain cannot leave these states."""
    if not 0 <= i0 <= two_n or two_n < 1:
        raise ValueError("need 0 <= i0 <= 2N and 2N >= 1")
    xs = [i0]  # @line L1
    x = i0
    for _ in range(generations):  # @line L2
        if x == 0 or x == two_n:
            break
        p = x / two_n  # @line L3
        p_sel = selected_frequency(p, s, h)  # @line L4
        x = binomial(rng, two_n, min(1.0, max(0.0, p_sel)))  # @line L5
        xs.append(x)
    return xs  # @line L6


def run_to_absorption(rng, i0: int, two_n: int, s: float = 0.0, h: float = 0.5,
                      max_generations: int = 10 ** 6):
    """Run until loss or fixation. Returns (fixed, generations)."""
    x = i0
    t = 0
    while 0 < x < two_n:
        if t >= max_generations:
            raise RuntimeError("no absorption within max_generations")
        x = binomial(rng, two_n, min(1.0, max(0.0, selected_frequency(x / two_n, s, h))))
        t += 1
    return x == two_n, t


def transition_matrix(two_n: int, s=0, h=Fraction(1, 2), exact: bool = False):
    """The (2N + 1) by (2N + 1) matrix P[i][j] = Pr(X_(t+1) = j | X_t = i)."""
    rows = []
    for i in range(two_n + 1):
        if exact:
            p = selected_frequency(Fraction(i, two_n), Fraction(s), Fraction(h))
            q = 1 - p
            rows.append([math.comb(two_n, j) * p ** j * q ** (two_n - j) for j in range(two_n + 1)])
        else:
            p = selected_frequency(i / two_n, s, h)
            rows.append([binom_pmf(j, two_n, min(1.0, max(0.0, p))) for j in range(two_n + 1)])
    return rows


def _solve(a: List[list], b: List[list]) -> List[list]:
    """Solve a x = b by Gaussian elimination; b has one column per right side.
    Works for floats (partial pivoting) and for Fractions (exact)."""
    n = len(a)
    m = [row[:] + rhs[:] for row, rhs in zip(a, b)]
    k = len(b[0])
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if m[piv][col] == 0:
            raise ZeroDivisionError("singular system")
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                for c in range(col, n + k):
                    m[r][c] -= f * m[col][c]
    return [[m[r][n + c] / m[r][r] for c in range(k)] for r in range(n)]


def absorption(two_n: int, s=0, h=Fraction(1, 2), exact: bool = False) -> Dict[str, list]:
    """Exact fixation probabilities and the first two moments of the time to
    absorption (in generations), for each start i = 0, ..., 2N.

    Solves (I - Q) u = r, (I - Q) t = 1 and (I - Q) m2 = 1 + 2 Q t, where Q is
    the transition matrix on the interior states 1, ..., 2N - 1 and r is the
    column of the jumps to 2N."""
    P = transition_matrix(two_n, s, h, exact)
    zero, one = (Fraction(0), Fraction(1)) if exact else (0.0, 1.0)
    inner = range(1, two_n)
    if two_n == 1:
        return {"fix": [zero, one], "time": [zero, zero], "time2": [zero, zero]}
    a = [[(one if i == j else zero) - P[i][j] for j in inner] for i in inner]
    rhs = [[P[i][two_n], one] for i in inner]
    sol = _solve(a, rhs)
    u = [row[0] for row in sol]
    t = [row[1] for row in sol]
    rhs2 = [[one + 2 * sum(P[i][j] * t[j - 1] for j in inner)] for i in inner]
    m2 = [row[0] for row in _solve(a, rhs2)]
    return {"fix": [zero] + u + [one], "time": [zero] + t + [zero], "time2": [zero] + m2 + [zero]}


def propagate(dist: Sequence, P: List[list], steps: int) -> list:
    """The law of X_t after `steps` generations from the law dist of X_0."""
    d = list(dist)
    n = len(d)
    for _ in range(steps):
        d = [sum(d[i] * P[i][j] for i in range(n)) for j in range(n)]
    return d


def heterozygosity_decay(N: int, t: int) -> float:
    """E[H_t] / H_0 = (1 - 1/(2N))^t under neutral drift, N diploids."""
    return (1.0 - 1.0 / (2 * N)) ** t
