# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moran-model/. The authors are listed in prov/QM5Y7F.jsonl.
"""The Moran model of a haploid population of N individuals with two types.

X is the number of individuals of type A. In each step one individual is
chosen to reproduce, with probability proportional to fitness (r for A and
1 for a), and one individual is chosen uniformly to die; the offspring takes
its place. The same individual can be chosen for both. So X moves by +1, -1
or 0, and the chain is a birth-death chain on 0, ..., N with absorbing ends.
Time is in steps; one generation is N steps.

Exact results use the birth and death probabilities
    b_i = r i (N - i) / ((r i + N - i) N),   d_i = (N - i) i / ((r i + N - i) N).
With r a Fraction (or an int), they are exact rationals.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Tuple

from biostoch import binomial


def rates(i: int, N: int, r=1):
    """(b_i, d_i): the probabilities that one step moves X from i to i + 1
    and to i - 1."""
    w = r * i + (N - i)
    if w == 0:
        return 0, 0
    if isinstance(r, (int, Fraction)):
        b = Fraction(r * i, 1) / w * Fraction(N - i, N)
        d = Fraction(N - i, 1) / w * Fraction(i, N)
    else:
        b = r * i / w * (N - i) / N
        d = (N - i) / w * i / N
    return b, d


def step(rng, x: int, N: int, r: float = 1.0) -> int:
    """One birth and one death. Two draws from biostoch.binomial(rng, 1, .):
    first the type of the parent, then the type of the individual that dies."""
    birth_a = binomial(rng, 1, r * x / (r * x + N - x))  # @line L3
    death_a = binomial(rng, 1, x / N)  # @line L4
    return x + birth_a - death_a  # @line L5


def simulate(rng, i0: int, N: int, steps: int, r: float = 1.0) -> List[int]:
    """The counts X_0, ..., X_steps; the run stops early at 0 or N."""
    if N < 1 or not 0 <= i0 <= N:
        raise ValueError("need N >= 1 and 0 <= i0 <= N")
    x = i0  # @line L1
    xs = [x]
    for _ in range(steps):  # @line L2
        if x == 0 or x == N:
            break
        x = step(rng, x, N, r)
        xs.append(x)
    return xs  # @line L6


def run_to_absorption(rng, i0: int, N: int, r: float = 1.0) -> Tuple[bool, int]:
    """Run until one type is lost. Returns (A fixed, number of steps)."""
    x, t = i0, 0
    while 0 < x < N:
        x = step(rng, x, N, r)
        t += 1
    return x == N, t


def fixation_formula(i: int, N: int, r=1):
    """(1 - r^(-i)) / (1 - r^(-N)), and i / N when r = 1."""
    if r == 1:
        return Fraction(i, N) if isinstance(r, (int, Fraction)) else i / N
    return (1 - r ** (-i)) / (1 - r ** (-N))


def fixation_by_sums(i: int, N: int, r=1):
    """The birth-death formula sum_{k<i} prod_{j<=k} gamma_j / sum_{k<N} (same),
    with gamma_j = d_j / b_j, which needs no closed form."""
    terms = []
    prod = 1
    for k in range(N):
        terms.append(prod)
        if k + 1 < N:
            b, d = rates(k + 1, N, r)
            prod = prod * (d / b)
    return sum(terms[:i]) / sum(terms)


def absorption_times(N: int, r=1) -> Tuple[list, list]:
    """The first two moments of the number of steps to absorption from each
    start 0, ..., N, by solving the tridiagonal systems
        t_i = 1 + b_i t_(i+1) + d_i t_(i-1) + (1 - b_i - d_i) t_i,
    and the same with right side 1 + 2 (b_i t_(i+1) + d_i t_(i-1) + (1 - b_i - d_i) t_i)
    for the second moment, by the Thomas algorithm."""
    exact = isinstance(r, (int, Fraction))
    zero, one = (Fraction(0), Fraction(1)) if exact else (0.0, 1.0)
    n = N - 1
    if n <= 0:
        return [zero] * (N + 1), [zero] * (N + 1)
    lo, di, up = [], [], []
    for i in range(1, N):
        b, d = rates(i, N, r)
        lo.append(-d)
        di.append(b + d)
        up.append(-b)

    def solve(rhs):
        c = [zero] * n
        g = [zero] * n
        c[0] = up[0] / di[0]
        g[0] = rhs[0] / di[0]
        for k in range(1, n):
            den = di[k] - lo[k] * c[k - 1]
            c[k] = up[k] / den
            g[k] = (rhs[k] - lo[k] * g[k - 1]) / den
        x = [zero] * n
        x[-1] = g[-1]
        for k in range(n - 2, -1, -1):
            x[k] = g[k] - c[k] * x[k + 1]
        return x

    t = [zero] + solve([one] * n) + [zero]
    rhs2 = []
    for i in range(1, N):
        b, d = rates(i, N, r)
        rhs2.append(one + 2 * (b * t[i + 1] + d * t[i - 1] + (1 - b - d) * t[i]))
    m2 = [zero] + solve(rhs2) + [zero]
    return t, m2


def transition_matrix(N: int, r=1) -> List[list]:
    P = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        b, d = rates(i, N, r)
        if i < N:
            P[i][i + 1] = b
        if i > 0:
            P[i][i - 1] = d
        P[i][i] = 1 - b - d
    return P
