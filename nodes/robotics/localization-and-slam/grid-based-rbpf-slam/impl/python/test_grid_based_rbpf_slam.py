# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grid-based-rbpf-slam/. The authors are listed in prov/X1GN8F.jsonl.

import math
import random

from grid_based_rbpf_slam import (
    Params,
    Particle,
    World,
    best_particle,
    compose,
    gaussian_from_points,
    grid_rbpf_step,
    improved_proposal,
    initial_particles,
    integrate_scan,
    log_sum_exp,
    motion_logpdf,
    n_eff,
    new_grid,
    ray_cells,
    relative,
    sample_motion,
    scan_loglik,
    scan_match,
)

P = Params()
WORLD = World(P)
U = [0.2, 0.0, 0.2 / 1.2]  # the odometry step: a circle of radius 1.2 m around the box


def test_ray_cells_and_one_beam():
    cells = ray_cells((0, 0), (5, 2))
    assert cells == [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]
    p = Params(beams=1)
    grid = new_grid(p)
    integrate_scan(grid, p, [1.05, 1.05, 0.0], [0.5])
    assert grid[10 * p.width + 15] == p.l_occ  # the hit cell (15, 10)
    assert all(grid[10 * p.width + cx] == p.l_free for cx in range(10, 15))
    assert sum(1 for v in grid if v != 0.0) == 6


def test_compose_relative_and_motion_density():
    a, b = [1.0, 2.0, 0.7], [0.3, -0.1, 0.2]
    c = compose(a, b)
    assert max(abs(x - y) for x, y in zip(relative(a, c), b)) < 1e-12
    sd = P.motion_sd
    peak = sum(-math.log(s) - 0.5 * math.log(2.0 * math.pi) for s in sd)
    assert abs(motion_logpdf(a, compose(a, U), U, sd) - peak) < 1e-12
    rng = random.Random(3)
    draws = [relative(a, sample_motion(rng, a, U, sd)) for _ in range(3000)]
    for i in range(3):
        m = sum(d[i] for d in draws) / len(draws)
        v = sum((d[i] - m) ** 2 for d in draws) / len(draws)
        assert abs(m - U[i]) < 4.0 * sd[i] / math.sqrt(len(draws))
        assert abs(math.sqrt(v) / sd[i] - 1.0) < 0.06


def known_map(poses):
    grid = new_grid(P)
    for pose in poses:
        integrate_scan(grid, P, pose, WORLD.scan(pose))
    return grid


def test_scan_match_recovers_a_perturbed_pose():
    grid = [P.l_occ if occ else P.l_free for occ in WORLD.occ]  # the true map
    truth = [3.3, 0.9, 0.2]
    ranges = WORLD.scan(truth)
    for start in ([3.38, 0.84, 0.24], [3.24, 0.95, 0.17], [3.2, 1.0, 0.25]):
        found, score = scan_match(grid, P, start, ranges)
        assert math.hypot(found[0] - truth[0], found[1] - truth[1]) < 0.03
        assert abs(found[2] - truth[2]) < 0.02
        assert score >= scan_loglik(grid, P, start, ranges)[0]
        assert scan_loglik(grid, P, found, ranges)[1] == len(ranges)
    # hill climbing can stop at a local maximum: from this start it stops 5 cm off
    found, _ = scan_match(grid, P, [3.35, 0.86, 0.23], ranges)
    assert 0.03 < math.hypot(found[0] - truth[0], found[1] - truth[1]) < 0.1


def test_gaussian_from_points_page_example():
    pts = [[0.95, 0.0, 0.0], [1.0, 0.0, 0.0], [1.05, 0.0, 0.0]]
    mean, cov, log_eta = gaussian_from_points(pts, [0.0, math.log(2.0), 0.0], [1.0, 0.0, 0.0])
    assert abs(mean[0] - 1.0) < 1e-12 and abs(mean[1]) < 1e-12
    assert abs(cov[0][0] - (0.00125 + 1e-8)) < 1e-12 and abs(cov[1][1] - 1e-8) < 1e-15
    assert abs(log_eta - math.log(4.0)) < 1e-12


