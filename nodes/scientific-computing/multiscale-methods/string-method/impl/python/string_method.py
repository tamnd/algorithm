# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-method/. The authors are listed in prov/SDPAV5.jsonl.
"""The simplified zero-temperature string method (E, Ren and Vanden-Eijnden 2007).

A string is a list of N + 1 images phi_0, ..., phi_N. One iteration has
two steps:

1. evolve: each image takes one step of steepest descent,
   phi_i <- phi_i - h grad V(phi_i). The ends fall into the minima.
2. reparametrize: the images are moved along the piecewise linear curve
   through the new images, so that the arc lengths between neighbours
   are equal.

The second step removes the component of the motion along the string, so
the string moves only by the perpendicular part of the force, as in the
original method of 2002, without any projection. A fixed point is a
string on which the gradient is parallel to the string (up to the error
of the discretization): a minimum energy path.

A potential maps a point (list of floats) to (V, gradient).
"""

import math
from typing import Callable, Sequence

Point = list[float]
Potential = Callable[[Sequence[float]], tuple[float, list[float]]]


def arc_lengths(images: Sequence[Sequence[float]]) -> list[float]:
    """The normalized arc length alpha_i in [0, 1] at each image."""
    s = [0.0]
    for a, b in zip(images, images[1:]):
        s.append(s[-1] + math.dist(a, b))                                # @line L4
    total = s[-1]
    return [v / total for v in s]


def reparametrize(images: Sequence[Sequence[float]]) -> list[Point]:
    """Points at equal arc length along the polygon through the images."""
    n = len(images) - 1
    alpha = arc_lengths(images)
    out = [list(images[0])]
    j = 1
    for i in range(1, n):
        target = i / n
        while alpha[j] < target:
            j += 1
        w = (target - alpha[j - 1]) / (alpha[j] - alpha[j - 1])           # @line L5
        out.append([(1.0 - w) * a + w * b for a, b in zip(images[j - 1], images[j])])
    out.append(list(images[n]))
    return out


def string_method(potential: Potential, r_start: Sequence[float], r_end: Sequence[float],
                  n: int, h: float, tol: float, max_iter: int = 10000,
                  images: Sequence[Sequence[float]] = None):
    """Evolve a string of n + 1 images to a minimum energy path.

    The start string is the straight line from r_start to r_end, or the
    given images. The iteration stops when no image moves by more than
    h * tol in one iteration (the motion divided by h is a force).
    Returns (images, energies, iterations, converged).
    """
    if images is None:
        phi = [[a + (i / n) * (b - a) for a, b in zip(r_start, r_end)]   # @line L1
               for i in range(n + 1)]
    else:
        phi = [list(p) for p in images]
    for it in range(max_iter):                                          # @line L2
        moved = []
        for p in phi:
            g = potential(p)[1]
            moved.append([c - h * gc for c, gc in zip(p, g)])           # @line L3
        new = reparametrize(moved)                                       # @line L5
        change = max(math.dist(a, b) for a, b in zip(new, phi)) / h      # @line L6
        phi = new
        if change < tol:                                                 # @line L6
            return phi, [potential(p)[0] for p in phi], it + 1, True
    return phi, [potential(p)[0] for p in phi], max_iter, False         # @line L7


def perpendicular_gradient(potential: Potential, images: Sequence[Sequence[float]]) -> list[float]:
    """|grad V - (grad V . t) t| at each inner image, with the central tangent t."""
    out = []
    for i in range(1, len(images) - 1):
        t = [b - a for a, b in zip(images[i - 1], images[i + 1])]
        nt = math.sqrt(sum(c * c for c in t))
        t = [c / nt for c in t]
        g = potential(images[i])[1]
        gp = sum(a * b for a, b in zip(g, t))
        out.append(math.sqrt(sum((a - gp * b) ** 2 for a, b in zip(g, t))))
    return out


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
