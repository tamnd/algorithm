# SPDX-License-Identifier: MIT
# Shared helper of the mg4 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Exact geometry of trilinear hexahedra, shared by the mg4 pages.

A hex is a list of 8 points in the standard order: the bottom face
0, 1, 2, 3 counterclockwise seen from above, then the top face 4, 5, 6, 7
above 0, 1, 2, 3. Vertex k is the image of the reference corner
REF[k] of the unit cube, and the hex is the trilinear map of the cube with
these corner images. With int or Fraction coordinates every value here is
exact, so every sign is decided exactly.
"""

from fractions import Fraction
from typing import List, Sequence, Tuple

Point = Tuple
Hex = Sequence[Point]

REF = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]

# For corner k, three neighbours whose edge vectors form a right-handed frame on the unit cube.
CORNER_NEIGHBOURS = [(1, 3, 4), (2, 0, 5), (3, 1, 6), (0, 2, 7), (7, 5, 0), (4, 6, 1), (5, 7, 2), (6, 4, 3)]

# The six faces, each listed counterclockwise seen from outside the hex.
FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

# The twelve edges in three classes of four parallel edges (directions u, v, w).
EDGE_CLASSES = [
    [(0, 1), (3, 2), (4, 5), (7, 6)],
    [(0, 3), (1, 2), (4, 7), (5, 6)],
    [(0, 4), (1, 5), (2, 6), (3, 7)],
]


def sub(p: Point, q: Point) -> Point:
    """p - q, componentwise."""
    return tuple(a - b for a, b in zip(p, q))


def det3(a: Point, b: Point, c: Point):
    """The determinant of the 3 x 3 matrix with columns a, b, c."""
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def corner_jacobians(h: Hex) -> List:
    """The 8 corner Jacobian determinants det(e1, e2, e3) of a hex. Cost: O(1)."""
    out = []
    for k, (i, j, l) in enumerate(CORNER_NEIGHBOURS):
        out.append(det3(sub(h[i], h[k]), sub(h[j], h[k]), sub(h[l], h[k])))
    return out


def corners_positive(h: Hex) -> bool:
    """True when all 8 corner Jacobians are positive (necessary for validity, not sufficient)."""
    return all(d > 0 for d in corner_jacobians(h))


def trilinear(h: Hex, u, v, w) -> Point:
    """The point of the trilinear hex at the reference point (u, v, w)."""
    out = [0, 0, 0]
    for k, (a, b, c) in enumerate(REF):
        wt = (u if a else 1 - u) * (v if b else 1 - v) * (w if c else 1 - w)
        for t in range(3):
            out[t] += wt * h[k][t]
    return tuple(out)


def jacobian_det(h: Hex, u, v, w):
    """det of the Jacobian matrix of the trilinear hex at (u, v, w), exact for exact input."""
    du, dv, dw = [0, 0, 0], [0, 0, 0], [0, 0, 0]
    for k, (a, b, c) in enumerate(REF):
        fu, fv, fw = (u if a else 1 - u), (v if b else 1 - v), (w if c else 1 - w)
        su, sv, sw = (1 if a else -1), (1 if b else -1), (1 if c else -1)
        for t in range(3):
            du[t] += su * fv * fw * h[k][t]
            dv[t] += fu * sv * fw * h[k][t]
            dw[t] += fu * fv * sw * h[k][t]
    return det3(du, dv, dw)


def _to_bernstein2(f0, fh, f1):
    """Bernstein coefficients of the quadratic with values f0, fh, f1 at 0, 1/2, 1."""
    return (f0, 2 * fh - (f0 + f1) / Fraction(2), f1)


def jacobian_bernstein(h: Hex) -> List:
    """The 27 Bernstein coefficients of det J, which has degree 2 in each of u, v, w.

    The determinant is sampled at {0, 1/2, 1}^3 and converted direction by direction.
    Index order: coefficient (i, j, k) is at position 9 i + 3 j + k. Cost: O(1).
    """
    half = Fraction(1, 2)
    ts = (0, half, 1)
    vals = [[[jacobian_det(h, ts[i], ts[j], ts[k]) for k in range(3)] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            vals[i][j] = list(_to_bernstein2(*vals[i][j]))
    for i in range(3):
        for k in range(3):
            col = _to_bernstein2(vals[i][0][k], vals[i][1][k], vals[i][2][k])
            for j in range(3):
                vals[i][j][k] = col[j]
    for j in range(3):
        for k in range(3):
            col = _to_bernstein2(vals[0][j][k], vals[1][j][k], vals[2][j][k])
            for i in range(3):
                vals[i][j][k] = col[i]
    return [vals[i][j][k] for i in range(3) for j in range(3) for k in range(3)]


def bernstein_certified(h: Hex) -> bool:
    """True when every Bernstein coefficient of det J is positive, which proves det J > 0 on the whole hex."""
    return all(c > 0 for c in jacobian_bernstein(h))


def hex_volume(h: Hex):
    """The signed volume of the trilinear hex, the integral of det J over the unit cube.

    Each quadratic Bernstein polynomial integrates to 1/3 on [0, 1], so the integral is
    the mean of the 27 coefficients. Exact for exact input.
    """
    return sum(jacobian_bernstein(h)) / Fraction(27)


def solve(a: List[List], b: List) -> List:
    """Solve a x = b by Gaussian elimination with Fraction. Raises ValueError if singular."""
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(y)] for row, y in zip(a, b)]
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            raise ValueError("singular system")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[r][n] / m[r][r] for r in range(n)]
