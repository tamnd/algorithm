# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/catmull-clark-subdivision/. The authors are listed in prov/8H54E8.jsonl.

"""One step of Catmull-Clark subdivision on a closed polygon mesh.

A mesh is a list of vertex positions (tuples of numbers, any dimension) and a
list of faces, each face a list of vertex indices in a consistent cyclic
order. The mesh must be a closed oriented 2-manifold: each directed edge
appears in exactly one face, and its reverse appears in exactly one other
face. With int or Fraction coordinates the result is exact.
"""

from fractions import Fraction
from typing import Sequence

Point = tuple
Face = list


def half_edges(faces: Sequence[Sequence[int]]) -> dict:
    """Map each directed edge (a, b) to the index of the face that has it.

    Raise ValueError if a directed edge appears twice or has no twin, so the
    mesh is not a closed oriented 2-manifold. Cost: O(sum of face sizes).
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
            half[e] = fi
    for a, b in half:
        if (b, a) not in half:
            raise ValueError("edge %r has no twin" % ((a, b),))
    return half


def _average(points: Sequence[Point]) -> Point:
    m = Fraction(len(points))
    return tuple(sum(c) / m for c in zip(*points))


def catmull_clark(vertices: Sequence[Point], faces: Sequence[Sequence[int]]) -> tuple[list[Point], list[Face]]:
    """Return the vertices and faces of the mesh after one Catmull-Clark step.

    Precondition: a closed oriented 2-manifold mesh in which every vertex is
    in some face. The new vertex list holds the V vertex points, then the E
    edge points in the order of the sorted edges, then the F face points.
    All new faces are quads. Cost: O(V + E + F) arithmetic on points.
    """
    half = half_edges(faces)
    nv = len(vertices)
    face_pts = [_average([vertices[i] for i in f]) for f in faces]  # @line L1
    edges = sorted((a, b) for a, b in half if a < b)
    edge_id = {}
    edge_pts = []
    for a, b in edges:  # @line L2
        edge_id[(a, b)] = edge_id[(b, a)] = len(edge_pts)
        f, g = half[(a, b)], half[(b, a)]  # @line L2
        edge_pts.append(_average([vertices[a], vertices[b], face_pts[f], face_pts[g]]))  # @line L2
    around = [[] for _ in range(nv)]
    nbrs = [[] for _ in range(nv)]
    for fi, f in enumerate(faces):
        for v in f:
            around[v].append(fi)
    for a, b in edges:
        nbrs[a].append(b)
        nbrs[b].append(a)
    vert_pts = []
    for v in range(nv):  # @line L3
        n = len(nbrs[v])  # @line L3
        if n == 0:
            raise ValueError("vertex %d is in no face" % v)
        q = _average([face_pts[f] for f in around[v]])  # @line L3
        r = _average([_average([vertices[v], vertices[u]]) for u in nbrs[v]])  # @line L3
        vert_pts.append(tuple((q[k] + 2 * r[k] + (n - 3) * vertices[v][k]) / Fraction(n) for k in range(len(q))))  # @line L4
    new_faces = []
    for fi, f in enumerate(faces):  # @line L5
        k = len(f)
        for i in range(k):  # @line L5
            a, b, z = f[i], f[(i + 1) % k], f[i - 1]
            new_faces.append([a, nv + edge_id[(a, b)], nv + len(edges) + fi, nv + edge_id[(z, a)]])  # @line L5
    return vert_pts + edge_pts + face_pts, new_faces  # @line L6


def euler_characteristic(faces: Sequence[Sequence[int]]) -> int:
    """Return V - E + F of a closed mesh given by its faces. Cost: O(sum of face sizes)."""
    verts = {v for f in faces for v in f}
    edges = {frozenset((f[i], f[(i + 1) % len(f)])) for f in faces for i in range(len(f))}
    return len(verts) - len(edges) + len(faces)
