# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sqrt3-subdivision/. The authors are listed in prov/E9X6ZR.jsonl.

"""One step of Kobbelt's sqrt(3) subdivision on a closed triangle mesh.

A mesh is a list of vertex positions (tuples of numbers, any dimension) and a
list of triangles, each a list of three vertex indices in a consistent cyclic
order. The mesh must be a closed oriented 2-manifold. A step inserts the
centroid of each triangle, moves the old vertices, and flips every old edge.
The weights are exact fractions for valence 3, 4 and 6, and floating point
for other valences.
"""

import math
from fractions import Fraction
from typing import Sequence

Point = tuple
Face = list

_EXACT_COS = {
    Fraction(0): Fraction(1),
    Fraction(1, 6): Fraction(1, 2),
    Fraction(1, 4): Fraction(0),
    Fraction(1, 3): Fraction(-1, 2),
    Fraction(1, 2): Fraction(-1),
    Fraction(2, 3): Fraction(-1, 2),
    Fraction(3, 4): Fraction(0),
    Fraction(5, 6): Fraction(1, 2),
}


def cos_turn(m: int, k: int):
    """Return cos(2 pi m / k), as a Fraction when the value is rational. Cost: O(1)."""
    r = Fraction(m, k) % 1
    if r in _EXACT_COS:
        return _EXACT_COS[r]
    return math.cos(2 * math.pi * m / k)


def sqrt3_alpha(n: int):
    """Return alpha_n = (4 - 2 cos(2 pi / n)) / 9, the weight of the ring of a vertex of valence n.

    Precondition: n >= 3. Cost: O(1).
    """
    return (4 - 2 * cos_turn(1, n)) / Fraction(9)


def half_edges(faces: Sequence[Sequence[int]]) -> dict:
    """Map each directed edge (a, b) to the index of the triangle that has it.

    Raise ValueError if a face is not a triangle or the mesh is not a closed
    oriented 2-manifold. Cost: O(F).
    """
    half = {}
    for fi, f in enumerate(faces):
        if len(f) != 3:
            raise ValueError("sqrt(3) subdivision needs triangles")
        for i in range(3):
            e = (f[i], f[(i + 1) % 3])
            if e[0] == e[1] or e in half:
                raise ValueError("repeated directed edge %r" % (e,))
            half[e] = fi
    for a, b in half:
        if (b, a) not in half:
            raise ValueError("edge %r has no twin" % ((a, b),))
    return half


def sqrt3_subdivision(vertices: Sequence[Point], faces: Sequence[Sequence[int]]) -> tuple[list[Point], list[Face]]:
    """Return the vertices and triangles of the mesh after one sqrt(3) step.

    Precondition: a closed oriented 2-manifold triangle mesh in which every
    vertex is in some triangle. The new vertex list holds the V moved old
    vertices and then the F centroids, in the order of the faces. The new
    triangles come two per old edge, in the order of the sorted edges.
    Cost: O(V + E + F) arithmetic on points.
    """
    half = half_edges(faces)
    nv = len(vertices)
    dim = len(vertices[0]) if nv else 0
    cents = []
    for a, b, c in faces:  # @line L1
        cents.append(tuple((vertices[a][k] + vertices[b][k] + vertices[c][k]) / Fraction(3) for k in range(dim)))  # @line L1
    nbrs = [[] for _ in range(nv)]
    for a, b in half:
        nbrs[a].append(b)
    vert_pts = []
    for v in range(nv):  # @line L2
        n = len(nbrs[v])  # @line L2
        if n == 0:
            raise ValueError("vertex %d is in no triangle" % v)
        alpha = sqrt3_alpha(n)  # @line L2
        vert_pts.append(tuple((1 - alpha) * vertices[v][k] + alpha / n * sum(vertices[u][k] for u in nbrs[v]) for k in range(dim)))  # @line L2
    new_faces = []
    for a, b in sorted(e for e in half if e[0] < e[1]):  # @line L3
        cf, cg = nv + half[(a, b)], nv + half[(b, a)]  # @line L3
        new_faces += [[cf, a, cg], [cg, b, cf]]  # @line L3
    return vert_pts + cents, new_faces  # @line L4


def euler_characteristic(faces: Sequence[Sequence[int]]) -> int:
    """Return V - E + F of a closed mesh given by its faces. Cost: O(F)."""
    verts = {v for f in faces for v in f}
    edges = {frozenset((f[i], f[(i + 1) % len(f)])) for f in faces for i in range(len(f))}
    return len(verts) - len(edges) + len(faces)
