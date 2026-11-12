# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/butterfly-subdivision/. The authors are listed in prov/SBR69E.jsonl.

"""One step of butterfly subdivision on a closed triangle mesh.

A mesh is a list of vertex positions (tuples of numbers, any dimension) and a
list of triangles, each a list of three vertex indices in a consistent cyclic
order. The mesh must be a closed oriented 2-manifold. The old vertices are
kept, and each edge gets one new point from the eight point butterfly stencil.
The option modified=True uses the rule of Zorin, Schroeder and Sweldens at
vertices of valence other than 6.
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


def half_edges(faces: Sequence[Sequence[int]]) -> dict:
    """Map each directed edge (a, b) to the third vertex of its triangle.

    Raise ValueError if a face is not a triangle or the mesh is not a closed
    oriented 2-manifold. Cost: O(F).
    """
    half = {}
    for f in faces:
        if len(f) != 3:
            raise ValueError("butterfly subdivision needs triangles")
        for i in range(3):
            e = (f[i], f[(i + 1) % 3])
            if e[0] == e[1] or e in half:
                raise ValueError("repeated directed edge %r" % (e,))
            half[e] = f[(i + 2) % 3]
    for a, b in half:
        if (b, a) not in half:
            raise ValueError("edge %r has no twin" % ((a, b),))
    return half


def butterfly_stencil(half: dict, a: int, b: int, w=Fraction(1, 16)) -> dict:
    """Return the weights of the eight point stencil of the edge ab as a dict vertex -> weight.

    The triangles of the edge are (a, b, c) and (b, a, d). The wings are the
    third vertices of the triangles across the other edges of these two.
    Precondition: half is the map of half_edges. Cost: O(1).
    """
    c, d = half[(a, b)], half[(b, a)]
    wings = [half[(c, b)], half[(a, c)], half[(d, a)], half[(b, d)]]
    st = {}
    for v, x in [(a, Fraction(1, 2)), (b, Fraction(1, 2)), (c, 2 * w), (d, 2 * w)] + [(u, -w) for u in wings]:
        st[v] = st.get(v, 0) + x
    return st


def ring(half: dict, v: int, start: int) -> list[int]:
    """Return the neighbors of v in cyclic order, beginning at start. Cost: O(n)."""
    out = [start]
    u = half[(v, start)]
    while u != start:
        out.append(u)
        u = half[(v, u)]
    return out


def zss_weights(k: int) -> list:
    """Return the weights s_0, ..., s_(k-1) of the ring of a vertex of valence k in the modified butterfly rule.

    The vertex itself has the weight 3/4. Precondition: k >= 3. Cost: O(k).
    """
    if k == 3:
        return [Fraction(5, 12), Fraction(-1, 12), Fraction(-1, 12)]
    if k == 4:
        return [Fraction(3, 8), Fraction(0), Fraction(-1, 8), Fraction(0)]
    return [(Fraction(1, 4) + cos_turn(j, k) + cos_turn(2 * j, k) / 2) / k for j in range(k)]


def modified_stencil(half: dict, a: int, b: int) -> dict:
    """Return the stencil of the edge ab in the modified butterfly rule. Cost: O(n_a + n_b)."""
    ra, rb = ring(half, a, b), ring(half, b, a)
    if len(ra) == 6 and len(rb) == 6:
        return butterfly_stencil(half, a, b)
    parts = []
    for v, r in [(a, ra), (b, rb)]:
        if len(r) != 6:
            st = {v: Fraction(3, 4)}
            for u, s in zip(r, zss_weights(len(r))):
                st[u] = st.get(u, 0) + s
            parts.append(st)
    out = {}
    for st in parts:
        for u, x in st.items():
            out[u] = out.get(u, 0) + x / len(parts)
    return out


def butterfly_subdivision(vertices: Sequence[Point], faces: Sequence[Sequence[int]], w=Fraction(1, 16), modified: bool = False) -> tuple[list[Point], list[Face]]:
    """Return the vertices and triangles of the mesh after one butterfly step.

    Precondition: a closed oriented 2-manifold triangle mesh. The new vertex
    list holds the V old vertices, unchanged, and then the E edge points in the
    order of the sorted edges. Cost: O(V + E + F) arithmetic on points.
    """
    half = half_edges(faces)
    nv = len(vertices)
    dim = len(vertices[0]) if nv else 0
    edges = sorted((a, b) for a, b in half if a < b)
    edge_id = {}
    edge_pts = []
    for a, b in edges:  # @line L1
        edge_id[(a, b)] = edge_id[(b, a)] = nv + len(edge_pts)
        st = modified_stencil(half, a, b) if modified else butterfly_stencil(half, a, b, w)  # @line L1
        edge_pts.append(tuple(sum(x * vertices[u][k] for u, x in st.items()) for k in range(dim)))  # @line L1
    vert_pts = [tuple(p) for p in vertices]  # @line L2
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
