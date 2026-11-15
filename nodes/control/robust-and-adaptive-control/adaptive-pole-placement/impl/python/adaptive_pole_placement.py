# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-pole-placement/. The authors are listed in prov/G5MEWV.jsonl.

"""Indirect adaptive pole placement (a self-tuning regulator with a polynomial design).

Plant, in the forward shift operator q, of order n and delay one:

    A(q) y = B(q) u + e,   A = q^n + a_1 q^(n-1) + ... + a_n,
                           B = b_0 q^(n-1) + ... + b_(n-1).

Polynomials are lists of coefficients, highest power first. The
controller is R u = T u_c - S y with R monic of degree n - 1 and S of
degree n - 1. Given a wanted closed loop polynomial A_c (degree n) and an
observer polynomial A_o (degree n - 1), R and S solve the Diophantine
equation

    A R + B S = A_c A_o,

and T = t0 A_o with t0 = A_c(1) / B(1), so the closed loop is
y = t0 B / A_c u_c with static gain 1.

The adaptive loop estimates (a_1..a_n, b_0..b_(n-1)) by recursive least
squares, keeps b_0 at least b_min (projection), and solves the design for
the estimate at every sample (certainty equivalence). It keeps the last
controller when the Sylvester matrix of the estimate is close to singular.

diophantine is exact when the inputs are int or Fraction.
"""

import random

from ctlmat import det, polyadd, polymul, polyval, solve

__all__ = ["sylvester_matrix", "diophantine", "design", "app_simulate"]


def _pad(p, length):
    return [0] * (length - len(p)) + list(p)


def sylvester_matrix(A, B):
    """Matrix of the map (r_1..r_(n-1), s_0..s_(n-1)) -> coefficients of A R + B S.

    A is monic of degree n, B has degree at most n - 1 (padded to n
    coefficients). The rows are the coefficients of q^(2n-2) down to q^0.
    Its determinant is, up to sign, the resultant of A and B, so it is
    nonzero exactly when A and B are coprime.
    """
    n = len(A) - 1
    Bp = _pad(B, n)
    m = 2 * n - 1
    cols = []
    for i in range(1, n):
        cols.append(_pad(polymul(A, [1] + [0] * (n - 1 - i)), m))
    for j in range(n):
        cols.append(_pad(polymul(Bp, [1] + [0] * (n - 1 - j)), m)[-m:])
    return [[cols[c][r] for c in range(m)] for r in range(m)]


def diophantine(A, B, Acl):
    """Solve A R + B S = Acl for R (monic, degree n - 1) and S (degree n - 1).

    Acl must be monic of degree 2n - 1. Raises ValueError if A and B have a
    common factor (singular Sylvester matrix).
    """
    n = len(A) - 1
    m = 2 * n - 1
    lead = polymul(A, [1] + [0] * (n - 1))  # A q^(n-1)
    rhs = polyadd(Acl, [-c for c in lead])
    rhs = _pad(rhs, m)[-m:]
    x = solve(sylvester_matrix(A, B), rhs)
    R = [1] + list(x[:n - 1])
    S = list(x[n - 1:])
    return R, S


def design(A, B, Ac, Ao):
    """Return (R, S, T) of the pole placement design for the model (A, B)."""
    R, S = diophantine(A, B, polymul(Ac, Ao))
    t0 = polyval(Ac, 1) / polyval(B, 1)
    T = [t0 * c for c in Ao]
    return R, S, T


def app_simulate(a, b, Ac, Ao, uc, N, theta0, p0=100.0, b_min=0.1, tol=1e-6, sigma=0.0, seed=0,
                 adapt=True):
    """Run adaptive pole placement on the plant with coefficients a, b.

    a = [a_1..a_n], b = [b_0..b_(n-1)] define A and B of the module notes.
    uc(t) is the command. theta0 = (a_1..a_n, b_0..b_(n-1)) is the first
    estimate. With adapt=False the estimate stays at theta0. Process noise
    e_t is Gaussian with standard deviation sigma from random.Random(seed).
    Returns (thetas, ys, us): the estimate after each sample, the outputs
    and the inputs.
    """
    rng = random.Random(seed)
    n = len(a)
    d = 2 * n
    theta = [float(v) for v in theta0]  # @line L1
    P = [[p0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    try:
        R, S, T = design([1.0] + theta[:n], theta[n:], Ac, Ao)
    except (ValueError, ZeroDivisionError):
        R, S, T = [1.0] + [0.0] * (n - 1), [0.0] * n, [0.0] * n  # u = 0 until a design exists
    ys, us, ucs = [0.0] * n, [0.0] * n, [0.0] * n
    thetas = []
    for t in range(N):  # @line L2
        e = rng.gauss(0.0, sigma) if sigma > 0 else 0.0
        y = (-sum(a[i] * ys[-1 - i] for i in range(n))
             + sum(b[j] * us[-1 - j] for j in range(n)) + e)  # @line L3
        phi = [-ys[-1 - i] for i in range(n)] + [us[-1 - j] for j in range(n)]
        ys.append(y)
        if adapt:
            Pphi = [sum(P[i][j] * phi[j] for j in range(d)) for i in range(d)]
            den = 1.0 + sum(phi[i] * Pphi[i] for i in range(d))
            eps = y - sum(phi[i] * theta[i] for i in range(d))
            theta = [theta[i] + Pphi[i] * eps / den for i in range(d)]  # @line L4
            P = [[P[i][j] - Pphi[i] * Pphi[j] / den for j in range(d)] for i in range(d)]
            if theta[n] < b_min:
                theta[n] = b_min  # @line L5
            Ah, Bh = [1.0] + theta[:n], theta[n:]  # @line L6
            if abs(det(sylvester_matrix(Ah, Bh))) > tol and abs(sum(Bh)) > tol:
                R, S, T = design(Ah, Bh, Ac, Ao)  # @line L7
        ucs.append(uc(t))
        # R u = T u_c - S y, divided by q^(n-1): coefficient k acts on lag k
        u = (sum(T[k] * ucs[-1 - k] for k in range(n)) - sum(S[k] * ys[-1 - k] for k in range(n))
             - sum(R[k] * us[-k] for k in range(1, n)))  # @line L8
        us.append(u)
        thetas.append(list(theta))
    return thetas, ys[n:], us[n:]  # @line L9
