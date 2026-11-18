# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-quaternion-skinning/. The authors are listed in prov/SVNNAZ.jsonl.
"""Tests of dual quaternion skinning.

They check the dual quaternion round trip, the bind pose, the agreement with
LBS (one rigid transform) when each vertex has one joint, the candy wrapper
check value, that every blended transform is rigid, the invariance under a
change of coordinates, that pure translations blend as in LBS, the lower
bound on the blended real part after the pivot alignment, and the failure of
the blend without alignment when the real part is zero.
"""

import math
import random

import pytest

import anim
from dual_quaternion_skinning import (
    blend,
    dq_apply,
    dq_from_transform,
    dq_palette,
    dq_translation,
    dual_quaternion_skinning,
)


def rand_q(rng):
    return anim.q_normalize([rng.gauss(0.0, 1.0) for _ in range(4)])


def rand_T(rng, spread=2.0):
    t = tuple(rng.uniform(-spread, spread) for _ in range(3))
    return anim.make_T(anim.q_to_mat3(rand_q(rng)), t)


def rand_weights(rng, nj, k):
    js = rng.sample(range(nj), k)
    ws = [rng.random() + 0.05 for _ in js]
    s = sum(ws)
    return [(j, w / s) for j, w in zip(js, ws)]


def rand_points(rng, n):
    return [tuple(rng.uniform(-1.0, 1.0) for _ in range(3)) for _ in range(n)]


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def rx(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]]


def blended_matrix(c0, ce):
    r = anim.q_to_mat3(c0)
    return anim.make_T(r, dq_translation(c0, ce))


def test_round_trip():
    rng = random.Random(1)
    for _ in range(50):
        m = rand_T(rng)
        r, d = dq_from_transform(m)
        back = blended_matrix(r, d)
        assert all(close(a, b, 1e-12) for a, b in zip(m, back))
        assert abs(anim.q_dot(r, d)) <= 1e-12


def test_bind_pose_gives_rest_mesh():
    rng = random.Random(2)
    pal = [anim.eye(4) for _ in range(5)]
    verts = rand_points(rng, 40)
    normals = [anim.normalize(p) for p in rand_points(rng, 40)]
    weights = [rand_weights(rng, 5, 3) for _ in verts]
    out_v, out_n = dual_quaternion_skinning(verts, weights, pal, normals)
    for a, b in zip(out_v, verts):
        assert close(a, b, 1e-12)
    for a, b in zip(out_n, normals):
        assert close(a, b, 1e-12)


def test_single_joint_agrees_with_lbs():
    rng = random.Random(3)
    pal = [rand_T(rng) for _ in range(4)]
    verts = rand_points(rng, 60)
    weights = [[(rng.randrange(4), 1.0)] for _ in verts]
    out, _ = dual_quaternion_skinning(verts, weights, pal)
    for v, wl, a in zip(verts, weights, out):
        lbs = anim.T_apply(pal[wl[0][0]], v)
        assert close(a, lbs, 1e-12)


def test_candy_wrapper_check_value():
    pal = [anim.make_T(rx(0.0), (0.0, 0.0, 0.0)), anim.make_T(rx(math.pi), (0.0, 0.0, 0.0))]
    out, _ = dual_quaternion_skinning([(0.0, 1.0, 0.0)], [[(0, 0.5), (1, 0.5)]], pal)
    assert close(out[0], (0.0, 0.0, 1.0), 1e-12)
    assert abs(math.hypot(out[0][1], out[0][2]) - 1.0) <= 1e-12
    for theta in [0.2 * k for k in range(16)]:
        pal[1] = anim.make_T(rx(theta), (0.0, 0.0, 0.0))
        out, _ = dual_quaternion_skinning([(0.3, 1.0, 0.0)], [[(0, 0.5), (1, 0.5)]], pal)
        assert close(out[0], (0.3, math.cos(theta / 2.0), math.sin(theta / 2.0)), 1e-12)


