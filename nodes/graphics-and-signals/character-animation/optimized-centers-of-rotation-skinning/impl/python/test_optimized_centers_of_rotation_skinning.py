# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimized-centers-of-rotation-skinning/. The authors are listed in prov/3BKQB9.jsonl.
"""Tests of skinning with optimized centers of rotation.

They check the similarity, the refinement, the centers against a direct
quadrature of the integral, the bind pose, the single joint case, a common
rigid motion, the twist of a tube (no volume loss, unlike linear blend
skinning), unit normals, and that the centers move with the rest mesh.
"""

import functools
import math
import random

import anim
from optimized_centers_of_rotation_skinning import (
    centers_of_rotation,
    cor_skinning,
    lbs,
    max_edge_weight_change,
    refine,
    similarity,
)


def smoothstep(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3.0 - 2.0 * x)


def tube(nr=8, ny=9, radius=0.5, length=2.0):
    """An open tube along y with two joints, at y = 0 and y = 1."""
    verts, normals, weights = [], [], []
    for r in range(ny):
        y = length * r / (ny - 1)
        w1 = smoothstep(y - 0.5)
        for k in range(nr):
            a = 2.0 * math.pi * k / nr
            verts.append((radius * math.cos(a), y, radius * math.sin(a)))
            normals.append((math.cos(a), 0.0, math.sin(a)))
            weights.append([1.0 - w1, w1])
    tris = []
    for r in range(ny - 1):
        for k in range(nr):
            a, b = r * nr + k, r * nr + (k + 1) % nr
            c, d = a + nr, b + nr
            tris += [(a, c, b), (b, c, d)]
    return verts, normals, weights, tris


@functools.lru_cache(maxsize=None)
def tube_centers():
    verts, _, weights, tris = tube()
    return tuple(centers_of_rotation(verts, tris, weights, eps=0.2))


def rand_T(rng):
    q = anim.q_normalize([rng.gauss(0.0, 1.0) for _ in range(4)])
    return anim.make_T(anim.q_to_mat3(q), tuple(rng.uniform(-2.0, 2.0) for _ in range(3)))


def rot_y(t):
    return anim.make_T(anim.q_to_mat3(anim.q_from_axis_angle((0.0, 1.0, 0.0), t)), (0.0, 0.0, 0.0))


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def grid(rng, n=3, nj=3):
    """A small bumpy grid with random weights over nj joints."""
    verts, weights = [], []
    for r in range(n):
        for c in range(n):
            verts.append((float(c), float(r), 0.3 * rng.random()))
            w = [rng.random() + 0.05 for _ in range(nj)]
            s = sum(w)
            weights.append([x / s for x in w])
    tris = []
    for r in range(n - 1):
        for c in range(n - 1):
            a = r * n + c
            tris += [(a, a + 1, a + n), (a + 1, a + n + 1, a + n)]
    return verts, tris, weights


def quadrature_centers(verts, tris, weights, m, sigma=0.1):
    """The integral of the center formula by the midpoint rule on an m by m split of each triangle."""
    out = []
    for wi in weights:
        num, den = (0.0, 0.0, 0.0), 0.0
        for a, b, c in tris:
            area = 0.5 * anim.norm(anim.cross(anim.sub(verts[b], verts[a]), anim.sub(verts[c], verts[a]))) / (m * m)
            for i in range(m):
                for j in range(m - i):
                    pts = [((i + 1 / 3) / m, (j + 1 / 3) / m)]
                    if i + j < m - 1:
                        pts.append(((i + 2 / 3) / m, (j + 2 / 3) / m))
                    for u, v in pts:
                        bc = (1.0 - u - v, u, v)
                        x = tuple(sum(bc[k] * verts[t][d] for k, t in enumerate((a, b, c))) for d in range(3))
                        w = [sum(bc[k] * weights[t][q] for k, t in enumerate((a, b, c))) for q in range(len(wi))]
                        s = similarity(wi, w, sigma) * area
                        num = anim.add(num, anim.scale(x, s))
                        den += s
        out.append(anim.scale(num, 1.0 / den))
    return out


def test_similarity():
    rng = random.Random(1)
    for _ in range(50):
        a = [rng.random() for _ in range(4)]
        b = [rng.random() for _ in range(4)]
        assert abs(similarity(a, b) - similarity(b, a)) < 1e-15
        assert similarity(a, b) > 0.0
    assert similarity([1.0, 0.0, 0.0], [0.5, 0.5, 0.0]) == 0.0
    assert similarity([0.5, 0.0, 0.5], [0.0, 0.5, 0.5]) == 0.0
    # for a fixed own weight vector, the closest match is the most similar
    w = [0.5, 0.5]
    assert similarity(w, [0.5, 0.5]) > similarity(w, [0.6, 0.4]) > similarity(w, [0.8, 0.2])


