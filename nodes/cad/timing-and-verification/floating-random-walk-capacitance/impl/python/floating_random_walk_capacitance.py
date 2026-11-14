# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floating-random-walk-capacitance/. The authors are listed in prov/0AP7M8.jsonl.
"""Floating random walk capacitance extraction, in two dimensions.

The geometry is Manhattan. Conductors are closed axis-parallel rectangles
(x0, y0, x1, y1) with integer corners, inside a grounded box whose inner
side is the open rectangle (X0, X1) x (Y0, Y1). The box is conductor 0 and
the rectangles are conductors 1, 2, ... in the order given. Conductors must
not touch. The dielectric is uniform with permittivity eps.

Each step of a walk jumps from a point p to the boundary of the largest
square centred at p that holds no conductor, at a point drawn from the
surface Green's function (the Poisson kernel) of the square at its centre.
The square in 2D plays the part of the cube of Le Coz and Iverson in 3D.
Positions are integers, so the test "the walk stands on a conductor" is an
exact integer test, and the integer grid is the stopping layer. The only
rounding is the offset of each jump along a side of the square, which is
rounded to the grid; use coordinates large enough (for example 2**24 per
length unit) that this is negligible. The estimates are floats with a
standard error.
"""

import bisect
import math

TERMS = 30
_COSH = [math.cosh(n * math.pi / 2) for n in range(TERMS + 1)]
_SINH = [math.sinh(n * math.pi / 2) if n else 1.0 for n in range(TERMS + 1)]


