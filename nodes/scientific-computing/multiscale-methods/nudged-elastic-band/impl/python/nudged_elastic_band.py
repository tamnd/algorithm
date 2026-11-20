# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nudged-elastic-band/. The authors are listed in prov/NNCV7X.jsonl.
"""The nudged elastic band method with the improved tangent and the climbing image.

A chain of images R_0, ..., R_N joins two minima of a potential V. The end
images stay fixed. Each inner image moves under the NEB force: the part of
the true force -grad V that is perpendicular to the path, plus a spring
force along the path. The climbing image (the image with the highest
energy) feels no spring and has the parallel part of the true force
inverted, so it moves up along the path and down in the other directions.

The tangent is the one of Henkelman and Jonsson (2000): the vector to the
neighbour with the higher energy, and a weighted mean of the two vectors at
an extremum of the energy along the path.

The iteration is plain steepest descent on the NEB force with a fixed
step h. The NEB force is not the gradient of a function, so the iteration
is a fixed point iteration and its convergence is not proved in general.
A potential is a function that maps a point (a list of floats) to the pair
(V, gradient). Coordinates are mass weighted if masses are not all equal.
"""

import math
from typing import Callable, Sequence

Point = list[float]
Potential = Callable[[Sequence[float]], tuple[float, list[float]]]


def _sub(a, b):
    return [p - q for p, q in zip(a, b)]


def _dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def _norm(a):
    return math.sqrt(_dot(a, a))


def improved_tangent(r_prev, r, r_next, e_prev, e, e_next) -> Point:
    """The unit tangent at r of Henkelman and Jonsson (2000)."""
    t_plus = _sub(r_next, r)
    t_minus = _sub(r, r_prev)
    if e_next > e > e_prev:
        t = t_plus
    elif e_next < e < e_prev:
        t = t_minus
    else:
        d_max = max(abs(e_next - e), abs(e_prev - e))
        d_min = min(abs(e_next - e), abs(e_prev - e))
        if e_next > e_prev:
            t = [d_max * p + d_min * m for p, m in zip(t_plus, t_minus)]
        else:
            t = [d_min * p + d_max * m for p, m in zip(t_plus, t_minus)]
    n = _norm(t)
    if n == 0.0:
        # e_next = e = e_prev: use the mean of the two segment vectors.
        t = [p + m for p, m in zip(t_plus, t_minus)]
        n = _norm(t)
    return [c / n for c in t]


def neb_forces(images: Sequence[Point], energies: Sequence[float], grads: Sequence[Point],
               k: float, climb: bool) -> tuple[list[Point], int]:
    """The NEB forces on the inner images 1..N-1 (zero vectors at the ends).

    Returns the list of forces and the index of the climbing image (-1 if
    climb is False).
    """
    n = len(images) - 1
    forces = [[0.0] * len(images[0]) for _ in range(n + 1)]
    i_max = -1
    if climb:
        i_max = max(range(1, n), key=lambda i: energies[i])
    for i in range(1, n):
        tau = improved_tangent(images[i - 1], images[i], images[i + 1],    # @line L4
                               energies[i - 1], energies[i], energies[i + 1])
        g = grads[i]
        g_par = _dot(g, tau)
        if i == i_max:
            # Invert the parallel part of the true force; no spring.
            forces[i] = [-gc + 2.0 * g_par * tc for gc, tc in zip(g, tau)]  # @line L7
            continue
        stretch = _norm(_sub(images[i + 1], images[i])) - _norm(_sub(images[i], images[i - 1]))
        f_spring = k * stretch                                             # @line L5
        forces[i] = [-gc + g_par * tc + f_spring * tc for gc, tc in zip(g, tau)]  # @line L6
    return forces, i_max


def nudged_elastic_band(potential: Potential, r_start: Sequence[float], r_end: Sequence[float],
                        n: int, k: float, h: float, tol: float, climb: bool = True,
                        climb_tol: float = math.inf, max_iter: int = 10000,
                        images: Sequence[Point] = None):
    """Relax a band of n + 1 images from r_start to r_end.

    The start band is the straight line (or the given images). The climbing
    image is switched on when climb is True and the largest force is below
    climb_tol. The iteration stops when the largest force is below tol and
    the climbing image is on (if climb is True).

    Returns (images, energies, i_climb, iterations, converged).
    """
    if images is None:
        images = [[a + (i / n) * (b - a) for a, b in zip(r_start, r_end)]  # @line L1
                  for i in range(n + 1)]
    else:
        images = [list(p) for p in images]
    climbing = climb and climb_tol == math.inf
    energies, grads = [], []
    for p in images:
        e, g = potential(p)
        energies.append(e)
        grads.append(g)
    i_max = -1
    for it in range(max_iter):                                             # @line L2
        for i in range(1, n):                                              # @line L3
            energies[i], grads[i] = potential(images[i])
        forces, i_max = neb_forces(images, energies, grads, k, climbing)
        f_max = max(_norm(f) for f in forces)                              # @line L8
        if climb and not climbing and f_max < climb_tol:
            climbing = True
            continue
        if f_max < tol and climbing == climb:                              # @line L8
            return images, energies, i_max, it, True
        for i in range(1, n):                                              # @line L9
            images[i] = [c + h * f for c, f in zip(images[i], forces[i])]
    return images, energies, i_max, max_iter, False


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
