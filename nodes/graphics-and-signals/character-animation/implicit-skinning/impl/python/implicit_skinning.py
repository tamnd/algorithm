# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-skinning/. The authors are listed in prov/KN8M9F.jsonl.
"""A 2D toy of implicit skinning (Vaillant et al. 2013).

This is a toy. The method of the paper fits a field to the mesh part of each
bone with Hermite radial basis functions (HRBF) and composes the fields with
gradient-based operators. Here each bone has a closed-form field of the
distance to its segment, the fields are composed by the union max, and the
mesh is a closed polygon in the plane. The steps of the method are the same:

1. In the rest pose, store the field value iso_i of each vertex.
2. In each frame, skin the vertices by linear blend skinning, and move the
   field of each bone rigidly with the bone.
3. Project each vertex back to its own iso value by steps along the
   gradient, v <- v + sigma (iso_i - f(v)) grad f / |grad f|^2, and stop the
   vertex when the gradient turns by more than MAX_ANGLE between two steps,
   which marks a contact between two parts of the skin.
4. Relax the vertices: move each one along the chord of its two neighbors
   toward the point that has its rest position along the chord, and
   project them again. The paper relaxes in the tangent plane of the
   surface; the chord is the 2D stand-in of this toy.

The field of a bone with the rest radius r is f = t(d / (2 r)), where d is
the distance to the segment of the bone and t(u) = 1 - 3 u^2 + 2 u^3 for
u < 1 and 0 beyond. So f = 0.5 at the distance r, f decreases outward, and
the support is the distance 2 r. The field is flat near the bone, so a step
is cut to the length MAX_STEP. SIGMA, MAX_ANGLE, MAX_STEP, the relaxation
step and the number of rounds are tuning values of this toy.
"""

import math

from anim import add, dot, norm, scale, sub

SIGMA = 0.35
MAX_ANGLE = math.radians(55.0)
TOL = 1e-10
MAX_ITER = 200
RELAX = 0.3
MAX_STEP = 0.05


def apply2(m, p):
    """Apply a 3 by 3 homogeneous transform of the plane to a point."""
    return (m[0][0] * p[0] + m[0][1] * p[1] + m[0][2], m[1][0] * p[0] + m[1][1] * p[1] + m[1][2])


def segment_distance(x, a, b):
    """Return the distance from x to the segment ab and its gradient in x."""
    ab = sub(b, a)
    t = dot(sub(x, a), ab) / dot(ab, ab)
    t = 0.0 if t < 0.0 else 1.0 if t > 1.0 else t
    d = sub(x, add(a, scale(ab, t)))
    n = norm(d)
    if n == 0.0:
        return 0.0, (0.0, 0.0)
    return n, scale(d, 1.0 / n)


def bone_field(x, bone):
    """Return (f, grad f) of one bone given as (a, b, r)."""
    a, b, r = bone
    d, gd = segment_distance(x, a, b)
    u = d / (2.0 * r)
    if u >= 1.0:
        return 0.0, (0.0, 0.0)
    f = 1.0 - 3.0 * u * u + 2.0 * u ** 3
    df = (-6.0 * u + 6.0 * u * u) / (2.0 * r)
    return f, scale(gd, df)


def field(x, bones):
    """Return (f, grad f) of the union max of the bone fields."""
    best = (0.0, (0.0, 0.0))
    for bone in bones:
        fg = bone_field(x, bone)
        if fg[0] > best[0]:
            best = fg
    return best


def pose_bones(bones, palette):
    """Move each bone (a, b, r) by its rigid transform."""
    return [(apply2(m, a), apply2(m, b), r) for (a, b, r), m in zip(bones, palette)]


def project(x, iso, bones, sigma=SIGMA, max_angle=MAX_ANGLE, tol=TOL, max_iter=MAX_ITER, max_step=MAX_STEP):
    """Move x toward the level iso of the field. Return (x, reason)."""
    g_prev = None  # @line L5
    for _ in range(max_iter):  # @line L6
        f, g = field(x, bones)  # @line L7
        gg = dot(g, g)
        if abs(f - iso) <= tol:  # @line L8
            return x, "converged"
        if gg == 0.0:
            return x, "outside"
        if g_prev is not None:
            c = dot(g, g_prev) / math.sqrt(gg * dot(g_prev, g_prev))
            if math.acos(max(-1.0, min(1.0, c))) > max_angle:  # @line L9
                return x, "contact"
        step = scale(g, sigma * (iso - f) / gg)
        ls = norm(step)
        if ls > max_step:  # near the bone the field is flat and the step is too long
            step = scale(step, max_step / ls)
        x = add(x, step)  # @line L10
        g_prev = g
    return x, "max_iter"


def rest_iso(vertices, bones):
    """Return the field value of each rest vertex."""
    return [field(v, bones)[0] for v in vertices]


def chord_params(vertices):
    """Return s_i, the position of the rest vertex i along the chord of its two neighbors.

    The relaxation moves a vertex along the chord toward the point with the
    same parameter, so the rest polygon is a fixed point.
    """
    n = len(vertices)
    out = []
    for i in range(n):
        a, b = vertices[i - 1], vertices[(i + 1) % n]
        c = sub(b, a)
        out.append(dot(sub(vertices[i], a), c) / dot(c, c))
    return out


def lbs2(vertices, weights, palette):
    out = []
    for v, wi in zip(vertices, weights):
        p = (0.0, 0.0)
        for j, w in wi:
            p = add(p, scale(apply2(palette[j], v), w))
        out.append(p)
    return out


def implicit_skinning(vertices, weights, bones, palette, iso=None, rounds=2, relax=RELAX, sigma=SIGMA, max_angle=MAX_ANGLE):
    """Return (positions, reasons) of a closed polygon skinned by the toy method.

    vertices: the rest polygon in order; weights: lists of (joint, weight);
    bones: rest bones (a, b, r), one per joint; palette: 3 by 3 rigid
    transforms of the plane, one per joint.
    """
    if iso is None:
        iso = rest_iso(vertices, bones)  # @line L1
    posed = pose_bones(bones, palette)
    pts = lbs2(vertices, weights, palette)  # @line L2
    n = len(pts)
    reasons = [None] * n
    for i in range(n):  # @line L3
        pts[i], reasons[i] = project(pts[i], iso[i], posed, sigma, max_angle)  # @line L4
    s = chord_params(vertices)
    for _ in range(rounds):  # @line L11
        moved = []
        for i in range(n):
            a, b = pts[i - 1], pts[(i + 1) % n]
            c = sub(b, a)
            cc = dot(c, c)
            target = add(a, scale(c, s[i]))
            moved.append(add(pts[i], scale(c, relax * dot(sub(target, pts[i]), c) / cc)))
        for i in range(n):
            pts[i], reasons[i] = project(moved[i], iso[i], posed, sigma, max_angle)
    return pts, reasons  # @line L12