def test_blend_is_rigid_and_normals_unit():
    rng = random.Random(4)
    dqs = dq_palette([rand_T(rng) for _ in range(6)])
    for _ in range(200):
        c0, ce = blend(rand_weights(rng, 6, 4), dqs)
        assert abs(anim.q_dot(c0, c0) - 1.0) <= 1e-12
        assert abs(anim.q_dot(c0, ce)) <= 1e-12
        p, q = rand_points(rng, 2)
        d0 = anim.norm(anim.sub(p, q))
        d1 = anim.norm(anim.sub(dq_apply(c0, ce, p), dq_apply(c0, ce, q)))
        assert abs(d0 - d1) <= 1e-12
        n = anim.q_rotate(c0, anim.normalize(p))
        assert abs(anim.norm(n) - 1.0) <= 1e-12


def test_coordinate_invariance():
    rng = random.Random(5)
    for _ in range(20):
        pal = [rand_T(rng) for _ in range(4)]
        g = rand_T(rng)
        gi = anim.T_inv(g)
        conj = [anim.T_mul(anim.T_mul(g, p), gi) for p in pal]
        verts = rand_points(rng, 10)
        weights = [rand_weights(rng, 4, 3) for _ in verts]
        out, _ = dual_quaternion_skinning(verts, weights, pal)
        out_g, _ = dual_quaternion_skinning([anim.T_apply(g, v) for v in verts], weights, conj)
        for a, b in zip(out, out_g):
            assert close(anim.T_apply(g, a), b, 1e-10)


def test_pure_translations_blend_like_lbs():
    rng = random.Random(6)
    pal = [anim.make_T(anim.eye(3), tuple(rng.uniform(-3.0, 3.0) for _ in range(3))) for _ in range(5)]
    verts = rand_points(rng, 30)
    weights = [rand_weights(rng, 5, 3) for _ in verts]
    out, _ = dual_quaternion_skinning(verts, weights, pal)
    for v, wl, a in zip(verts, weights, out):
        lbs = [0.0, 0.0, 0.0]
        for j, w in wl:
            p = anim.T_apply(pal[j], v)
            for k in range(3):
                lbs[k] += w * p[k]
        assert close(a, lbs, 1e-12)


def test_aligned_real_part_is_bounded_below():
    rng = random.Random(7)
    for _ in range(300):
        rs = [rand_q(rng) for _ in range(4)]
        wl = rand_weights(rng, 4, 4)
        jp = max(wl, key=lambda jw: jw[1])[0]
        b0 = [0.0] * 4
        for j, w in wl:
            s = -1.0 if anim.q_dot(rs[jp], rs[j]) < 0.0 else 1.0
            for k in range(4):
                b0[k] += s * w * rs[j][k]
        assert anim.norm(b0) >= wl[[j for j, _ in wl].index(jp)][1] - 1e-15


def test_zero_real_part_without_alignment_raises():
    # r and -r are the same rotation; the unaligned blend of them is zero
    m = anim.make_T(rx(1.0), (0.0, 0.0, 0.0))
    dqs = dq_palette([m, m])
    r, d = dqs[1]
    dqs[1] = (tuple(-x for x in r), tuple(-x for x in d))
    with pytest.raises(ValueError):
        blend([(0, 0.5), (1, 0.5)], dqs, align=False)
    c0, ce = blend([(0, 0.5), (1, 0.5)], dqs)
    assert close(anim.q_to_mat3(c0)[1], rx(1.0)[1], 1e-12)


def test_three_joints_no_consistent_signs_still_rigid():
    # pairwise signs cannot all be made nonnegative: q1.q2 > 0, q1.q3 > 0, q2.q3 < 0
    q1 = (1.0, 0.0, 0.0, 0.0)
    q2 = anim.q_normalize((0.2, 1.0, 0.0, 0.0))
    q3 = anim.q_normalize((0.2, -1.0, 0.0, 0.0))
    assert anim.q_dot(q1, q2) > 0 and anim.q_dot(q1, q3) > 0 and anim.q_dot(q2, q3) < 0
    pal = [anim.make_T(anim.q_to_mat3(q), (0.0, 0.0, 0.0)) for q in (q1, q2, q3)]
    dqs = dq_palette(pal)
    c0, ce = blend([(0, 0.4), (1, 0.3), (2, 0.3)], dqs)
    assert abs(anim.q_dot(c0, c0) - 1.0) <= 1e-12
    assert abs(anim.q_dot(c0, ce)) <= 1e-12
