# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leslie-matrix/. The authors are listed in prov/V3XCAW.jsonl.
"""The Leslie matrix model n_(t+1) = L n_t of an age-structured population.

The model is given by the fertilities F_1, ..., F_k (the first row of L)
and the survival rates P_1, ..., P_(k-1) (the subdiagonal). project uses
this structure, so one step costs Theta(k) and not Theta(k^2). The other
functions give the characteristic polynomial with exact coefficients, the
growth rate from the Euler-Lotka equation and by power iteration, the
stable age distribution, the reproductive values, R_0, the sensitivities
and elasticities of the growth rate, and a test for primitivity.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import List, Sequence, Tuple


def _check(F: Sequence, P: Sequence) -> None:
    if len(F) < 1 or len(P) != len(F) - 1:
        raise ValueError("need k >= 1 fertilities and k - 1 survival rates")
    if any(f < 0 for f in F) or any(not 0 < p <= 1 for p in P):
        raise ValueError("need F_i >= 0 and 0 < P_i <= 1")


def leslie(F: Sequence[float], P: Sequence[float]) -> List[List[float]]:
    """The k by k Leslie matrix."""
    _check(F, P)
    k = len(F)
    L = [[0 * F[0] for _ in range(k)] for _ in range(k)]
    L[0] = list(F)
    for i, p in enumerate(P):
        L[i + 1][i] = p
    return L


def project(F: Sequence[float], P: Sequence[float], n0: Sequence[float], steps: int) -> List[List[float]]:
    """The vectors n_1, ..., n_steps from n_0."""
    _check(F, P)
    if len(n0) != len(F) or steps < 0:
        raise ValueError("need len(n0) == k and steps >= 0")
    n = list(n0)  # @line L1
    out: List[List[float]] = []
    for _ in range(steps):  # @line L2
        n = [sum(f * x for f, x in zip(F, n))] + [p * x for p, x in zip(P, n)]  # @line L3
        out.append(n)  # @line L4
    return out  # @line L5


def survivorship(P: Sequence) -> List:
    """l_1 = 1 and l_i = P_1 ... P_(i-1)."""
    l = [1 + 0 * (P[0] if P else 0)]
    for p in P:
        l.append(l[-1] * p)
    return l


def characteristic(F: Sequence, P: Sequence) -> List:
    """Coefficients c_0..c_k of det(lambda I - L) = sum c_j lambda^(k - j)."""
    _check(F, P)
    l = survivorship(P)
    return [1] + [-f * li for f, li in zip(F, l)]


def net_reproductive_rate(F: Sequence, P: Sequence):
    """R_0 = sum F_i l_i, the expected offspring of a newborn over its life."""
    _check(F, P)
    return sum(f * li for f, li in zip(F, survivorship(P)))


def euler_lotka_root(F: Sequence[float], P: Sequence[float], tol: float = 1e-15) -> float:
    """The positive root of sum F_i l_i lambda^(-i) = 1, by bisection."""
    _check(F, P)
    l = survivorship(P)
    terms = [(i + 1, float(f * li)) for i, (f, li) in enumerate(zip(F, l)) if f > 0]
    if not terms:
        raise ValueError("need some F_i > 0")
    phi = lambda x: sum(c / x ** i for i, c in terms)
    lo, hi = 0.0, 1.0
    while phi(hi) > 1:
        hi *= 2
    lo = hi / 2
    while phi(lo) < 1:
        lo /= 2
    while hi - lo > tol * hi:
        mid = (lo + hi) / 2
        if phi(mid) > 1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def stable_distribution(F: Sequence[float], P: Sequence[float]) -> List[float]:
    """w_i proportional to l_i lambda^(-(i - 1)), with sum 1."""
    lam = euler_lotka_root(F, P)
    w = [float(li) / lam ** i for i, li in enumerate(survivorship(P))]
    s = sum(w)
    return [x / s for x in w]


def reproductive_values(F: Sequence[float], P: Sequence[float]) -> List[float]:
    """v_i = (lambda^(i - 1) / l_i) sum_(j >= i) F_j l_j lambda^(-j), so v_1 = 1."""
    lam = euler_lotka_root(F, P)
    l = [float(x) for x in survivorship(P)]
    k = len(F)
    return [lam ** i / l[i] * sum(F[j] * l[j] / lam ** (j + 1) for j in range(i, k)) for i in range(k)]


def power_iteration(F: Sequence[float], P: Sequence[float], iters: int = 10000,
                    tol: float = 1e-13) -> Tuple[float, List[float]]:
    """lambda_1 and w by repeated projection with normalisation to sum 1."""
    k = len(F)
    w = [1.0 / k] * k
    lam = 0.0
    for _ in range(iters):
        x = project(F, P, w, 1)[0]
        s = sum(x)
        x = [v / s for v in x]
        done = abs(s - lam) < tol * s and max(abs(a - b) for a, b in zip(x, w)) < tol
        lam, w = s, x
        if done:
            break
    return lam, w


def sensitivities(F: Sequence[float], P: Sequence[float]) -> Tuple[List[List[float]], List[List[float]]]:
    """s_ij = v_i w_j / <v, w> and the elasticities e_ij = a_ij s_ij / lambda."""
    lam = euler_lotka_root(F, P)
    w = stable_distribution(F, P)
    v = reproductive_values(F, P)
    vw = sum(a * b for a, b in zip(v, w))
    A = leslie(F, P)
    k = len(F)
    s = [[v[i] * w[j] / vw for j in range(k)] for i in range(k)]
    e = [[A[i][j] * s[i][j] / lam for j in range(k)] for i in range(k)]
    return s, e


def is_primitive(F: Sequence, P: Sequence) -> bool:
    """Some power of L is positive. Wielandt: checking power (k - 1)^2 + 1 is enough."""
    A = leslie(F, P)
    k = len(F)
    B = [[A[i][j] > 0 for j in range(k)] for i in range(k)]
    M = [row[:] for row in B]
    for _ in range((k - 1) ** 2):
        M = [[any(M[i][t] and B[t][j] for t in range(k)) for j in range(k)] for i in range(k)]
    return all(all(row) for row in M)


def gcd_rule(F: Sequence, P: Sequence) -> bool:
    """For F_k > 0: L is primitive iff the gcd of the ages i with F_i > 0 is 1."""
    if not F[-1] > 0:
        raise ValueError("the rule needs F_k > 0")
    g = 0
    for i, f in enumerate(F, start=1):
        if f > 0:
            g = math.gcd(g, i)
    return g == 1
