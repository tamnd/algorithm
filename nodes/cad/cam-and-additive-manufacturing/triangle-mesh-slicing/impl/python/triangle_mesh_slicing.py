# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-mesh-slicing/. The authors are listed in prov/ETJZAW.jsonl.

"""Slice a closed triangle mesh by horizontal planes into closed, oriented contours.

The method is the plane sweep of Minetto, Volpato, Stolfi, Gregori and da Silva
(2017). Each triangle goes into the bucket of the first plane above its lowest
vertex (binary search), the planes are swept from the bottom up with a list of
active triangles, and the segments of one plane are linked into loops with a
hash table keyed by the crossed mesh edge.

Input: vertices as (x, y, z) tuples of int or Fraction, faces as index triples
in counterclockwise order seen from outside (outward normal by the right-hand
rule), and strictly increasing plane heights. The mesh must be closed, oriented
and edge-manifold. A vertex at the height of a plane counts as above it, so the
plane z = Z acts as the plane z = Z - epsilon for a tiny epsilon > 0.

Output: for each plane, a list of loops, each a list of (x, y) points. Outer
loops are counterclockwise seen from above and holes are clockwise.
"""

from bisect import bisect_right
from fractions import Fraction


def crossing(vertices, face, z):
    """Return (e_out, p, e_in) for the face at height z, or None.

    e_out is the edge that goes from above to below in the face order, p its
    crossing point, and e_in the edge that goes from below to above. Edges are
    keys (min index, max index).
    """
    above = [vertices[v][2] >= z for v in face]
    if all(above) or not any(above):
        return None
    e_out = e_in = p = None
    for i in range(3):
        a, b = face[i], face[(i + 1) % 3]
        if above[i] and not above[(i + 1) % 3]:
            e_out, p = (min(a, b), max(a, b)), edge_point(vertices[a], vertices[b], z)
        elif not above[i] and above[(i + 1) % 3]:
            e_in = (min(a, b), max(a, b))
    return e_out, p, e_in


def edge_point(a, b, z):
    """Exact (x, y) where the segment ab meets the plane of height z (a[2] != b[2])."""
    t = Fraction(z - a[2]) / (b[2] - a[2])
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def link(segments):
    """Link segments {e_out: (p, e_in)} into loops of points."""
    loops = []  # @line L15
    while segments:  # @line L16
        e0 = next(iter(segments))  # @line L17
        e, loop = e0, []
        while True:  # @line L18
            p, e = segments.pop(e)  # @line L19
            loop.append(p)
            if e == e0:  # @line L20
                break
        loops.append(loop)  # @line L21
    return loops  # @line L22


def slice_mesh(vertices, faces, planes):
    """Return one list of loops for each plane height, in the order of planes."""
    k = len(planes)
    if any(planes[i] >= planes[i + 1] for i in range(k - 1)):
        raise ValueError("plane heights must be strictly increasing")
    zmin = [min(vertices[v][2] for v in f) for f in faces]
    zmax = [max(vertices[v][2] for v in f) for f in faces]
    buckets = [[] for _ in range(k + 1)]  # @line L1
    for t in range(len(faces)):  # @line L2
        j = bisect_right(planes, zmin[t])  # @line L3
        buckets[j].append(t)  # @line L4
    active = []  # @line L5
    result = []
    for j in range(k):  # @line L6
        active.extend(buckets[j])  # @line L7
        active = [t for t in active if zmax[t] >= planes[j]]  # @line L8
        segments = {}  # @line L9
        for t in active:  # @line L10
            e_out, p, e_in = crossing(vertices, faces[t], planes[j])  # @line L11
            segments[e_out] = (p, e_in)  # @line L12
        result.append(link(segments))  # @line L13
    return result  # @line L14


def signed_area(loop):
    """Shoelace signed area of a closed loop of (x, y) points."""
    s = 0
    for i in range(len(loop)):
        (x0, y0), (x1, y1) = loop[i], loop[(i + 1) % len(loop)]
        s += x0 * y1 - x1 * y0
    return Fraction(s) / 2


if __name__ == "__main__":
    cube_v = [(x, y, z) for z in (0, 2) for y in (0, 2) for x in (0, 2)]
    cube_f = [(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4),
              (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)]
    for z, loops in zip([0, 1, 2], slice_mesh(cube_v, cube_f, [0, 1, 2])):
        print(z, [[(str(x), str(y)) for x, y in lp] for lp in loops], [str(signed_area(lp)) for lp in loops])
