# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projection-pursuit/. The authors are listed in prov/WHZFZK.jsonl.

"""Projection pursuit: search for the directions whose 1D projections are most interesting.

The data are sphered first, so every unit direction gives a projection with
mean 0 and variance 1, and an index measures how far the projection is from
Gaussian. The search uses random restarts and a pattern search on the unit
sphere. Later directions are kept orthogonal to earlier ones in the sphered
space (structure removal by deflation).
"""

import math
import random

Vector = list[float]
Matrix = list[list[float]]


def jacobi_eigh(a: Matrix, tol: float = 1e-14, max_sweeps: int = 100) -> tuple[Vector, Matrix]:
    """Eigenvalues (descending) and eigenvectors (as columns) of a symmetric matrix."""
    d = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(d) for j in range(d) if i != j)
        scale = sum(m[i][i] ** 2 for i in range(d)) + off
        if off <= tol * tol * max(scale, 1e-300):
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    m[k][p], m[k][q] = c * m[k][p] - s * m[k][q], s * m[k][p] + c * m[k][q]
                for k in range(d):
                    m[p][k], m[q][k] = c * m[p][k] - s * m[q][k], s * m[p][k] + c * m[q][k]
                for k in range(d):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    order = sorted(range(d), key=lambda i: -m[i][i])
    return [m[i][i] for i in order], [[v[r][i] for i in order] for r in range(d)]


def sphere(xs: list[Vector]) -> tuple[list[Vector], Matrix]:
    """Return (sphered points z_t = V (x_t - mean), V). The z_t have mean 0 and covariance I."""
    n, d = len(xs), len(xs[0])
    mean = [sum(x[j] for x in xs) / n for j in range(d)]
    xc = [[x[j] - mean[j] for j in range(d)] for x in xs]
    cov = [[sum(x[i] * x[j] for x in xc) / n for j in range(d)] for i in range(d)]
    lam, e = jacobi_eigh(cov)
    if lam[-1] <= 1e-12 * lam[0]:
        raise ValueError("the covariance is singular; reduce the dimension first")
    v = [[e[j][k] / math.sqrt(lam[k]) for j in range(d)] for k in range(d)]
    return [[sum(v[k][j] * x[j] for j in range(d)) for k in range(d)] for x in xc], v


def _standardize(y: Vector) -> Vector:
    n = len(y)
    mu = sum(y) / n
    sd = math.sqrt(sum((v - mu) ** 2 for v in y) / n)
    return [(v - mu) / sd for v in y]


def moment_index(y: Vector) -> float:
    """Jones and Sibson's moment index (k3^2 + k4^2 / 4) / 12 of the standardized projection.

    It is the cumulant approximation of negentropy, k3^2 / 12 + k4^2 / 48.
    """
    u = _standardize(y)
    n = len(u)
    k3 = sum(v ** 3 for v in u) / n
    k4 = sum(v ** 4 for v in u) / n - 3.0
    return (k3 * k3 + k4 * k4 / 4.0) / 12.0


def _gauss_logcosh() -> float:
    """E[log cosh(nu)] for a standard Gaussian nu, by Simpson's rule on [-12, 12]."""
    m, a, b = 4000, -12.0, 12.0
    h = (b - a) / m
    total = 0.0
    for i in range(m + 1):
        x = a + i * h
        w = 1 if i in (0, m) else (4 if i % 2 else 2)
        total += w * math.log(math.cosh(x)) * math.exp(-x * x / 2.0)
    return total * h / 3.0 / math.sqrt(2.0 * math.pi)


GAUSS_LOGCOSH = _gauss_logcosh()


def negentropy_index(y: Vector) -> float:
    """Hyvärinen's negentropy approximation (E[log cosh u] - E[log cosh nu])^2 of the standardized projection."""
    u = _standardize(y)
    return (sum(math.log(math.cosh(v)) for v in u) / len(u) - GAUSS_LOGCOSH) ** 2


def friedman_tukey_index(y: Vector, radius: float = 0.5) -> float:
    """A Friedman-Tukey style local density: the mean of (R - |u_i - u_j|)_+ over all pairs.

    For sphered data the spread factor of the original index is constant, so
    only the local density term is kept. It costs O(n^2) per evaluation.
    """
    u = _standardize(y)
    n = len(u)
    total = 0.0
    for i in range(n):
        for j in range(n):
            r = abs(u[i] - u[j])
            if r < radius:
                total += radius - r
    return total / (n * n)


def _project_out(w: Vector, basis: list[Vector]) -> Vector:
    for q in basis:
        dot = sum(a * b for a, b in zip(w, q))
        w = [a - dot * b for a, b in zip(w, q)]
    return w


def _unit(w: Vector) -> Vector | None:
    s = math.sqrt(sum(a * a for a in w))
    return None if s < 1e-12 else [a / s for a in w]


def _score(z: list[Vector], w: Vector, index) -> float:
    return index([sum(a * b for a, b in zip(w, zt)) for zt in z])


def projection_pursuit(xs: list[Vector], k: int, rng: random.Random, index=moment_index,
                       restarts: int = 5, h0: float = 0.5, h_min: float = 1e-6,
                       max_moves: int = 1000) -> tuple[Matrix, list[float]]:
    """Return (directions as rows in the original coordinates, their index values).

    The projection of a point x on direction p is directions[p] . (x - mean).
    """
    z, v = sphere(xs)  # @line L1
    d = len(v)
    found: list[Vector] = []
    values: list[float] = []
    for _ in range(k):  # @line L2
        best_w, best_val = None, -math.inf
        for _ in range(restarts):  # @line L3
            w = None
            while w is None:
                w = _unit(_project_out([rng.gauss(0.0, 1.0) for _ in range(d)], found))
            cur = _score(z, w, index)
            h = h0
            moves = 0
            while h > h_min:  # @line L4
                cand_best, cand_val = None, cur
                for j in range(d):  # @line L5
                    for sign in (1.0, -1.0):
                        trial = w[:]
                        trial[j] += sign * h
                        trial = _unit(_project_out(trial, found))
                        if trial is None:
                            continue
                        val = _score(z, trial, index)
                        if val > cand_val:
                            cand_best, cand_val = trial, val
                if cand_best is not None and moves < max_moves:  # @line L6
                    w, cur = cand_best, cand_val
                    moves += 1
                else:
                    h /= 2.0
                    moves = 0
            if cur > best_val:  # @line L7
                best_w, best_val = w, cur
        found.append(best_w)
        values.append(best_val)
    directions = [[sum(w[i] * v[i][j] for i in range(d)) for j in range(d)] for w in found]
    return directions, values  # @line L8
