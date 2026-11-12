# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadly-triad/. The authors are listed in prov/4D15PJ.jsonl.

import math
from fractions import Fraction as F

from deadly_triad import (
    baird_example,
    expected_update,
    projected_value_iteration,
    true_values,
    tvr_example,
    w_to_2w_factor,
)

G = F(99, 100)


def fl(m):
    return [[float(x) for x in row] for row in m]


def test_w_to_2w() -> None:
    assert w_to_2w_factor(F(9, 10), F(1, 10)) == F(108, 100)
    assert w_to_2w_factor(F(1, 2), F(1, 10)) == 1
    assert w_to_2w_factor(F(2, 5), F(1, 10)) < 1
    # The same factor from the general expected update with all weight on the first state.
    f, p, r = [[F(1)], [F(2)]], [[F(0), F(1)], [F(0), F(0)]], [F(0), F(0)]
    w = expected_update(f, p, r, F(9, 10), [F(1), F(0)], [F(3)], F(1, 10))
    assert w == [F(3) * F(108, 100)]


def test_tvr_projected_value_iteration_diverges_exactly() -> None:
    eps = F(1, 10)
    f, p, r = tvr_example(eps)
    ws = projected_value_iteration(f, p, r, G, [F(1, 2), F(1, 2)], [F(1)], 6)
    factor = G * (6 - 4 * eps) / 5
    assert factor == F(693, 625) and factor > 1
    assert all(ws[k] == [factor**k] for k in range(7))
    assert true_values(p, r, G) == [0, 0]


def test_tvr_on_policy_weighting_converges_exactly() -> None:
    eps = F(1, 10)
    f, p, r = tvr_example(eps)
    d = [eps / (1 + eps), 1 / (1 + eps)]  # visits per episode: 1 and 1/eps
    w = [F(1)]
    for g in (F(1, 2), F(9, 10), G):
        w1 = expected_update(f, p, r, g, d, w, F(1))
        coeff = (w1[0] - 1) * (1 + eps)
        assert coeff == -(4 * (1 - g) + eps * (1 + 2 * g)) and coeff < 0


def test_baird_expected_update_diverges() -> None:
    feats, p, r = baird_example()
    w = [1.0] * 6 + [10.0, 1.0]
    for _ in range(2000):
        w = expected_update(fl(feats), fl(p), [0.0] * 7, 0.99, [1 / 7] * 7, w, 0.01)
    assert math.hypot(*w) > 5000


def test_baird_without_function_approximation_converges() -> None:
    _, p, _ = baird_example()
    eye = [[1.0 if i == j else 0.0 for j in range(7)] for i in range(7)]
    w = [1.0] * 6 + [12.0]
    for _ in range(8000):
        w = expected_update(eye, fl(p), [0.0] * 7, 0.99, [1 / 7] * 7, w, 1.0)
    assert max(abs(x) for x in w) < 1e-3


def test_baird_without_bootstrapping_converges() -> None:
    feats, p, _ = baird_example()
    w = [1.0] * 6 + [10.0, 1.0]
    for _ in range(3000):
        w = expected_update(fl(feats), fl(p), [0.0] * 7, 0.99, [1 / 7] * 7, w, 0.1, [0.0] * 7)
    assert max(abs(sum(a * b for a, b in zip(x, w))) for x in fl(feats)) < 1e-9
    assert math.hypot(*w) < 11


def test_baird_on_policy_weighting_converges() -> None:
    feats, p, _ = baird_example()
    w = [1.0] * 6 + [10.0, 1.0]
    for _ in range(5000):
        w = expected_update(fl(feats), fl(p), [0.0] * 7, 0.99, [0.0] * 6 + [1.0], w, 0.1)
    assert abs(sum(a * b for a, b in zip(fl(feats)[6], w))) < 1e-6 and math.hypot(*w) < 11
