# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/label-smoothing/. The authors are listed in prov/6Q5BPV.jsonl.

import math
import random
from fractions import Fraction as F

from label_smoothing import (cross_entropy, cross_entropy_bits, ls_grad, ls_loss, optimal_gap, smooth_labels, softmax,
                             train_softmax_regression)


def test_smoothed_target_values() -> None:
    q = smooth_labels(2, 5, F(1, 10))
    assert q == [F(1, 50)] * 2 + [F(46, 50)] + [F(1, 50)] * 2 and sum(q) == 1


def test_loss_decomposition_exactly_in_bits() -> None:
    p = [F(1, 2), F(1, 4), F(1, 8), F(1, 8)]
    k = 4
    u = [F(1, k)] * k
    for eps in [F(0), F(1, 10), F(1, 3), F(1)]:
        for label in range(k):
            y = [F(int(j == label)) for j in range(k)]
            q = smooth_labels(label, k, eps)
            lhs = cross_entropy_bits(q, p)
            assert lhs == (1 - eps) * cross_entropy_bits(y, p) + eps * cross_entropy_bits(u, p)
    assert cross_entropy_bits(u, p) == F(9, 4)
    kl_u_p = sum(F(1, k) * (cross_entropy_bits([1], [pj]) - 2) for pj in p)
    assert kl_u_p == F(1, 4) and cross_entropy_bits(u, p) == kl_u_p + 2


def test_eps_zero_is_cross_entropy() -> None:
    z = [0.3, -1.2, 2.0, 0.0]
    assert math.isclose(ls_loss(z, 1, 0.0), cross_entropy([0, 1, 0, 0], softmax(z)), rel_tol=1e-12)
    assert math.isclose(ls_loss(z, 1, 0.2), cross_entropy(smooth_labels(1, 4, 0.2), softmax(z)), rel_tol=1e-12)


def test_gradient_matches_central_differences() -> None:
    rng = random.Random(0)
    for _ in range(20):
        k = rng.randint(2, 6)
        z = [rng.gauss(0.0, 2.0) for _ in range(k)]
        y, eps = rng.randrange(k), rng.uniform(0.0, 0.5)
        g = ls_grad(z, y, eps)
        assert abs(sum(g)) < 1e-12
        for j in range(k):
            zp, zm = z[:], z[:]
            zp[j] += 1e-6
            zm[j] -= 1e-6
            assert abs((ls_loss(zp, y, eps) - ls_loss(zm, y, eps)) / 2e-6 - g[j]) < 1e-7


def test_minimizer_has_the_finite_optimal_gap() -> None:
    for k, eps in [(3, 0.1), (10, 0.2), (1000, 0.1)]:
        q = smooth_labels(0, k, eps)
        z = [math.log(v) for v in q]
        assert max(abs(v) for v in ls_grad(z, 0, eps)) < 1e-12
        assert math.isclose(z[0] - z[1], optimal_gap(k, eps), rel_tol=1e-12)
        if k <= 10:
            w = [0.0] * k
            for _ in range(3000):
                w = [a - 1.0 * b for a, b in zip(w, ls_grad(w, 0, eps))]
            assert abs((w[0] - w[1]) - optimal_gap(k, eps)) < 1e-6
    assert math.isclose(optimal_gap(1000, 0.1), math.log(9001), rel_tol=1e-12)


def test_the_other_convention_is_a_rescaled_eps() -> None:
    k, eps = 5, F(1, 10)
    other = [1 - eps if j == 3 else eps / (k - 1) for j in range(k)]
    assert other == smooth_labels(3, k, eps * k / (k - 1))


def test_logits_stay_bounded_with_smoothing_and_grow_without() -> None:
    xs = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0], [1.0, 0.2], [0.1, 1.0], [-0.8, -1.2]]
    ys = [0, 1, 2, 0, 1, 2]

    def gaps(w):
        out = []
        for x, y in zip(xs, ys):
            z = [sum(a * b for a, b in zip(r, x)) for r in w]
            out.append(z[y] - max(z[j] for j in range(3) if j != y))
        return out

    ls_short = gaps(train_softmax_regression(xs, ys, 3, 0.1, 0.5, 500))
    ls_long = gaps(train_softmax_regression(xs, ys, 3, 0.1, 0.5, 2000))
    ce_short = gaps(train_softmax_regression(xs, ys, 3, 0.0, 0.5, 500))
    ce_long = gaps(train_softmax_regression(xs, ys, 3, 0.0, 0.5, 2000))
    assert max(abs(a - b) for a, b in zip(ls_short, ls_long)) < 0.05
    assert max(ls_long) < optimal_gap(3, 0.1) + 0.1
    assert min(b - a for a, b in zip(ce_short, ce_long)) > 0.5
