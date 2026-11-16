# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inexact-newton-bundle-adjustment/. The authors are listed in prov/HF6T4X.jsonl.

import math
import random

from cvgeom import add_noise, axis_angle_to_R, random_scene
from cvla import inv, mul, solve, transpose
from inexact_newton_bundle_adjustment import (ReducedSystem, build_blocks, cost,
                                              inexact_newton_bundle_adjustment,
                                              inexact_newton_step, observation_blocks,
                                              pcg, project_point, quadratic_form,
                                              reprojection_rms)


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


def explicit_s(U, V, W, mu, free):
    """S = U* - W V*^-1 W^T as a dense matrix."""
    pos = {i: 6 * k for k, i in enumerate(free)}
    n = 6 * len(free)
    s = [[0.0] * n for _ in range(n)]
    for i in free:
        for p in range(6):
            for q in range(6):
                s[pos[i] + p][pos[i] + q] = U[i][p][q] + (mu if p == q else 0.0)
    for j in range(len(V)):
        vinv = inv([[V[j][p][q] + (mu if p == q else 0.0) for q in range(3)] for p in range(3)])
        for i in free:
            for k in free:
                if (i, j) in W and (k, j) in W:
                    blk = mul(mul(W[(i, j)], vinv), transpose(W[(k, j)]))
                    for p in range(6):
                        for q in range(6):
                            s[pos[i] + p][pos[k] + q] -= blk[p][q]
    return s


def setup(seed=2, n_cams=4, n_pts=12, mu=2.5):
    rng, K, cams, pts, obs = make_problem(seed, n_cams=n_cams, n_pts=n_pts)
    cams, pts = perturb(rng, cams, pts)
    free = list(range(1, n_cams))
    U, V, W, ga, gb = build_blocks(K, cams, pts, obs, free)
    return K, cams, pts, obs, free, U, V, W, ga, gb, mu


def test_implicit_product_equals_explicit_schur_complement():
    _, _, _, _, free, U, V, W, ga, gb, mu = setup()
    system = ReducedSystem(U, V, W, ga, gb, mu, free)
    s = explicit_s(U, V, W, mu, free)
    rng = random.Random(1)
    for _ in range(3):
        x = [rng.uniform(-1, 1) for _ in range(system.size)]
        y = system.apply(x)
        ref = [sum(a * b for a, b in zip(row, x)) for row in s]
        scale_ = max(abs(v) for v in ref)
        assert max(abs(a - b) for a, b in zip(y, ref)) <= 1e-9 * scale_
    blocks = system.block_jacobi()
    for k, i in enumerate(free):
        d = [row[6 * k:6 * k + 6] for row in s[6 * k:6 * k + 6]]
        prod = mul(blocks[i], d)
        assert max(abs(prod[p][q] - (1.0 if p == q else 0.0)) for p in range(6) for q in range(6)) < 1e-8


def test_pcg_with_small_tolerance_matches_the_direct_solve():
    _, _, _, _, free, U, V, W, ga, gb, mu = setup()
    system = ReducedSystem(U, V, W, ga, gb, mu, free)
    e = system.rhs()
    direct = solve(explicit_s(U, V, W, mu, free), e)
    blocks = system.block_jacobi()
    x, its = pcg(system.apply, lambda r: system.precondition(blocks, r), e, 1e-12, 10 * system.size)
    assert its <= 10 * system.size
    size = max(abs(v) for v in direct)
    assert max(abs(a - b) for a, b in zip(x, direct)) <= 1e-7 * size


def test_truncated_steps_have_the_stated_predicted_reduction():
    K, cams, pts, obs, free, U, V, W, ga, gb, _ = setup(seed=3, n_pts=15)
    f0 = cost(K, cams, pts, obs)
    g = [x for i in free for x in ga[i]] + [x for d in gb for x in d]
    for mu in (1e-2, 1.0, 1e3, 1e6):
        for max_cg in (1, 2, 5):
            da, db, its = inexact_newton_step(U, V, W, ga, gb, mu, free, eta=1e-14, max_cg=max_cg)
            assert its == max_cg
            delta = [x for i in free for x in da[i]] + [x for d in db for x in d]
            # the linear model L(delta) = 1/2 ||r + J delta||^2, from the observation blocks
            model = 0.0
            for i, j, u, v in obs:
                R, t = cams[i]
                p = project_point(K, R, t, pts[j])
                a, b = observation_blocks(K, R, t, pts[j])
                for k in range(2):
                    lin = p[k] - (u, v)[k] + sum(b[k][c] * db[j][c] for c in range(3))
                    if i in da:
                        lin += sum(a[k][c] * da[i][c] for c in range(6))
                    model += 0.5 * lin * lin
            pred = f0 - model
            assert pred > 0
            # the code computes pred = -g^T delta - 1/2 ||J delta||^2 from the blocks
            jd = quadratic_form(U, V, W, free, da, db)
            assert abs(pred - (-sum(x * y for x, y in zip(g, delta)) - 0.5 * jd)) <= 1e-8 * f0


def test_exact_data_is_recovered_up_to_the_gauge():
    rng, K, cams_true, pts_true, obs = make_problem(3)
    cams0, pts0 = perturb(rng, cams_true, pts_true)
    assert reprojection_rms(K, cams0, pts0, obs) > 1.0
    cams, pts, info = inexact_newton_bundle_adjustment(K, cams0, pts0, obs, eta=0.1)
    assert reprojection_rms(K, cams, pts, obs) < 1e-8
    s = math.sqrt(sum(v * v for v in cams[1][1])) / math.sqrt(sum(v * v for v in cams_true[1][1]))
    assert abs(s - 1.0) < 0.2
    for (R, t), (Rt, tt) in zip(cams, cams_true):
        assert max(abs(R[a][b] - Rt[a][b]) for a in range(3) for b in range(3)) < 1e-6
        assert max(abs(x - s * y) for x, y in zip(t, tt)) < 1e-6 * max(1.0, s * max(abs(y) for y in tt))
    for x, y in zip(pts, pts_true):
        assert max(abs(a - s * b) for a, b in zip(x, y)) < 1e-6 * max(1.0, max(abs(b) for b in y))


def test_costs_decrease_strictly_with_few_cg_iterations():
    rng, K, cams_true, pts_true, obs = make_problem(4, noise=0.5)
    cams0, pts0 = perturb(rng, cams_true, pts_true, rot=0.05, trans=0.2, point=0.1)
    _, _, info = inexact_newton_bundle_adjustment(K, cams0, pts0, obs, eta=0.5, max_cg=3)
    costs = info["costs"]
    assert len(costs) > 3
    assert all(c1 < c0 for c0, c1 in zip(costs, costs[1:]))
    assert all(1 <= c <= 3 for c in info["cg"])


def test_noisy_data_reaches_at_most_the_cost_of_the_truth():
    rng, K, cams_true, pts_true, obs = make_problem(5, noise=1.0)
    cams0, pts0 = perturb(rng, cams_true, pts_true)
    cams, pts, _ = inexact_newton_bundle_adjustment(K, cams0, pts0, obs, eta=0.1)
    assert cost(K, cams, pts, obs) <= cost(K, cams_true, pts_true, obs)
    free = [1, 2, 3]
    _, _, _, ga, gb = build_blocks(K, cams, pts, obs, free)
    g = [x for i in free for x in ga[i]] + [x for d in gb for x in d]
    assert max(abs(x) for x in g) < 1e-6
