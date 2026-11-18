# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verbs-and-adverbs/. The authors are listed in prov/G3VDNR.jsonl.
"""Verbs and adverbs interpolation (Rose, Cohen and Bodenheimer 1998).

A verb has n time aligned example motions. Example i has an adverb vector
p_i (a numbers, for example speed and turn) and a value vector y_i (q
numbers, for example the control points of every joint curve after time
alignment to a common key time structure). The interpolant is

    y(p) = c_0 + C p + sum_i w_i R_i(|p - p_i|),

computed in two steps:
  1. the linear part (c_0, C) by least squares over the examples;
  2. the radial part: the residuals of step 1 are interpolated exactly by
     the radial functions R_i(d) = B(2 d / alpha_i), where B is the cubic
     B-spline with support [0, 2] and alpha_i is twice the distance from p_i
     to the nearest other example. So R_i is zero beyond alpha_i.

The matrix K[k][i] = R_i(|p_k - p_i|) of step 2 is not symmetric, because
the alpha_i differ, and its invertibility is not proved; solve() raises an
error if it is singular.
"""

import math


def bspline(s):
    """The uniform cubic B-spline B(s), s >= 0, with B(0) = 2/3, zero for s >= 2."""
    s = abs(s)
    if s >= 2.0:
        return 0.0
    if s >= 1.0:
        return (2.0 - s) ** 3 / 6.0
    return 2.0 / 3.0 - s * s + 0.5 * s ** 3


def solve(A, b, eps=1e-14):
    """Gaussian elimination with partial pivoting. b has one row per row of
    A, and each row of b holds one value per right hand side."""
    n = len(A)
    A = [row[:] for row in A]
    B = [list(r) for r in b]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        if abs(A[p][c]) < eps:
            raise ValueError("singular matrix")
        A[c], A[p] = A[p], A[c]
        B[c], B[p] = B[p], B[c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            if f:
                for k in range(c, n):
                    A[r][k] -= f * A[c][k]
                for k in range(len(B[r])):
                    B[r][k] -= f * B[c][k]
    X = [[0.0] * len(B[0]) for _ in range(n)]
    for r in range(n - 1, -1, -1):
        for k in range(len(B[0])):
            s = B[r][k] - sum(A[r][t] * X[t][k] for t in range(r + 1, n))
            X[r][k] = s / A[r][r]
    return X


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


class Verb:
    def __init__(self, adverbs, values):
        self.P = [list(p) for p in adverbs]
        self.Y = [list(y) for y in values]
        n, a = len(self.P), len(self.P[0])
        self.n, self.a, self.q = n, a, len(self.Y[0])
        # step 1: least squares for the linear part, by the normal equations
        X = [[1.0] + p for p in self.P]  # @line L1
        XtX = [[sum(X[r][i] * X[r][j] for r in range(n)) for j in range(a + 1)] for i in range(a + 1)]
        XtY = [[sum(X[r][i] * self.Y[r][k] for r in range(n)) for k in range(self.q)] for i in range(a + 1)]
        self.lin = solve(XtX, XtY)  # @line L2
        resid = [[self.Y[r][k] - self.linear(self.P[r])[k] for k in range(self.q)] for r in range(n)]  # @line L3
        # step 2: radial functions through the residuals
        self.alpha = []
        for i in range(n):
            near = min(dist(self.P[i], self.P[k]) for k in range(n) if k != i) if n > 1 else 1.0
            self.alpha.append(2.0 * near)  # @line L4
        K = [[self.radial(i, self.P[r]) for i in range(n)] for r in range(n)]  # @line L5
        self.w = solve(K, resid)  # @line L6
        self.resid = resid

    def linear(self, p):
        return [self.lin[0][k] + sum(self.lin[1 + l][k] * p[l] for l in range(self.a))
                for k in range(self.q)]

    def radial(self, i, p):
        return bspline(2.0 * dist(p, self.P[i]) / self.alpha[i])

    def __call__(self, p):
        y = self.linear(p)
        for i in range(self.n):
            r = self.radial(i, p)
            if r:
                for k in range(self.q):
                    y[k] += self.w[i][k] * r
        return y  # @line L7
