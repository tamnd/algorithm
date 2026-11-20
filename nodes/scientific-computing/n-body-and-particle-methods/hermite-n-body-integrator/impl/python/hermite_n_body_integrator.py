# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hermite-n-body-integrator/. The authors are listed in prov/M1QQTQ.jsonl.
"""Fourth-order Hermite predictor-corrector integrator for the N-body problem.

The force and its time derivative (the jerk) are computed by direct
summation. A step predicts positions and velocities with a Taylor series in
the acceleration and the jerk, evaluates the force and the jerk at the
predicted state, fits the second and third derivatives of the acceleration
from the two values of the acceleration and of the jerk (Hermite
interpolation), and corrects. Plummer softening eps; G = 1 unless given.
"""

import math
from typing import Sequence

Vec = Sequence[float]
State = list[list[float]]


def acc_jerk(m: Sequence[float], x: Sequence[Vec], v: Sequence[Vec], eps: float = 0.0,
             G: float = 1.0) -> tuple[State, State]:
    """Accelerations and jerks of all bodies, by summation over pairs."""
    n, dim = len(m), len(x[0])
    a = [[0.0] * dim for _ in range(n)]
    j = [[0.0] * dim for _ in range(n)]
    e2 = eps * eps
    for p in range(n - 1):
        for q in range(p + 1, n):
            dx = [x[q][k] - x[p][k] for k in range(dim)]
            dv = [v[q][k] - v[p][k] for k in range(dim)]
            r2 = sum(c * c for c in dx) + e2
            rinv3 = G / (r2 * math.sqrt(r2))
            rv = 3.0 * sum(dx[k] * dv[k] for k in range(dim)) / r2
            for k in range(dim):
                fa = rinv3 * dx[k]  # @line L9
                fj = rinv3 * (dv[k] - rv * dx[k])  # @line L10
                a[p][k] += m[q] * fa
                a[q][k] -= m[p] * fa
                j[p][k] += m[q] * fj
                j[q][k] -= m[p] * fj
    return a, j


def hermite_step(m: Sequence[float], x: State, v: State, a: State, j: State, h: float,
                 eps: float = 0.0, G: float = 1.0):
    """One step of size h. Returns x1, v1, a1, j1 and the second and third
    derivatives of the acceleration at the end of the step (for the step criterion)."""
    n, dim = len(m), len(x[0])
    h2, h3 = h * h, h * h * h
    xp = [[x[i][k] + v[i][k] * h + a[i][k] * h2 / 2 + j[i][k] * h3 / 6 for k in range(dim)] for i in range(n)]  # @line L1
    vp = [[v[i][k] + a[i][k] * h + j[i][k] * h2 / 2 for k in range(dim)] for i in range(n)]  # @line L2
    a1, j1 = acc_jerk(m, xp, vp, eps, G)  # @line L3
    x1, v1, s1, c1 = [], [], [], []
    for i in range(n):
        xi, vi, si, ci = [], [], [], []
        for k in range(dim):
            da = a[i][k] - a1[i][k]
            snap = (-6.0 * da - h * (4.0 * j[i][k] + 2.0 * j1[i][k])) / h2  # @line L4
            crackle = (12.0 * da + 6.0 * h * (j[i][k] + j1[i][k])) / h3  # @line L5
            xi.append(xp[i][k] + snap * h2 * h2 / 24 + crackle * h2 * h3 / 120)  # @line L6
            vi.append(vp[i][k] + snap * h3 / 6 + crackle * h2 * h2 / 24)  # @line L7
            si.append(snap + crackle * h)
            ci.append(crackle)
        x1.append(xi)
        v1.append(vi)
        s1.append(si)
        c1.append(ci)
    return x1, v1, a1, j1, s1, c1  # @line L8


def integrate(m: Sequence[float], x: Sequence[Vec], v: Sequence[Vec], h: float, steps: int,
              eps: float = 0.0, G: float = 1.0) -> tuple[State, State]:
    """Shared constant step h for all bodies."""
    x = [list(p) for p in x]
    v = [list(q) for q in v]
    a, j = acc_jerk(m, x, v, eps, G)
    for _ in range(steps):
        x, v, a, j, _, _ = hermite_step(m, x, v, a, j, h, eps, G)
    return x, v


def aarseth_step(a: Vec, j: Vec, snap: Vec, crackle: Vec, eta: float = 0.02) -> float:
    """Aarseth's step criterion sqrt(eta (|a||a2| + |j|^2) / (|j||a3| + |a2|^2))."""
    na, nj, ns, nc = (math.hypot(*u) for u in (a, j, snap, crackle))
    return math.sqrt(eta * (na * ns + nj * nj) / (nj * nc + ns * ns))


def energy(m: Sequence[float], x: Sequence[Vec], v: Sequence[Vec], eps: float = 0.0, G: float = 1.0) -> float:
    n = len(m)
    k = 0.5 * sum(m[i] * sum(c * c for c in v[i]) for i in range(n))
    u = -sum(G * m[i] * m[q] / math.sqrt(sum((x[i][d] - x[q][d]) ** 2 for d in range(len(x[i]))) + eps * eps)
             for i in range(n) for q in range(i + 1, n))
    return k + u
