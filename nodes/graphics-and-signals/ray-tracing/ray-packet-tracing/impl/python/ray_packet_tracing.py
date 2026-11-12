# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ray-packet-tracing/. The authors are listed in prov/Y70MRZ.jsonl.
"""Ray packet traversal of a bounding volume hierarchy (BVH) of triangles.

A packet is a list of rays (o, d) traced together. The traversal keeps one stack of
(node, active rays). A node is visited once for the whole packet, with the subset of rays whose
current closest hit lies beyond the entry into the node's box. The result for each ray is the
same as tracing the ray alone. Coordinates may be float or Fraction; with Fraction every result
is exact. The `stats` dictionaries count node visits and ray-box tests.
"""

import math


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def triangle_hit(o, d, tri, t_max):
    """Parameter t in (0, t_max] where the ray meets the closed triangle, or None."""
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
    return t if 0 < t <= t_max else None


def box_hit(o, d, box, t_max):
    """True if the ray meets the closed box for some t in [0, t_max]."""
    lo, hi = box
    t0, t1 = 0, t_max
    for a in range(3):
        if d[a] == 0:
            if o[a] < lo[a] or o[a] > hi[a]:
                return False
            continue
        ta, tb = (lo[a] - o[a]) / d[a], (hi[a] - o[a]) / d[a]
        if ta > tb:
            ta, tb = tb, ta
        t0, t1 = max(t0, ta), min(t1, tb)
        if t0 > t1:
            return False
    return True


def build_bvh(tris, leaf_size=2):
    """Median split on the longest axis of the centroid box. Nodes are dicts."""

    def box_of(ids):
        pts = [v for i in ids for v in tris[i]]
        return (tuple(min(p[a] for p in pts) for a in range(3)), tuple(max(p[a] for p in pts) for a in range(3)))

    def build(ids):
        box = box_of(ids)
        if len(ids) <= leaf_size:
            return {"box": box, "prims": ids}
        cents = {i: tuple(sum(v[a] for v in tris[i]) for a in range(3)) for i in ids}
        ext = [max(cents[i][a] for i in ids) - min(cents[i][a] for i in ids) for a in range(3)]
        axis = ext.index(max(ext))
        ids = sorted(ids, key=lambda i: (cents[i][axis], i))
        mid = len(ids) // 2
        return {"box": box, "axis": axis, "kids": (build(ids[:mid]), build(ids[mid:]))}

    return build(list(range(len(tris))))


def better(t, k, best):
    """Closest hit by (t, primitive index), so that ties do not depend on the visiting order."""
    return best[0] is None or (t, k) < best


def trace_packet(root, tris, rays, t_max=math.inf, stats=None):
    """Closest hit (t, triangle index) or (None, None) for each ray of the packet."""
    best = [(None, None)] * len(rays)  # @line L1
    limit = [t_max] * len(rays)
    stack = [(root, list(range(len(rays))))]  # @line L2
    while stack:  # @line L3
        node, mask = stack.pop()  # @line L4
        if stats is not None:
            stats["nodes"] = stats.get("nodes", 0) + 1
            stats["box_tests"] = stats.get("box_tests", 0) + len(mask)
        mask = [i for i in mask if box_hit(rays[i][0], rays[i][1], node["box"], limit[i])]  # @line L5
        if not mask:  # @line L6
            continue
        if "prims" in node:  # @line L7
            for k in node["prims"]:  # @line L8
                for i in mask:
                    t = triangle_hit(rays[i][0], rays[i][1], tris[k], limit[i])
                    if t is not None and better(t, k, best[i]):
                        best[i], limit[i] = (t, k), t
        else:  # @line L9
            axis = node["axis"]
            near, far = node["kids"]
            if rays[mask[0]][1][axis] < 0:  # @line L10
                near, far = far, near
            stack.append((far, mask))  # @line L11
            stack.append((near, mask))
    return best  # @line L12


def trace_single(root, tris, o, d, t_max=math.inf, stats=None):
    """Closest hit of one ray by the usual depth-first BVH traversal: a packet of one ray."""
    return trace_packet(root, tris, [(o, d)], t_max, stats)[0]


def trace_linear(tris, o, d, t_max=math.inf):
    """Reference: test every triangle."""
    best = (None, None)
    for k, tri in enumerate(tris):
        t = triangle_hit(o, d, tri, t_max)
        if t is not None and better(t, k, best):
            best = (t, k)
    return best
