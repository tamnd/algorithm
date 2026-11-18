# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-skinning/. The authors are listed in prov/KN8M9F.jsonl.
"""Tests of the 2D toy of implicit skinning.

They check the field and its gradient against central differences, the
projection against a bisection on the distance for one bone, the bind pose,
a common rigid motion, the bend of an arm (the skin stays out of the bones
where linear blend skinning lets it in), the per-vertex iso values of a
bumpy arm, and the contact stop.
"""

import math
import random

import anim
from implicit_skinning import (
    bone_field,
    field,
    implicit_skinning,
    lbs2,
    pose_bones,
    project,
    rest_iso,
    segment_distance,
)

R = 0.25
BONES = [((0.0, 0.0), (1.0, 0.0), R), ((1.0, 0.0), (2.0, 0.0), R)]


def smoothstep(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3.0 - 2.0 * x)


def arm(n=80, r=R, bump=0.0):
    """The outline of a stadium around the two bones, counterclockwise."""
    pts = []
    length = 2.0
    per = 2.0 * length + 2.0 * math.pi * r
    for k in range(n):
        s = per * k / n
        if s < length:
            p, nrm = (s, -r), (0.0, -1.0)
        elif s < length + math.pi * r:
            a = -math.pi / 2 + (s - length) / r
            p, nrm = (length + r * math.cos(a), r * math.sin(a)), (math.cos(a), math.sin(a))
        elif s < 2 * length + math.pi * r:
            p, nrm = (length - (s - length - math.pi * r), r), (0.0, 1.0)
        else:
            a = math.pi / 2 + (s - 2 * length - math.pi * r) / r
            p, nrm = (r * math.cos(a), r * math.sin(a)), (math.cos(a), math.sin(a))
        pts.append(anim.add(p, anim.scale(nrm, bump * r * math.sin(7.0 * s))))
    weights = []
    for v in pts:
        w1 = smoothstep((v[0] - 0.8) / 0.4)
        weights.append([jw for jw in ((0, 1.0 - w1), (1, w1)) if jw[1] > 0.0])
    return pts, weights


def bend(theta):
    rot = anim.rot2(theta)
    c = (1.0, 0.0)
    return [anim.eye(3), anim.make_T(rot, anim.sub(c, anim.matvec(rot, c)))]


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def min_dist(p, bones):
    return min(segment_distance(p, a, b)[0] for a, b, _ in bones)


def test_gradient_matches_central_differences():
    rng = random.Random(1)
    for _ in range(200):
        x = (rng.uniform(-0.4, 2.4), rng.uniform(-0.45, 0.45))
        if min_dist(x, BONES) < 0.02:
            continue
        f, g = field(x, BONES)
        d0 = bone_field(x, BONES[0])[0]
        d1 = bone_field(x, BONES[1])[0]
        if abs(d0 - d1) < 1e-3:
            continue  # the union max has a kink there
        num = anim.num_grad(lambda y: field(y, BONES)[0], x, h=1e-6)
        assert close(g, num, 1e-6)
        assert 0.0 <= f <= 1.0


def test_projection_matches_bisection_for_one_bone():
    rng = random.Random(2)
    bone = [((0.0, 0.0), (1.0, 0.3), R)]
    for _ in range(50):
        x = (rng.uniform(-0.3, 1.3), rng.uniform(-0.3, 0.6))
        d, gd = segment_distance(x, bone[0][0], bone[0][1])
        if d < 0.05 or d > 0.45:
            continue
        iso = rng.uniform(0.1, 0.9)
        got, why = project(x, iso, bone)
        assert why == "converged"
        # reference: bisection on the distance for t(d / 2r) = iso
        lo, hi = 0.0, 2.0 * R
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            u = mid / (2.0 * R)
            if 1.0 - 3.0 * u * u + 2.0 * u ** 3 > iso:
                lo = mid
            else:
                hi = mid
        foot = anim.sub(x, anim.scale(gd, d))
        assert close(got, anim.add(foot, anim.scale(gd, lo)), 1e-8)


def test_bind_pose_gives_rest_mesh():
    pts, weights = arm(bump=0.2)
    out, why = implicit_skinning(pts, weights, BONES, [anim.eye(3), anim.eye(3)])
    for a, b in zip(out, pts):
        assert close(a, b, 1e-12)
    assert all(w == "converged" for w in why)


def test_common_rigid_motion():
    rng = random.Random(3)
    pts, weights = arm(bump=0.2)
    g = anim.make_T(anim.rot2(rng.uniform(-3.0, 3.0)), (rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)))
    out, _ = implicit_skinning(pts, weights, BONES, [g, g])
    for a, v in zip(out, pts):
        assert close(a, anim.T_apply(g, v), 1e-9)


def test_bend_keeps_the_skin_out_of_the_bones():
    pts, weights = arm()
    for deg in (60.0, 100.0, 130.0):
        pal = bend(math.radians(deg))
        posed = pose_bones(BONES, pal)
        out, why = implicit_skinning(pts, weights, BONES, pal)
        lbs = lbs2(pts, weights, pal)
        assert min(min_dist(p, posed) for p in out) > min(min_dist(p, posed) for p in lbs)
        for p, w in zip(out, why):
            if w == "converged":
                assert abs(field(p, posed)[0] - 0.5) < 1e-9
                assert min_dist(p, posed) > R - 1e-8
            else:
                assert w == "contact"
                # a stopped vertex lies near the plane where the two fields meet
                d0 = segment_distance(p, *posed[0][:2])[0]
                d1 = segment_distance(p, *posed[1][:2])[0]
                assert abs(d0 - d1) < 0.05
        if deg >= 100.0:
            assert "contact" in why


def test_bumpy_arm_keeps_each_iso_value():
    pts, weights = arm(bump=0.2)
    iso = rest_iso(pts, BONES)
    assert max(iso) - min(iso) > 0.1
    pal = bend(math.radians(45.0))
    posed = pose_bones(BONES, pal)
    out, why = implicit_skinning(pts, weights, BONES, pal, iso=iso)
    for p, w, s in zip(out, why, iso):
        if w == "converged":
            assert abs(field(p, posed)[0] - s) < 1e-9


def test_contact_stop():
    # two bones at a right angle; a point inside the corner is pushed by one
    # field across the line where the other takes over
    bones = [((0.0, 0.0), (1.0, 0.0), R), ((0.0, 0.0), (0.0, 1.0), R)]
    x = (0.2, 0.18)
    _, why = project(x, 0.5, bones)
    assert why == "contact"
    _, why = project(x, 0.5, bones, max_angle=math.pi)
    assert why != "contact"
