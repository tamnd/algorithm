# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spherical-blend-skinning/. The authors are listed in prov/E1S4SH.jsonl.
"""Tests of spherical blend skinning.

They check the bind pose, the single weight case, the recovery of a common
center of rotation, the minimal norm center against a direct solve and a
zero gradient, the candy wrapper case, rigidity per joint set, the
invariance under a change of coordinates, the cache, and that the linear
rotation blend gives linear blend skinning.
"""

import math
import random

import anim
from spherical_blend_skinning import center_of_rotation, qlerp, spherical_blend_skinning


def rand_quat(rng):
    return anim.q_normalize([rng.gauss(0.0, 1.0) for _ in range(4)])


def rand_rot(rng):
    return anim.q_to_mat3(rand_quat(rng))


def rand_T(rng):
    return anim.make_T(rand_rot(rng), tuple(rng.uniform(-2.0, 2.0) for _ in range(3)))


def about(c, r):
    """The rigid transform that rotates by r about the point c."""
    return anim.make_T(r, anim.sub(c, anim.matvec(r, c)))


def rot_x(t):
    return anim.q_to_mat3(anim.q_from_axis_angle((1.0, 0.0, 0.0), t))


def mesh(rng, n, nj, k):
    verts, normals, weights = [], [], []
    for _ in range(n):
        verts.append(tuple(rng.uniform(-1.0, 1.0) for _ in range(3)))
        normals.append(anim.normalize([rng.gauss(0.0, 1.0) for _ in range(3)]))
        js = rng.sample(range(nj), k)
        ws = [rng.random() + 0.05 for _ in js]
        s = sum(ws)
        weights.append([(j, w / s) for j, w in zip(js, ws)])
    return verts, normals, weights


def lbs(v, infl, palette):
    out = (0.0, 0.0, 0.0)
    for j, w in infl:
        out = anim.add(out, anim.scale(anim.T_apply(palette[j], v), w))
    return out


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def test_bind_pose_gives_rest_mesh():
    rng = random.Random(1)
    verts, normals, weights = mesh(rng, 50, 4, 3)
    pal = [anim.eye(4) for _ in range(4)]
    out_v, out_n = spherical_blend_skinning(verts, weights, pal, normals)
    for a, b in zip(out_v, verts):
        assert close(a, b, 1e-12)
    for a, b in zip(out_n, normals):
        assert close(a, b, 1e-12)


def test_single_weight_is_rigid():
    rng = random.Random(2)
    pal = [rand_T(rng) for _ in range(3)]
    verts = [tuple(rng.uniform(-1.0, 1.0) for _ in range(3)) for _ in range(20)]
    weights = [[(i % 3, 1.0)] for i in range(20)]
    out_v, _ = spherical_blend_skinning(verts, weights, pal)
    for i, (a, v) in enumerate(zip(out_v, verts)):
        assert close(a, anim.T_apply(pal[i % 3], v), 1e-12)


def test_common_center_is_recovered():
    rng = random.Random(3)
    for _ in range(20):
        c = tuple(rng.uniform(-3.0, 3.0) for _ in range(3))
        pal = [about(c, rand_rot(rng)) for _ in range(3)]
        rc = center_of_rotation((0, 1, 2), pal)
        assert close(rc, c, 1e-8)


def test_minimal_norm_center_on_a_shared_axis():
    # both joints turn about the same line, so the center is not unique and
    # the method takes the point of the line nearest to the origin
    rng = random.Random(4)
    for _ in range(20):
        c = tuple(rng.uniform(-3.0, 3.0) for _ in range(3))
        u = anim.normalize([rng.gauss(0.0, 1.0) for _ in range(3)])
        ra = anim.q_to_mat3(anim.q_from_axis_angle(u, rng.uniform(-3.0, 3.0)))
        rb = anim.q_to_mat3(anim.q_from_axis_angle(u, rng.uniform(-3.0, 3.0)))
        rc = center_of_rotation((0, 1), [about(c, ra), about(c, rb)])
        nearest = anim.sub(c, anim.scale(u, anim.dot(c, u)))
        assert close(rc, nearest, 1e-8)


def objective(palette, js):
    def f(r):
        s = 0.0
        for ia in range(len(js)):
            for ib in range(ia + 1, len(js)):
                d = anim.sub(anim.T_apply(palette[js[ia]], r), anim.T_apply(palette[js[ib]], r))
                s += anim.dot(d, d)
        return s

    return f


def test_center_matches_direct_least_squares():
    rng = random.Random(5)
    for _ in range(20):
        pal = [rand_T(rng) for _ in range(4)]
        js = (0, 1, 2, 3)
        rc = center_of_rotation(js, pal)
        # reference: the normal equations solved by Gaussian elimination
        n = anim.zeros(3)
        g = [0.0, 0.0, 0.0]
        for ia in range(4):
            for ib in range(ia + 1, 4):
                ra = [row[:3] for row in pal[ia][:3]]
                rb = [row[:3] for row in pal[ib][:3]]
                d = [[ra[r][c] - rb[r][c] for c in range(3)] for r in range(3)]
                e = [pal[ib][r][3] - pal[ia][r][3] for r in range(3)]
                dt = anim.transpose(d)
                n = [[n[r][c] + anim.mul(dt, d)[r][c] for c in range(3)] for r in range(3)]
                g = [g[r] + anim.matvec(dt, e)[r] for r in range(3)]
        assert close(rc, anim.solve(n, g), 1e-7)
        grad = anim.num_grad(objective(pal, js), rc, h=1e-5)
        assert max(abs(x) for x in grad) < 1e-6