def test_refine_meets_the_bound():
    verts, _, weights, tris = tube()
    fv, ft, fw = refine(verts, tris, weights, eps=0.2)
    assert max_edge_weight_change(ft, fw) <= 0.2
    assert fv[: len(verts)] == verts
    for w in fw:
        assert abs(sum(w) - 1.0) < 1e-12


def test_centers_match_quadrature():
    rng = random.Random(2)
    verts, tris, weights = grid(rng)
    # three levels of splitting are the midpoint rule on an 8 by 8 split
    got = centers_of_rotation(verts, tris, weights, eps=0.0, max_levels=3)
    ref = quadrature_centers(verts, tris, weights, 8)
    for a, b in zip(got, ref):
        assert close(a, b, 1e-12)
    # and the refinement converges to the integral
    fine = quadrature_centers(verts, tris, weights, 24)
    errs = []
    for lv in (0, 1, 2):
        c = centers_of_rotation(verts, tris, weights, eps=0.0, max_levels=lv)
        errs.append(max(anim.norm(anim.sub(a, b)) for a, b in zip(c, fine)))
    assert errs[0] > errs[1] > errs[2]


def test_bind_pose_gives_rest_mesh():
    verts, normals, weights, _ = tube()
    pal = [anim.eye(4), anim.eye(4)]
    out_v, out_n = cor_skinning(verts, weights, tube_centers(), pal, normals)
    for a, b in zip(out_v, verts):
        assert close(a, b, 1e-12)
    for a, b in zip(out_n, normals):
        assert close(a, b, 1e-12)


def test_single_joint_is_rigid():
    rng = random.Random(3)
    verts, _, weights, _ = tube()
    centers = tube_centers()
    pal = [rand_T(rng), rand_T(rng)]
    out_v, _ = cor_skinning(verts, weights, centers, pal)
    count = 0
    for v, w, c, a in zip(verts, weights, centers, out_v):
        if w[1] == 0.0:
            assert c == v
            assert close(a, anim.T_apply(pal[0], v), 1e-12)
            count += 1
    assert count >= 8


def test_common_rigid_motion():
    rng = random.Random(4)
    verts, normals, weights, _ = tube()
    g = rand_T(rng)
    out_v, out_n = cor_skinning(verts, weights, tube_centers(), [g, g], normals)
    gr = [row[:3] for row in g[:3]]
    for v, n, a, b in zip(verts, normals, out_v, out_n):
        assert close(a, anim.T_apply(g, v), 1e-12)
        assert close(b, anim.matvec(gr, n), 1e-12)


def test_twist_keeps_the_radius():
    verts, normals, weights, _ = tube()
    centers = tube_centers()
    for c, w in zip(centers, weights):
        if min(w) > 0.0:
            assert math.hypot(c[0], c[2]) < 1e-9
    for t in (1.0, math.pi / 2, 2.5, math.pi):
        pal = [anim.eye(4), rot_y(t)]
        out_v, out_n = cor_skinning(verts, weights, centers, pal, normals)
        ref = lbs(verts, weights, pal)
        for v, a, b, n in zip(verts, out_v, ref, out_n):
            assert abs(math.hypot(a[0], a[2]) - 0.5) < 1e-12
            assert abs(a[1] - v[1]) < 1e-12
            assert abs(anim.norm(n) - 1.0) < 1e-12
        lbs_min = min(math.hypot(b[0], b[2]) for b in ref)
        assert lbs_min < 0.5 * abs(math.cos(t / 2)) + 1e-9


def test_bend_reduces_the_loss_of_volume():
    # bend joint 1 by pi/2 about the z axis through (0, 1, 0); the mean
    # distance of the middle ring from the elbow drops less than with LBS
    verts, _, weights, _ = tube()
    centers = tube_centers()
    r = anim.q_to_mat3(anim.q_from_axis_angle((0.0, 0.0, 1.0), math.pi / 2))
    elbow = (0.0, 1.0, 0.0)
    pal = [anim.eye(4), anim.make_T(r, anim.sub(elbow, anim.matvec(r, elbow)))]
    out_v, _ = cor_skinning(verts, weights, centers, pal)
    ref = lbs(verts, weights, pal)
    ring = [i for i, v in enumerate(verts) if abs(v[1] - 1.0) < 1e-12]
    d_cor = sum(anim.norm(anim.sub(out_v[i], elbow)) for i in ring) / len(ring)
    d_lbs = sum(anim.norm(anim.sub(ref[i], elbow)) for i in ring) / len(ring)
    assert d_cor > d_lbs


def test_centers_move_with_the_mesh():
    rng = random.Random(5)
    verts, tris, weights = grid(rng)
    g = rand_T(rng)
    c0 = centers_of_rotation(verts, tris, weights, eps=0.0, max_levels=2)
    c1 = centers_of_rotation([anim.T_apply(g, v) for v in verts], tris, weights, eps=0.0, max_levels=2)
    for a, b in zip(c0, c1):
        assert close(anim.T_apply(g, a), b, 1e-9)
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    for a in c0:
        assert min(xs) <= a[0] <= max(xs) and min(ys) <= a[1] <= max(ys)
