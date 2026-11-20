# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strong-stability-preserving-runge-kutta/. The authors are listed in prov/4YEW5E.jsonl.

"""Explicit SSP Runge-Kutta methods in Shu-Osher form for the semidiscrete system u' = L(u).

A method with s stages has lower triangular tables alpha and beta, where row i - 1 holds the
coefficients of stage i on the stages 0, ..., i - 1:

    y_0 = u,  y_i = sum over k < i of (alpha[i-1][k] y_k + dt beta[i-1][k] L(y_k)),  u_new = y_s.

States are lists of numbers. The arithmetic is generic, so Fraction data give exact results.
"""

from fractions import Fraction as Fr


def shu_osher_step(u: list, rhs, dt, alpha: list, beta: list) -> list:
    """One step of the method with tables alpha and beta. Each L(y_k) is computed once."""
    ys = [list(u)]  # @line L1
    ls = []
    for i in range(1, len(alpha) + 1):  # @line L2
        ls.append(rhs(ys[i - 1]))
        a, b = alpha[i - 1], beta[i - 1]
        y = [0] * len(u)
        for k in range(i):  # @line L3
            if a[k] or b[k]:
                y = [yv + a[k] * yk + dt * b[k] * lk for yv, yk, lk in zip(y, ys[k], ls[k])]
        ys.append(y)
    return ys[-1]  # @line L4


def ssp_coefficient(alpha: list, beta: list):
    """The SSP coefficient C of a Shu-Osher form: min of alpha/beta over beta > 0, and 0 if any entry is negative."""
    c = None
    for a_row, b_row in zip(alpha, beta):
        for a, b in zip(a_row, b_row):
            if a < 0 or b < 0:  # @line L5
                return Fr(0)
            if b > 0:  # @line L6
                c = a / b if c is None else min(c, a / b)
    return c


def _ssprk104():
    s = Fr(1, 6)
    alpha = [[Fr(0)] * i for i in range(1, 11)]
    beta = [[Fr(0)] * i for i in range(1, 11)]
    for i in (1, 2, 3, 4, 6, 7, 8, 9):
        alpha[i - 1][i - 1], beta[i - 1][i - 1] = Fr(1), s
    alpha[4][0], alpha[4][4], beta[4][4] = Fr(3, 5), Fr(2, 5), Fr(2, 5) * s
    alpha[9][0], alpha[9][4], alpha[9][9] = Fr(1, 25), Fr(9, 25), Fr(3, 5)
    beta[9][4], beta[9][9] = Fr(9, 25) * s, Fr(3, 5) * s
    return alpha, beta


# name: (alpha, beta, order)
METHODS = {
    "forward-euler": ([[Fr(1)]], [[Fr(1)]], 1),
    "ssprk22": ([[Fr(1)], [Fr(1, 2), Fr(1, 2)]], [[Fr(1)], [Fr(0), Fr(1, 2)]], 2),
    "ssprk33": (
        [[Fr(1)], [Fr(3, 4), Fr(1, 4)], [Fr(1, 3), Fr(0), Fr(2, 3)]],
        [[Fr(1)], [Fr(0), Fr(1, 4)], [Fr(0), Fr(0), Fr(2, 3)]],
        3,
    ),
    "ssprk104": _ssprk104() + (4,),
}


def integrate(u0: list, rhs, dt, steps: int, method: str = "ssprk33") -> list:
    """Take the given number of steps of a method from METHODS."""
    alpha, beta, _ = METHODS[method]
    if not isinstance(dt, Fr):
        alpha = [[float(a) for a in row] for row in alpha]
        beta = [[float(b) for b in row] for row in beta]
    u = list(u0)
    for _ in range(steps):
        u = shu_osher_step(u, rhs, dt, alpha, beta)
    return u
