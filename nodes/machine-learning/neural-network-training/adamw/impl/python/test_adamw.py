# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adamw/. The authors are listed in prov/P87340.jsonl.

import math
import random
from fractions import Fraction as F

from adamw import (
    adam_l2,
    adam_l2_step,
    adamw,
    adamw_step,
    new_state,
    sgd_l2_step,
    sgd_momentum_l2_step,
    sgdw_momentum_step,
    sgdw_step,
)

CONST = lambda th, t: [1.0, 0.0]


def close(a, b, tol=1e-9):
    return all(math.isclose(x, y, rel_tol=0, abs_tol=tol) for x, y in zip(a, b))


def test_first_step_by_hand() -> None:
    # theta = (1, 1), data gradient (1, 0), alpha = 0.01.
    th = adamw_step([1.0, 1.0], [1.0, 0.0], new_state(2), alpha=0.01, lam=0.001)
    assert close(th, [1 - 0.01 - 0.001, 1 - 0.001])
    th = adam_l2_step([1.0, 1.0], [1.0, 0.0], new_state(2), alpha=0.01, lam=0.1)
    # Adam normalizes g + lam * theta = (1.1, 0.1), so each coordinate moves by alpha.
    assert close(th, [0.99, 0.99], 1e-7)


def test_two_parameter_example_differs() -> None:
    a = adamw(CONST, [1.0, 1.0], 5, alpha=0.01, lam=0.001)
    b = adam_l2(CONST, [1.0, 1.0], 5, alpha=0.01, lam=0.1)
    assert close(a[5], [0.94511, 0.99501], 1e-5)
    assert close(b[5], [0.950004, 0.950046], 1e-5)
    # The weight with zero data gradient decays geometrically under AdamW.
    a = adamw(CONST, [1.0, 1.0], 100, alpha=0.01, lam=0.001)
    assert math.isclose(a[100][1], 0.999 ** 100, rel_tol=1e-12)
    b = adam_l2(CONST, [1.0, 1.0], 100, alpha=0.01, lam=0.1)
    assert b[100][1] < 0.25 < 0.9 < a[100][1]


def test_no_l2_coefficient_matches_adamw() -> None:
    # The first AdamW step is (alpha + lam, lam); every L2 run moves both
    # coordinates by alpha (lam2 > 0) or the second by 0 (lam2 = 0).
    target = adamw_step([1.0, 1.0], [1.0, 0.0], new_state(2), alpha=0.01, lam=0.001)
    for lam2 in [0.0, 1e-4, 1e-3, 0.01, 0.1, 1.0, 10.0]:
        th = adam_l2_step([1.0, 1.0], [1.0, 0.0], new_state(2), alpha=0.01, lam=lam2)
        assert not close(th, target, 1e-6)


def test_zero_decay_gives_the_same_adam() -> None:
    rng = random.Random(3)
    grad = lambda th, t: [rng.gauss(0, 1) + x for x in th]
    rng.seed(3)
    a = adamw(grad, [0.5, -1.0, 2.0], 20, alpha=0.1, lam=0.0)
    rng.seed(3)
    b = adam_l2(grad, [0.5, -1.0, 2.0], 20, alpha=0.1, lam=0.0)
    assert a == b


def test_sgd_equivalence_exact() -> None:
    # Proposition 1: SGD with L2 coefficient lam2 equals SGDW with lam = alpha * lam2.
    rng = random.Random(7)
    alpha, lam2 = F(1, 10), F(3, 10)
    th1 = [F(rng.randint(-9, 9), 4) for _ in range(4)]
    th2 = list(th1)
    for _ in range(10):
        g = [F(rng.randint(-9, 9), 8) for _ in range(4)]
        th1 = sgd_l2_step(th1, g, alpha, lam2)
        th2 = sgdw_step(th2, g, alpha, alpha * lam2)
        assert th1 == th2


def test_momentum_breaks_the_equivalence() -> None:
    g = [F(1, 2), F(-1)]
    th1, th2 = [F(1), F(2)], [F(1), F(2)]
    b1, b2 = [F(0)] * 2, [F(0)] * 2
    th1 = sgd_momentum_l2_step(th1, g, b1, F(1, 10), F(9, 10), F(1, 10))
    th2 = sgdw_momentum_step(th2, g, b2, F(1, 10), F(9, 10), F(1, 100))
    assert th1 == th2 == [F(47, 50), F(52, 25)]
    th1 = sgd_momentum_l2_step(th1, g, b1, F(1, 10), F(9, 10), F(1, 10))
    th2 = sgdw_momentum_step(th2, g, b2, F(1, 10), F(9, 10), F(1, 100))
    assert th1 == [F(4133, 5000), F(2789, 1250)]
    assert th2 == [F(2089, 2500), F(5623, 2500)]


def test_schedule_scales_the_decay() -> None:
    a = adamw(lambda th, t: [0.0], [1.0], 4, alpha=0.01, lam=0.1, schedule=lambda t: 0.5)
    assert math.isclose(a[4][0], 0.95 ** 4, rel_tol=1e-12)


def test_trains_least_squares() -> None:
    # Fit y = 2 x0 - x1 with a small decay; the result stays near the
    # least squares solution, shrunk a little toward zero.
    rng = random.Random(0)
    data = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(32)]
    ys = [2 * a - b for a, b in data]

    def grad(th, t):
        g = [0.0, 0.0]
        for (a, b), y in zip(data, ys):
            r = th[0] * a + th[1] * b - y
            g[0] += 2 * r * a / len(data)
            g[1] += 2 * r * b / len(data)
        return g

    th = adamw(grad, [0.0, 0.0], 3000, alpha=0.01, lam=1e-4)[-1]
    assert abs(th[0] - 2) < 0.05 and abs(th[1] + 1) < 0.05
