# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimization-of-metabolic-adjustment/. The authors are listed in prov/845EGQ.jsonl.
"""Minimization of metabolic adjustment (MOMA), solved exactly.

Given the wild-type flux vector w (an FBA optimum of the wild type) and the
bounds of a mutant (a knocked-out reaction has lb = ub = 0), MOMA returns the
mutant flux vector closest to w in the Euclidean norm:

    minimize |v - w|^2  subject to  S v = 0,  lb <= v <= ub.

This is a strictly convex quadratic program, so the minimizer is unique. The
solver here is exact and meant for small networks: it tries every active set
(each reaction at its lower bound, at its upper bound, or free), solves the
equality-constrained problem for that set, and accepts the first candidate
that satisfies the KKT conditions. The cost is up to 3^m candidates.

KKT conditions, with lambda the multipliers of S v = 0 and
g = v - w + S^T lambda: g_j = 0 for a free reaction, g_j >= 0 at the lower
bound, g_j <= 0 at the upper bound (and any sign if lb_j = ub_j). lambda may
be not unique when S has dependent rows, so the sign test is a small LP
feasibility problem in lambda.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import List, Optional, Sequence

from sy3lp import frac, solve_linear, solve_lp

LOW, UP, FREE = 0, 1, 2


def _choices(lo, hi):
    if lo is not None and hi is not None and lo == hi:
        return (LOW,)
    out = []
    if lo is not None:
        out.append(LOW)
    if hi is not None:
        out.append(UP)
    out.append(FREE)
    return tuple(out)


def _multipliers_exist(S, v, w, state, lo, hi) -> bool:
    """Is there lambda with g = v - w + S^T lambda of the right signs?"""
    n, m = len(S), len(v)
    A_eq, b_eq, A_le, b_le = [], [], [], []
    for j in range(m):
        col = [frac(S[i][j]) for i in range(n)]
        d = v[j] - w[j]
        if lo[j] is not None and hi[j] is not None and lo[j] == hi[j]:
            continue
        if state[j] == FREE:
            A_eq.append(col)
            b_eq.append(-d)
        elif state[j] == LOW:  # d + col . lam >= 0
            A_le.append([-x for x in col])
            b_le.append(d)
        else:  # d + col . lam <= 0
            A_le.append(col)
            b_le.append(-d)
    if n == 0:
        return all(x == 0 for x in b_eq) and all(x >= 0 for x in b_le)
    res = solve_lp([0] * n, A_eq=A_eq, b_eq=b_eq, A_le=A_le, b_le=b_le,
                   lb=[None] * n)
    return res.status == "optimal"


def moma(S: Sequence[Sequence], lb: Sequence, ub: Sequence,
         w: Sequence) -> Optional[List[Fraction]]:
    """The flux vector of the mutant closest to w, or None if infeasible."""
    m = len(w)
    w = [frac(x) for x in w]
    lo = [None if x is None else frac(x) for x in lb]
    hi = [None if x is None else frac(x) for x in ub]
    n = len(S)
    options = [_choices(lo[j], hi[j]) for j in range(m)]
    # Try sets with more free reactions first: the answer is often interior.
    states = sorted(product(*options), key=lambda s: -s.count(FREE))
    for state in states:  # @line L1
        v = [Fraction(0)] * m
        free = [j for j in range(m) if state[j] == FREE]
        for j in range(m):  # @line L2
            if state[j] == LOW:
                v[j] = lo[j]
            elif state[j] == UP:
                v[j] = hi[j]
        # Project w_F onto {x : S_F x = r}: solve [I S_F^T; S_F 0] [x; mu] = [w_F; r].
        r = [-sum(frac(S[i][j]) * v[j] for j in range(m) if state[j] != FREE)  # @line L3
             for i in range(n)]
        k = len(free)
        K = []
        rhs = []
        for a, j in enumerate(free):
            K.append([Fraction(int(a == b)) for b in range(k)]
                     + [frac(S[i][j]) for i in range(n)])
            rhs.append(w[j])
        for i in range(n):
            K.append([frac(S[i][j]) for j in free] + [Fraction(0)] * n)
            rhs.append(r[i])
        sol = solve_linear(K, rhs)  # @line L4
        if sol is None:
            continue
        for a, j in enumerate(free):
            v[j] = sol[a]
        if any((lo[j] is not None and v[j] < lo[j]) or  # @line L5
               (hi[j] is not None and v[j] > hi[j]) for j in free):
            continue
        if _multipliers_exist(S, v, w, state, lo, hi):  # @line L6
            return v  # @line L7
    return None  # @line L8


def sq_dist(v, w) -> Fraction:
    return sum((frac(a) - frac(b)) ** 2 for a, b in zip(v, w))


# The toy network N of the flux-balance-analysis page.
NAMES = ["EX_A", "RESP1", "RESP2", "FERM", "EX_P", "BIO"]
S_N = [
    [1, -1, -1, -1, 0, -1],  # A
    [0, 2, 2, 1, 0, -1],     # E
    [0, 0, 0, 1, -1, 0],     # P
]
LB_N = [0, 0, 0, 0, 0, 0]
UB_N = [10, None, None, None, None, None]
C_N = [0, 0, 0, 0, 0, 1]
