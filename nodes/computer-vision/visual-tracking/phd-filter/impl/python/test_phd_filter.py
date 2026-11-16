# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phd-filter/. The authors are listed in prov/9HR0MT.jsonl.

import math
import random

from phd_filter import cv_model, extract, gaussian, phd_density, phd_step, predict, prune_and_merge, update


def normal_1d(x, m, v):
    return math.exp(-0.5 * (x - m) ** 2 / v) / math.sqrt(2 * math.pi * v)


def test_matches_a_grid_phd_recursion_in_1d():
    # 1D model: x' = x + noise(0.5), z = x + noise(0.3)
    f, q, h, r = [[1.0]], [[0.5]], [[1.0]], [[0.3]]
    p_s, p_d, kap = 0.95, 0.8, 0.05
    birth = [(0.1, [0.0], [[4.0]])]
    comps = [(1.0, [-3.0], [[1.0]]), (0.7, [4.0], [[0.5]])]
    step = 0.1
    grid = [-15.0 + step * i for i in range(301)]
    mix_1d = lambda cs, x: sum(w * normal_1d(x, m[0], p[0][0]) for w, m, p in cs)
    dens = [mix_1d(comps, x) for x in grid]
    assert abs(dens[150] - phd_density(comps, [0.0])) < 1e-15
    for zs in ([[-2.5], [4.3], [8.0]], [[-1.8], [5.0]]):
        # the PHD recursion on the grid, with sums in place of the integrals
        pred = []
        for x in grid:
            s = sum(normal_1d(x, y, 0.5) * dy for y, dy in zip(grid, dens)) * step
            pred.append(p_s * s + 0.1 * normal_1d(x, 0.0, 4.0))
        new = [(1.0 - p_d) * v for v in pred]
        for (z,) in zs:
            g = [p_d * normal_1d(z, x, 0.3) * v for x, v in zip(grid, pred)]
            denom = kap + sum(g) * step
            new = [a + b / denom for a, b in zip(new, g)]
        dens = new
        comps = update(predict(comps, f, q, p_s, birth), zs, h, r, p_d, lambda z: kap)
        gm = [mix_1d(comps, x) for x in grid]
        assert max(abs(a - b) for a, b in zip(gm, dens)) < 1e-6
        assert abs(sum(c[0] for c in comps) - sum(dens) * step) < 1e-6


def test_no_measurements():
    model = cv_model(0.1, 0.25)
    comps = [(0.9, [0.0, 0.0, 1.0, 0.0], [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)])]
    birth = [(0.2, [5.0, 5.0, 0.0, 0.0], [[2.0 if i == j else 0.0 for j in range(4)] for i in range(4)])]
    out = update(predict(comps, model[0], model[1], 0.98, birth), [], model[2], model[3], 0.9, lambda z: 0.01)
    assert abs(sum(c[0] for c in out) - (1 - 0.9) * (0.98 * 0.9 + 0.2)) < 1e-12
    assert out[0][1] == [1.0, 0.0, 1.0, 0.0]


def test_each_measurement_adds_at_most_one_target():
    rng = random.Random(2006)
    f, q, h, r = cv_model(0.1, 0.25)
    for _ in range(20):
        comps = [(rng.uniform(0.1, 1.5), [rng.uniform(-5, 5), rng.uniform(-5, 5), 0.0, 0.0],
                  [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]) for _ in range(4)]
        zs = [[rng.uniform(-6, 6), rng.uniform(-6, 6)] for _ in range(rng.randint(0, 5))]
        kap = rng.uniform(0.001, 0.1)
        out = update(comps, zs, h, r, 0.9, lambda z: kap)
        w = sum(c[0] for c in comps)
        # the weights of one measurement sum to its share p_D Σ w q / (κ + p_D Σ w q) < 1
        per_z = []
        for z in zs:
            s = sum(0.9 * c[0] * gaussian(z, c[1][:2], [[c[2][0][0] + 0.25, c[2][0][1]], [c[2][1][0], c[2][1][1] + 0.25]]) for c in comps)
            per_z.append(s / (kap + s))
        assert all(0.0 <= p < 1.0 for p in per_z)
        assert abs(sum(c[0] for c in out) - ((1 - 0.9) * w + sum(per_z))) < 1e-9


def test_merge_keeps_weight_mean_and_second_moment():
    comps = [(0.6, [0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]), (0.3, [0.5, -0.2], [[0.8, 0.1], [0.1, 1.2]]),
             (0.2, [0.1, 0.4], [[1.0, 0.0], [0.0, 1.0]]), (0.4, [20.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]),
             (1e-7, [5.0, 5.0], [[1.0, 0.0], [0.0, 1.0]])]
    out = prune_and_merge(comps, threshold=1e-5, merge_dist=4.0)
    assert len(out) == 2
    w, m, p = out[0]
    group = comps[:3]
    assert abs(w - 1.1) < 1e-12
    for a in range(2):
        assert abs(m[a] - sum(c[0] * c[1][a] for c in group) / 1.1) < 1e-12
        for b in range(2):
            second = sum(c[0] * (c[2][a][b] + c[1][a] * c[1][b]) for c in group) / 1.1
            assert abs(p[a][b] + m[a] * m[b] - second) < 1e-12
    assert out[1][0] == 0.4 and out[1][1] == [20.0, 0.0]
    n_hat, states = extract(out)
    assert abs(n_hat - 1.5) < 1e-12 and len(states) == 1


def poisson(rng, lam):
    k, p, limit = 0, 1.0, math.exp(-lam)
    while True:
        p *= rng.random()
        if p < limit:
            return k
        k += 1


def test_scene_with_births_deaths_and_clutter():
    rng = random.Random(2003)
    model = cv_model(0.01, 0.25)
    # (birth frame, death frame, start state)
    targets = [(0, 40, [0.0, 0.0, 1.0, 0.5]), (0, 25, [0.0, 20.0, 1.0, -0.3]), (8, 40, [30.0, 0.0, -0.5, 1.0])]
    birth_cov = [[4.0, 0, 0, 0], [0, 4.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0]]
    birth = [(0.05, [x, y, 0.0, 0.0], birth_cov) for x, y in ((0.0, 0.0), (0.0, 20.0), (30.0, 0.0))]
    area, rate = 60.0 * 60.0, 5.0
    kappa = lambda z: rate / area
    comps = []
    good, counted = 0, 0
    for k in range(40):
        zs, truth = [], []
        for i, (b, d, s0) in enumerate(targets):
            if b <= k < d:
                t = k - b
                x = [s0[0] + t * s0[2], s0[1] + t * s0[3]]
                truth.append(x)
                if rng.random() < 0.95:
                    zs.append([x[0] + rng.gauss(0, 0.5), x[1] + rng.gauss(0, 0.5)])
        for _ in range(poisson(rng, rate)):
            zs.append([rng.uniform(-10, 50), rng.uniform(-10, 50)])
        rng.shuffle(zs)
        comps, n_hat, est = phd_step(comps, zs, model, 0.99, 0.95, kappa, birth)
        assert len(comps) <= 100
        if k in (0, 1, 2, 8, 9, 10, 25, 26, 27):
            continue  # a few frames to settle after a birth or a death
        counted += 1
        if len(est) == len(truth) and all(min(math.dist(x, e[:2]) for e in est) < 1.5 for x in truth):
            good += 1
    assert good >= 0.8 * counted
