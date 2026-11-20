# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dimer-method/. The authors are listed in prov/JXAQP4.jsonl.
"""The dimer method for saddle points (Henkelman and Jonsson 1999).

A dimer is a pair of points R +- dR N around a centre R, with a unit
vector N. Only gradients are used. From the two gradients:

- the curvature along N is C = (F2 - F1) . N / (2 dR), where F = -grad V
  at the two points. It is N^T H N up to O(dR^2).
- the rotation turns N in the plane of N and the rotational force, to the
  angle that minimizes the curvature. The angle comes from the fit
  C(phi) = a0 / 2 + a1 cos(2 phi) + b1 sin(2 phi), which is exact for a
  quadratic V (Heyden, Bell and Keil 2005). It costs one extra gradient.
- the translation moves R along the force with the component along N
  inverted (F - 2 (F . N) N) if C < 0, and along -(F . N) N only if
  C >= 0, so that the dimer leaves a convex region fast.

A potential maps a point (list of floats) to (V, gradient).
"""

import math
from typing import Callable, Sequence

Point = list[float]
Potential = Callable[[Sequence[float]], tuple[float, list[float]]]


def _dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def _norm(a):
    return math.sqrt(_dot(a, a))


def _axpy(alpha, x, y):
    return [alpha * p + q for p, q in zip(x, y)]


def _unit(a):
    n = _norm(a)
    return [c / n for c in a]


def curvature(potential: Potential, r: Sequence[float], n: Sequence[float], dr: float,
              g0: Sequence[float]) -> tuple[float, list[float]]:
    """The curvature along the unit vector n and the force difference F1 - F2.

    Uses the gradient g0 at the centre and one new gradient at R1 = r + dr n;
    the gradient at R2 = r - dr n is taken as 2 g0 - g1 (central difference).
    """
    g1 = potential(_axpy(dr, n, r))[1]
    f1 = [-c for c in g1]
    f2 = [-(2.0 * a - b) for a, b in zip(g0, g1)]
    c = _dot([b - a for a, b in zip(f1, f2)], n) / (2.0 * dr)         # @line L4
    return c, [a - b for a, b in zip(f1, f2)]


def rotate(potential: Potential, r, n, dr, g0, phi_trial=None):
    """One rotation of the dimer to the lowest curvature in one plane.

    Returns (n_new, c_new, c_old, f_rot): the new unit vector, its estimated
    curvature, the curvature before, and the norm of the rotational force.
    """
    c0, df = curvature(potential, r, n, dr, g0)
    f_perp = _axpy(-_dot(df, n), n, df)                                 # @line L5
    f_rot = _norm(f_perp)
    if f_rot == 0.0:
        return list(n), c0, c0, 0.0
    theta = [c / f_rot for c in f_perp]
    # dC/dphi at phi = 0 is 2 theta^T H n = -(F1 - F2) . theta / dR.
    dc = -_dot(df, theta) / dr
    if phi_trial is None:
        phi_trial = -0.5 * math.atan(dc / (2.0 * abs(c0)))
        if abs(phi_trial) < 1e-3:
            phi_trial = 1e-3 if phi_trial >= 0 else -1e-3
    n1 = _unit(_axpy(math.sin(phi_trial), theta, [math.cos(phi_trial) * c for c in n]))
    c1, _ = curvature(potential, r, n1, dr, g0)
    b1 = 0.5 * dc                                                       # @line L6
    a1 = (c0 - c1 + b1 * math.sin(2.0 * phi_trial)) / (1.0 - math.cos(2.0 * phi_trial))
    a0 = 2.0 * (c0 - a1)
    phi = 0.5 * math.atan2(b1, a1)                                      # @line L6
    c_min = 0.5 * a0 + a1 * math.cos(2.0 * phi) + b1 * math.sin(2.0 * phi)
    if c_min > c0:
        phi += 0.5 * math.pi
        c_min = 0.5 * a0 + a1 * math.cos(2.0 * phi) + b1 * math.sin(2.0 * phi)
    n_new = _unit(_axpy(math.sin(phi), theta, [math.cos(phi) * c for c in n]))  # @line L7
    return n_new, c_min, c0, f_rot


def dimer_method(potential: Potential, r0: Sequence[float], n0: Sequence[float], dr: float,
                 h: float, tol: float, max_step: float = 0.02, rot_tol: float = 1e-3,
                 max_rot: int = 4, max_iter: int = 2000):
    """Search for a first-order saddle point from r0 with the start direction n0.

    h is the step factor of the translation where c < 0, and each step is
    at most max_step long. Where c >= 0 every step has the length max_step. Returns (r, n, c, iterations, converged): the centre,
    the unit vector of the lowest curvature mode, the curvature along it,
    the number of translations and whether |grad V| < tol with c < 0.
    """
    r = list(r0)
    n = _unit(n0)                                                       # @line L1
    c = 0.0
    for it in range(max_iter):                                          # @line L2
        g0 = potential(r)[1]                                            # @line L3
        for _ in range(max_rot):
            n, c, _c_old, f_rot = rotate(potential, r, n, dr, g0)
            if f_rot < rot_tol:
                break
        if _norm(g0) < tol and c < 0.0:                                 # @line L8
            return r, n, c, it, True
        f = [-a for a in g0]
        f_par = _dot(f, n)
        if c < 0.0:
            f_eff = _axpy(-2.0 * f_par, n, f)                           # @line L9
        else:
            f_eff = [-f_par * a for a in n]                             # @line L9
        step = [h * a for a in f_eff]
        s = _norm(step)
        if s > max_step or (c >= 0.0 and s > 0.0):
            # In a convex region, take a full step of length max_step uphill along n.
            step = [a * max_step / s for a in step]
        r = [a + b for a, b in zip(r, step)]                            # @line L10
    return r, n, c, max_iter, False


def muller_brown(p: Sequence[float]) -> tuple[float, list[float]]:
    """The Muller-Brown potential (Muller and Brown 1979) and its gradient."""
    x, y = p
    A = (-200.0, -100.0, -170.0, 15.0)
    a = (-1.0, -1.0, -6.5, 0.7)
    b = (0.0, 0.0, 11.0, 0.6)
    c = (-10.0, -10.0, -6.5, 0.7)
    x0 = (1.0, 0.0, -0.5, -1.0)
    y0 = (0.0, 0.5, 1.5, 1.0)
    v = gx = gy = 0.0
    for j in range(4):
        dx, dy = x - x0[j], y - y0[j]
        e = A[j] * math.exp(a[j] * dx * dx + b[j] * dx * dy + c[j] * dy * dy)
        v += e
        gx += e * (2.0 * a[j] * dx + b[j] * dy)
        gy += e * (b[j] * dx + 2.0 * c[j] * dy)
    return v, [gx, gy]
