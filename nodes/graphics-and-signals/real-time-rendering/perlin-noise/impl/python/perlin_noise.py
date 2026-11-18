# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perlin-noise/. The authors are listed in prov/QWP9HR.jsonl.

"""Improved Perlin noise in 3D (Perlin 2002).

The lattice is the integer grid. A permutation P of 0..255, doubled to 512
entries, hashes each lattice point to one of 16 gradient vectors: the 12
vectors from the center of a cube to the midpoints of its edges, and 4 of
them again, so that the index is h & 15. The value at a point is the
trilinear blend, with the quintic fade 6t^5 - 15t^4 + 10t^3 as the weight,
of the 8 corner values g . (p - corner).

Perlin's reference code uses one fixed table for P. This module makes P from
a seed with a Fisher-Yates shuffle, so different seeds give different noise.
"""

import random
from math import floor

# Index h & 15 -> gradient. The order is that of the bit tests in Perlin's
# reference code: entry h is (u-sign, v-sign) applied to the chosen axes.
GRADIENTS = (
    (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
    (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
    (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
    (1, 1, 0), (0, -1, 1), (-1, 1, 0), (0, -1, -1),
)


def make_permutation(rng):
    """Return a list of 512 entries: a random permutation of 0..255, twice."""
    p = list(range(256))
    rng.shuffle(p)
    return p + p


def fade(t):
    """The quintic fade 6t^5 - 15t^4 + 10t^3."""
    return t * t * t * (t * (t * 6 - 15) + 10)  # @line L9


def grad(h, x, y, z):
    """Dot product of gradient h & 15 with (x, y, z), as in Perlin's code."""
    h &= 15  # @line L10
    u = x if h < 8 else y
    v = y if h < 4 else (x if h in (12, 14) else z)
    return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v)


def lerp(t, a, b):
    return a + t * (b - a)


def noise(x, y, z, perm):
    """Improved Perlin noise at (x, y, z) for a doubled permutation perm."""
    fx, fy, fz = floor(x), floor(y), floor(z)
    X, Y, Z = fx & 255, fy & 255, fz & 255  # @line L1
    x, y, z = x - fx, y - fy, z - fz  # @line L2
    u, v, w = fade(x), fade(y), fade(z)  # @line L3
    p = perm
    # The 8 corners, with the hashes nested as in Perlin's code.
    a = p[X] + Y  # @line L4
    aa, ab = p[a] + Z, p[a + 1] + Z  # @line L5: P[P[P[X + a] + Y + b] + Z + c] shares lookups
    b = p[X + 1] + Y
    ba, bb = p[b] + Z, p[b + 1] + Z
    # The 8 corner values g . (p - corner).
    n000 = grad(p[aa], x, y, z)  # @line L6
    n100 = grad(p[ba], x - 1, y, z)
    n010 = grad(p[ab], x, y - 1, z)
    n110 = grad(p[bb], x - 1, y - 1, z)
    n001 = grad(p[aa + 1], x, y, z - 1)
    n101 = grad(p[ba + 1], x - 1, y, z - 1)
    n011 = grad(p[ab + 1], x, y - 1, z - 1)
    n111 = grad(p[bb + 1], x - 1, y - 1, z - 1)
    return lerp(w,  # @line L7
                lerp(v, lerp(u, n000, n100), lerp(u, n010, n110)),
                lerp(v, lerp(u, n001, n101), lerp(u, n011, n111)))  # @line L8


def corner_gradient(i, j, k, perm):
    """The gradient vector that perm assigns to the lattice point (i, j, k)."""
    p = perm
    h = p[p[p[i & 255] + (j & 255)] + (k & 255)]
    return GRADIENTS[h & 15]


class PerlinNoise:
    """Seeded 3D improved Perlin noise."""

    def __init__(self, seed=0):
        self.perm = make_permutation(random.Random(seed))

    def __call__(self, x, y, z=0.0):
        return noise(x, y, z, self.perm)
