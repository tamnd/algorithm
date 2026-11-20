# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaspari-cohn-function/. The authors are listed in prov/4P6AFK.jsonl.

"""The Gaspari-Cohn function, eq. (4.10) of Gaspari and Cohn (1999).

gaspari_cohn(r, c) is a correlation function of the distance r with the
half-width c: it is 1 at r = 0, 5/24 at r = c and 0 for r >= 2c. With
fractions.Fraction arguments the result is exact.

taper_matrix(points, c, dist) builds the matrix of the weights for a list of
points and a distance function, for covariance localization. ring_distance
and chordal_ring_distance are two distances on a ring of n equally spaced
points (the grid of the Lorenz-96 model).
"""

import math


def _inner(z):
    """The piece for 0 <= z <= 1."""
    return -z ** 5 / 4 + z ** 4 / 2 + 5 * z ** 3 / 8 - 5 * z ** 2 / 3 + 1


def _outer(z):
    """The piece for 1 <= z <= 2."""
    return z ** 5 / 12 - z ** 4 / 2 + 5 * z ** 3 / 8 + 5 * z ** 2 / 3 - 5 * z + 4 - 2 / (3 * z)


def gaspari_cohn(r, c):
    """Return the Gaspari-Cohn weight of the distance r for the half-width c > 0."""
    z = abs(r) / c  # @line L1
    if z <= 1:  # @line L2
        return _inner(z)
    if z < 2:  # @line L3
        return _outer(z)
    return 0 * z  # @line L4


def taper_matrix(points, c, dist):
    """Return the matrix [gaspari_cohn(dist(p, q), c)] for the points p and q."""
    return [[gaspari_cohn(dist(p, q), c) for q in points] for p in points]


def ring_distance(n):
    """Distance along a ring of n points with spacing 1: min(|i - j|, n - |i - j|)."""
    def dist(i, j):
        k = abs(i - j) % n
        return min(k, n - k)
    return dist


def chordal_ring_distance(n):
    """Chordal distance on a ring of n points with spacing 1 along the ring.

    The ring is the circle of circumference n in the plane, so the chordal
    distance is (n / pi) sin(pi |i - j| / n). It is close to ring_distance
    for nearby points.
    """
    def dist(i, j):
        return n / math.pi * math.sin(math.pi * (abs(i - j) % n) / n)
    return dist
