# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-entropy-loss/. The authors are listed in prov/0EGAS8.jsonl.

import math
import random

from cross_entropy_loss import (cross_entropy, cross_entropy_grad, cross_entropy_soft, entropy, kl_divergence,
                                log_sum_exp, mean_cross_entropy, one_hot, softmax)


def naive_loss(z, y):
    e = [math.exp(v) for v in z]
    return -math.log(e[y] / sum(e))


def test_worked_example() -> None:
    z = [2.0, 1.0, 0.1]
    assert abs(log_sum_exp(z) - 2.41703) < 1e-5
    p = softmax(z)
    assert [round(v, 4) for v in p] == [0.659, 0.2424, 0.0986]
    assert abs(cross_entropy(z, 0) - 0.41703) < 1e-5
    assert abs(cross_entropy(z, 2) - 2.31703) < 1e-5
    g = cross_entropy_grad(z, one_hot(0, 3))
    assert [round(v, 4) for v in g] == [-0.341, 0.2424, 0.0986]


def test_matches_naive_formula_on_small_scores() -> None:
    r = random.Random(11)
    for _ in range(500):
        k = r.randint(1, 6)
        z = [r.uniform(-5, 5) for _ in range(k)]
        y = r.randrange(k)
        assert abs(cross_entropy(z, y) - naive_loss(z, y)) < 1e-9


def test_large_scores_do_not_overflow() -> None:
    assert cross_entropy([1000.0, 0.0], 0) == 0.0
    assert cross_entropy([1000.0, 0.0], 1) == 1000.0
    assert abs(cross_entropy([-1000.0, -1000.0], 0) - math.log(2)) < 1e-12
    assert softmax([1000.0, 1000.0]) == [0.5, 0.5]


def test_shift_invariance() -> None:
    z = [0.3, -1.2, 2.5]
    for c in (-100.0, 0.0, 50.0):
        assert abs(cross_entropy([v + c for v in z], 1) - cross_entropy(z, 1)) < 1e-9


def test_gradient_is_p_minus_y_by_finite_differences() -> None:
    r = random.Random(5)
    h = 1e-6
    for _ in range(200):
        k = r.randint(2, 5)
        z = [r.uniform(-3, 3) for _ in range(k)]
        raw = [r.random() for _ in range(k)]
        q = [v / sum(raw) for v in raw]
        g = cross_entropy_grad(z, q)
        for j in range(k):
            zp = z[:]
            zm = z[:]
            zp[j] += h
            zm[j] -= h
            fd = (cross_entropy_soft(zp, q) - cross_entropy_soft(zm, q)) / (2 * h)
            assert abs(fd - g[j]) < 1e-6
        assert abs(sum(g)) < 1e-12


def test_cross_entropy_is_entropy_plus_kl() -> None:
    r = random.Random(8)
    for _ in range(300):
        k = r.randint(2, 5)
        z = [r.uniform(-3, 3) for _ in range(k)]
        raw = [r.random() for _ in range(k)]
        q = [v / sum(raw) for v in raw]
        p = softmax(z)
        assert abs(cross_entropy_soft(z, q) - (entropy(q) + kl_divergence(q, p))) < 1e-9
        assert kl_divergence(q, p) >= -1e-12


def test_one_hot_target_and_mean() -> None:
    z = [[2.0, 1.0, 0.1], [0.0, 0.0, 0.0]]
    assert abs(cross_entropy_soft(z[0], one_hot(0, 3)) - cross_entropy(z[0], 0)) < 1e-12
    assert abs(mean_cross_entropy(z, [0, 2]) - (0.41703 + math.log(3)) / 2) < 1e-5