def test_candy_wrapper_keeps_the_radius():
    for t in (0.5, 1.0, math.pi / 2, 2.5, math.pi):
        pal = [anim.eye(4), anim.make_T(rot_x(t), (0.0, 0.0, 0.0))]
        out_v, _ = spherical_blend_skinning([(0.3, 1.0, 0.0)], [[(0, 0.5), (1, 0.5)]], pal)
        p = out_v[0]
        assert abs(p[0] - 0.3) < 1e-12
        assert abs(math.hypot(p[1], p[2]) - 1.0) < 1e-12
        assert abs(math.atan2(p[2], p[1]) - t / 2) < 1e-12
    pal = [anim.eye(4), anim.make_T(rot_x(math.pi), (0.0, 0.0, 0.0))]
    out_v, _ = spherical_blend_skinning([(0.0, 1.0, 0.0)], [[(0, 0.5), (1, 0.5)]], pal)
    assert close(out_v[0], (0.0, 0.0, 1.0), 1e-12)


def test_rigid_per_joint_set_and_unit_normals():
    rng = random.Random(6)
    pal = [rand_T(rng) for _ in range(3)]
    infl = [(0, 0.2), (1, 0.5), (2, 0.3)]
    verts = [tuple(rng.uniform(-1.0, 1.0) for _ in range(3)) for _ in range(15)]
    normals = [anim.normalize([rng.gauss(0.0, 1.0) for _ in range(3)]) for _ in range(15)]
    out_v, out_n = spherical_blend_skinning(verts, [infl] * 15, pal, normals)
    for a in range(15):
        assert abs(anim.norm(out_n[a]) - 1.0) < 1e-12
        for b in range(a + 1, 15):
            d0 = anim.norm(anim.sub(verts[a], verts[b]))
            d1 = anim.norm(anim.sub(out_v[a], out_v[b]))
            assert abs(d0 - d1) < 1e-12


def test_change_of_coordinates():
    rng = random.Random(7)
    verts, normals, weights = mesh(rng, 40, 4, 3)
    pal = [rand_T(rng) for _ in range(4)]
    # one joint set with a shared axis, so the minimal norm choice is used
    u = (0.0, 0.0, 1.0)
    pal[3] = anim.T_mul(pal[2], about((0.5, -1.0, 0.0), anim.q_to_mat3(anim.q_from_axis_angle(u, 1.1))))
    weights[0] = [(2, 0.4), (3, 0.6)]
    g = rand_T(rng)
    gi = anim.T_inv(g)
    gr = [row[:3] for row in g[:3]]
    pal_g = [anim.T_mul(g, anim.T_mul(p, gi)) for p in pal]
    out_v, out_n = spherical_blend_skinning(verts, weights, pal, normals)
    out_vg, out_ng = spherical_blend_skinning([anim.T_apply(g, v) for v in verts], weights, pal_g, [anim.matvec(gr, n) for n in normals])
    for a, b in zip(out_v, out_vg):
        assert close(anim.T_apply(g, a), b, 1e-9)
    for a, b in zip(out_n, out_ng):
        assert close(anim.matvec(gr, a), b, 1e-9)


def test_cache_gives_the_same_result():
    rng = random.Random(8)
    verts, normals, weights = mesh(rng, 60, 4, 2)
    pal = [rand_T(rng) for _ in range(4)]
    cache = {}
    out1, _ = spherical_blend_skinning(verts, weights, pal, cache=cache)
    assert len(cache) <= 6
    out2, _ = spherical_blend_skinning(verts, weights, pal, cache=cache)
    for i, v in enumerate(verts):
        assert close(out1[i], out2[i], 0.0)
        alone, _ = spherical_blend_skinning([v], [weights[i]], pal)
        assert close(out1[i], alone[0], 1e-12)


def test_linear_rotation_gives_lbs():
    rng = random.Random(9)
    verts, _, weights = mesh(rng, 40, 5, 3)
    pal = [rand_T(rng) for _ in range(5)]
    out_v, _ = spherical_blend_skinning(verts, weights, pal, linear_rotation=True)
    for v, infl, a in zip(verts, weights, out_v):
        assert close(a, lbs(v, infl, pal), 1e-12)


def test_qlerp_is_sign_invariant():
    rng = random.Random(10)
    quats = [rand_quat(rng) for _ in range(3)]
    infl = [(0, 0.5), (1, 0.3), (2, 0.2)]
    q = qlerp(infl, quats)
    flipped = [quats[0], tuple(-x for x in quats[1]), quats[2]]
    q2 = qlerp(infl, flipped)
    assert close(q, q2, 1e-12)
    assert abs(anim.q_dot(q, q) - 1.0) < 1e-12
    # the aligned sum is at least the pivot weight away from zero
    for _ in range(50):
        quats = [rand_quat(rng) for _ in range(4)]
        ws = [rng.random() + 0.01 for _ in range(4)]
        s = sum(ws)
        q = qlerp([(j, w / s) for j, w in enumerate(ws)], quats)
        assert abs(anim.q_dot(q, q) - 1.0) < 1e-12
