# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magsac/. The authors are listed in prov/RA0N0V.jsonl.

import math
import random

from magsac import (K_CHI2_99, fit_affine_minimal, fit_affine_weighted, magsac_loss, magsac_pp,
                    magsac_weight, residual, sigma_consensus_pp, total_loss)

EXAMPLE = [((0, 0), (1, 0.1)), ((1, 0), (2, 0)), ((0, 1), (1, 1)), ((1, 1), (2.1, 1)), ((2, 1), (3, 1)),
           ((2, 2), (5, -1)), ((0, 2), (-2, 4))]


def simpson(f, a, b, m=2000):
    h = (b - a) / m
    acc = f(a) + f(b)
    for i in range(1, m):
        acc += (4 if i % 2 else 2) * f(a + i * h)
    return acc * h / 3.0


def apply(model, p):
    a11, a12, b1, a21, a22, b2 = model
    return (a11 * p[0] + a12 * p[1] + b1, a21 * p[0] + a22 * p[1] + b2)


def planted(rng, n_in, n_out, sigma):
    true = (1.1, 0.2, 2.0, -0.1, 0.9, -1.0)
    data = []
    for _ in range(n_in):
        p = (rng.uniform(0, 10), rng.uniform(0, 10))
        q = apply(true, p)
        data.append((p, (q[0] + rng.gauss(0, sigma), q[1] + rng.gauss(0, sigma))))
    for _ in range(n_out):
        p = (rng.uniform(0, 10), rng.uniform(0, 10))
        data.append((p, (rng.uniform(-5, 20), rng.uniform(-5, 20))))
    rng.shuffle(data)
    return data, true


def test_weight_is_marginal_density():
    # w(r) = (1/sigma_max) * integral over sigma in [r/k, sigma_max] of the chi(2) density r/sigma^2 exp(-r^2/2sigma^2)
    for sm in (0.5, 1.0, 2.0):
        for frac in (0.05, 0.2, 0.5, 0.9):
            r = frac * K_CHI2_99 * sm
            num = simpson(lambda s: r / (s * s) * math.exp(-r * r / (2 * s * s)) / sm, r / K_CHI2_99, sm)
            assert abs(magsac_weight(r, sm) - num) < 1e-7
        assert magsac_weight(K_CHI2_99 * sm, sm) == 0.0 and magsac_weight(10 * sm, sm) == 0.0


def test_loss_is_integral_of_x_w():
    for sm in (0.5, 1.0):
        top = K_CHI2_99 * sm
        for r in (0.1, 0.5, 1.0, 1.4, top):
            r = min(r, top)
            num = simpson(lambda x: x * magsac_weight(x, sm), 0.0, r)
            assert abs(magsac_loss(r, sm) - num) < 1e-8
        assert abs(magsac_loss(0.0, sm)) < 1e-15
        assert magsac_loss(5 * top, sm) == magsac_loss(top, sm)
    # the constant beyond k sigma_max, sigma_max C(2) sqrt(2) gamma(3/2, k^2/2)
    x = K_CHI2_99 ** 2 / 2
    g32 = 0.5 * math.sqrt(math.pi) * math.erf(math.sqrt(x)) - math.sqrt(x) * math.exp(-x)
    assert abs(magsac_loss(100.0, 1.0) - 0.5 * math.sqrt(2) * g32) < 1e-12
    assert abs(magsac_loss(100.0, 1.0) - 0.609975) < 1e-6


def test_weights_decrease_and_loss_increases():
    sm = 1.0
    rs = [i * 0.01 for i in range(400)]
    ws = [magsac_weight(r, sm) for r in rs]
    ls = [magsac_loss(r, sm) for r in rs]
    assert all(a >= b for a, b in zip(ws, ws[1:]))
    assert all(a <= b + 1e-15 for a, b in zip(ls, ls[1:]))


def test_example_values():
    sm = 0.5
    th = fit_affine_minimal(EXAMPLE[:3])
    assert all(abs(a - b) < 1e-12 for a, b in zip(th, (1.0, 0.0, 1.0, -0.1, 0.9, 0.1)))
    assert abs(total_loss(th, EXAMPLE, sm) - 0.6708) < 1e-4
    assert abs(total_loss(fit_affine_minimal([EXAMPLE[i] for i in (0, 4, 5)]), EXAMPLE, sm) - 1.2199) < 1e-4
    assert abs(total_loss(fit_affine_minimal([EXAMPLE[i] for i in (0, 1, 3)]), EXAMPLE, sm) - 0.6525) < 1e-4
    pol = sigma_consensus_pp(th, EXAMPLE, sm, iters=5)
    assert abs(total_loss(pol, EXAMPLE, sm) - 0.62259) < 1e-5
    assert all(abs(a - b) < 1e-3 for a, b in zip(pol, (1.0, 0.0322, 1.0, -0.0199, 0.96, 0.06)))
    for seed in range(4):
        model, loss, t = magsac_pp(EXAMPLE, sm, random.Random(seed))
        assert abs(loss - 0.62259) < 1e-5 and t == 11


def test_irls_never_increases_loss():
    for seed in range(5):
        rng = random.Random(seed)
        data, _ = planted(rng, 40, 30, 0.3)
        sm = 1.0
        for _ in range(10):
            th = fit_affine_minimal(rng.sample(data, 3))
            if th is None:
                continue
            prev = total_loss(th, data, sm)
            w = [magsac_weight(residual(th, x), sm) for x in data]
            if sum(1 for v in w if v > 0) < 3:
                continue
            for _ in range(6):
                nxt = sigma_consensus_pp(th, data, sm, iters=1)
                cur = total_loss(nxt, data, sm)
                assert cur <= prev + 1e-9
                th, prev = nxt, cur


def test_invariant_best_of_sampled():
    data, _ = planted(random.Random(3), 50, 50, 0.3)
    seen = []
    model, loss, t = magsac_pp(data, 1.0, random.Random(7), on_model=lambda th, q: seen.append(q))
    assert loss <= min(seen) + 1e-12
    assert abs(total_loss(model, data, 1.0) - loss) < 1e-9
    assert 1 <= t <= 2000


def test_planted_affine():
    for seed in range(3):
        data, true = planted(random.Random(20 + seed), 60, 40, 0.3)
        model, _, _ = magsac_pp(data, 1.0, random.Random(seed))
        for p in ((0, 0), (10, 0), (0, 10), (10, 10)):
            a, b = apply(model, p), apply(true, p)
            assert math.hypot(a[0] - b[0], a[1] - b[1]) < 0.5


def test_weighted_fit_exact_and_degenerate():
    true = (2.0, -1.0, 0.5, 0.3, 1.5, -2.0)
    pairs = [((x, y), apply(true, (x, y))) for x, y in ((0, 0), (1, 0), (0, 1), (2, 3), (5, 1))]
    got = fit_affine_weighted(pairs, [1.0, 2.0, 0.5, 1.0, 3.0])
    assert all(abs(a - b) < 1e-9 for a, b in zip(got, true))
    assert fit_affine_minimal([((0, 0), (0, 0)), ((1, 1), (1, 1)), ((2, 2), (3, 3))]) is None
    assert magsac_pp(EXAMPLE[:2], 0.5, random.Random(0)) == (None, math.inf, 0)
