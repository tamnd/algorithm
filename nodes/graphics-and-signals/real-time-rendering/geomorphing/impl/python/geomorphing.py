# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geomorphing/. The authors are listed in prov/N3KQ0C.jsonl.

"""Geomorphing between two levels of a regular height grid.

The fine mesh has vertices at the integer points (x, y) with 0 <= x, y <= m,
m even, and splits each unit cell by the diagonal from (x, y) to (x+1, y+1).
The coarse mesh uses only the even points and the same diagonal direction on
its cells of side 2, so every coarse triangle is the union of four fine
triangles. A point of the domain is (x, y); its height is a separate value.

The morph keeps the fine connectivity and moves each vertex that is not a
coarse vertex from the coarse surface (alpha = 0) to its own height
(alpha = 1). Every such vertex is the midpoint of a coarse edge.
"""

from fractions import Fraction
from math import floor


def coarse_edge(v):
    """The two ends of the coarse edge whose midpoint is the fine vertex v."""
    x, y = v
    if x % 2 and y % 2:
        return (x - 1, y - 1), (x + 1, y + 1)
    if x % 2:
        return (x - 1, y), (x + 1, y)
    return (x, y - 1), (x, y + 1)


def geomorph(h, m, alpha):
    """Vertex heights of the morphed mesh for alpha in [0, 1]."""
    g = {}
    for x in range(m + 1):  # @line L1
        for y in range(m + 1):
            if x % 2 == 0 and y % 2 == 0:
                g[(x, y)] = h[(x, y)]  # @line L2
            else:
                a, b = coarse_edge((x, y))
                g[(x, y)] = (1 - alpha) * Fraction(h[a] + h[b], 2) + alpha * h[(x, y)]  # @line L3
    return g  # @line L4


def surface(g, step, p):
    """The height at domain point p of the grid surface with vertex heights g and cell side step."""
    x, y = p
    top = max(k for k, _ in g) // step - 1
    i = min(max(floor(x / step), 0), top)
    j = min(max(floor(y / step), 0), top)
    u, v = Fraction(x) / step - i, Fraction(y) / step - j
    x0, y0, x1, y1 = i * step, j * step, (i + 1) * step, (j + 1) * step
    if u >= v:
        # Triangle (x0, y0), (x1, y0), (x1, y1).
        return g[(x0, y0)] + u * (g[(x1, y0)] - g[(x0, y0)]) + v * (g[(x1, y1)] - g[(x1, y0)])
    # Triangle (x0, y0), (x1, y1), (x0, y1).
    return g[(x0, y0)] + v * (g[(x0, y1)] - g[(x0, y0)]) + u * (g[(x1, y1)] - g[(x0, y1)])
