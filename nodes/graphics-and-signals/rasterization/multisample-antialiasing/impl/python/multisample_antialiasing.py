# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multisample-antialiasing/. The authors are listed in prov/X9CB9D.jsonl.

"""Multisample antialiasing (MSAA) with a per-sample depth buffer and a box resolve.

Screen coordinates are in pixel units with y pointing down; pixel (i, j) covers
[i, i+1] x [j, j+1] and its center is (i + 1/2, j + 1/2). A triangle is
((x0, y0, z0), (x1, y1, z1), (x2, y2, z2), color); depth z is interpolated
linearly in screen space and a smaller z is nearer. The sample pattern is a list
of offsets inside the unit square. A sample on an edge belongs to the triangle
by the top-left rule. Colors are tuples of linear values.
Use fractions.Fraction coordinates for exact results.
"""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Tuple

Color = tuple
Vertex = Tuple[Fraction, Fraction, Fraction]
Triangle = Tuple[Vertex, Vertex, Vertex, Color]
Shader = Callable[[int, Fraction, Fraction], Color]

# A 4-sample rotated grid, in sixteenths of a pixel from the center: all x and all y differ.
ROTATED_GRID_4 = [(Fraction(8 + dx, 16), Fraction(8 + dy, 16)) for dx, dy in ((-2, -6), (6, -2), (-6, 2), (2, 6))]


def _edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def _setup(tri: Triangle):
    """Return the vertices in positive orientation, or None for a zero-area triangle."""
    a, b, c, _ = tri
    area2 = _edge(a[0], a[1], b[0], b[1], c[0], c[1])
    if area2 == 0:
        return None
    if area2 < 0:
        b, c = c, b
        area2 = -area2
    return a, b, c, area2


def _owns(ax, ay, bx, by, e) -> bool:
    """Top-left rule for one edge a -> b with the interior on the side e > 0."""
    if e > 0:
        return True
    if e < 0:
        return False
    dx, dy = bx - ax, by - ay
    return dy < 0 or (dy == 0 and dx > 0)


def covers(setup, px, py) -> Optional[Fraction]:
    """Return the interpolated depth if the triangle owns the point, else None."""
    a, b, c, area2 = setup
    e0 = _edge(b[0], b[1], c[0], c[1], px, py)  # weight of a
    e1 = _edge(c[0], c[1], a[0], a[1], px, py)  # weight of b
    e2 = _edge(a[0], a[1], b[0], b[1], px, py)  # weight of c
    if not (_owns(b[0], b[1], c[0], c[1], e0) and _owns(c[0], c[1], a[0], a[1], e1) and _owns(a[0], a[1], b[0], b[1], e2)):
        return None
    return (e0 * a[2] + e1 * b[2] + e2 * c[2]) / area2


def multisample_antialiasing(
    triangles: Sequence[Triangle],
    width: int,
    height: int,
    pattern: Sequence[Tuple[Fraction, Fraction]],
    background: Color,
    shade: Optional[Shader] = None,
) -> Tuple[List[List[Color]], List[List[List[Color]]], int]:
    """Render with MSAA; return (image, sample colors, number of shader calls).

    The shader runs once per pixel and triangle that covers at least one sample
    of the pixel, at the pixel center. image[j][i] is the mean of the n samples.
    Precondition: the pattern offsets lie in [0, 1) x [0, 1).
    Cost: O(n W H) for the buffers plus, per triangle, O(n) per pixel of its
    bounding box, and one shader call per touched pixel.
    """
    if shade is None:
        shade = lambda t, x, y: triangles[t][3]  # noqa: E731
    n = len(pattern)
    color = [[[background] * n for _ in range(width)] for _ in range(height)]  # @line L1
    depth: List[List[List[object]]] = [[[math.inf] * n for _ in range(width)] for _ in range(height)]
    calls = 0
    for t, tri in enumerate(triangles):  # @line L2
        setup = _setup(tri)
        if setup is None:
            continue
        xs, ys = [v[0] for v in tri[:3]], [v[1] for v in tri[:3]]
        i_lo, i_hi = max(0, math.floor(min(xs))), min(width - 1, math.floor(max(xs)))
        j_lo, j_hi = max(0, math.floor(min(ys))), min(height - 1, math.floor(max(ys)))
        for j in range(j_lo, j_hi + 1):  # @line L3
            for i in range(i_lo, i_hi + 1):
                zs = [covers(setup, i + ox, j + oy) for ox, oy in pattern]  # @line L4
                if all(z is None for z in zs):  # @line L5
                    continue
                c = shade(t, i + Fraction(1, 2), j + Fraction(1, 2))  # @line L6
                calls += 1
                for m, z in enumerate(zs):  # @line L7
                    if z is not None and z < depth[j][i][m]:  # @line L8
                        depth[j][i][m], color[j][i][m] = z, c  # @line L9
    image = [[_mean(color[j][i]) for i in range(width)] for j in range(height)]  # @line L10
    return image, color, calls  # @line L11


def _mean(samples: Sequence[Color]) -> Color:
    n = len(samples)
    out = []
    for ch in zip(*samples):
        if all(isinstance(x, (int, Fraction)) for x in ch):
            out.append(Fraction(sum(ch), n))
        else:
            out.append(sum(ch) / n)
    return tuple(out)
