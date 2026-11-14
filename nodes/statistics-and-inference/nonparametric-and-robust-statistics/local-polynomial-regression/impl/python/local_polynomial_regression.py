# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-polynomial-regression/. The authors are listed in prov/C1XC0A.jsonl.

import math


def epanechnikov(u):
    """(3/4)(1 - u^2) on [-1, 1]; works with floats and Fractions."""
    return 3 * (1 - u * u) / 4 if -1 <= u <= 1 else 0 * u


def tricube(u):
    """(1 - |u|^3)^3 on [-1, 1], the weight of LOESS and LOWESS."""
    a = abs(u)
    return (1 - a * a * a) ** 3 if a < 1 else 0 * u


def bisquare(u):
    """(1 - u^2)^2 on [-1, 1], the robustness weight of LOWESS."""
    return (1 - u * u) ** 2 if abs(u) < 1 else 0 * u


def solve(A, b):
    """Gauss-Jordan elimination with pivoting on the largest entry.
    Exact for Fractions. Returns None if A is singular."""
    n = len(A)
    M = [list(row) + [v] for row, v in zip(A, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            return None
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * e for a, e in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def local_poly_coefficients(x, xs, ys, h, degree=1, kernel=epanechnikov, delta=None):
    """Weighted least squares fit of y on 1, (x_i - x), ..., (x_i - x)^p.

    beta_k estimates m^(k)(x) / k!. Returns None if the local design is singular.
    """
    n = len(xs)
    w = [kernel((xi - x) / h) * (1 if delta is None else delta[i])  # @line L1
         for i, xi in enumerate(xs)]
    p = degree
    d = [xi - x for xi in xs]
    S = [[sum(w[i] * d[i] ** (j + k) for i in range(n)) for k in range(p + 1)]  # @line L2
         for j in range(p + 1)]
    t = [sum(w[i] * d[i] ** j * ys[i] for i in range(n)) for j in range(p + 1)]
    return solve(S, t)  # @line L3


def local_poly(x, xs, ys, h, degree=1, kernel=epanechnikov, delta=None):
    """The local polynomial estimate of m(x): the intercept beta_0."""
    beta = local_poly_coefficients(x, xs, ys, h, degree, kernel, delta)
    return None if beta is None else beta[0]


def local_linear_closed_form(x, xs, ys, h, kernel=epanechnikov):
    """Reference: m(x) = sum w_i (S2 - S1 d_i) y_i / (S0 S2 - S1^2), d_i = x_i - x."""
    w = [kernel((xi - x) / h) for xi in xs]
    d = [xi - x for xi in xs]
    s0 = sum(w)
    s1 = sum(wi * di for wi, di in zip(w, d))
    s2 = sum(wi * di * di for wi, di in zip(w, d))
    den = s0 * s2 - s1 * s1
    if den == 0:
        return None
    return sum(wi * (s2 - s1 * di) * yi for wi, di, yi in zip(w, d, ys)) / den


def median(v):
    s = sorted(v)
    k = len(s)
    return s[k // 2] if k % 2 else (s[k // 2 - 1] + s[k // 2]) / 2


def lowess(xs, ys, frac=2 / 3, iterations=2):
    """LOWESS of Cleveland (1979): local linear fits with tricube weights over
    the k = round(frac n) nearest neighbours, then robustness iterations with
    bisquare weights of the residuals scaled by 6 times their median absolute value.

    Returns the fitted values at the x_i.
    """
    n = len(xs)
    k = max(2, min(n, int(frac * n + 0.5)))
    delta = [1] * n  # @line L4
    # h_i: the distance from x_i to its k-th nearest x_j (x_i itself counts).
    hs = [sorted(abs(xj - xi) for xj in xs)[k - 1] for xi in xs]
    fit = list(ys)
    for it in range(iterations + 1):  # @line L5
        fit = []
        for i in range(n):
            h = hs[i]
            if h == 0:
                fit.append(ys[i])
                continue
            v = local_poly(xs[i], xs, ys, h, 1, tricube, delta)  # @line L6
            if v is None:  # too few distinct points with weight: fall back to degree 0
                v = local_poly(xs[i], xs, ys, h, 0, tricube, delta)
            fit.append(ys[i] if v is None else v)
        if it == iterations:
            break
        r = [y - f for y, f in zip(ys, fit)]  # @line L7
        s = median([abs(v) for v in r])
        if s == 0:  # @line L8
            delta = [1 if v == 0 else 0 for v in r]
        else:
            delta = [bisquare(v / (6 * s)) for v in r]
    return fit  # @line L9
