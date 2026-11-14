# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shape-diameter-function/. The authors are listed in prov/WRAPDK.jsonl.

"""Shape diameter function (Shapira, Shamir and Cohen-Or, The Visual Computer 2008).

For a face f of a closed triangle mesh with outward normals, rays leave the
centroid of f inside a cone about the inward normal. Each ray stops at the
first face it hits. The lengths that are far from the median are dropped,
and the mean of the others is the SDF of f, a measure of the local thickness.

The ray-triangle tests are exact: all coordinates, ray origins and ray
directions are turned into Fractions, so the hit parameter t, the choice of
the first face and the side from which the ray reaches it are decided without
rounding. Only the final lengths t |d| are floats.
"""

import math
import statistics

from mx1mesh import cross, dot, exact, norm, sub, unit


def ray_triangle(o, d, a, b, c):
    """The exact t > 0 with o + t d in the closed triangle abc, or None. A ray parallel to the plane of abc misses."""
    o, d, a, b, c = exact(o), exact(d), exact(a), exact(b), exact(c)
    e1, e2 = sub(b, a), sub(c, a)
    pv = cross(d, e2)
    det = dot(e1, pv)
    if det == 0:
        return None
    s = sub(o, a)
    u = dot(s, pv) / det
    if u < 0 or u > 1:
        return None
    qv = cross(s, e1)
    v = dot(d, qv) / det
    if v < 0 or u + v > 1:
        return None
    t = dot(e2, qv) / det
    return t if t > 0 else None


def exact_cross(points, face):
    """cross(b - a, c - a) of the face, computed exactly: its direction is the outward normal."""
    a, b, c = (exact(points[i]) for i in face)
    return cross(sub(b, a), sub(c, a))


def first_hit(points, faces, o, d, skip):
    """The smallest exact t of a hit of the ray o + t d with a face other than skip, and the faces hit at that t."""
    best, hit = None, []
    for g, (a, b, c) in enumerate(faces):
        if g == skip:
            continue
        t = ray_triangle(o, d, points[a], points[b], points[c])
        if t is None:
            continue
        if best is None or t < best:
            best, hit = t, [g]
        elif t == best:
            hit.append(g)  # the ray passes through an edge or a vertex
    return best, hit


def cone_directions(n, rays, angle):
    """Directions in the cone of full opening angle about the vector n: n itself, then rings of 8.

    rays is rounded down to 1 + 8 k. The ring r of k sits at the angle (angle / 2) r / k from n.
    The directions are floats made exact with Fraction, so every later test on them is exact.
    """
    axis = unit(n)
    helper = (1.0, 0.0, 0.0) if abs(axis[0]) < 0.9 else (0.0, 1.0, 0.0)
    u = unit(cross(axis, helper))
    w = cross(axis, u)
    out = [exact(n)]
    rings = (rays - 1) // 8
    for r in range(1, rings + 1):
        th = angle / 2 * r / rings
        for k in range(8):
            ph = 2 * math.pi * (k + r / 2) / 8
            d = tuple(math.cos(th) * axis[i] + math.sin(th) * (math.cos(ph) * u[i] + math.sin(ph) * w[i]) for i in range(3))
            out.append(exact(d))
    return out


def ray_lengths(points, faces, f, rays=25, angle=2 * math.pi / 3):
    """The lengths of the rays of face f that leave the solid at their first hit."""
    a, b, c = (exact(points[i]) for i in faces[f])
    o = tuple((x + y + z) / 3 for x, y, z in zip(a, b, c))  # @line L1
    inward = tuple(-x for x in exact_cross(points, faces[f]))
    lengths = []
    directions = cone_directions(inward, rays, angle)  # @line L2
    for d in directions:  # @line L3
        t, hit = first_hit(points, faces, o, d, f)  # @line L4
        if t is None:
            continue  # the ray leaves through a hole
        if any(dot(d, exact_cross(points, faces[g])) > 0 for g in hit):  # exact: the ray goes out at g
            lengths.append(float(t) * norm(tuple(float(x) for x in d)))  # @line L5
    return lengths


def shape_diameter(points, faces, f, rays=25, angle=2 * math.pi / 3):
    """The SDF of face f: the mean of the ray lengths within one standard deviation of their median, or None."""
    lengths = ray_lengths(points, faces, f, rays, angle)
    if not lengths:
        return None
    m = statistics.median(lengths)  # @line L6
    s = statistics.pstdev(lengths)
    kept = [x for x in lengths if abs(x - m) <= s]  # @line L7
    return sum(kept) / len(kept)  # @line L8


def normalize(values, alpha=4):
    """Map SDF values to [0, 1] with log(alpha (x - min) / (max - min) + 1) / log(alpha + 1)."""
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    return [math.log(alpha * (x - lo) / (hi - lo) + 1) / math.log(alpha + 1) for x in values]
