# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plucker-ray-triangle-test/. The authors are listed in prov/C4PQD6.jsonl.

"""Ray-triangle test with Plucker line coordinates.

A directed line through p and then q has the Plucker coordinates
(U, V) = (q - p, p x q). The permuted inner product of two lines,
side(L1, L2) = U1 . V2 + U2 . V1, is zero when the lines meet or are
parallel, and its sign tells on which side one line passes the other.
A ray passes through a triangle when its sides with the three directed
edges have one sign. The ray parameter t comes from the plane of the
triangle. Points are 3-tuples of float, int or fractions.Fraction; with
Fraction inputs every step is exact.
"""

from typing import Optional, Sequence, Tuple

Vec = Sequence
Line = Tuple[tuple, tuple]


def sub(a: Vec, b: Vec) -> tuple:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec, b: Vec):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> tuple:
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def plucker_line(p: Vec, q: Vec) -> Line:
    """Plucker coordinates (direction, moment) of the line from p to q."""
    return (sub(q, p), cross(p, q))


def ray_line(o: Vec, d: Vec) -> Line:
    """Plucker coordinates of the ray o + t d: (d, o x d)."""
    return (tuple(d), cross(o, d))


def side(l1: Line, l2: Line):
    """Permuted inner product U1 . V2 + U2 . V1."""
    return dot(l1[0], l2[1]) + dot(l2[0], l1[1])


def plucker_intersect(o: Vec, d: Vec, a: Vec, b: Vec, c: Vec,
                      tmin=0, tmax=float("inf"),
                      edges: Optional[Tuple[Line, Line, Line]] = None):
    """Return (t, wa, wb, wc) of the hit with tmin < t < tmax, or None.

    wa, wb, wc are the barycentric weights of a, b, c. The edge lines
    ab, bc, ca can be given in edges, so that a mesh computes each
    shared edge once and its two triangles see the same numbers.
    """
    r = ray_line(o, d)                                       # @line L1
    if edges is None:
        edges = (plucker_line(a, b), plucker_line(b, c), plucker_line(c, a))
    s_ab = side(r, edges[0])                                 # @line L2
    s_bc = side(r, edges[1])
    s_ca = side(r, edges[2])
    if (s_ab < 0 or s_bc < 0 or s_ca < 0) and (s_ab > 0 or s_bc > 0 or s_ca > 0):
        return None                                          # @line L3
    total = s_ab + s_bc + s_ca                               # @line L4
    if total == 0:
        return None
    n = cross(sub(b, a), sub(c, a))                          # @line L5
    t = dot(n, sub(a, o)) / total                            # total = n . d
    if not (tmin < t < tmax):                                # @line L6
        return None
    return (t, s_bc / total, s_ca / total, s_ab / total)     # @line L7
