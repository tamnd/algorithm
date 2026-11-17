# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optknock/. The authors are listed in prov/K9KY6N.jsonl.
"""OptKnock with the inner problem replaced by its LP dual.

OptKnock is the bilevel program

    maximize v_prod over knockout sets D with |D| <= K
    where v solves  max v_bio  s.t.  S v = 0,  lb_D <= v <= ub_D,

and lb_D, ub_D are the bounds with lb_j = ub_j = 0 for j in D, plus an
outer floor v_bio >= mu_min. For a fixed D the inner LP has the dual

    minimize ub^T alpha - lb^T beta  s.t.  S^T lam + alpha - beta = e_bio,
    alpha, beta >= 0, lam free

(alpha_j is left out when ub_j is infinite and beta_j when lb_j is
infinite). By strong duality, v is optimal for the inner LP if and only if
some dual feasible (lam, alpha, beta) has v_bio = ub^T alpha - lb^T beta.
So the bilevel program for a fixed D is the single LP below. Burgard,
Pharkya and Maranas write the same thing with binary variables y_j for the
knockouts, which makes it a MILP. This code fixes y by enumerating every D
with |D| <= K, which is exact and only fit for small K and small networks.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import List, Optional, Sequence, Tuple

from sy3lp import frac, solve_lp


def knockout(lb, ub, D):
    lb, ub = list(lb), list(ub)
    for j in D:
        lb[j] = 0
        ub[j] = 0
    return lb, ub


def single_level_lp(S, lb, ub, bio, prod, mu_min=0):
    """The OptKnock LP for fixed bounds: primal, dual and strong duality.

    Variables, in order: v (m), lam (n), alpha (one per finite ub),
    beta (one per finite lb). Returns the LPResult and the slice of v.
    """
    n, m = len(S), len(lb)
    A_idx = [j for j in range(m) if ub[j] is not None]
    B_idx = [j for j in range(m) if lb[j] is not None]
    N = m + n + len(A_idx) + len(B_idx)
    A_eq: List[List[Fraction]] = []
    b_eq: List[Fraction] = []
    for i in range(n):  # primal: S v = 0
        A_eq.append([frac(S[i][j]) for j in range(m)] + [Fraction(0)] * (N - m))
        b_eq.append(Fraction(0))
    for j in range(m):  # dual: S^T lam + alpha - beta = e_bio
        row = [Fraction(0)] * N
        for i in range(n):
            row[m + i] = frac(S[i][j])
        if j in A_idx:
            row[m + n + A_idx.index(j)] = Fraction(1)
        if j in B_idx:
            row[m + n + len(A_idx) + B_idx.index(j)] = Fraction(-1)
        A_eq.append(row)
        b_eq.append(Fraction(int(j == bio)))
    row = [Fraction(0)] * N  # strong duality: v_bio = ub^T alpha - lb^T beta
    row[bio] = Fraction(1)
    for k, j in enumerate(A_idx):
        row[m + n + k] = -frac(ub[j])
    for k, j in enumerate(B_idx):
        row[m + n + len(A_idx) + k] = frac(lb[j])
    A_eq.append(row)
    b_eq.append(Fraction(0))
    lo = list(lb) + [None] * n + [0] * (len(A_idx) + len(B_idx))
    hi = list(ub) + [None] * (N - m)
    if mu_min is not None:
        lo[bio] = mu_min if lo[bio] is None else max(frac(lo[bio]), frac(mu_min))
    c = [0] * N
    c[prod] = 1
    return solve_lp(c, A_eq=A_eq, b_eq=b_eq, lb=lo, ub=hi, maximize=True)


def optknock(S: Sequence[Sequence], lb: Sequence, ub: Sequence, bio: int,
             prod: int, K: int, candidates: Sequence[int], mu_min=0):
    """Best knockout set of size at most K for the product, by enumeration.

    Returns (D, v) with the largest v_prod; among equal products the first
    set in the order of size, then lexicographic order, wins. Returns None
    if no set gives a feasible LP.
    """
    m = len(lb)
    best: Optional[Tuple[Tuple[int, ...], List[Fraction]]] = None  # @line L1
    for k in range(K + 1):
        for D in combinations(candidates, k):  # @line L2
            lbD, ubD = knockout(lb, ub, D)  # @line L3
            res = single_level_lp(S, lbD, ubD, bio, prod, mu_min)  # @line L4
            if res.status != "optimal":  # @line L5
                continue
            v = res.x[:m]
            if best is None or v[prod] > best[1][prod]:  # @line L6
                best = (D, v)
    return best  # @line L7


# The toy network N of the flux-balance-analysis page.
NAMES = ["EX_A", "RESP1", "RESP2", "FERM", "EX_P", "BIO"]
S_N = [
    [1, -1, -1, -1, 0, -1],  # A
    [0, 2, 2, 1, 0, -1],     # E
    [0, 0, 0, 1, -1, 0],     # P
]
LB_N = [0, 0, 0, 0, 0, 0]
UB_N = [10, None, None, None, None, None]
BIO_N, PROD_N = 5, 4
CAND_N = [1, 2, 3]
