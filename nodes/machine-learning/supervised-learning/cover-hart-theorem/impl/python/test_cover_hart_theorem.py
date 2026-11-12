# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cover-hart-theorem/. The authors are listed in prov/B8ZFXM.jsonl.

import random
from fractions import Fraction as F

from cover_hart_theorem import (
    bayes_risk,
    cover_hart_upper,
    nn_asymptotic_risk,
    one_nn_error_uniform,
    one_nn_risk_finite,
)

EXAMPLE = [
    (F(1, 3), (F(7, 10), F(2, 10), F(1, 10))),
    (F(1, 3), (F(2, 10), F(6, 10), F(2, 10))),
    (F(1, 3), (F(1, 3), F(1, 3), F(1, 3))),
]


def random_finite(rng: random.Random, atoms: int, m: int):
    ps = [F(rng.randrange(1, 10)) for _ in range(atoms)]
    total = sum(ps)
    dist = []
    for p in ps:
        raw = [F(rng.randrange(0, 6)) for _ in range(m)]
        if sum(raw) == 0:
            raw[0] = F(1)
        s = sum(raw)
        dist.append((p / total, tuple(r / s for r in raw)))
    return dist


def test_worked_example() -> None:
    assert bayes_risk(EXAMPLE) == F(41, 90)
    assert nn_asymptotic_risk(EXAMPLE) == F(253, 450)
    assert cover_hart_upper(F(41, 90), 3) == F(3239, 5400)


def test_bound_holds_exactly_on_random_distributions() -> None:
    rng = random.Random(11)
    for _ in range(2000):
        m = rng.randrange(2, 6)
        dist = random_finite(rng, rng.randrange(1, 6), m)
        rs, r = bayes_risk(dist), nn_asymptotic_risk(dist)
        assert 0 <= rs <= F(m - 1, m)
        assert rs <= r <= cover_hart_upper(rs, m) <= 2 * rs


def test_two_class_identity() -> None:
    rng = random.Random(12)
    for _ in range(500):
        dist = random_finite(rng, rng.randrange(1, 6), 2)
        second = sum((p * (1 - max(eta)) ** 2 for p, eta in dist), F(0))
        assert nn_asymptotic_risk(dist) == 2 * bayes_risk(dist) - 2 * second


def test_upper_bound_is_attained() -> None:
    for m in range(2, 6):
        for rs in (F(0), F(1, 10), F(1, 4), F(m - 1, m)):
            eta = (1 - rs,) + tuple(rs / (m - 1) for _ in range(m - 1))
            dist = [(F(1), eta)]
            assert bayes_risk(dist) == rs
            assert nn_asymptotic_risk(dist) == cover_hart_upper(rs, m)


def test_lower_bound_is_attained() -> None:
    # Half the mass is noise free, half is uniform over three classes.
    dist = [(F(1, 2), (F(1), F(0), F(0))), (F(1, 2), (F(1, 3), F(1, 3), F(1, 3)))]
    assert bayes_risk(dist) == nn_asymptotic_risk(dist) == F(1, 3)


def test_simulation_uniform_eta_equals_x() -> None:
    # R* = 1/4, R = 1/3, upper bound 2 R*(1 - R*) = 3/8.
    rng = random.Random(1)
    errs = [one_nn_error_uniform(10000, 20000, rng) for _ in range(5)]
    mean = sum(errs) / len(errs)
    assert abs(mean - 1 / 3) < 0.01
    assert 0.25 < mean < 0.375


def test_simulation_finite_three_classes() -> None:
    rng = random.Random(2)
    risks = [one_nn_risk_finite(EXAMPLE, 50, rng) for _ in range(4000)]
    mean = float(sum(risks)) / len(risks)
    assert abs(mean - 253 / 450) < 0.01
