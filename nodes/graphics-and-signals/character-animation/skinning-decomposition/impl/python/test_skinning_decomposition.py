# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skinning-decomposition/. The authors are listed in prov/H700TR.jsonl.
"""Tests of smooth skinning decomposition with rigid bones.

The weight step is checked against a brute force search over a grid of the
simplex and against the KKT conditions, and the bone step against a brute
force search over the angle. The error does not increase over the
iterations, the ground truth is a fixed point, and data made by linear blend
skinning is fitted closely from the k-means start. The weights are
nonnegative, sum to 1 and have at most K nonzero entries. The check values of
the page hold.
"""

import math
import random

from skinning_decomposition import (
    error,
    simplex_lsq,
    skin,
    ssdr,
    transform,
    update_bone,
    update_weights,
    weighted_procrustes,
)

REST = [(0.25 * k, y) for k in range(13) for y in (-0.2, 0.0, 0.2)]


def true_weights(x):
    if x <= 0.75:
        return [1.0, 0.0, 0.0]
    if x < 1.25:
        t = (x - 0.75) / 0.5
        return [1.0 - t, t, 0.0]
    if x <= 1.75:
        return [0.0, 1.0, 0.0]
    if x < 2.25:
        t = (x - 1.75) / 0.5
        return [0.0, 1.0 - t, t]
    return [0.0, 0.0, 1.0]


def chain(a, b, c):
    def child(theta, pivot, parent):
        pt = transform(parent, pivot)
        th = parent[0] + theta
        co, si = math.cos(th), math.sin(th)
        return (th, (pt[0] - (co * pivot[0] - si * pivot[1]), pt[1] - (si * pivot[0] + co * pivot[1])))

    b0 = (a, (0.0, 0.0))
    b1 = child(b, (1.0, 0.0), b0)
    return [b0, b1, child(c, (2.0, 0.0), b1)]


POSES = [(0, 0, 0), (0.3, 0.5, -0.4), (-0.2, 0.8, 0.6), (0.5, -0.6, 0.9), (0.1, 1.0, -0.8), (-0.4, -0.3, 0.3)]
W_TRUE = [true_weights(v[0]) for v in REST]
B_TRUE = [[chain(*p)[b] for p in POSES] for b in range(3)]
FRAMES = [skin(REST, W_TRUE, B_TRUE, f) for f in range(len(POSES))]


def sq(cols, w, target):
    r = [-t for t in target]
    for b, wb in enumerate(w):
        r = [x + wb * y for x, y in zip(r, cols[b])]
    return sum(x * x for x in r)


def test_simplex_lsq_against_a_grid():
    rng = random.Random(1)
    for _ in range(20):
        cols = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(3)]
        target = [rng.gauss(0, 1) for _ in range(6)]
        w, e = simplex_lsq(cols, target, [0, 1, 2])
        assert all(x >= 0.0 for x in w) and abs(sum(w) - 1.0) < 1e-12
        assert abs(e - sq(cols, w, target)) < 1e-9
        steps = 60
        best = min(
            sq(cols, (i / steps, j / steps, 1 - (i + j) / steps), target)
            for i in range(steps + 1)
            for j in range(steps + 1 - i)
        )
        assert e <= best + 1e-12


def test_simplex_lsq_kkt():
    rng = random.Random(2)
    for _ in range(20):
        cols = [[rng.gauss(0, 1) for _ in range(8)] for _ in range(4)]
        target = [rng.gauss(0, 1) for _ in range(8)]
        w, _ = simplex_lsq(cols, target, [0, 1, 2, 3])
        r = [-t for t in target]
        for b in range(4):
            r = [x + w[b] * y for x, y in zip(r, cols[b])]
        g = [2.0 * sum(x * y for x, y in zip(c, r)) for c in cols]
        lam = min(g[b] for b in range(4) if w[b] > 1e-12)
        for b in range(4):
            if w[b] > 1e-12:
                assert abs(g[b] - lam) < 1e-8
            else:
                assert g[b] >= lam - 1e-8


def test_weighted_procrustes_against_an_angle_search():
    rng = random.Random(3)
    pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(10)]
    tg = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(10)]
    w = [rng.uniform(0, 1) for _ in range(10)]

    def cost(theta, t):
        return sum(
            (r[0] - x * transform((theta, t), p)[0]) ** 2 + (r[1] - x * transform((theta, t), p)[1]) ** 2
            for x, p, r in zip(w, pts, tg)
        )

    def best_t(theta):
        sw2 = sum(x * x for x in w)
        c, s = math.cos(theta), math.sin(theta)
        return tuple(
            sum(x * (r[k] - x * (c * p[0] - s * p[1] if k == 0 else s * p[0] + c * p[1])) for x, p, r in zip(w, pts, tg))
            / sw2
            for k in range(2)
        )

    theta, t = weighted_procrustes(pts, tg, w)
    e = cost(theta, t)
    grid = min(cost(a, best_t(a)) for a in (2 * math.pi * i / 3600 for i in range(3600)))
    assert e <= grid + 1e-12


def test_ground_truth_is_a_fixed_point():
    w = update_weights(REST, FRAMES, W_TRUE, B_TRUE, 2)
    assert error(REST, FRAMES, w, B_TRUE) < 1e-20
    bones = [list(b) for b in B_TRUE]
    for b in range(3):
        bones[b] = update_bone(REST, FRAMES, w, bones, b)
    assert error(REST, FRAMES, w, bones) < 1e-20


def test_error_does_not_increase_and_fit_is_close():
    w, bones, errs = ssdr(REST, FRAMES, 3, k_max=2, iters=40, seed=0)
    assert all(errs[i + 1] <= errs[i] + 1e-12 for i in range(len(errs) - 1))
    assert errs[-1] < 1e-5 * errs[0]
    for row in w:
        assert all(x >= 0.0 for x in row)
        assert abs(sum(row) - 1.0) < 1e-12
        assert sum(1 for x in row if x > 0.0) <= 2


def test_sparsity_one_bone_per_vertex():
    w, _, errs = ssdr(REST, FRAMES, 3, k_max=1, iters=10, seed=0)
    assert all(sorted(row) == [0.0, 0.0, 1.0] for row in w)
    assert all(errs[i + 1] <= errs[i] + 1e-12 for i in range(len(errs) - 1))


def test_check_values_of_the_page():
    cols = [[1.0, 0.0], [0.0, 1.0]]
    for target, want, e_want in (
        ([0.5, 0.5], [0.5, 0.5], 0.0),
        ([1.0, 1.0], [0.5, 0.5], 0.5),
        ([2.0, 0.0], [1.0, 0.0], 1.0),
    ):
        w, e = simplex_lsq(cols, target, [0, 1])
        assert all(abs(a - b) < 1e-12 for a, b in zip(w, want))
        assert abs(e - e_want) < 1e-12
