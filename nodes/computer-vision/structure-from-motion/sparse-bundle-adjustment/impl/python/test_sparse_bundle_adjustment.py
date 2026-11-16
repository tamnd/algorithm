# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-bundle-adjustment/. The authors are listed in prov/C231EB.jsonl.

import math
import random

from cvgeom import add_noise, axis_angle_to_R, random_scene
from cvla import mul, solve
from sparse_bundle_adjustment import (apply_step, build_blocks, cost, observation_blocks,
                                      project_point, reprojection_rms, solve_damped,
                                      sparse_bundle_adjustment)


def make_problem(seed, n_cams=4, n_pts=20, noise=0.0):
    rng = random.Random(seed)
    sc = random_scene(rng, n=n_pts, n_cams=n_cams, first_identity=True)
    obs = []
    for i in range(n_cams):
        pix = add_noise(rng, sc["x"][i], noise) if noise > 0 else sc["x"][i]
        for j in range(n_pts):
            obs.append((i, j, pix[j][0], pix[j][1]))
    cams = list(zip(sc["R"], sc["t"]))
    return rng, sc["K"][0], cams, sc["X"], obs


def perturb(rng, cams, pts, rot=0.02, trans=0.05, point=0.05):
    out = [cams[0]]
    for R, t in cams[1:]:
        w = [rng.gauss(0, rot) for _ in range(3)]
        out.append((mul(axis_angle_to_R(w), R), [v + rng.gauss(0, trans) for v in t]))
    return out, [[v + rng.gauss(0, point) for v in x] for x in pts]


def test_jacobian_blocks_against_finite_differences():
    rng, K, cams, pts, _ = make_problem(1)
    h = 1e-6
    for i in range(1, 4):
        R, t = cams[i]
        for j in (0, 7, 13):
            X = pts[j]
            a, b = observation_blocks(K, R, t, X)
            for c in range(6):
                d = [0.0] * 6
                d[c] = h
                plus = apply_step([(R, t)], [], {0: d}, [])[0][0]
                d[c] = -h
                minus = apply_step([(R, t)], [], {0: d}, [])[0][0]
                pp, pm = project_point(K, plus[0], plus[1], X), project_point(K, minus[0], minus[1], X)
                for k in range(2):
                    fd = (pp[k] - pm[k]) / (2 * h)
                    assert abs(fd - a[k][c]) <= 1e-5 * max(1.0, abs(fd))
            for c in range(3):
                xp, xm = list(X), list(X)
                xp[c] += h
                xm[c] -= h
                pp, pm = project_point(K, R, t, xp), project_point(K, R, t, xm)
                for k in range(2):
                    fd = (pp[k] - pm[k]) / (2 * h)
                    assert abs(fd - b[k][c]) <= 1e-5 * max(1.0, abs(fd))


def test_reduced_system_matches_dense_solve():
    rng, K, cams, pts, obs = make_problem(2, n_cams=3, n_pts=8)
    cams, pts = perturb(rng, cams, pts)
    free = [1, 2]
    U, V, W, ga, gb = build_blocks(K, cams, pts, obs, free)
    mu = 3.7
    da, db = solve_damped(U, V, W, ga, gb, mu, free)
    # the full damped system, assembled densely from the per-observation blocks
    nc, n = 6 * len(free), 6 * len(free) + 3 * len(pts)
    a_full = [[0.0] * n for _ in range(n)]
    g_full = [0.0] * n
    for i, j, u, v in obs:
        R, t = cams[i]
        p = project_point(K, R, t, pts[j])
        r = [p[0] - u, p[1] - v]
        a, b = observation_blocks(K, R, t, pts[j])
        row = [[0.0] * n for _ in range(2)]
        for k in range(2):
            if i in free:
                o = 6 * free.index(i)
                row[k][o:o + 6] = a[k]
            row[k][nc + 3 * j:nc + 3 * j + 3] = b[k]
        for p_ in range(n):
            g_full[p_] += row[0][p_] * r[0] + row[1][p_] * r[1]
            for q in range(n):
                a_full[p_][q] += row[0][p_] * row[0][q] + row[1][p_] * row[1][q]
    for p_ in range(n):
        a_full[p_][p_] += mu
    dense = solve(a_full, [-v for v in g_full])
    ours = [x for i in free for x in da[i]] + [x for d in db for x in d]
    for x, y in zip(ours, dense):
        assert abs(x - y) <= 1e-8 * max(1.0, abs(y))


