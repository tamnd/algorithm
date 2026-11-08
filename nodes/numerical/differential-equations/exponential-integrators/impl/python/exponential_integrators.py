# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-integrators/. The authors are listed in prov/4R98K0.jsonl.

"""Exponential integrators for semilinear problems y' = A y + g(t, y).

The linear part is integrated exactly with the matrix exponential and the
phi-functions phi_1(Z) = (e^Z - I) Z^-1, phi_2(Z) = (e^Z - I - Z) Z^-2, which are
read off one exponential of a block matrix of size 3d. Two methods are given:
exponential Euler (order 1) and the two-stage exponential Runge-Kutta method
ETD2RK of Cox and Matthews (order 2).
"""

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, List

# A step count within this relative amount of an integer is rounded to it.
GRID_SLACK = 1e-9
# Taylor terms are added until their 1-norm drops below this.
TAYLOR_TOL = 1e-18
MAX_TERMS = 40


def mat_mul(X, Y):
    n, m, p = len(X), len(Y), len(Y[0])
    return [[sum(X[i][l] * Y[l][j] for l in range(m)) for j in range(p)] for i in range(n)]


def mat_vec(X, v):
    return [sum(xij * vj for xij, vj in zip(row, v)) for row in X]


def norm1(X):
    return max(sum(abs(X[i][j]) for i in range(len(X))) for j in range(len(X[0])))


def identity(n, one=1):
    return [[one if i == j else 0 * one for j in range(n)] for i in range(n)]


def expm(W):
    """exp(W) by scaling and squaring with a Taylor polynomial; returns (exp(W), squarings)."""
    n = len(W)
    s = 0
    nrm = norm1(W)
    while nrm > 0.5:
        nrm /= 2
        s += 1
    scale = 2 ** s
    V = [[w / scale for w in row] for row in W]
    one = Fraction(1) if any(isinstance(w, Fraction) for row in W for w in row) else 1.0
    S = identity(n, one)
    term = identity(n, one)
    for j in range(1, MAX_TERMS):
        term = [[x / j for x in row] for row in mat_mul(term, V)]
        if all(x == 0 for row in term for x in row):
            break
        S = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(S, term)]
        if not isinstance(one, Fraction) and norm1(term) < TAYLOR_TOL:
            break
    for _ in range(s):
        S = mat_mul(S, S)
    return S, s


def phi_blocks(A, k):
    """(e^(kA), phi_1(kA), phi_2(kA)) from one exponential of a 3d x 3d block matrix."""
    d = len(A)
    one = Fraction(1) if isinstance(k, Fraction) else 1.0
    W = [[0 * one] * (3 * d) for _ in range(3 * d)]
    for i in range(d):
        for j in range(d):
            W[i][j] = k * A[i][j]
        W[i][d + i] = one
        W[d + i][2 * d + i] = one
    X, s = expm(W)
    E = [row[:d] for row in X[:d]]
    P1 = [row[d:2 * d] for row in X[:d]]
    P2 = [row[2 * d:] for row in X[:d]]
    return E, P1, P2, s


def phi(kidx: int, z: float) -> float:
    """Scalar phi_k(z) = sum_(j>=0) z^j / (j + k)!, computed without cancellation.

    For |z| < 1 the Taylor series is summed; otherwise phi_0 = e^z and the
    recurrence phi_(j+1)(z) = (phi_j(z) - 1/j!) / z is used, which is stable there.
    """
    if abs(z) < 1:
        total, term, j = 0.0, 1.0 / math.factorial(kidx), 0
        while abs(term) > 1e-18 * max(1.0, abs(total)) or j < 2:
            total += term
            j += 1
            term *= z / (j + kidx)
        return total
    val = math.exp(z)
    for j in range(kidx):
        val = (val - 1.0 / math.factorial(j)) / z
    return val


@dataclass
class ExpResult:
    """Final time and value, steps, evaluations of g, matrix-vector products, squarings."""

    t: Any
    y: Any
    steps: int
    g_evals: int
    matvecs: int
    squarings: int


def exponential_rk(A, g: Callable, t0, y0, T, h, method: str = "etd2rk") -> ExpResult:
    """Integrate y' = A y + g(t, y) from t0 to T with N equal steps of length at most h.

    A is a d x d list of lists or a number (then y is a scalar). method is
    "etd2rk" (order 2) or "euler" (exponential Euler, order 1).
    """
    if method not in ("etd2rk", "euler"):
        raise ValueError("unknown method")
    if h <= 0:
        raise ValueError("step size must be positive")
    if T < t0:
        raise ValueError("T must not precede t0")
    scalar = not isinstance(A, (list, tuple))
    Am = [[A]] if scalar else [list(r) for r in A]
    y = [y0] if scalar else list(y0)
    out = (lambda v: v[0]) if scalar else (lambda v: v)
    if scalar:
        G = lambda t, v: [g(t, v[0])]
    else:
        G = lambda t, v: list(g(t, v))
    if T == t0:
        return ExpResult(t0, out(y), 0, 0, 0, 0)
    span = T - t0
    N = max(1, math.ceil(span / h - GRID_SLACK))                   # @line L1
    k = span / N
    E, P1, P2, s = phi_blocks(Am, k)                               # @line L2
    evals = matvecs = 0
    t = t0
    for n in range(N):                                             # @line L3
        Gn = G(t, y)                                               # @line L4
        a = [p + k * q for p, q in zip(mat_vec(E, y), mat_vec(P1, Gn))]   # @line L5
        evals += 1
        matvecs += 2
        tn = T if n == N - 1 else t0 + (n + 1) * k
        if method == "etd2rk":
            D = [p - q for p, q in zip(G(tn, a), Gn)]              # @line L6
            y = [p + k * q for p, q in zip(a, mat_vec(P2, D))]     # @line L7
            evals += 1
            matvecs += 1
        else:
            y = a
        t = tn
    return ExpResult(t, out(y), N, evals, matvecs, s)              # @line L8
