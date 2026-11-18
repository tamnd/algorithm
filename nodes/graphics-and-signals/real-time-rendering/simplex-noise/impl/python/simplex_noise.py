# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-noise/. The authors are listed in prov/PWY9S0.jsonl.

"""Simplex noise in n dimensions (Perlin 2001), in the form of Gustavson 2005.

The skew x' = x + F (x_1 + ... + x_n) with F = (sqrt(n + 1) - 1) / n maps the
simplex grid to the integer lattice, where the simplices are the cells of the
unit cube cut by the order of the coordinates. The point lies in the simplex
whose n + 1 corners are reached from floor(x') by unit steps along the axes,
in decreasing order of the fractional parts. Each corner adds
max(0, r2 - |d|^2)^4 (g . d), where d is the offset from the corner after the
unskew with G = (1 - 1 / sqrt(n + 1)) / n, and g is a hashed gradient.

In 2D and 3D the gradients are those of Gustavson's code: the 12 edge
directions of a cube (in 2D their first two components), with the index hash
mod 12. In 2D the sum is scaled by 70, as in his code. For n >= 4 the
gradients are the vectors with entries in {-1, 0, 1} that have exactly one
zero, and the scale is 1. The radius r2 = 0.5 keeps the noise continuous in
every dimension (see the proof of the page). Gustavson's 3D and 4D code uses
0.6, which makes small jumps on the faces of the simplices.
"""

import random
from itertools import product
from math import floor, sqrt

GRAD3 = (
    (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
    (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
    (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
)


def skew_constants(n):
    """Return (F, G) for dimension n."""
    return (sqrt(n + 1) - 1) / n, (1 - 1 / sqrt(n + 1)) / n


def gradient_set(n):
    """The gradient table for dimension n."""
    if n == 2:
        return tuple(g[:2] for g in GRAD3)
    if n == 3:
        return GRAD3
    out = []
    for zero in range(n):
        for signs in product((1, -1), repeat=n - 1):
            g = list(signs)
            g.insert(zero, 0)
            out.append(tuple(g))
    return tuple(out)


def make_permutation(rng):
    p = list(range(256))
    rng.shuffle(p)
    return p + p


def lattice_hash(k, perm):
    """Nested permutation hash of the integer point k (last axis innermost)."""
    h = 0
    for c in reversed(k):
        h = perm[(c & 255) + h]
    return h


def simplex_corners(x):
    """Return the skewed corner list of the simplex that holds the point x."""
    n = len(x)
    F, _ = skew_constants(n)
    s = sum(x) * F  # @line L1
    k = [floor(c + s) for c in x]  # @line L2
    f = [c + s - kc for c, kc in zip(x, k)]
    order = sorted(range(n), key=lambda a: -f[a])  # @line L3
    corners = [tuple(k)]
    cur = list(k)
    for a in order:  # @line L4
        cur[a] += 1
        corners.append(tuple(cur))
    return corners


def unskew(k):
    _, G = skew_constants(len(k))
    t = sum(k) * G
    return tuple(c - t for c in k)


def corner_term(x, k, perm, grads, r2):
    """The contribution of the lattice point k to the noise at x."""
    u = unskew(k)  # @line L6
    d = [a - b for a, b in zip(x, u)]
    t = r2 - sum(c * c for c in d)
    if t <= 0:  # @line L7
        return 0.0
    g = grads[lattice_hash(k, perm) % len(grads)]
    return t ** 4 * sum(a * b for a, b in zip(g, d))  # @line L8


class SimplexNoise:
    """Seeded simplex noise in n dimensions."""

    def __init__(self, n=2, seed=0, r2=0.5, scale=None):
        self.n = n
        self.perm = make_permutation(random.Random(seed))
        self.grads = gradient_set(n)
        self.r2 = r2
        self.scale = (70.0 if n == 2 else 1.0) if scale is None else scale

    def __call__(self, *x):
        if len(x) != self.n:
            raise ValueError("wrong number of coordinates")
        total = 0.0
        for k in simplex_corners(x):  # @line L5
            total += corner_term(x, k, self.perm, self.grads, self.r2)
        return self.scale * total  # @line L9