def test_exact_data_is_recovered_up_to_the_gauge():
    rng, K, cams_true, pts_true, obs = make_problem(3)
    cams0, pts0 = perturb(rng, cams_true, pts_true)
    assert reprojection_rms(K, cams0, pts0, obs) > 1.0
    cams, pts, info = sparse_bundle_adjustment(K, cams0, pts0, obs)
    assert reprojection_rms(K, cams, pts, obs) < 1e-8
    # camera 0 is fixed; the scale is the last gauge freedom
    s = math.sqrt(sum(v * v for v in cams[1][1])) / math.sqrt(sum(v * v for v in cams_true[1][1]))
    assert abs(s - 1.0) < 0.2
    for (R, t), (Rt, tt) in zip(cams, cams_true):
        assert max(abs(R[a][b] - Rt[a][b]) for a in range(3) for b in range(3)) < 1e-6
        assert max(abs(x - s * y) for x, y in zip(t, tt)) < 1e-6 * max(1.0, s * max(abs(y) for y in tt))
    for x, y in zip(pts, pts_true):
        assert max(abs(a - s * b) for a, b in zip(x, y)) < 1e-6 * max(1.0, max(abs(b) for b in y))


def test_costs_decrease_strictly():
    rng, K, cams_true, pts_true, obs = make_problem(4, noise=0.5)
    cams0, pts0 = perturb(rng, cams_true, pts_true, rot=0.05, trans=0.2, point=0.1)
    _, _, info = sparse_bundle_adjustment(K, cams0, pts0, obs)
    costs = info["costs"]
    assert len(costs) > 3
    assert all(c1 < c0 for c0, c1 in zip(costs, costs[1:]))


def test_noisy_data_reaches_at_most_the_cost_of_the_truth():
    rng, K, cams_true, pts_true, obs = make_problem(5, noise=1.0)
    cams0, pts0 = perturb(rng, cams_true, pts_true)
    cams, pts, _ = sparse_bundle_adjustment(K, cams0, pts0, obs)
    f_true = cost(K, cams_true, pts_true, obs)
    f_opt = cost(K, cams, pts, obs)
    assert f_opt <= f_true
    # the gradient is zero at the minimizer
    free = [1, 2, 3]
    _, _, _, ga, gb = build_blocks(K, cams, pts, obs, free)
    g = [x for i in free for x in ga[i]] + [x for d in gb for x in d]
    assert max(abs(x) for x in g) < 1e-6
    # with sigma = 1 pixel, the residual RMS per coordinate is close to 1
    rms = math.sqrt(2.0 * f_opt / (2 * len(obs)))
    assert 0.6 < rms < 1.2


def test_predicted_reduction_is_positive():
    rng, K, cams_true, pts_true, obs = make_problem(6, n_cams=3, n_pts=10)
    cams, pts = perturb(rng, cams_true, pts_true)
    free = [1, 2]
    U, V, W, ga, gb = build_blocks(K, cams, pts, obs, free)
    g = [x for i in free for x in ga[i]] + [x for d in gb for x in d]
    for mu in (1e-3, 1.0, 1e3, 1e6):
        da, db = solve_damped(U, V, W, ga, gb, mu, free)
        delta = [x for i in free for x in da[i]] + [x for d in db for x in d]
        assert 0.5 * sum(d * (mu * d - gi) for d, gi in zip(delta, g)) > 0
