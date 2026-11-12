# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-volume-algorithm/. The authors are listed in prov/K1P3D1.jsonl.

"""Shadow volumes for a point light, with z-pass and z-fail counting.

An occluder is a closed triangle mesh: a list of faces (v0, v1, v2) listed
counterclockwise seen from outside, with int or Fraction coordinates. For a
light L, the faces whose outer side faces L form the near cap; each edge
between such a face and a face that does not face L is a silhouette edge,
and it is extruded away from L into a quad; the other faces, moved away from
L by the map v -> v + k (v - L), form the far cap. The result is a closed,
consistently oriented polyhedron for each occluder, and its interior is the
region behind the occluder up to the far cap.

For each visible point P (the point that the z-buffer holds at a pixel) the
counter adds the signed crossings of the volume faces with the eye ray. The
z-pass rule counts the faces between the eye and P; the z-fail rule counts
the faces behind P. P is in shadow when the counter is not zero. This is the
stencil buffer algorithm done by exact ray casting in place of rasterizing.
"""

from typing import Sequence


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def normal(tri):
    return cross(sub(tri[1], tri[0]), sub(tri[2], tri[0]))


def faces_toward(tri, point) -> bool:
    """Is `point` strictly on the outer side of the plane of the face?"""
    return dot(normal(tri), sub(point, tri[0])) > 0


def build_volume(occluder: Sequence, light, k=1000) -> list:
    """The triangles of the closed shadow volume of one occluder."""
    lit = [faces_toward(f, light) for f in occluder]  # @line L2
    away = lambda v: tuple(v[m] + k * (v[m] - light[m]) for m in range(3))
    tris = [tuple(f) for f, s in zip(occluder, lit) if s]  # near cap
    owner = {}
    for f, s in zip(occluder, lit):
        for e in range(3):
            owner[(f[e], f[(e + 1) % 3])] = s
    for (u, v), s in owner.items():  # @line L3
        if s and not owner[(v, u)]:  # u -> v is in a lit face, v -> u in an unlit one
            tris.append((v, u, away(u)))  # @line L4
            tris.append((v, away(u), away(v)))
    tris.extend(tuple(away(v) for v in f) for f, s in zip(occluder, lit) if not s)  # far cap
    return tris


def side(c, p, a, b) -> int:
    """The side of the directed edge a -> b on which the line c -> p passes, never 0.

    A zero is broken by the order of a and b, so two triangles that share an
    edge, which use it in opposite directions, never both count one crossing.
    """
    s = dot(sub(p, c), cross(sub(a, c), sub(b, c)))
    if s != 0:
        return 1 if s > 0 else -1
    return 1 if a < b else -1


def crossing(tri, c, p):
    """Return (t, sign) where the line c + t (p - c) crosses the triangle, else None.

    sign is +1 when the line enters the volume there (the face faces c), -1 when it leaves.
    """
    a, b, d = tri
    n = normal(tri)
    den = dot(n, sub(p, c))
    if den == 0:
        return None
    s1, s2, s3 = side(c, p, a, b), side(c, p, b, d), side(c, p, d, a)
    if not (s1 == s2 == s3):
        return None
    num = dot(n, sub(a, c))
    return (num, den), (1 if den < 0 else -1)


def before(t, one=True) -> bool:
    """Is the parameter t = num / den strictly between 0 and 1 (z-pass) or strictly above 1 (z-fail)?"""
    num, den = t
    if den < 0:
        num, den = -num, -den
    return 0 < num < den if one else num > den


def shadow_volumes(occluders: Sequence, light, eye, points: Sequence, method: str = "zfail", k=1000) -> list[bool]:
    """For each visible point, is it in shadow? `method` is 'zpass' or 'zfail'."""
    volume = []
    for occ in occluders:  # @line L1
        volume.extend(build_volume(occ, light, k))
    result = []
    for p in points:  # @line L5
        count = 0  # @line L6
        for tri in volume:  # @line L7
            hit = crossing(tri, eye, p)
            if hit is None:
                continue
            t, sign = hit
            if method == "zpass" and before(t, True):  # @line L8
                count += sign  # the face is in front of p: depth test passes
            elif method == "zfail" and before(t, False):  # @line L9
                count -= sign  # the face is behind p: depth test fails
        result.append(count != 0)  # @line L10
    return result  # @line L11
