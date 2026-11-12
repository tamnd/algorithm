# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loop-subdivision/. The authors are listed in prov/4625V7.jsonl.

"""One step of Loop subdivision on a closed triangle mesh.

A mesh is a list of vertex positions (tuples of numbers, any dimension) and a
list of triangles, each a list of three vertex indices in a consistent cyclic
order. The mesh must be a closed oriented 2-manifold. The weights are exact
fractions for valence 3, 4 and 6 with Loop's rule, and for all valences with
Warren's rule; Loop's rule uses floating point cosines for other valences.
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


def loop_beta(n: int, rule: str = "loop"):
    """Return the weight beta of each neighbor of a vertex of valence n.

    rule "loop": beta = (5/8 - (3/8 + cos(2 pi / n) / 4)^2) / n.
    rule "warren": beta = 3/16 for n = 3 and 3/(8n) for n > 3.
    Precondition: n >= 3. Cost: O(1).
    """
    if rule == "warren":
        return Fraction(3, 16) if n == 3 else Fraction(3, 8 * n)
    if rule != "loop":
        raise ValueError("rule must be 'loop' or 'warren'")
    c = Fraction(3, 8) + cos_turn(1, n) / 4
    return (Fraction(5, 8) - c * c) / n


def half_edges(faces: Sequence[Sequence[int]]) -> dict:
    """Map each directed edge (a, b) to the third vertex of its triangle.

    Raise ValueError if a face is not a triangle or the mesh is not a closed
    oriented 2-manifold. Cost: O(F).
    """
    half = {}
    for f in faces:
        if len(f) != 3:
            raise ValueError("Loop subdivision needs triangles")
        for i in range(3):
            e = (f[i], f[(i + 1) % 3])
            if e[0] == e[1] or e in half:
                raise ValueError("repeated directed edge %r" % (e,))
            half[e] = f[(i + 2) % 3]
    for a, b in half:
        if (b, a) not in half:
            raise ValueError("edge %r has no twin" % ((a, b),))
    return half


def loop_subdivision(vertices: Sequence[Point], faces: Sequence[Sequence[int]], rule: str = "loop") -> tuple[list[Point], list[Face]]:
    """Return the vertices and triangles of the mesh after one Loop step.

    Precondition: a closed oriented 2-manifold triangle mesh in which every
    vertex is in some triangle. The new vertex list holds the V vertex points
    and then the E edge points in the order of the sorted edges.
    Cost: O(V + E + F) arithmetic on points.
    """
    half = half_edges(faces)
    nv = len(vertices)
    dim = len(vertices[0]) if nv else 0
    edges = sorted((a, b) for a, b in half if a < b)
    edge_id = {}
    edge_pts = []
    for a, b in edges:  # @line L1
        edge_id[(a, b)] = edge_id[(b, a)] = nv + len(edge_pts)
        c, d = half[(a, b)], half[(b, a)]  # @line L1
        edge_pts.append(tuple(Fraction(3, 8) * (vertices[a][k] + vertices[b][k]) + Fraction(1, 8) * (vertices[c][k] + vertices[d][k]) for k in range(dim)))  # @line L1
    nbrs = [[] for _ in range(nv)]
    for a, b in edges:
        nbrs[a].append(b)
        nbrs[b].append(a)
    vert_pts = []
    for v in range(nv):  # @line L2
        n = len(nbrs[v])  # @line L2
        if n == 0:
            raise ValueError("vertex %d is in no triangle" % v)
        beta = loop_beta(n, rule)  # @line L2
        vert_pts.append(tuple((1 - n * beta) * vertices[v][k] + beta * sum(vertices[u][k] for u in nbrs[v]) for k in range(dim)))  # @line L2
    new_faces = []
    for a, b, c in faces:  # @line L3
        ab, bc, ca = edge_id[(a, b)], edge_id[(b, c)], edge_id[(c, a)]  # @line L3
        new_faces += [[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]]  # @line L3
    return vert_pts + edge_pts, new_faces  # @line L4


def euler_characteristic(faces: Sequence[Sequence[int]]) -> int:
    """Return V - E + F of a closed mesh given by its faces. Cost: O(F)."""
    verts = {v for f in faces for v in f}
    edges = {frozenset((f[i], f[(i + 1) % len(f)])) for f in faces for i in range(len(f))}
    return len(verts) - len(edges) + len(faces)
