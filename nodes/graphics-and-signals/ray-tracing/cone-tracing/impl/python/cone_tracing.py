# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cone-tracing/. The authors are listed in prov/7SNYXJ.jsonl.
"""Cone tracing (Amanatides 1984) for scenes of spheres and planes.

A cone has an apex o, a unit axis d and a spread angle a, the angle between the axis and the
boundary. For each object the tracer makes a fast in or out test and then computes the
fractional coverage: the part of the cone's circular cross-section that the object blocks. It
keeps the eight nearest objects with nonzero coverage, sorted by depth, and mixes their colors
front to back with the coverage values.

Coverage is measured in the cross-section of the cone by a plane perpendicular to the axis, as
an area fraction. For a sphere it is the area of intersection of two circles, the cone's
cross-section and the sphere's great circle in the same plane. For a plane it is the area of a
circle on one side of a line.
"""

import bisect
import math

LIST_SIZE = 8  # the paper keeps the eight closest objects


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def scale(k, a):
    return (k * a[0], k * a[1], k * a[2])


def norm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    return scale(1 / norm(a), a)


class Cone:
    def __init__(self, apex, axis, spread):
        assert 0 < spread < math.pi / 2
        self.o, self.d, self.a = apex, unit(axis), spread
        # the trigonometric values depend only on the spread angle: compute them once
        self.tan_a, self.cos_a, self.sin_a = math.tan(spread), math.cos(spread), math.sin(spread)


def pixel_cone(eye, center, width):
    """The cone through a pixel: its radius at the virtual screen is the pixel width."""
    v = sub(center, eye)
    return Cone(eye, v, math.atan(width / norm(v)))


def axis_coordinates(cone, c):
    """T, the axial distance of the point CP of the axis closest to c, and SEP = |c - CP|."""
    w = sub(c, cone.o)
    t = dot(w, cone.d)
    return t, norm(sub(w, scale(t, cone.d)))


def cone_meets_sphere(cone, c, r):
    """The fast test: does the solid cone meet the open ball of center c and radius r?"""
    t, sep = axis_coordinates(cone, c)
    if t * cone.cos_a + sep * cone.sin_a < 0:  # nearest point of the cone is the apex
        return t * t + sep * sep < r * r
    return sep < t * cone.tan_a + r / cone.cos_a  # D = T tan A + R / cos A against SEP


def lens_area(r1, r2, s):
    """Area of the intersection of two disks of radii r1, r2 whose centers are s apart."""
    if s >= r1 + r2:
        return 0.0
    if s <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    a1 = math.acos(max(-1.0, min(1.0, (s * s + r1 * r1 - r2 * r2) / (2 * s * r1))))
    a2 = math.acos(max(-1.0, min(1.0, (s * s + r2 * r2 - r1 * r1) / (2 * s * r2))))
    k = (-s + r1 + r2) * (s + r1 - r2) * (s - r1 + r2) * (s + r1 + r2)
    return r1 * r1 * a1 + r2 * r2 * a2 - 0.5 * math.sqrt(max(0.0, k))


def disk_fraction_below(h):
    """Fraction of the unit disk where x < h."""
    if h <= -1:
        return 0.0
    if h >= 1:
        return 1.0
    return (math.asin(h) + h * math.sqrt(1 - h * h) + math.pi / 2) / math.pi


def sphere_coverage(cone, c, r):
    """(coverage, depth) of a sphere whose center is in front of the apex."""
    t, sep = axis_coordinates(cone, c)
    rc = t * cone.tan_a  # radius of the cone's cross-section through c
    f = lens_area(rc, r, sep) / (math.pi * rc * rc)
    depth = t - math.sqrt(r * r - sep * sep) if sep < r else t
    return f, depth


def plane_coverage(cone, p, n):
    """(coverage, depth) of the plane through p with unit normal n on the apex's side."""
    h = dot(sub(cone.o, p), n)  # height of the apex over the plane
    if h <= 0:
        return 0.0, math.inf
    dn = dot(cone.d, n)
    sp = norm(sub(n, scale(dn, cone.d)))  # sine of the angle between the axis and n
    depth = h / -dn if dn < 0 else math.inf  # a plane seen only near the horizon sorts last
    if sp < 1e-15:
        return (1.0 if dn < 0 else 0.0), depth
    # direction d + u hits the plane iff u . (n_perp / sp) < -dn / sp: a line in the cross-section
    return disk_fraction_below(-dn / (sp * cone.tan_a)), depth


def trace_cone(cone, spheres, planes, background):
    """Mix the colors of the eight nearest objects by their coverage, front to back."""
    hits = []  # @line L1
    k = 0
    for c, r, color in spheres:  # @line L2
        if dot(sub(c, cone.o), cone.d) <= 0 or not cone_meets_sphere(cone, c, r):  # @line L3
            continue
        f, depth = sphere_coverage(cone, c, r)  # @line L4
        if f > 0:
            bisect.insort(hits, (depth, k, f, color))  # @line L5
            del hits[LIST_SIZE:]
            k += 1
    for p, n, color in planes:  # @line L2
        f, depth = plane_coverage(cone, p, n)  # @line L3
        if f > 0:  # @line L4
            bisect.insort(hits, (depth, k, f, color))  # @line L5
            del hits[LIST_SIZE:]
            k += 1
    color, left = 0.0, 1.0  # @line L6
    for _, _, f, c in hits:  # @line L7
        color += left * f * c  # @line L8
        left *= 1 - f  # @line L9
    return color + left * background, hits  # @line L10
