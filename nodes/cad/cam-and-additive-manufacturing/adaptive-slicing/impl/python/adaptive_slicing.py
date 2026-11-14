# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-slicing/. The authors are listed in prov/BT4MQH.jsonl.

"""Adaptive slicing with a cusp height bound.

Each layer of thickness t on a facet with unit normal n leaves a cusp of height
t |n_z| (Dolenc and Makela 1994). The method goes up from the bottom of the
mesh and gives each layer the largest allowed thickness for which every facet
that meets the open slab of the layer has cusp height at most c. If no allowed
thickness works, it uses the smallest one.

All tests are exact: with an integer or Fraction normal n, the condition
t |n_z| / |n| <= c is t^2 n_z^2 <= c^2 |n|^2.
"""

from fractions import Fraction


def facet_data(vertices, faces):
    """Return (zmin, zmax, nz^2, |n|^2) for each face, with n the cross product."""
    out = []
    for a, b, c in faces:
        p, q, r = vertices[a], vertices[b], vertices[c]
        u = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
        w = (r[0] - p[0], r[1] - p[1], r[2] - p[2])
        n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        zs = (p[2], q[2], r[2])
        out.append((min(zs), max(zs), n[2] * n[2], n[0] * n[0] + n[1] * n[1] + n[2] * n[2]))
    return out


def feasible(facets, z, t, c):
    """True if every facet that meets the open slab (z, z + t) has cusp height <= c."""
    for lo, hi, nz2, nn in facets:  # @line L8
        if lo < z + t and hi > z and t * t * nz2 > c * c * nn:  # @line L9
            return False  # @line L10
    return True  # @line L11


def adaptive_slice(vertices, faces, thicknesses, c):
    """Return the layer tops z_1 < z_2 < ... for the mesh, from its lowest point up.

    thicknesses: allowed layer thicknesses (positive int or Fraction).
    c: cusp height bound (positive int or Fraction).
    """
    ts = sorted(set(Fraction(t) for t in thicknesses))
    if not ts or ts[0] <= 0 or c <= 0:
        raise ValueError("thicknesses and the cusp bound must be positive")
    facets = facet_data(vertices, faces)
    zlo = min(v[2] for v in vertices)
    zhi = max(v[2] for v in vertices)
    z = Fraction(zlo)  # @line L1
    tops = []
    while z < zhi:  # @line L2
        t = ts[0]  # @line L3
        for s in reversed(ts):  # @line L4
            if feasible(facets, z, s, c):  # @line L5
                t = s
                break
        z = z + t  # @line L6
        tops.append(z)
    return tops  # @line L7


def max_cusp_ratio(facets, z, t):
    """Largest t^2 nz^2 / |n|^2 over the facets in the open slab (the squared cusp height)."""
    best = Fraction(0)
    for lo, hi, nz2, nn in facets:
        if lo < z + t and hi > z:
            best = max(best, Fraction(t * t * nz2, 1) / nn)
    return best


if __name__ == "__main__":
    v = [(0, 0, 0), (4, 0, 0), (4, 4, 0), (0, 4, 0), (0, 0, 2), (4, 0, 2), (4, 4, 2), (0, 4, 2), (2, 2, 3)]
    f = [(0, 2, 1), (0, 3, 2), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6),
         (3, 0, 4), (3, 4, 7), (4, 5, 8), (5, 6, 8), (6, 7, 8), (7, 4, 8)]
    tops = adaptive_slice(v, f, [Fraction(1, 4), Fraction(1, 2), 1], Fraction(1, 4))
    print([str(z) for z in tops])
