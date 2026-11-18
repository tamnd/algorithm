# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-mush/. The authors are listed in prov/118N6H.jsonl.
"""Tests of delta mush.

They check the smoothing against powers of the dense smoothing matrix, the
frames, the bind pose, a common rigid motion, a full twist of a tube (the
middle ring does not collapse to the axis), a bend of the tube (the middle
ring keeps more of its radius than with linear blend skinning), and the
case of rigid weights.
"""

import math
import random

import anim
from delta_mush import delta_mush, frames, lbs, neighbors, precompute, smooth


def smoothstep(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3.0 - 2.0 * x)


def tube(nr=12, ny=13, radius=0.5, length=2.0, rigid=False):
    """An open tube along y with two joints, at y = 0 and y = 1."""
    verts, weights = [], []
    for r in range(ny):
        y = length * r / (ny - 1)
        w1 = (1.0 if y > 1.0 else 0.0) if rigid else smoothstep((y - 0.6) / 0.8)
        for k in range(nr):
            a = 2.0 * math.pi * k / nr
            verts.append((radius * math.cos(a), y, radius * math.sin(a)))
            weights.append([jw for jw in ((0, 1.0 - w1), (1, w1)) if jw[1] > 0.0])
    tris = []
    for r in range(ny - 1):
        for k in range(nr):
            a, b = r * nr + k, r * nr + (k + 1) % nr
            c, d = a + nr, b + nr
            tris += [(a, c, b), (b, c, d)]
    return verts, tris, weights


def rand_T(rng):
    q = anim.q_normalize([rng.gauss(0.0, 1.0) for _ in range(4)])
    return anim.make_T(anim.q_to_mat3(q), tuple(rng.uniform(-2.0, 2.0) for _ in range(3)))


def about(axis, angle, c):
    r = anim.q_to_mat3(anim.q_from_axis_angle(axis, angle))
    return anim.make_T(r, anim.sub(c, anim.matvec(r, c)))


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def ring_radius(points, ring, nr, center):
    pts = points[ring * nr : (ring + 1) * nr]
    return sum(anim.norm(anim.sub(p, center)) for p in pts) / nr


def test_smoothing_matches_matrix_power():
    rng = random.Random(1)
    verts, tris, _ = tube(nr=6, ny=5)
    verts = [anim.add(v, tuple(rng.uniform(-0.05, 0.05) for _ in range(3))) for v in verts]
    nb = neighbors(len(verts), tris)
    n = len(verts)
    m = anim.eye(n)
    for i in range(n):
        for k in nb[i]:
            m[i][k] += 0.4 / len(nb[i])
        m[i][i] -= 0.4
    p = anim.eye(n)
    for _ in range(7):
        p = anim.mul(m, p)
    ref = anim.mul(p, [list(v) for v in verts])
    got = smooth(verts, nb, 0.4, 7)
    for a, b in zip(got, ref):
        assert close(a, b, 1e-12)


def test_frames_are_orthonormal():
    rng = random.Random(2)
    verts, tris, _ = tube()
    verts = [anim.add(v, tuple(rng.uniform(-0.05, 0.05) for _ in range(3))) for v in verts]
    nb = neighbors(len(verts), tris)
    for t, b, n in frames(smooth(verts, nb), tris, nb):
        for u in (t, b, n):
            assert abs(anim.norm(u) - 1.0) < 1e-12
        assert abs(anim.dot(t, b)) < 1e-12 and abs(anim.dot(t, n)) < 1e-12 and abs(anim.dot(b, n)) < 1e-12
        assert close(anim.cross(t, b), n, 1e-12)
    # the normals of the tube point outward
    for v, (_, _, n) in zip(verts, frames(verts, tris, nb)):
        assert n[0] * v[0] + n[2] * v[2] > 0.0


def test_bind_pose_gives_rest_mesh():
    verts, tris, weights = tube()
    out = delta_mush(verts, tris, weights, [anim.eye(4), anim.eye(4)])
    for a, b in zip(out, verts):
        assert close(a, b, 1e-12)


def test_common_rigid_motion():
    rng = random.Random(3)
    verts, tris, weights = tube()
    pre = precompute(verts, tris)
    for _ in range(3):
        g = rand_T(rng)
        out = delta_mush(verts, tris, weights, [g, g], pre=pre)
        for a, v in zip(out, verts):
            assert close(a, anim.T_apply(g, v), 1e-9)


def test_full_twist_does_not_collapse_to_the_axis():
    # LBS puts the middle ring of a twist by pi on the axis; delta mush keeps
    # it open, but it does not restore the rest radius (see the page)
    verts, tris, weights = tube()
    pre = precompute(verts, tris)
    pal = [anim.eye(4), about((0.0, 1.0, 0.0), math.pi, (0.0, 0.0, 0.0))]
    out = delta_mush(verts, tris, weights, pal, pre=pre)
    ref = lbs(verts, weights, pal)
    c = (0.0, 1.0, 0.0)
    assert ring_radius(ref, 6, 12, c) < 1e-9
    assert 0.25 < ring_radius(out, 6, 12, c) < 0.5


def test_bend_keeps_more_radius_than_lbs():
    verts, tris, weights = tube()
    pre = precompute(verts, tris)
    pal = [anim.eye(4), about((0.0, 0.0, 1.0), math.pi / 2, (0.0, 1.0, 0.0))]
    out = delta_mush(verts, tris, weights, pal, pre=pre)
    ref = lbs(verts, weights, pal)
    c = (0.0, 1.0, 0.0)
    assert abs(ring_radius(out, 6, 12, c) - 0.5) < abs(ring_radius(ref, 6, 12, c) - 0.5)


def test_rigid_weights_are_smoothed():
    # with weights of 0 or 1 linear blend skinning tears the tube at the
    # joint; delta mush gives a gap between rings close to the rest one
    verts, tris, weights = tube(rigid=True)
    pal = [anim.eye(4), about((0.0, 0.0, 1.0), math.pi / 3, (0.0, 1.0, 0.0))]
    out = delta_mush(verts, tris, weights, pal)
    ref = lbs(verts, weights, pal)
    rest_edge = anim.norm(anim.sub(verts[6 * 12], verts[7 * 12]))

    def worst(points):
        return max(abs(anim.norm(anim.sub(points[6 * 12 + k], points[7 * 12 + k])) - rest_edge) for k in range(12))

    assert worst(out) < worst(ref)


def test_any_deformer_and_identity():
    # the correction of the rest mesh itself is the rest mesh, whatever the
    # weights and the palette
    rng = random.Random(4)
    verts, tris, weights = tube()
    out = delta_mush(verts, tris, weights, [rand_T(rng), rand_T(rng)], deformed=list(verts))
    for a, b in zip(out, verts):
        assert close(a, b, 1e-12)
