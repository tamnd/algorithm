# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilevel-learning-of-regularizers/. The authors are listed in prov/VE2JDY.jsonl.

import random

from bilevel_learning_of_regularizers import bilevel_learn, tikhonov, upper_loss


def seeded_pairs(seed, m=5, n=4, count=4, noise=0.5):
    rng = random.Random(seed)
    a = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(m)]
    pairs = []
    for _ in range(count):
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        y = [sum(a[r][j] * x[j] for j in range(n)) + rng.gauss(0.0, noise)
             for r in range(m)]
        pairs.append((x, y))
    return a, pairs


def upper_gradient(pairs, lower, lower_vjp, alpha):
    g = 0.0
    for x_true, y in pairs:
        x = lower(alpha, y)
        g += 2.0 * lower_vjp(alpha, y, x, [p - q for p, q in zip(x, x_true)])
    return g / len(pairs)


def test_hand_example():
    lower, vjp = tikhonov([[1.0]])
    pairs = [([1.0], [1.2])]
    assert abs(lower(1.0, [1.2])[0] - 0.6) < 1e-15
    assert abs(upper_loss(pairs, lower, 1.0) - 0.16) < 1e-15
    assert abs(upper_gradient(pairs, lower, vjp, 1.0) - 0.24) < 1e-15
    alpha, losses = bilevel_learn(pairs, lower, vjp, 1.0, 0.5, 60)
    assert abs(alpha - 0.2) < 1e-10 and losses[-1] < 1e-18


def test_projection_keeps_alpha_nonnegative():
    lower, vjp = tikhonov([[1.0]])
    alpha, losses = bilevel_learn([([1.0], [0.8])], lower, vjp, 1.0, 0.5, 60)
    assert alpha == 0.0 and abs(losses[-1] - 0.04) < 1e-12


def test_adjoint_gradient_matches_finite_differences():
    a, pairs = seeded_pairs(5)
    lower, vjp = tikhonov(a)
    h = 1e-6
    for alpha in (0.05, 0.4, 2.0):
        fd = (upper_loss(pairs, lower, alpha + h) - upper_loss(pairs, lower, alpha - h)) / (2 * h)
        assert abs(fd - upper_gradient(pairs, lower, vjp, alpha)) < 1e-8


def test_learned_weight_matches_a_grid_search():
    a, pairs = seeded_pairs(5)
    lower, vjp = tikhonov(a)
    alpha, losses = bilevel_learn(pairs, lower, vjp, 1.0, 0.5, 300)
    assert all(l2 <= l1 + 1e-15 for l1, l2 in zip(losses, losses[1:]))
    assert abs(upper_gradient(pairs, lower, vjp, alpha)) < 1e-9
    best = min((upper_loss(pairs, lower, k / 1000), k / 1000) for k in range(0, 2001))
    assert abs(alpha - best[1]) < 1e-3 and upper_loss(pairs, lower, alpha) <= best[0] + 1e-15
    assert abs(alpha - 0.36527) < 1e-5


def test_many_scalar_pairs_give_the_noise_to_signal_ratio():
    rng = random.Random(6)
    pairs = []
    for _ in range(2000):
        x = rng.gauss(0.0, 1.0)
        pairs.append(([x], [x + rng.gauss(0.0, 0.5)]))

    def lower(alpha, y):  # Tikhonov with A = 1, written by hand
        return [y[0] / (1.0 + alpha)]

    def vjp(alpha, y, x, v):
        return -x[0] * v[0] / (1.0 + alpha)

    alpha, _ = bilevel_learn(pairs, lower, vjp, 1.0, 1.0, 100)
    sxy = sum(x[0] * y[0] for x, y in pairs)
    syy = sum(y[0] * y[0] for _, y in pairs)
    assert abs(alpha - (syy / sxy - 1.0)) < 1e-9  # the exact minimizer
    assert abs(alpha - 0.25) < 0.05  # sigma^2 / sigma_x^2 for large N
    assert abs(lower(0.3, [0.7])[0] - tikhonov([[1.0]])[0](0.3, [0.7])[0]) < 1e-15
