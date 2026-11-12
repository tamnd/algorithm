# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-tetrahedra/. The authors are listed in prov/2FMDJR.jsonl.

"""Marching tetrahedra: a triangle mesh of the level set f = c of a 3D sample grid.

The field is field[z][y][x]. A sample is inside when it is less than c. Each
cell (a unit cube) is cut into the 6 tetrahedra of the Kuhn (Freudenthal)
triangulation, which all share the diagonal from corner 0 to corner 7. On
each tetrahedron the piecewise linear interpolant of the samples is linear, so
its level set is one triangle (1 or 3 inside corners), one quadrilateral
(2 inside corners) or nothing. The cut of each face of a tetrahedron depends
only on the three signs of that face, so there is no ambiguous case.
"""

from fractions import Fraction
from typing import Union

Number = Union[int, float, Fraction]
Vec = tuple[Number, Number, Number]

# Corner k of a cell is at offset (k & 1, (k >> 1) & 1, (k >> 2) & 1).
CORNERS = [(k & 1, (k >> 1) & 1, (k >> 2) & 1) for k in range(8)]
# The 6 tetrahedra: monotone paths from corner 0 to corner 7, one axis at a time.
TETS = [(0, 1, 3, 7), (0, 3, 2, 7), (0, 2, 6, 7), (0, 6, 4, 7), (0, 4, 5, 7), (0, 5, 1, 7)]


def _sub(p: Vec, q: Vec) -> Vec:
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _cross(u: Vec, v: Vec) -> Vec:
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _dot(u: Vec, v: Vec) -> Number:
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def tet_triangles(inside: list[bool]) -> list[tuple[tuple[int, int], ...]]:
    """Triangles of one tetrahedron, as triples of its edges (i, j) with i inside.

    The vertices of the tetrahedron are 0..3 and inside[i] tells which are
    inside. The triangles are oriented with the normal toward the outside
    vertices; the orientation is decided by a test at the edge midpoints of a
    regular reference tetrahedron, where the cut is a plane that separates
    the inside vertices from the outside ones.
    """
    ins = [i for i in range(4) if inside[i]]
    out = [i for i in range(4) if not inside[i]]
    if len(ins) in (0, 4):
        return []
    if len(ins) == 1:  # @line L11
        a = ins[0]
        polys = [[(a, out[0]), (a, out[1]), (a, out[2])]]
    elif len(ins) == 3:
        b = out[0]
        polys = [[(ins[0], b), (ins[1], b), (ins[2], b)]]
    else:
        a, b = ins
        c, d = out
        # the quadrilateral ac, ad, bd, bc, cut along the chord ac-bd inside the tetrahedron
        polys = [[(a, c), (a, d), (b, d)], [(a, c), (b, d), (b, c)]]  # @line L12
    ref = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2)]
    tris = []
    for tri in polys:
        mids = [tuple(ref[i][k] + ref[j][k] for k in range(3)) for i, j in tri]  # twice the midpoints
        n = _cross(_sub(mids[1], mids[0]), _sub(mids[2], mids[0]))
        o = tuple(2 * v for v in ref[out[0]])
        if _dot(n, _sub(o, mids[0])) < 0:  # @line L13
            tri = [tri[0], tri[2], tri[1]]
        tris.append(tuple(tri))
    return tris


# Table over the 16 sign patterns of a tetrahedron (bit i set when vertex i is inside).
TET_TABLE = [tet_triangles([bool(m >> i & 1) for i in range(4)]) for m in range(16)]  # @line L10


def _lerp(pa: Vec, pb: Vec, fa: Number, fb: Number, c: Number) -> Vec:
    if isinstance(fa, float) or isinstance(fb, float) or isinstance(c, float):
        t: Number = (c - fa) / (fb - fa)
    else:
        t = Fraction(c - fa) / (fb - fa)
    return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]), pa[2] + t * (pb[2] - pa[2]))


def marching_tetrahedra(field: list[list[list[Number]]], c: Number) -> tuple[list[Vec], list[tuple[int, int, int]]]:
    """Return (vertices, triangles) of the level set field = c.

    Precondition: field[z][y][x] is a box of at least 2 by 2 by 2 numbers.
    Each vertex lies on an edge of the Kuhn tetrahedralization (a cell edge, a
    face diagonal or a body diagonal) whose two samples are on different sides
    of c, at the point of linear interpolation, and is shared by all
    tetrahedra around that edge. Triangles are oriented with the normal toward
    the outside (values at least c). If every border sample is outside, the
    mesh is a closed, oriented 2-manifold, and it is the exact level set of the
    piecewise linear interpolant. Cost: O(X Y Z) time for an X by Y by Z grid.
    """
    nz, ny, nx = len(field), len(field[0]), len(field[0][0])
    verts: list[Vec] = []  # @line L1
    index: dict[tuple[tuple[int, int, int], tuple[int, int, int]], int] = {}
    tris: list[tuple[int, int, int]] = []

    def vertex(pa: tuple[int, int, int], pb: tuple[int, int, int]) -> int:
        key = (pa, pb) if pa < pb else (pb, pa)  # @line L6
        k = index.get(key)
        if k is None:  # @line L7
            fa = field[pa[2]][pa[1]][pa[0]]
            fb = field[pb[2]][pb[1]][pb[0]]
            k = len(verts)
            verts.append(_lerp(pa, pb, fa, fb, c))
            index[key] = k
        return k

    for z in range(nz - 1):  # @line L2
        for y in range(ny - 1):
            for x in range(nx - 1):
                pts = [(x + dx, y + dy, z + dz) for dx, dy, dz in CORNERS]
                ins = [field[p[2]][p[1]][p[0]] < c for p in pts]
                for tet in TETS:  # @line L3
                    m = sum(1 << i for i in range(4) if ins[tet[i]])  # @line L4
                    for tri in TET_TABLE[m]:  # @line L5
                        tris.append(tuple(vertex(pts[tet[i]], pts[tet[j]]) for i, j in tri))  # @line L8
    return verts, tris  # @line L9
