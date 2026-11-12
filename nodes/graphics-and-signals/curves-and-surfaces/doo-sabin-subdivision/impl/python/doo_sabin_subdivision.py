# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doo-sabin-subdivision/. The authors are listed in prov/4NCX83.jsonl.

"""One step of Doo-Sabin subdivision on a closed polygon mesh.

A mesh is a list of vertex positions (tuples of numbers, any dimension) and a
list of faces, each face a list of vertex indices in a consistent cyclic
order. The mesh must be a closed oriented 2-manifold. The step makes one new
point for each corner of each face, and one new face for each old face, each
old edge and each old vertex. The weights are exact fractions for faces with
3, 4 or 6 sides, and floats for other sizes.
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


def doo_sabin_weights(k: int) -> list:
    """Return the weights a_0, ..., a_(k-1) of the new point of corner 0 of a k-gon.

    The weight of the corner i steps away is a_i. Precondition: k >= 3.
    Cost: O(k).
    """
    w = [(3 + 2 * cos_turn(i, k)) / Fraction(4 * k) for i in range(k)]
    w[0] += Fraction(1, 4)
    return w


def half_edges(faces: Sequence[Sequence[int]]) -> dict:
    """Map each directed edge (a, b) to (face index, position of a in the face).

    Raise ValueError if the mesh is not a closed oriented 2-manifold.
    Cost: O(sum of face sizes).
    """
    half = {}
    for fi, f in enumerate(faces):
        k = len(f)
        if k < 3:
            raise ValueError("a face needs at least 3 vertices")
        for i in range(k):
            e = (f[i], f[(i + 1) % k])
            if e[0] == e[1] or e in half:
                raise ValueError("repeated directed edge %r" % (e,))
            half[e] = (fi, i)
    for a, b in half:
        if (b, a) not in half:
            raise ValueError("edge %r has no twin" % ((a, b),))
    return half


def doo_sabin(vertices: Sequence[Point], faces: Sequence[Sequence[int]]) -> tuple[list[Point], list[Face]]:
    """Return the vertices and faces of the mesh after one Doo-Sabin step.

    Precondition: a closed oriented 2-manifold mesh in which every vertex is
    in some face. The new point of corner i of face f has the index
    offset[f] + i, where offset[f] is the number of corners of the faces
    before f. Cost: O(sum over faces of deg(f)^2) arithmetic on points.
    """
    half = half_edges(faces)
    offset, total = [], 0
    for f in faces:
        offset.append(total)
        total += len(f)
    new_pts = []
    for f in faces:  # @line L1
        k = len(f)
        w = doo_sabin_weights(k)  # @line L1
        for i in range(k):  # @line L1
            new_pts.append(tuple(sum(w[(j - i) % k] * vertices[f[j]][c] for j in range(k)) for c in range(len(vertices[f[0]]))))  # @line L1
    new_faces = []
    for fi, f in enumerate(faces):  # @line L2
        new_faces.append([offset[fi] + i for i in range(len(f))])  # @line L2
    for (a, b), (fi, i) in sorted(half.items()):  # @line L3
        if a < b:  # @line L3
            gi, j = half[(b, a)]  # @line L3
            kf, kg = len(faces[fi]), len(faces[gi])
            pa, pb = offset[fi] + i, offset[fi] + (i + 1) % kf  # @line L3
            qb, qa = offset[gi] + j, offset[gi] + (j + 1) % kg  # @line L3
            new_faces.append([pb, pa, qa, qb])  # @line L3
    first = {}
    for (a, b), (fi, i) in half.items():
        first.setdefault(a, (fi, i))
    for v in range(len(vertices)):  # @line L4
        if v not in first:
            raise ValueError("vertex %d is in no face" % v)
        fi, i = first[v]  # @line L4
        ring = []
        while True:  # @line L4
            ring.append(offset[fi] + i)  # @line L4
            f = faces[fi]
            before = f[i - 1]
            fi, i = half[(v, before)]  # @line L4
            if (fi, i) == first[v]:
                break
        new_faces.append(ring)  # @line L4
    return new_pts, new_faces  # @line L5


def euler_characteristic(faces: Sequence[Sequence[int]]) -> int:
    """Return V - E + F of a closed mesh given by its faces. Cost: O(sum of face sizes)."""
    verts = {v for f in faces for v in f}
    edges = {frozenset((f[i], f[(i + 1) % len(f)])) for f in faces for i in range(len(f))}
    return len(verts) - len(edges) + len(faces)
