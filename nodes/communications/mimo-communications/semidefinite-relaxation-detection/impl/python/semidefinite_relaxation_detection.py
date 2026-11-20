# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semidefinite-relaxation-detection/. The authors are listed in prov/QN7FSW.jsonl.

"""Semidefinite relaxation (SDR) detection of BPSK and 4-QAM vectors.

The model is y = H x + w with x a vector of BPSK (constel.pam(2)) or 4-QAM
(constel.qam(4)) points. In the real-valued model every real symbol is a b_i
with b_i in {-1, +1}, so ML detection is

    minimize ||y_r - G b||^2 over b in {-1, +1}^N,   G = a H_r.

With the extra variable t in {-1, +1} and v = (b, t), the metric is v^T Q v
for Q = [[G^T G, -G^T y_r], [-y_r^T G, y_r^T y_r]], and the SDR replaces
v v^T by any positive semidefinite X with unit diagonal:

    minimize trace(Q X) subject to X_ii = 1 and X positive semidefinite.

This file is a teaching solver. It solves the SDR by the mixing method, a
low-rank coordinate descent over unit vectors u_i with X_ij = u_i . u_j, and
it does not claim the accuracy of an interior-point solver. Its lower bound
is always valid, because it comes from a dual feasible point that is built
from the smallest eigenvalue of Q - Diag(lambda) (Jacobi eigenvalue method).
Candidates come from randomized hyperplane rounding.
"""

import math
import random

import constel


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _real_model(y, h, points):
    """(G, yr, kind) with ||y - H x||^2 = ||yr - G b||^2 for b in {-1, +1}^N."""
    if len(points) == 2 and all(abs(p - q) < 1e-12 for p, q in zip(points, constel.pam(2))):
        a, kind = 1.0, "pam"
    elif len(points) == 4 and all(abs(p - q) < 1e-12 for p, q in zip(points, constel.qam(4))):
        a, kind = 1.0 / math.sqrt(2.0), "qam"
    else:
        raise ValueError("points must be constel.pam(2) or constel.qam(4)")
    yr = [complex(v).real for v in y] + [complex(v).imag for v in y]
    if kind == "qam":
        top = [[a * complex(c).real for c in row] + [-a * complex(c).imag for c in row] for row in h]
        bot = [[a * complex(c).imag for c in row] + [a * complex(c).real for c in row] for row in h]
    else:
        top = [[complex(c).real for c in row] for row in h]
        bot = [[complex(c).imag for c in row] for row in h]
    return top + bot, yr, kind


def homogeneous_matrix(g: list[list[float]], yr: list[float]) -> list[list[float]]:
    """Q of size N + 1 with (b, 1)^T Q (b, 1) = ||yr - G b||^2."""
    n = len(g[0])
    cols = [[row[k] for row in g] for k in range(n)]
    q = [[_dot(cols[i], cols[j]) for j in range(n)] + [-_dot(cols[i], yr)] for i in range(n)]
    q.append([-_dot(cols[j], yr) for j in range(n)] + [_dot(yr, yr)])
    return q


def mixing_method(q: list[list[float]], rank: int, sweeps: int, rng: random.Random, tol: float = 1e-10):
    """Unit vectors u_0, ..., u_N in R^rank that locally minimize sum_ij Q_ij u_i . u_j."""
    n = len(q)
    u = []
    for _ in range(n):
        v = [rng.gauss(0.0, 1.0) for _ in range(rank)]
        s = math.sqrt(_dot(v, v))
        u.append([c / s for c in v])
    used = 0
    for used in range(1, sweeps + 1):  # @line L3
        change = 0.0
        for i in range(n):
            g = [0.0] * rank
            for j in range(n):
                if j != i and q[i][j] != 0.0:
                    g = [a + q[i][j] * c for a, c in zip(g, u[j])]
            s = math.sqrt(_dot(g, g))
            if s == 0.0:
                continue
            new = [-c / s for c in g]  # the exact minimizer over u_i  # @line L4
            change += sum((a - c) ** 2 for a, c in zip(new, u[i]))
            u[i] = new
        if change < tol:
            break
    return u, used


def jacobi_min_eig(a: list[list[float]]) -> float:
    """The smallest eigenvalue of a symmetric matrix, by the cyclic Jacobi method."""
    n = len(a)
    m = [list(map(float, row)) for row in a]
    for _ in range(100):
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22 * max(1.0, sum(m[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for r in range(p + 1, n):
                if abs(m[p][r]) < 1e-300:
                    continue
                theta = (m[r][r] - m[p][p]) / (2.0 * m[p][r])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    mkp, mkr = m[k][p], m[k][r]
                    m[k][p], m[k][r] = c * mkp - s * mkr, s * mkp + c * mkr
                for k in range(n):
                    mpk, mrk = m[p][k], m[r][k]
                    m[p][k], m[r][k] = c * mpk - s * mrk, s * mpk + c * mrk
    return min(m[i][i] for i in range(n))


def dual_bound(q: list[list[float]], u: list[list[float]]) -> tuple[float, float]:
    """(lower bound, relaxed value): a valid lower bound on the SDR value and trace(Q X) for X = U U^T."""
    n = len(q)
    lam = [sum(q[i][j] * _dot(u[i], u[j]) for j in range(n)) for i in range(n)]  # @line L5
    s = [[q[i][j] - (lam[i] if i == j else 0.0) for j in range(n)] for i in range(n)]
    emin = jacobi_min_eig(s)  # @line L6
    return sum(lam) + n * emin, sum(lam)


def sdr_detect(
    y: list[complex],
    h: list[list[complex]],
    points: list[complex],
    draws: int = 30,
    seed: int = 0,
    sweeps: int = 300,
    info: dict | None = None,
) -> list[int]:
    """Constellation indices from SDR with randomized rounding.

    If info is a dict, it receives the lower bound "lower" on the ML metric
    of the real model, the metric "metric" of the result, the relaxed value
    "relaxed" and the number of sweeps "sweeps".
    """
    if draws < 0:
        raise ValueError("draws must be at least 0")
    g, yr, kind = _real_model(y, h, points)  # @line L1
    q = homogeneous_matrix(g, yr)  # @line L2
    n = len(q)
    rank = min(n, int(math.ceil(math.sqrt(2.0 * n))) + 1)
    rng = random.Random(seed)
    u, used = mixing_method(q, rank, sweeps, rng)
    lower, relaxed = dual_bound(q, u)

    def metric(b):
        v = b + [1.0]
        return sum(q[i][j] * v[i] * v[j] for i in range(n) for j in range(n))

    best = [1.0 if _dot(u[i], u[-1]) >= 0 else -1.0 for i in range(n - 1)]  # @line L7
    best_m = metric(best)
    for _ in range(draws):
        r = [rng.gauss(0.0, 1.0) for _ in range(rank)]
        st = 1.0 if _dot(u[-1], r) >= 0 else -1.0
        b = [st * (1.0 if _dot(u[i], r) >= 0 else -1.0) for i in range(n - 1)]  # @line L8
        mb = metric(b)
        if mb < best_m:
            best, best_m = b, mb
    if info is not None:
        info.update(lower=lower, metric=best_m, relaxed=relaxed, sweeps=used)
    nc = len(h[0])
    a = 1.0 if kind == "pam" else 1.0 / math.sqrt(2.0)
    if kind == "qam":
        x = [complex(a * best[k], a * best[nc + k]) for k in range(nc)]
    else:
        x = [complex(best[k]) for k in range(nc)]
    return [constel.ml_detect(v, points) for v in x]  # @line L9
