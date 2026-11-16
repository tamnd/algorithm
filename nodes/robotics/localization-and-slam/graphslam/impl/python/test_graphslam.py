# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graphslam/. The authors are listed in prov/DRMB6N.jsonl.

import math
import random

import pytest

from graphslam import (
    ANCHOR,
    Problem,
    graphslam,
    initialize,
    inverse,
    linearize,
    matvec,
    measure,
    motion,
    reduce,
    solve,
    wrap,
)

RM = [[0.02 ** 2, 0.0, 0.0], [0.0, 0.02 ** 2, 0.0], [0.0, 0.0, 0.01 ** 2]]
QM = [[0.05 ** 2, 0.0], [0.0, 0.02 ** 2]]
LANDMARKS = [(2.0, 0.5), (3.5, 2.5), (1.5, 4.0), (-0.5, 2.5), (0.5, -1.0)]


def simulate(seed, steps=12, noise=True, max_range=3.5):
    """Drive a circle of radius about 2 m around (1.5, 1.5) and measure the landmarks in range."""
    rng = random.Random(seed)
    u_true = (1.0, 0.0, 2.0 * math.pi / steps)
    poses = [[0.0, 0.0, 0.0]]
    controls = []
    for _ in range(steps):
        poses.append(motion(poses[-1], u_true))
        if noise:
            controls.append([u_true[0] + rng.gauss(0, 0.02), u_true[1] + rng.gauss(0, 0.02), u_true[2] + rng.gauss(0, 0.01)])
        else:
            controls.append(list(u_true))
    meas = []
    for t, x in enumerate(poses):
        for j, m in enumerate(LANDMARKS):
            z = measure(x, m)
            if z[0] <= max_range:
                if noise:
                    z = [z[0] + rng.gauss(0, 0.05), wrap(z[1] + rng.gauss(0, 0.02))]
                meas.append((t, j, z))
    return Problem(controls, meas, len(LANDMARKS), RM, QM), poses


def cost(pb, mu, lm):
    """The negative log posterior up to a constant: the sum that GraphSLAM minimizes."""
    c = 0.5 * ANCHOR * sum(v * v for v in mu[0])
    for t in range(1, pb.T + 1):
        g = motion(mu[t - 1], pb.u[t - 1])
        d = [mu[t][0] - g[0], mu[t][1] - g[1], wrap(mu[t][2] - g[2])]
        c += 0.5 * sum(d[a] * pb.rinv[a][b] * d[b] for a in range(3) for b in range(3))
    for t, j, z in pb.z:
        h = measure(mu[t], lm[j])
        d = [z[0] - h[0], wrap(z[1] - h[1])]
        c += 0.5 * sum(d[a] * pb.qinv[a][b] * d[b] for a in range(2) for b in range(2))
    return c


def test_noise_free_data_gives_the_true_map_and_path():
    pb, poses = simulate(1, noise=False)
    mu, lm, _, it = graphslam(pb)
    assert it <= 3
    for p, q in zip(mu, poses):
        assert abs(p[0] - q[0]) < 1e-9 and abs(p[1] - q[1]) < 1e-9 and abs(wrap(p[2] - q[2])) < 1e-9
    for p, q in zip(lm, LANDMARKS):
        assert abs(p[0] - q[0]) < 1e-9 and abs(p[1] - q[1]) < 1e-9
    assert cost(pb, mu, lm) < 1e-12


def test_reduce_then_solve_equals_the_full_joint_solve():
    pb, _ = simulate(2)
    mu, lm = initialize(pb)
    om, xi = linearize(pb, mu, lm)
    omr, xir = reduce(pb, om, xi)
    poses, lms, sigma = solve(pb, omr, xir, om, xi)
    full = matvec(inverse(om), xi)
    flat = [v for p in poses for v in p] + [v for m in lms for v in m]
    assert max(abs(a - b) for a, b in zip(flat, full)) < 1e-8
    # Sigma of the path equals the pose block of the inverse of the full Omega.
    big = inverse(om)
    p = 3 * (pb.T + 1)
    assert max(abs(sigma[r][c] - big[r][c]) for r in range(p) for c in range(p)) < 1e-9


def test_reduced_matrix_couples_poses_that_saw_the_same_landmark():
    pb, _ = simulate(3)
    mu, lm = initialize(pb)
    om, xi = linearize(pb, mu, lm)
    omr, _ = reduce(pb, om, xi)
    seen = {}
    for t, j, _ in pb.z:
        seen.setdefault(j, set()).add(t)
    for a in range(pb.T + 1):
        for b in range(pb.T + 1):
            linked = abs(a - b) <= 1 or any(a in s and b in s for s in seen.values())
            block = max(abs(omr[3 * a + r][3 * b + c]) for r in range(3) for c in range(3))
            if not linked:
                assert block == 0.0


def test_noisy_solution_is_a_stationary_point_of_the_cost():
    pb, poses = simulate(4)
    mu, lm, _, it = graphslam(pb)
    assert it < 20
    flat = [v for p in mu for v in p] + [v for m in lm for v in m]

    def unflat(v):
        return [v[3 * t:3 * t + 3] for t in range(pb.T + 1)], [v[3 * (pb.T + 1) + 2 * j:3 * (pb.T + 1) + 2 * j + 2] for j in range(pb.m)]

    h = 1e-6
    for k in range(3, len(flat)):  # x_0 is pinned by the anchor
        vp, vm = list(flat), list(flat)
        vp[k] += h
        vm[k] -= h
        grad = (cost(pb, *unflat(vp)) - cost(pb, *unflat(vm))) / (2 * h)
        assert abs(grad) < 1e-3
    # The estimate is better than dead reckoning at the end of the loop.
    dr, _ = initialize(pb)
    end_err = math.hypot(mu[-1][0] - poses[-1][0], mu[-1][1] - poses[-1][1])
    dr_err = math.hypot(dr[-1][0] - poses[-1][0], dr[-1][1] - poses[-1][1])
    assert end_err < dr_err


def test_iteration_lowers_the_cost():
    pb, _ = simulate(5)
    mu0, lm0 = initialize(pb)
    mu, lm, _, _ = graphslam(pb)
    assert cost(pb, mu, lm) < cost(pb, mu0, lm0)


def test_unseen_landmark_is_an_error():
    pb, _ = simulate(6)
    pb.m += 1
    with pytest.raises(ValueError):
        initialize(pb)
