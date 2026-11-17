# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wire-deformation/. The authors are listed in prov/TTFYST.jsonl.
"""Wires deformation in the spirit of Singh and Fiume (1998).

A wire is a pair of curves: the reference curve R and the wire curve W,
with the same parameter. Here both are polylines with the same number of
vertices, and the parameter u = i + t means the point at the fraction t of
segment i. A point P near R is bound to its closest point R(u). It then
moves with W: it is scaled about R(u), rotated by the turn from the tangent
R'(u) to the tangent W'(u), and translated by W(u) - R(u). The amount of
each step is the falloff F = f(|P - R(u)| / r), so points at distance r or
more from R do not move.

The falloff f(x) = (1 - x^2)^2 for x < 1, and 0 otherwise, is one smooth
choice: f(0) = 1, f(1) = 0 and f'(1) = 0. Any decreasing f with these
properties can be passed in.
"""

import math


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(a, c):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    return math.sqrt(dot(a, a))


def default_falloff(x):
    """Return (1 - x^2)^2 for 0 <= x < 1 and 0 for x >= 1."""
    if x >= 1:
        return 0.0
    return (1 - x * x) ** 2


def closest_parameter(poly, p):
    """Return (u, distance) of the point of the polyline closest to p.

    The search is brute force over all segments; ties keep the first segment.
    """
    best_u, best_d = 0.0, math.inf
    for i in range(len(poly) - 1):
        a, b = poly[i], poly[i + 1]
        d = sub(b, a)
        dd = dot(d, d)
        t = 0.0 if dd == 0 else min(1.0, max(0.0, dot(sub(p, a), d) / dd))
        dist = norm(sub(p, add(a, scale(d, t))))
        if dist < best_d:
            best_u, best_d = i + t, dist
    return best_u, best_d


def point_at(poly, u):
    """Return the polyline point with the parameter u."""
    i = min(int(math.floor(u)), len(poly) - 2)
    t = u - i
    return add(scale(poly[i], 1 - t), scale(poly[i + 1], t))


def tangent_at(poly, u):
    """Return the unit direction of the segment that holds the parameter u."""
    i = min(int(math.floor(u)), len(poly) - 2)
    d = sub(poly[i + 1], poly[i])
    return scale(d, 1 / norm(d))


def rotate(v, axis, angle):
    """Rotate v about the unit axis by angle (Rodrigues' formula)."""
    c, s = math.cos(angle), math.sin(angle)
    return add(add(scale(v, c), scale(cross(axis, v), s)), scale(axis, dot(axis, v) * (1 - c)))


def deform(p, ref, wire, radius, s=1.0, falloff=default_falloff):
    """Move the point p by one wire. Return the new point."""
    if len(ref) != len(wire) or len(ref) < 2:
        raise ValueError("R and W need the same number of vertices, at least 2")
    p = tuple(p)
    u, dist = closest_parameter(ref, p)  # @line L1
    f = falloff(dist / radius)  # @line L2
    if f == 0:  # @line L3
        return p
    c = point_at(ref, u)
    q = add(c, scale(sub(p, c), 1 + (s - 1) * f))  # @line L4
    tr, tw = tangent_at(ref, u), tangent_at(wire, u)
    axis = cross(tr, tw)  # @line L5
    sin_t, cos_t = norm(axis), dot(tr, tw)
    if sin_t > 1e-15:
        theta = math.atan2(sin_t, cos_t)
        q = add(c, rotate(sub(q, c), scale(axis, 1 / sin_t), theta * f))  # @line L6
    elif cos_t < 0:
        raise ValueError("the tangents are opposite; the rotation axis is not defined")
    return add(q, scale(sub(point_at(wire, u), c), f))  # @line L7


def deform_many(p, wires, m=1.0):
    """Blend several wires: p + sum d_i |d_i|^m / sum |d_i|^m.

    Each item of wires is a tuple (ref, wire, radius, s). With m = 0 this
    is the plain average of the moves; a large m lets the largest move win.
    """
    p = tuple(p)
    moves = [sub(deform(p, *w), p) for w in wires]
    weights = [norm(d) ** m if norm(d) > 0 else 0.0 for d in moves]
    total = sum(weights)
    if total == 0:
        return p
    out = p
    for d, w in zip(moves, weights):
        out = add(out, scale(d, w / total))
    return out
