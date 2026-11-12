# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fastica/. The authors are listed in prov/6J62KD.jsonl.

"""FastICA: the fixed-point algorithm of Hyvärinen and Oja.

After whitening, each weight vector w is updated by

    w+ = mean(z g(w.z)) - mean(g'(w.z)) w,   then w+ is normalized,

with g the derivative of a contrast G. Several components are found one by
one with Gram-Schmidt deflation, or all at once with symmetric decorrelation
W <- (W W^T)^(-1/2) W.
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


def whiten(xs: list[Vector]) -> tuple[list[Vector], Matrix]:
    """Return (whitened points z_t, the whitening matrix V); z_t = V (x_t - mean)."""
    n, d = len(xs), len(xs[0])
    mean = [sum(x[j] for x in xs) / n for j in range(d)]
    xc = [[x[j] - mean[j] for j in range(d)] for x in xs]
    cov = [[sum(x[i] * x[j] for x in xc) / n for j in range(d)] for i in range(d)]
    lam, e = jacobi_eigh(cov)
    if lam[-1] <= 1e-12 * lam[0]:
        raise ValueError("the covariance is singular; reduce the dimension first")
    v = [[e[j][k] / math.sqrt(lam[k]) for j in range(d)] for k in range(d)]
    z = [[sum(v[k][j] * x[j] for j in range(d)) for k in range(d)] for x in xc]
    return z, v


def nonlinearity(name: str, a: float = 1.0):
    """Return (g, g') for the contrasts 'pow3' (kurtosis), 'logcosh' and 'exp'."""
    if name == "pow3":
        return (lambda u: u ** 3), (lambda u: 3.0 * u * u)
    if name == "logcosh":
        return (lambda u: math.tanh(a * u)), (lambda u: a * (1.0 - math.tanh(a * u) ** 2))
    if name == "exp":
        return (lambda u: u * math.exp(-u * u / 2.0)), (lambda u: (1.0 - u * u) * math.exp(-u * u / 2.0))
    raise ValueError("unknown nonlinearity " + name)


def _normalize(w: Vector) -> Vector:
    s = math.sqrt(sum(x * x for x in w))
    return [x / s for x in w]


def one_unit_update(z: list[Vector], w: Vector, g, dg) -> Vector:
    """The FastICA fixed-point step w+ = E[z g(w.z)] - E[g'(w.z)] w (not normalized)."""
    n, d = len(z), len(w)
    acc = [0.0] * d
    mean_dg = 0.0
    for zt in z:
        u = sum(a * b for a, b in zip(w, zt))
        gu = g(u)
        for j in range(d):
            acc[j] += zt[j] * gu
        mean_dg += dg(u)
    return [acc[j] / n - (mean_dg / n) * w[j] for j in range(d)]


def fastica_deflation(xs: list[Vector], k: int, rng: random.Random, g_name: str = "logcosh",
                      tol: float = 1e-10, max_iter: int = 200) -> tuple[Matrix, list[int]]:
    """Return (unmixing matrix B with k rows, the iteration count of each unit)."""
    z, v = whiten(xs)  # @line L1
    d = len(v)
    g, dg = nonlinearity(g_name)
    ws: list[Vector] = []
    counts = []
    for _ in range(k):  # @line L2
        w = _normalize([rng.gauss(0.0, 1.0) for _ in range(d)])  # @line L3
        it = 0
        while True:  # @line L4
            it += 1
            w_new = one_unit_update(z, w, g, dg)  # @line L5
            for q in ws:  # @line L6
                dot = sum(a * b for a, b in zip(w_new, q))
                w_new = [a - dot * b for a, b in zip(w_new, q)]
            w_new = _normalize(w_new)  # @line L7
            done = abs(abs(sum(a * b for a, b in zip(w_new, w))) - 1.0) < tol
            w = w_new
            if done or it >= max_iter:  # @line L8
                break
        ws.append(w)
        counts.append(it)
    unmix = [[sum(w[i] * v[i][j] for i in range(d)) for j in range(d)] for w in ws]
    return unmix, counts  # @line L9


def symmetric_decorrelation(w: Matrix) -> Matrix:
    """Return (W W^T)^(-1/2) W, which has orthonormal rows."""
    k = len(w)
    m = [[sum(a * b for a, b in zip(w[i], w[j])) for j in range(k)] for i in range(k)]
    lam, e = jacobi_eigh(m)
    inv_sqrt = [[sum(e[i][t] * e[j][t] / math.sqrt(lam[t]) for t in range(k)) for j in range(k)] for i in range(k)]
    return [[sum(inv_sqrt[i][t] * w[t][j] for t in range(k)) for j in range(len(w[0]))] for i in range(k)]


def fastica_symmetric(xs: list[Vector], k: int, rng: random.Random, g_name: str = "logcosh",
                      tol: float = 1e-10, max_iter: int = 200) -> tuple[Matrix, int]:
    """Return (unmixing matrix B with k rows, the number of iterations) with all units updated in parallel."""
    z, v = whiten(xs)
    d = len(v)
    g, dg = nonlinearity(g_name)
    w = symmetric_decorrelation([[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(k)])
    it = 0
    while True:
        it += 1
        w_new = symmetric_decorrelation([one_unit_update(z, row, g, dg) for row in w])
        change = max(abs(abs(sum(a * b for a, b in zip(r1, r2))) - 1.0) for r1, r2 in zip(w_new, w))
        w = w_new
        if change < tol or it >= max_iter:
            break
    unmix = [[sum(row[i] * v[i][j] for i in range(d)) for j in range(d)] for row in w]
    return unmix, it


def population_kurtosis_step(kappa: Vector, w: Vector) -> Vector:
    """One FastICA step with g(u) = u^3 on the exact distribution, in source coordinates.

    For whitened independent sources with fourth cumulants kappa_i and a unit
    vector w, E[s g(w.s)] - E[g'(w.s)] w has coordinates kappa_i w_i^3.
    """
    return _normalize([k * x ** 3 for k, x in zip(kappa, w)])


def amari_index(p: Matrix) -> float:
    """Amari's performance index of P = B A, scaled to [0, 1]. It is 0 iff P is a scaled permutation."""
    m = len(p)
    a = [[abs(x) for x in row] for row in p]
    rows = sum(sum(row) / max(row) - 1.0 for row in a)
    cols = sum(sum(a[i][j] for i in range(m)) / max(a[i][j] for i in range(m)) - 1.0 for j in range(m))
    return (rows + cols) / (2.0 * m * (m - 1))