def test_the_weight_factor_estimates_the_integral_over_the_box():
    """With many points, the factor of line L6 matches a midpoint rule over the same box."""
    grid = known_map([[3.0, 0.8, 0.0], [4.2, 2.0, 1.57]])
    prev = [3.0, 0.8, 0.0]
    ranges = WORLD.scan(compose(prev, [0.21, 0.01, 0.18]))
    best, _ = scan_match(grid, P, compose(prev, U), ranges)
    p = Params(k_points=3000)
    _, log_factor = improved_proposal(random.Random(4), grid, p, prev, U, ranges)
    n = 14
    logs = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                q = [best[0] + P.delta[0] * (2.0 * (i + 0.5) / n - 1.0), best[1] + P.delta[1] * (2.0 * (j + 0.5) / n - 1.0), best[2] + P.delta[2] * (2.0 * (k + 0.5) / n - 1.0)]
                logs.append(scan_loglik(grid, P, q, ranges)[0] + motion_logpdf(prev, q, U, P.motion_sd))
    volume = 8.0 * P.delta[0] * P.delta[1] * P.delta[2]
    exact = log_sum_exp(logs) + math.log(volume / n**3)
    assert abs(log_factor - exact) < 0.05


def test_adaptive_resampling():
    rng = random.Random(5)
    grids = [new_grid(P) for _ in range(4)]
    even = [Particle([0.0, 0.0, 0.0], g, math.log(w)) for g, w in zip(grids, [0.5, 0.3, 0.1, 0.1])]
    assert abs(n_eff([q.logw for q in even]) - 1.0 / 0.36) < 1e-9
    # N_eff = 2.78 >= N/2 = 2: no resampling. With the weights 0.7, 0.1, 0.1, 0.1, N_eff = 1.92 < 2.
    skew = [Particle([0.0, 0.0, 0.0], g, math.log(w)) for g, w in zip(grids, [0.7, 0.1, 0.1, 0.1])]
    assert abs(n_eff([q.logw for q in skew]) - 1.0 / 0.52) < 1e-9
    zero = [10.0] * len(P.angles)
    kept, resampled = grid_rbpf_step(even, [0.0, 0.0, 0.0], zero, rng, P, improved=False)
    assert not resampled and kept is even
    out, resampled = grid_rbpf_step(skew, [0.0, 0.0, 0.0], zero, rng, P, improved=False)
    assert resampled and len(out) == 4
    assert all(abs(q.logw + math.log(4.0)) < 1e-12 for q in out)
    assert len({id(q.grid) for q in out}) == 4  # every copy owns its grid
    out[0].grid[0] = 99.0
    assert all(q.grid[0] != 99.0 for q in out[1:])


def run(seed, n, improved, steps=25, slip=0.015):
    """A loop around the box. The robot turns 0.015 rad per step more than the odometry says."""
    rng = random.Random(seed)
    truth = [3.0, 0.8, 0.0]
    odo = list(truth)
    ranges = WORLD.scan(truth, rng, 0.02)
    particles = initial_particles(n, truth, ranges, P)
    odo_grid = new_grid(P)
    integrate_scan(odo_grid, P, odo, ranges)
    for _ in range(steps):
        step = [U[0] + 0.02 * rng.gauss(0.0, 1.0), 0.01 * rng.gauss(0.0, 1.0), U[2] + slip + 0.01 * rng.gauss(0.0, 1.0)]
        truth = compose(truth, step)
        odo = compose(odo, U)
        ranges = WORLD.scan(truth, rng, 0.02)
        particles, _ = grid_rbpf_step(particles, U, ranges, rng, P, improved)
        integrate_scan(odo_grid, P, odo, ranges)
    w = [math.exp(q.logw) for q in particles]
    x = sum(wi * q.pose[0] for wi, q in zip(w, particles)) / sum(w)
    y = sum(wi * q.pose[1] for wi, q in zip(w, particles)) / sum(w)
    err = math.hypot(x - truth[0], y - truth[1])
    return err, math.hypot(odo[0] - truth[0], odo[1] - truth[1]), particles, odo_grid


def map_agreement(grid):
    """The share of occupied cells of the grid that are within one cell of a true wall."""
    occ = [i for i, v in enumerate(grid) if v > 0.0]
    good = sum(1 for i in occ if any(WORLD.occupied(i % P.width + dx, i // P.width + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)))
    return good / len(occ)


def test_simulation_with_the_improved_proposal():
    """A measurement: 5 particles, 25 steps, 2 seeds."""
    for seed in range(2):
        err, odo_err, particles, odo_grid = run(seed, 5, True)
        assert err < 0.15
        assert odo_err > 0.4
        assert map_agreement(best_particle(particles).grid) > 0.9
        assert map_agreement(odo_grid) < 0.75


def test_the_motion_proposal_does_worse_with_5_particles():
    """A measurement: the same runs with the motion model as the proposal, 6 seeds."""
    errs = [run(seed, 5, False)[0] for seed in range(6)]
    assert sum(errs) / len(errs) > 0.1
