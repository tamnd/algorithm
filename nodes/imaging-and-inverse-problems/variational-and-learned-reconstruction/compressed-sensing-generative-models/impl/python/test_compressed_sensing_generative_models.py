# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compressed-sensing-generative-models/. The authors are listed in prov/ZV36YT.jsonl.

import math
import random

from compressed_sensing_generative_models import (
    csgm,
    gaussian_matrix,
    loss,
    loss_grad,
    matvec,
    tanh_generator,
)


def seeded_problem(seed, n=20, k=2, m=5):
    rng = random.Random(seed)
    w = [[rng.gauss(0.0, 1.0 / math.sqrt(k)) for _ in range(k)] for _ in range(n)]
    b = [rng.gauss(0.0, 0.1) for _ in range(n)]
    gen, vjp = tanh_generator(w, b)
    a = gaussian_matrix(rng, m, n)
    z_true = [rng.gauss(0.0, 1.0) for _ in range(k)]
    x_true = gen(z_true)
    starts = [[rng.gauss(0.0, 1.0) for _ in range(k)] for _ in range(4)]
    return a, gen, vjp, x_true, matvec(a, x_true), starts


def test_generator_jacobian_matches_finite_differences():
    rng = random.Random(4)
    n, k = 8, 3
    w = [[rng.gauss(0.0, 1.0) for _ in range(k)] for _ in range(n)]
    b = [rng.gauss(0.0, 0.5) for _ in range(n)]
    gen, vjp = tanh_generator(w, b)
    z = [rng.gauss(0.0, 1.0) for _ in range(k)]
    v = [rng.gauss(0.0, 1.0) for _ in range(n)]
    g = vjp(z, v)
    h = 1e-6
    for j in range(k):
        zp, zm = list(z), list(z)
        zp[j] += h
        zm[j] -= h
        fd = sum(vi * (p - q) for vi, p, q in zip(v, gen(zp), gen(zm))) / (2 * h)
        assert abs(fd - g[j]) < 1e-7


def test_loss_gradient_matches_finite_differences():
    a, gen, vjp, _, y, _ = seeded_problem(9, n=10, k=3, m=4)
    z = [0.3, -0.7, 1.1]
    g = loss_grad(a, y, gen, vjp, z, 0.1)
    h = 1e-6
    for j in range(3):
        zp, zm = list(z), list(z)
        zp[j] += h
        zm[j] -= h
        fd = (loss(a, y, gen, zp, 0.1) - loss(a, y, gen, zm, 0.1)) / (2 * h)
        assert abs(fd - g[j]) < 1e-6


def test_one_measurement_of_a_curve():
    gen, vjp = tanh_generator([[1.0], [2.0]], [0.0, 0.0])
    a = [[1.0, 1.0]]
    y = [math.tanh(0.5) + math.tanh(1.0)]
    assert abs(y[0] - 1.2237113) < 1e-7
    x1, z1, _ = csgm(a, y, gen, vjp, [[0.0]], 0.1, 1)
    assert abs(z1[0] - 0.734227) < 1e-6
    x, z, val = csgm(a, y, gen, vjp, [[0.0]], 0.1, 40)
    assert abs(z[0] - 0.5) < 1e-9 and val < 1e-18
    assert abs(x[0] - math.tanh(0.5)) < 1e-9 and abs(x[1] - math.tanh(1.0)) < 1e-9


def test_a_bad_measurement_has_two_answers():
    gen, vjp = tanh_generator([[1.0], [2.0]], [0.0, 0.0])
    a = [[1.0, -1.0]]
    y = [-0.2]
    xa, za, la = csgm(a, y, gen, vjp, [[0.1]], 0.2, 3000)
    xb, zb, lb = csgm(a, y, gen, vjp, [[2.0]], 0.2, 3000)
    assert la < 1e-16 and lb < 1e-16
    assert abs(za[0] - 0.224106) < 1e-5 and abs(zb[0] - 1.008746) < 1e-5
    assert math.dist(xa, xb) > 0.6


def test_grid_search_agrees_for_one_latent_variable():
    rng = random.Random(12)
    n, m = 12, 3
    w = [[rng.gauss(0.0, 1.0)] for _ in range(n)]
    b = [rng.gauss(0.0, 0.2) for _ in range(n)]
    gen, vjp = tanh_generator(w, b)
    a = gaussian_matrix(rng, m, n)
    y = [v + rng.gauss(0.0, 0.05) for v in matvec(a, gen([0.8]))]
    lam = 0.01
    grid = [-3.0 + i * 0.0005 for i in range(12001)]
    best = min(grid, key=lambda t: loss(a, y, gen, [t], lam))
    starts = [[-2.0], [-0.5], [0.5], [2.0]]
    _, z, val = csgm(a, y, gen, vjp, starts, 0.02, 2000, lam)
    assert val <= loss(a, y, gen, [best], lam) + 1e-9
    assert abs(z[0] - best) < 1e-3


def test_recovery_from_fewer_measurements_than_unknowns():
    for seed in (1, 2, 3, 4):
        a, gen, vjp, x_true, y, starts = seeded_problem(seed)
        x, _, val = csgm(a, y, gen, vjp, starts[:3], 0.02, 800)
        assert val < 1e-12
        assert math.dist(x, x_true) < 1e-6


def test_bad_starts_and_restarts():
    a, gen, vjp, x_true, y, starts = seeded_problem(5)
    # Without the penalty this start runs off to where tanh saturates.
    x_bad, z_bad, val_bad = csgm(a, y, gen, vjp, [starts[1]], 0.02, 800)
    assert val_bad > 19.0 and abs(z_bad[0]) > 10.0
    assert math.dist(x_bad, x_true) > 1.0
    # With lam = 0.1 it stops at a spurious stationary point.
    _, z_loc, val_loc = csgm(a, y, gen, vjp, [starts[1]], 0.02, 3000, 0.1)
    assert val_loc > 20.0 and math.hypot(*loss_grad(a, y, gen, vjp, z_loc, 0.1)) < 1e-8
    # The best of four starts finds the true code.
    x, _, val = csgm(a, y, gen, vjp, starts, 0.02, 800)
    assert val < 1e-12 and math.dist(x, x_true) < 1e-6
