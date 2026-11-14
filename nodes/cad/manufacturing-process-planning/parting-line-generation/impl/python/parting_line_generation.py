# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parting-line-generation/. The authors are listed in prov/D4D190.jsonl.

"""Parting line candidates of a closed polyhedral mesh for a parting direction.

The mesh is a closed, oriented 2-manifold: `verts` is a list of integer
points (x, y, z) and `faces` is a list of vertex index lists, each in
counterclockwise order seen from outside. A face is *upper* when its outward
normal n has n . d > 0 and *lower* when n . d < 0. A face with n . d = 0 goes
to the side given by `zero_side` (-1, the lower side, by default).

The parting line candidates are the boundary loops of the union of the upper
faces. Each loop is a list of vertex indices; the loop closes from the last
vertex back to the first, and the upper faces are on its left when seen from
outside. All arithmetic is on integers, so the face signs are exact.
"""

from typing import Dict, List, Sequence, Set, Tuple

Point = Tuple[int, int, int]
HalfEdge = Tuple[int, int]


def newell_normal(verts: Sequence[Point], face: Sequence[int]) -> Point:
    """Return twice the area vector of a planar face (Newell's method).

    For a planar polygon in counterclockwise order seen from outside, this
    is an outward normal whose length is twice the area. Exact on integers.
    Cost: O(k) for a face with k vertices.
    """
    nx = ny = nz = 0
    k = len(face)
    for i in range(k):
        x0, y0, z0 = verts[face[i]]
        x1, y1, z1 = verts[face[(i + 1) % k]]
        nx += (y0 - y1) * (z0 + z1)
        ny += (z0 - z1) * (x0 + x1)
        nz += (x0 - x1) * (y0 + y1)
    return (nx, ny, nz)


def face_signs(verts: Sequence[Point], faces: Sequence[Sequence[int]], d: Point, zero_side: int = -1) -> List[int]:
    """Return +1 for each upper face and -1 for each lower face.

    A face with n . d = 0 gets `zero_side`. Cost: O(total face size).
    """
    if zero_side not in (1, -1):
        raise ValueError("zero_side must be +1 or -1")
    signs = []
    for f in faces:  # @line L1
        n = newell_normal(verts, f)
        dot = n[0] * d[0] + n[1] * d[1] + n[2] * d[2]
        signs.append(1 if dot > 0 else -1 if dot < 0 else zero_side)
    return signs


def _half_edge_maps(faces: Sequence[Sequence[int]]) -> Tuple[Dict[HalfEdge, int], Dict[HalfEdge, HalfEdge]]:
    """Map each half-edge to its face, and to the next half-edge of that face.

    Cost: O(total face size) expected time with hashing.
    """
    owner: Dict[HalfEdge, int] = {}
    succ: Dict[HalfEdge, HalfEdge] = {}
    for fi, f in enumerate(faces):  # @line L2
        k = len(f)
        for i in range(k):
            h = (f[i], f[(i + 1) % k])
            if h in owner:
                raise ValueError("half-edge %r is used by two faces; the mesh is not oriented" % (h,))
            owner[h] = fi
            succ[h] = (f[(i + 1) % k], f[(i + 2) % k])
    for (u, v) in owner:
        if (v, u) not in owner:
            raise ValueError("edge %r has no twin; the mesh is not closed" % ((u, v),))
    return owner, succ


def silhouette_edges(verts: Sequence[Point], faces: Sequence[Sequence[int]], d: Point, zero_side: int = -1) -> Set[Tuple[int, int]]:
    """Return the edges (u, v), u < v, between an upper face and a lower face.

    Cost: O(total face size).
    """
    signs = face_signs(verts, faces, d, zero_side)
    owner, _ = _half_edge_maps(faces)
    out = set()
    for (u, v), f in owner.items():
        if signs[f] > 0 and signs[owner[(v, u)]] < 0:
            out.add((min(u, v), max(u, v)))
    return out


def parting_loops(verts: Sequence[Point], faces: Sequence[Sequence[int]], d: Point, zero_side: int = -1) -> List[List[int]]:
    """Return the boundary loops of the union of the upper faces.

    Each loop is a list of vertex indices with the upper faces on its left.
    The loops are in a fixed order (by their first half-edge in face order),
    so the result is deterministic. Cost: O(total face size).
    """
    signs = face_signs(verts, faces, d, zero_side)  # @line L1
    owner, succ = _half_edge_maps(faces)  # @line L2
    boundary: List[HalfEdge] = []
    for fi, f in enumerate(faces):  # @line L3
        if signs[fi] < 0:
            continue
        k = len(f)
        for i in range(k):
            h = (f[i], f[(i + 1) % k])
            if signs[owner[(h[1], h[0])]] < 0:
                boundary.append(h)
    nxt: Dict[HalfEdge, HalfEdge] = {}
    for h in boundary:
        g = succ[h]  # @line L4
        while signs[owner[(g[1], g[0])]] > 0:  # @line L5
            g = succ[(g[1], g[0])]
        nxt[h] = g  # @line L6
    loops: List[List[int]] = []
    used: Set[HalfEdge] = set()
    for h in boundary:  # @line L7
        if h in used:
            continue
        loop = []
        g = h
        while g not in used:
            used.add(g)
            loop.append(g[0])
            g = nxt[g]
        loops.append(loop)
    return loops  # @line L8
