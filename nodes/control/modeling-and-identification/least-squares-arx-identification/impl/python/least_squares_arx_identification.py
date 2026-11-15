# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-arx-identification/. The authors are listed in prov/HXP9D6.jsonl.

"""Least squares identification of an ARX model.

The ARX model with orders na, nb and input delay nk is

    y(t) + a_1 y(t-1) + ... + a_na y(t-na)
        = b_1 u(t-nk) + ... + b_nb u(t-nk-nb+1) + e(t).

With the regressor phi(t) = (-y(t-1), ..., -y(t-na), u(t-nk), ...,
u(t-nk-nb+1)) and theta = (a_1, ..., a_na, b_1, ..., b_nb) this is the
linear regression y(t) = phi(t)^T theta + e(t). arx_ls returns the theta
that minimizes the sum of e(t)^2 over the samples t = t0, ..., N-1 whose
regressor is fully inside the data, t0 = max(na, nk + nb - 1).

Precondition: na >= 0, nb >= 1, nk >= 0 and the d by d matrix R = sum of
phi phi^T, d = na + nb, is nonsingular (the data are informative for the
model). With int or Fraction data the result is exact (Fraction).

Cost: O(N d^2) to form R and f, and O(d^3) to solve, in the real RAM.
"""

from typing import Sequence

from ctlmat import solve


def arx_regressor(y: Sequence, u: Sequence, na: int, nb: int, nk: int, t: int) -> list:
    """Return phi(t) = (-y(t-1), ..., -y(t-na), u(t-nk), ..., u(t-nk-nb+1))."""
    return [-y[t - i] for i in range(1, na + 1)] + [u[t - nk - j] for j in range(nb)]


def first_sample(na: int, nb: int, nk: int) -> int:
    """Return t0 = max(na, nk + nb - 1), the first t with a full regressor."""
    return max(na, nk + nb - 1)


def arx_ls(y: Sequence, u: Sequence, na: int, nb: int, nk: int = 1) -> list:
    """Least squares estimate (a_1, ..., a_na, b_1, ..., b_nb) of an ARX model.

    Raises ValueError if the orders are invalid, the data are too short, or
    R is singular (the input is not persistently exciting enough, or the
    data are otherwise not informative).
    """
    if na < 0 or nb < 1 or nk < 0:
        raise ValueError("need na >= 0, nb >= 1 and nk >= 0")
    if len(y) != len(u):
        raise ValueError("y and u must have the same length")
    d = na + nb
    t0 = first_sample(na, nb, nk)  # @line L1
    if len(y) - t0 < d:
        raise ValueError("too few samples for the model orders")
    r = [[0] * d for _ in range(d)]  # @line L2
    f = [0] * d
    for t in range(t0, len(y)):  # @line L3
        phi = arx_regressor(y, u, na, nb, nk, t)  # @line L4
        for i in range(d):
            pi = phi[i]
            if pi == 0:
                continue
            row = r[i]
            for j in range(d):
                row[j] += pi * phi[j]  # @line L5
            f[i] += pi * y[t]  # @line L6
    try:
        theta = solve(r, f)  # @line L8
    except ValueError:
        raise ValueError("R is singular: the data are not informative for this model") from None  # @line L7
    return theta  # @line L9


def arx_loss(theta: Sequence, y: Sequence, u: Sequence, na: int, nb: int, nk: int = 1):
    """Return the sum of squared equation errors y(t) - phi(t)^T theta over t >= t0."""
    s = 0
    for t in range(first_sample(na, nb, nk), len(y)):
        phi = arx_regressor(y, u, na, nb, nk, t)
        e = y[t] - sum(p * th for p, th in zip(phi, theta))
        s += e * e
    return s


def arx_simulate(a: Sequence, b: Sequence, nk: int, u: Sequence, e: Sequence = None, c: Sequence = ()) -> list:
    """Simulate A(q) y = B(q) u + C(q) e from rest (all signals 0 before t = 0).

    a = (a_1, ..., a_na), b = (b_1, ..., b_nb) with b_1 on u(t-nk), and
    c = (c_1, ..., c_nc) for the moving average of the noise (C = 1 when c
    is empty, which is the ARX case). e defaults to zero noise.
    """
    n = len(u)
    if e is None:
        e = [0] * n
    y = []
    for t in range(n):
        v = e[t]
        for i, ci in enumerate(c, start=1):
            if t - i >= 0:
                v += ci * e[t - i]
        for j, bj in enumerate(b):
            if t - nk - j >= 0:
                v += bj * u[t - nk - j]
        for i, ai in enumerate(a, start=1):
            if t - i >= 0:
                v -= ai * y[t - i]
        y.append(v)
    return y
