# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-information/. The authors are listed in prov/10AS4N.jsonl.

import math
import random
from fractions import Fraction

import pytest

from self_information import (
    arithmetic_interval, ideal_length, message_information, self_information, shortest_dyadic_inside,
)


def test_values() -> None:
    assert self_information(1.0) == 0.0
    assert math.isclose(self_information(0.5), 1.0)
    assert math.isclose(self_information(1 / 8), 3.0)
    assert math.isclose(self_information(1 / 6), math.log2(6))
    assert math.isclose(self_information(0.5, base=math.e), math.log(2))
    with pytest.raises(ValueError):
        self_information(0.0)
    with pytest.raises(ValueError):
        self_information(1.5)


def test_additive_for_independent_events() -> None:
    rng = random.Random(1)
    for _ in range(1000):
        p, q = rng.uniform(1e-6, 1), rng.uniform(1e-6, 1)
        assert math.isclose(self_information(p * q), self_information(p) + self_information(q), abs_tol=1e-9)


def test_decreasing_in_p() -> None:
    ps = [i / 100 for i in range(1, 101)]
    vals = [self_information(p) for p in ps]
    assert all(a > b for a, b in zip(vals, vals[1:]))


def test_entropy_is_expected_information() -> None:
    p = [0.5, 0.25, 0.125, 0.125]
    assert math.isclose(sum(q * self_information(q) for q in p), 1.75)


def test_worked_message() -> None:
    model = {"a": Fraction(1, 2), "b": Fraction(1, 4), "c": Fraction(1, 4)}
    low, width = arithmetic_interval("abac", model)
    assert width == Fraction(1, 64)
    assert low == Fraction(1, 2) * 0 + Fraction(1, 2) * Fraction(1, 2) + Fraction(1, 8) * 0 + Fraction(1, 16) * Fraction(3, 4)
    assert math.isclose(ideal_length(width), 6.0)
    assert math.isclose(message_information("abac", {k: float(v) for k, v in model.items()}), 6.0)
    assert shortest_dyadic_inside(low, width) == "010011"


def test_arithmetic_ideal_length_is_sum_of_information() -> None:
    rng = random.Random(2)
    for _ in range(200):
        m = rng.randint(1, 5)
        weights = [rng.randint(1, 9) for _ in range(m)]
        total = sum(weights)
        model = {i: Fraction(w, total) for i, w in enumerate(weights)}
        msg = [rng.randrange(m) for _ in range(rng.randint(0, 40))]
        low, width = arithmetic_interval(msg, model)
        info = message_information(msg, {k: float(v) for k, v in model.items()})
        assert math.isclose(ideal_length(width), info, abs_tol=1e-9)
        bits = shortest_dyadic_inside(low, width)
        # The code is at least the ideal length and less than two bits longer.
        assert info - 1e-9 <= len(bits) <= math.ceil(info - 1e-9) + 1
        # The bits point inside the interval of the message.
        k = len(bits)
        v = Fraction(int(bits, 2) if bits else 0, 1 << k)
        assert low <= v and v + Fraction(1, 1 << k) <= low + width