def density(u):
    """Poisson kernel of the square [0, pi]^2 at its centre, for a point at
    abscissa u of one side. Each side carries total mass 1/4."""
    s = 0.0
    for n in range(1, TERMS, 2):
        s += (-1) ** ((n - 1) // 2) * math.sin(n * u) / _COSH[n]
    return s / math.pi


def normal_derivative(u):
    """Derivative of the kernel when the centre moves toward that side."""
    s = 0.0
    for n in range(1, TERMS, 2):
        s += (-1) ** ((n - 1) // 2) * n * math.sin(n * u) / _SINH[n]
    return s / math.pi


def tangent_derivative(u):
    """Derivative of the kernel when the centre moves along the side, in the
    direction of growing u."""
    s = 0.0
    for n in range(2, TERMS, 2):
        s += (-1) ** (n // 2) * n * math.sin(n * u) / _COSH[n]
    return s / math.pi


def side_cdf(u):
    """Mass of [0, u] on one side, divided by 1/4, so side_cdf(pi) = 1."""
    s = 0.0
    for n in range(1, TERMS, 2):
        s += (-1) ** ((n - 1) // 2) * (1 - math.cos(n * u)) / (n * _COSH[n])
    return 4 * s / math.pi


_GRID = 4096
_U = [math.pi * i / _GRID for i in range(_GRID + 1)]
_F = [side_cdf(u) for u in _U]
_F[-1] = 1.0


def sample_side_position(rng):
    """Draw u in [0, pi] with the density of one side, by inverting a table."""
    r = rng.random()
    i = min(bisect.bisect_right(_F, r), _GRID) - 1
    f0, f1 = _F[i], _F[i + 1]
    t = 0.0 if f1 == f0 else (r - f0) / (f1 - f0)
    return _U[i] + t * (_U[i + 1] - _U[i])


# The four sides in counterclockwise order: start corner, tangent, outward normal.
_SIDES = (
    ((-1, -1), (1, 0), (0, -1)),  # bottom
    ((1, -1), (0, 1), (1, 0)),  # right
    ((1, 1), (-1, 0), (0, 1)),  # top
    ((-1, 1), (0, -1), (-1, 0)),  # left
)


def jump(p, h, rng):
    """One jump from the centre p of an empty square of half width h.
    Returns the new point, the side and u."""
    side = rng.randrange(4)
    (sx, sy), (tx, ty), _ = _SIDES[side]
    u = sample_side_position(rng)
    off = round(2 * h * u / math.pi)
    return (p[0] + sx * h + tx * off, p[1] + sy * h + ty * off), side, u


def gradient_weight(h, side, u, normal):
    """(grad of the kernel at the centre, dotted with normal) / kernel, for a
    square of half width h; the mean of weight * phi(q) is grad(phi) . normal."""
    _, tangent, outward = _SIDES[side]
    dot = (normal_derivative(u) * (outward[0] * normal[0] + outward[1] * normal[1])
           + tangent_derivative(u) * (tangent[0] * normal[0] + tangent[1] * normal[1]))
    return math.pi / (2 * h) * dot / density(u)


class Geometry:
    def __init__(self, box, conductors):
        self.box = box
        self.rects = list(conductors)
        X0, Y0, X1, Y1 = box
        for (x0, y0, x1, y1) in self.rects:
            if not (X0 < x0 <= x1 < X1 and Y0 < y0 <= y1 < Y1):
                raise ValueError("conductor outside the box")

    def nearest(self, p):
        """(L-infinity distance to the nearest conductor, its number)."""
        x, y = p
        X0, Y0, X1, Y1 = self.box
        best, k = min(x - X0, X1 - x, y - Y0, Y1 - y), 0
        for i, (x0, y0, x1, y1) in enumerate(self.rects, 1):
            d = max(x0 - x, x - x1, y0 - y, y - y1, 0)
            if d < best:
                best, k = d, i
        return best, k


def gaussian_point(rect, gap, rng):
    """A uniform point on the rectangle rect grown by gap, with its outward normal."""
    x0, y0, x1, y1 = rect[0] - gap, rect[1] - gap, rect[2] + gap, rect[3] + gap
    w, h = x1 - x0, y1 - y0
    t = rng.randrange(2 * (w + h))
    if t < w:
        return (x0 + t, y0), (0, -1)
    t -= w
    if t < h:
        return (x1, y0 + t), (1, 0)
    t -= h
    if t < w:
        return (x1 - t, y1), (0, 1)
    t -= w
    return (x0, y1 - t), (-1, 0)


def walks(geom, i, gap, n_walks, rng, eps=1.0, max_steps=10**6):
    """Yield n_walks triples (value, conductor, end point). If phi is harmonic
    in the free space and phi = score(k, point) on conductor k, the mean of
    value * score(conductor, end) is -eps times the flux of grad(phi) out of
    the Gaussian rectangle at distance gap around conductor i. With
    score = [k == j] that mean is the capacitance coefficient C_ij."""
    rect = geom.rects[i - 1]
    length = 2 * ((rect[2] - rect[0]) + (rect[3] - rect[1]) + 4 * gap)
    for _ in range(n_walks):  # @line L1
        r, normal = gaussian_point(rect, gap, rng)  # @line L2
        h, _ = geom.nearest(r)  # @line L3
        q, side, u = jump(r, h, rng)  # @line L4
        w = gradient_weight(h, side, u, normal)  # @line L5
        for _ in range(max_steps):
            h, k = geom.nearest(q)  # @line L6
            if h == 0:  # @line L7
                break
            q, _, _ = jump(q, h, rng)  # @line L8
        else:
            raise RuntimeError("walk too long")
        yield -eps * length * w, k, q  # @line L9


def flux_estimate(geom, i, gap, n_walks, rng, score, eps=1.0):
    """Mean and standard error of the flux functional of walks()."""
    return mean_and_error([v * score(k, q) for v, k, q in walks(geom, i, gap, n_walks, rng, eps)])


def capacitance_row(geom, i, gap, n_walks, rng, eps=1.0):
    """Estimates (mean, standard error) of C_ij for j = 0 (the box), 1, 2, ...,
    all from the same walks."""
    m = len(geom.rects) + 1
    cols = [[] for _ in range(m)]
    for v, k, _ in walks(geom, i, gap, n_walks, rng, eps):
        for j in range(m):
            cols[j].append(v if j == k else 0.0)
    return [mean_and_error(c) for c in cols]


def mean_and_error(xs):
    n = len(xs)
    mu = sum(xs) / n
    var = sum((x - mu) ** 2 for x in xs) / (n - 1)
    return mu, math.sqrt(var / n)
