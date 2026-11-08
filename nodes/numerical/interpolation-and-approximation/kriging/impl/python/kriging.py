# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kriging/. The authors are listed in prov/ZHD0F7.jsonl.
"""Ordinary and simple kriging with a user-supplied covariance function (standard library only)."""
import math


def gaussian_cov(sill=1.0, length=1.0):
    return lambda r: sill * math.exp(-(r / length) ** 2)


def exponential_cov(sill=1.0, length=1.0):
    return lambda r: sill * math.exp(-r / length)


def matern32_cov(sill=1.0, length=1.0):
    def c(r):
        a = math.sqrt(3.0) * r / length
        return sill * (1.0 + a) * math.exp(-a)
    return c


def _dist(p, q):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def cholesky(K):
    """Lower triangular L with K = L L^T; raises ValueError if K is not positive definite."""
    n = len(K)
    L = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = K[j][j] - math.fsum(L[j][k] * L[j][k] for k in range(j))
        if not s > 0.0:
            raise ValueError("covariance matrix is not positive definite (repeated points? add a nugget)")
        L[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            L[i][j] = (K[i][j] - math.fsum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    return L


def _forward(L, b):
    n = len(L)
    z = [0.0] * n
    for i in range(n):
        z[i] = (b[i] - math.fsum(L[i][k] * z[k] for k in range(i))) / L[i][i]
    return z


def _backward(L, z):
    n = len(L)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (z[i] - math.fsum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
    return x


class Kriging:
    """Kriging predictor for points (tuples or numbers) with isotropic covariance cov(r).

    mean=None gives ordinary kriging (unknown constant mean, estimated by
    generalized least squares); a number gives simple kriging with that mean.
    nugget is added to the diagonal (measurement noise); with nugget 0 the
    predictor interpolates.
    """

    def __init__(self, points, values, cov, mean=None, nugget=0.0):
        if len(points) != len(values) or not points:
            raise ValueError("need equal, nonzero numbers of points and values")
        self.pts = [tuple(p) if isinstance(p, (tuple, list)) else (p,) for p in points]
        self.cov = cov
        self.nugget = nugget
        n = len(self.pts)
        K = [[cov(_dist(self.pts[i], self.pts[j])) for j in range(n)] for i in range(n)]  # @line L1
        for i in range(n):
            K[i][i] += nugget
        self.L = cholesky(K)  # @line L2
        y = [float(v) for v in values]
        if mean is None:  # @line L3
            self.a = _backward(self.L, _forward(self.L, [1.0] * n))
            b = _backward(self.L, _forward(self.L, y))
            self.s = math.fsum(self.a)
            self.beta = math.fsum(b) / self.s
            self.w = [bi - self.beta * ai for ai, bi in zip(self.a, b)]
        else:
            self.a = None
            self.beta = float(mean)
            self.w = _backward(self.L, _forward(self.L, [v - self.beta for v in y]))

    def _k(self, x):
        x = tuple(x) if isinstance(x, (tuple, list)) else (x,)
        return x, [self.cov(_dist(x, p)) for p in self.pts]  # @line L4

    def predict(self, x):
        _, k = self._k(x)
        return self.beta + math.fsum(ki * wi for ki, wi in zip(k, self.w))  # @line L5

    def variance(self, x):
        """Kriging variance of the prediction error (of the noise-free value)."""
        x, k = self._k(x)
        r = _forward(self.L, k)  # @line L6
        v = self.cov(0.0) - math.fsum(t * t for t in r)
        if self.a is not None:
            g = 1.0 - math.fsum(ai * ki for ai, ki in zip(self.a, k))
            v += g * g / self.s
        return max(v, 0.0)

    def weights(self, x):
        """The kriging weights lambda with prediction = sum lambda_i y_i (ordinary or simple)."""
        _, k = self._k(x)
        lam = _backward(self.L, _forward(self.L, k))
        if self.a is not None:
            g = (1.0 - math.fsum(lam)) / self.s
            lam = [li + g * ai for li, ai in zip(lam, self.a)]
        return lam
