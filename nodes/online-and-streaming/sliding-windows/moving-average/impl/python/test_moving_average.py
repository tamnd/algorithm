# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moving-average/. The authors are listed in prov/G6SM48.jsonl.

import random
import sys
from fractions import Fraction

import pytest

from moving_average import (
    MovingAverage,
    integer_moving_sums,
    moving_averages,
    weighted_moving_sums,
)

U = sys.float_info.epsilon / 2  # unit roundoff of binary64


def exact_avgs(xs, w):
    out = []
    for t in range(len(xs)):
        win = xs[max(0, t - w + 1): t + 1]
        out.append(sum(Fraction(x) for x in win) / len(win))
    return out


def test_page_example():
    xs = [4, 8, 6, 2, 10, 7]
    assert list(moving_averages(xs, 3)) == [4, 6, 6, 16 / 3, 6, 19 / 3]


def test_drift_example():
    xs = [1e16] + [1.0] * 20
    naive = list(moving_averages(xs, 2, compensated=False))
    assert naive[2:] == [0.0] * 19  # the true average is 1 from step 3 on
    comp = list(moving_averages(xs, 2))
    assert comp[2:] == [1.0] * 19
    fixed = list(moving_averages(xs, 2, compensated=False, recompute=2))
    assert fixed[2] == 0.0 and fixed[3] == 1.0  # wrong until the next recomputation
    assert all(v == 1.0 for v in fixed[3:])


@pytest.mark.parametrize("w", [1, 2, 5, 16])
def test_integers_exact(w):
    rng = random.Random(w)
    for _ in range(40):
        xs = [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 100))]
        assert list(moving_averages(xs, w, compensated=False)) == [float(v) for v in exact_avgs(xs, w)]
        sums = [sum(xs[max(0, t - w + 1): t + 1]) for t in range(len(xs))]
        assert list(integer_moving_sums(xs, w)) == sums


def test_wrapping_integers_exact_after_overflow():
    big = 2 ** 62
    xs = [big, big - 1, big, -big, -big, 5]
    sums = [sum(xs[max(0, t - 1): t + 1]) for t in range(len(xs))]
    assert all(-(2 ** 63) <= s < 2 ** 63 for s in sums)
    # At step 3 the partial sum (2**63 - 1) + 2**62 overflows a 64-bit word.
    assert list(integer_moving_sums(xs, 2)) == sums


def test_compensated_error_bound_on_random_floats():
    rng = random.Random(3)
    w = 50
    xs = [rng.choice([1e8, 1.0, 1e-3]) * rng.uniform(-1, 1) for _ in range(3000)]
    exact = exact_avgs(xs, w)
    abs_total = Fraction(0)
    worst_comp = worst_naive = 0.0
    m_comp = MovingAverage(w)
    m_naive = MovingAverage(w, compensated=False)
    for t, x in enumerate(xs):
        abs_total += abs(Fraction(x)) * (2 if t >= w else 1)
        m = min(t + 1, w)
        n_terms = 2 * (t + 1) - m
        true_sum = exact[t] * m
        err_comp = abs(Fraction(m_comp.step(x)) * m - true_sum)
        err_naive = abs(Fraction(m_naive.step(x)) * m - true_sum)
        # Neumaier: |error| <= 2u|S| + 2 m u^2 sum|terms|, plus the final rounding of s + c.
        bound = 3 * U * abs(true_sum) + 2 * n_terms * U * U * abs_total + U * abs(true_sum)
        assert err_comp <= bound + Fraction(1, 10 ** 30)
        worst_comp = max(worst_comp, float(err_comp))
        worst_naive = max(worst_naive, float(err_naive))
    assert worst_comp < worst_naive


def test_recompute_matches_fsum():
    rng = random.Random(9)
    xs = [rng.uniform(-1e6, 1e6) for _ in range(500)]
    m = MovingAverage(7, compensated=False, recompute=7)
    for t, x in enumerate(xs):
        v = m.step(x)
        if (t + 1) % 7 == 0:
            win = xs[max(0, t - 6): t + 1]
            assert v == float(sum(Fraction(y) for y in win)) / len(win)


def test_weighted_moving_sums():
    rng = random.Random(4)
    for w in [1, 2, 3, 6]:
        xs = [rng.randint(-9, 9) for _ in range(60)]
        got = list(weighted_moving_sums(xs, w))
        for t in range(len(xs)):
            want = sum((w - j) * xs[t - j] for j in range(min(t + 1, w)))
            assert got[t] == want


def test_bad_arguments():
    with pytest.raises(ValueError):
        MovingAverage(0)
    with pytest.raises(ValueError):
        MovingAverage(3, recompute=0)
