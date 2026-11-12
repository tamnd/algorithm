# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/object-instancing/. The authors are listed in prov/H66630.jsonl.
"""Object instancing for a ray tracer.

An instance is a reference to one shared object together with an affine map x -> A x + s from
object space to world space. A ray is intersected with the instance by mapping the ray into
object space with the inverse map, and the normal is mapped back with the inverse transpose of
A. Coordinates may be float or Fraction; with Fraction every result is exact.
"""

import math


def mat_vec(m, v):
    return tuple(sum(m[i][j] * v[j] for j in range(3)) for i in range(3))


def transpose(m):
    return tuple(tuple(m[j][i] for j in range(3)) for i in range(3))


def sub(a, b):
    return tuple(a[i] - b[i] for i in range(3))


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def det3(m):
    return dot(m[0], cross(m[1], m[2]))


def inverse3(m):
    """Inverse of a 3x3 matrix by the adjugate."""
    det = det3(m)
    if det == 0:
        raise ValueError("singular matrix")
    cols = (cross(m[1], m[2]), cross(m[2], m[0]), cross(m[0], m[1]))  # columns of the inverse
    return tuple(tuple(cols[j][i] / det for j in range(3)) for i in range(3))


def make_instance(obj, a, shift):
    """An instance of object `obj` (an index into the shared objects) under x -> a x + shift."""
    return {"obj": obj, "a": a, "shift": shift, "inv": inverse3(a)}


def to_world(inst, p):
    return tuple(c + s for c, s in zip(mat_vec(inst["a"], p), inst["shift"]))


def triangle_hit(o, d, tri, t_min, t_max):
    """(t, normal) where o + t d meets the closed triangle, with t_min < t <= t_max, or None.

    The normal is the cross product of the edges, not normalized.
    """
    v0, v1, v2 = tri
    e1, e2 = sub(v1, v0), sub(v2, v0)
    pv = cross(d, e2)
    det = dot(e1, pv)
    if det == 0:
        return None
    tv = sub(o, v0)
    u = dot(tv, pv) / det
    if u < 0 or u > 1:
        return None
    qv = cross(tv, e1)
    v = dot(d, qv) / det
    if v < 0 or u + v > 1:
        return None
    t = dot(e2, qv) / det
    if t <= t_min or t > t_max:
        return None
    return t, cross(e1, e2)


def mesh_hitter(mesh):
    """An object-space intersector for a triangle list: returns (t, triangle index, normal)."""

    def hit(o, d, t_min, t_max):
        best = None
        for k, tri in enumerate(mesh):
            h = triangle_hit(o, d, tri, t_min, t_max)
            if h is not None and (best is None or h[0] < best[0]):
                best = (h[0], k, h[1])
        return best

    return hit


def unit_sphere_hit(o, d, t_min, t_max):
    """Object-space intersector for the unit sphere at the origin (float): (t, 0, normal)."""
    a, b, c = dot(d, d), 2 * dot(o, d), dot(o, o) - 1
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    root = math.sqrt(disc)
    for t in ((-b - root) / (2 * a), (-b + root) / (2 * a)):
        if t_min < t <= t_max:
            p = tuple(o[i] + t * d[i] for i in range(3))
            return t, 0, p
    return None


def intersect_instance(inst, hit_object, o, d, t_min=0, t_max=math.inf):
    """Hit (t, world point, primitive index, world normal) of the ray with the instance, or None."""
    inv = inst["inv"]
    o2 = mat_vec(inv, sub(o, inst["shift"]))  # @line L1
    d2 = mat_vec(inv, d)  # not normalized, so t is the same in both spaces
    hit = hit_object(o2, d2, t_min, t_max)  # @line L2
    if hit is None:  # @line L3
        return None
    t, k, n_obj = hit  # @line L4
    p = tuple(o[i] + t * d[i] for i in range(3))  # @line L5
    n = mat_vec(transpose(inv), n_obj)  # @line L6
    return t, p, k, n  # @line L7


def object_box(mesh):
    lo = tuple(min(v[a] for tri in mesh for v in tri) for a in range(3))
    hi = tuple(max(v[a] for tri in mesh for v in tri) for a in range(3))
    return lo, hi


def world_box(inst, box):
    """World bounding box of an instance: the box of the 8 mapped corners of the object box."""
    lo, hi = box
    corners = [to_world(inst, (x, y, z)) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
    return (tuple(min(c[a] for c in corners) for a in range(3)), tuple(max(c[a] for c in corners) for a in range(3)))


def box_entry(o, d, box, t_min, t_max):
    """Slab test: the entry parameter of the ray into the closed box within [t_min, t_max], or None."""
    lo, hi = box
    for a in range(3):
        if d[a] == 0:
            if o[a] < lo[a] or o[a] > hi[a]:
                return None
            continue
        ta, tb = (lo[a] - o[a]) / d[a], (hi[a] - o[a]) / d[a]
        if ta > tb:
            ta, tb = tb, ta
        t_min, t_max = max(t_min, ta), min(t_max, tb)
        if t_min > t_max:
            return None
    return t_min


def trace_scene(instances, hitters, boxes, o, d, t_min=0, t_max=math.inf):
    """Closest hit (t, instance index, primitive index, world point, world normal), or None.

    `hitters[k]` intersects object k in object space and `boxes[k]` is its object box.
    """
    best = None  # @line L8
    for idx, inst in enumerate(instances):  # @line L9
        limit = t_max if best is None else best[0]
        if box_entry(o, d, world_box(inst, boxes[inst["obj"]]), t_min, limit) is None:
            continue
        h = intersect_instance(inst, hitters[inst["obj"]], o, d, t_min, limit)  # @line L10
        if h is not None and (best is None or h[0] < best[0]):  # @line L11
            best = (h[0], idx, h[2], h[1], h[3])
    return best  # @line L12
