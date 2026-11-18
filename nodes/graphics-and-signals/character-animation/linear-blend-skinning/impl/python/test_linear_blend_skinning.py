# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-blend-skinning/. The authors are listed in prov/1WQ6KE.jsonl.
"""Tests of linear blend skinning.

They check that the bind pose gives the rest mesh, that a vertex with one
weight of 1 moves rigidly, that the blend of matrices equals the blend of
the transformed points, the candy wrapper check value, the radius cos(t/2)
of a twist t, unit normals, and the invariance under a common rigid motion.
"""

import math
import random

import pytest

import anim
from linear_blend_skinning import (
    blend_matrix,
    linear_blend_skinning,
    skin_by_points,
    skinning_matrices,
)


def rand_rot(rng):
    v = [rng.gauss(0.0, 1.0) for _ in range(4)]
    return anim.q_to_mat3(anim.q_normalize(v))


def rand_T(rng):
    t = tuple(rng.uniform(-2.0, 2.0) for _ in range(3))
    return anim.make_T(rand_rot(rng), t)


def fk(parents, local):
    """World transforms of joints stored in parent order."""
    world = []
    for j, p in enumerate(parents):
        world.append(local[j] if p < 0 else anim.T_mul(world[p], local[j]))
    return world


def chain(rng, nj):
    parents = [j - 1 for j in range(nj)]
    bind_local = [anim.make_T(anim.eye(3), (0.0, 1.0 if j else 0.0, 0.0)) for j in range(nj)]
    pose_local = [anim.T_mul(bl, anim.make_T(rand_rot(rng), (0.0, 0.0, 0.0))) for bl in bind_local]
    return parents, fk(parents, bind_local), fk(parents, pose_local)


def mesh(rng, n, nj, k):
    verts, normals, weights = [], [], []
    for _ in range(n):
        verts.append((rng.uniform(-0.5, 0.5), rng.uniform(0.0, nj - 1.0), rng.uniform(-0.5, 0.5)))
        normals.append(anim.normalize([rng.gauss(0.0, 1.0) for _ in range(3)]))
        js = rng.sample(range(nj), k)
        ws = [rng.random() + 0.05 for _ in js]
        s = sum(ws)
        weights.append([(j, w / s) for j, w in zip(js, ws)])
    return verts, normals, weights


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def test_bind_pose_gives_rest_mesh():
    rng = random.Random(1)
    _, bind, _ = chain(rng, 5)
    verts, normals, weights = mesh(rng, 60, 5, 3)
    pal = skinning_matrices(bind, [anim.T_inv(b) for b in bind])
    out_v, out_n = linear_blend_skinning(verts, weights, pal, normals)
    for a, b in zip(out_v, verts):
        assert close(a, b, 1e-12)
    for a, b in zip(out_n, normals):
        assert close(a, b, 1e-12)


def test_single_weight_is_rigid():
    rng = random.Random(2)
    _, bind, pose = chain(rng, 4)
    pal = skinning_matrices(pose, [anim.T_inv(b) for b in bind])
    verts, _, _ = mesh(rng, 40, 4, 1)
    j = 2
    weights = [[(j, 1.0)] for _ in verts]
    out, _ = linear_blend_skinning(verts, weights, pal)
    for a, v in zip(out, verts):
        assert close(a, anim.T_apply(pal[j], v), 1e-12)
    for p in range(len(verts)):
        for q in range(p + 1, len(verts)):
            d0 = anim.norm(anim.sub(verts[p], verts[q]))
            d1 = anim.norm(anim.sub(out[p], out[q]))
            assert abs(d0 - d1) <= 1e-12


def test_blend_of_matrices_equals_blend_of_points():
    rng = random.Random(3)
    _, bind, pose = chain(rng, 6)
    pal = skinning_matrices(pose, [anim.T_inv(b) for b in bind])
    verts, _, weights = mesh(rng, 100, 6, 4)
    out, _ = linear_blend_skinning(verts, weights, pal)
    ref = skin_by_points(verts, weights, pal)
    for a, b in zip(out, ref):
        assert close(a, b, 1e-12)


def rx(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]]


def test_candy_wrapper_check_value():
    pal = [anim.make_T(rx(0.0), (0.0, 0.0, 0.0)), anim.make_T(rx(math.pi), (0.0, 0.0, 0.0))]
    out, _ = linear_blend_skinning([(0.0, 1.0, 0.0)], [[(0, 0.5), (1, 0.5)]], pal)
    assert close(out[0], (0.0, 0.0, 0.0), 1e-15)


def test_twist_radius_is_cos_half_angle():
    for theta in [0.1 * k for k in range(32)]:
        pal = [anim.make_T(rx(0.0), (0.0, 0.0, 0.0)), anim.make_T(rx(theta), (0.0, 0.0, 0.0))]
        out, _ = linear_blend_skinning([(0.3, 1.0, 0.0)], [[(0, 0.5), (1, 0.5)]], pal)
        r = math.hypot(out[0][1], out[0][2])
        assert abs(r - abs(math.cos(theta / 2.0))) <= 1e-12
        assert abs(out[0][0] - 0.3) <= 1e-15


def test_normals_stay_unit():
    rng = random.Random(4)
    _, bind, pose = chain(rng, 5)
    pal = skinning_matrices(pose, [anim.T_inv(b) for b in bind])
    verts, normals, weights = mesh(rng, 80, 5, 3)
    _, out_n = linear_blend_skinning(verts, weights, pal, normals)
    for n in out_n:
        assert abs(anim.norm(n) - 1.0) <= 1e-12


def test_normal_is_inverse_transpose():
    rng = random.Random(5)
    _, bind, pose = chain(rng, 3)
    pal = skinning_matrices(pose, [anim.T_inv(b) for b in bind])
    verts, normals, weights = mesh(rng, 20, 3, 3)
    _, out_n = linear_blend_skinning(verts, weights, pal, normals)
    for i in range(len(verts)):
        a = blend_matrix(weights[i], pal)
        a3 = [row[:3] for row in a[:3]]
        m = anim.matvec(anim.transpose(anim.inv(a3)), normals[i])
        assert close(out_n[i], anim.normalize(m), 1e-10)
        # the normal stays orthogonal to any tangent t, which maps to A t
        t = anim.cross(normals[i], (1.0, 0.0, 0.0))
        assert abs(anim.dot(out_n[i], anim.matvec(a3, t))) <= 1e-10


def test_common_rigid_motion_moves_mesh_rigidly():
    rng = random.Random(6)
    _, bind, pose = chain(rng, 4)
    g = rand_T(rng)
    bind_inv = [anim.T_inv(b) for b in bind]
    verts, _, weights = mesh(rng, 50, 4, 3)
    out, _ = linear_blend_skinning(verts, weights, skinning_matrices(pose, bind_inv))
    moved = [anim.T_mul(g, m) for m in pose]
    out_g, _ = linear_blend_skinning(verts, weights, skinning_matrices(moved, bind_inv))
    for a, b in zip(out, out_g):
        assert close(anim.T_apply(g, a), b, 1e-12)


def test_bad_weights_raise():
    pal = [anim.eye(4)]
    with pytest.raises(ValueError):
        linear_blend_skinning([(0.0, 0.0, 0.0)], [[(0, 0.7)]], pal)
    with pytest.raises(ValueError):
        linear_blend_skinning([(0.0, 0.0, 0.0)], [[(0, 1.5), (0, -0.5)]], pal)
