# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-smoothing/. The authors are listed in prov/8BS9ES.jsonl.

"""Laplacian smoothing of a triangle mesh with the uniform (umbrella) weights.

Each step moves every free vertex a fraction lam of the way to the average of
its neighbours, all at once (a Jacobi step): x_i <- x_i + lam (c_i - x_i).
The border vertices of an open mesh are fixed by default. The coordinates can
be int, float or Fraction, so a test can follow the steps exactly.
"""

from fractions import Fraction
from typing import Iterable, Optional, Sequence

from mp2mesh import boundary_vertices, neighbours

Point = tuple


def laplacian_smoothing(points: Sequence[Sequence], faces: Sequence[Sequence[int]], lam=Fraction(1, 2),
                        iterations: int = 1, fixed: Optional[Iterable[int]] = None) -> list[Point]:
    """Return the points after `iterations` uniform Laplacian steps with factor lam.

    fixed: the vertices that do not move. The default is the border vertices.
    """
    n = len(points)
    nb = neighbours(n, faces)                                  # @line L1
    stay = set(boundary_vertices(faces) if fixed is None else fixed)
    x = [tuple(p) for p in points]
    for _ in range(iterations):                                # @line L2
        y = list(x)                                            # @line L6
        for i in range(n):                                     # @line L3
            if i in stay or not nb[i]:
                continue
            d = len(nb[i])
            c = tuple(sum(x[j][k] for j in nb[i]) / d for k in range(3))    # @line L4
            y[i] = tuple(x[i][k] + lam * (c[k] - x[i][k]) for k in range(3))  # @line L5
        x = y                                                  # @line L7
    return x


def umbrella(points: Sequence[Sequence], faces: Sequence[Sequence[int]]) -> list[Point]:
    """The uniform Laplacian U(x)_i = c_i - x_i at every vertex."""
    nb = neighbours(len(points), faces)
    out = []
    for i, p in enumerate(points):
        if not nb[i]:
            out.append((0, 0, 0))
            continue
        d = len(nb[i])
        out.append(tuple(sum(points[j][k] for j in nb[i]) / d - p[k] for k in range(3)))
    return out
