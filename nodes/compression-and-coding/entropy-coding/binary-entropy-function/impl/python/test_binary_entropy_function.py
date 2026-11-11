# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-entropy-function/. The authors are listed in prov/MA49SE.jsonl.

import math
import random
from math import comb

import pytest

from binary_entropy_function import binomial_bounds_hold, h, h_derivative, h_inverse, two_pow_n_h


def test_values() -> None:
    assert h(0.0) == 0.0 and h(1.0) == 0.0
    assert h(0.5) == 1.0
    assert math.isclose(h(0.25), 2 - 0.75 * math.log2(3))
    assert math.isclose(h(0.1), 0.4689955935892812, rel_tol=1e-12)
    with pytest.raises(ValueError):
        h(1.5)


def test_symmetry_and_maximum() -> None:
    for i in range(1001):
        p = i / 1000
        assert math.isclose(h(p), h(1 - p), abs_tol=1e-12)
        assert h(p) <= 1.0
        if p != 0.5:
            assert h(p) < 1.0


def test_concavity() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        a, b, t = rng.random(), rng.random(), rng.random()
        assert h(t * a + (1 - t) * b) >= t * h(a) + (1 - t) * h(b) - 1e-12


def test_derivative() -> None:
    for p in [0.01, 0.1, 0.3, 0.5, 0.7, 0.99]:
        eps = 1e-6
        numeric = (h(p + eps) - h(p - eps)) / (2 * eps)
        assert math.isclose(h_derivative(p), numeric, abs_tol=1e-6)
    assert h_derivative(0.5) == 0.0
    assert math.isclose(h_derivative(0.1), math.log2(9))


def test_inverse() -> None:
    assert h_inverse(0.0) == pytest.approx(0.0, abs=1e-12)
    assert h_inverse(1.0) == pytest.approx(0.5, abs=1e-7)
    assert h_inverse(0.5) == pytest.approx(0.110027864438, abs=1e-10)
    for i in range(1, 500):
        p = i / 1000
        assert h_inverse(h(p)) == pytest.approx(p, abs=1e-9)


def test_binomial_bounds_exact_up_to_60() -> None:
    for n in range(0, 61):
        for k in range(0, n + 1):
            assert binomial_bounds_hold(n, k), (n, k)


def test_binomial_upper_bound_is_tight_only_at_the_ends() -> None:
    for n in range(1, 61):
        for k in range(0, n + 1):
            num, den = two_pow_n_h(n, k)
            equal = comb(n, k) * den == num
            assert equal == (k in (0, n))


def test_worked_example() -> None:
    num, den = two_pow_n_h(10, 3)
    assert (num, den) == (10 ** 10, 27 * 823543)
    assert num / den / 11 < comb(10, 3) == 120 < num / den


def test_bsc_capacity_example() -> None:
    # 1 - h(0.11) is just above 1/2.
    assert 0.5 < 1 - h(0.11) < 0.5001
