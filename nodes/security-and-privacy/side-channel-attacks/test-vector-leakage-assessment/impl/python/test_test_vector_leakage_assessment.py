# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/test-vector-leakage-assessment/. The authors are listed in prov/89GDF4.jsonl.

import math
import random
import statistics

import pytest
from leakage_assessment import (
    PRESENT_SBOX,
    centred_products,
    collect,
    hamming_weight,
    tvla,
    welch_t,
)

KEY = 0xB
FIXED = 0x1  # S(1 xor B) = F, Hamming weight 4


def test_welch_t_against_statistics() -> None:
    rng = random.Random(20240507)
    for _ in range(500):
        x = [rng.gauss(rng.uniform(-1, 1), rng.uniform(0.1, 3)) for _ in range(rng.randrange(2, 40))]
        y = [rng.gauss(rng.uniform(-1, 1), rng.uniform(0.1, 3)) for _ in range(rng.randrange(2, 40))]
        se = math.sqrt(statistics.variance(x) / len(x) + statistics.variance(y) / len(y))
        want = (statistics.mean(x) - statistics.mean(y)) / se
        assert welch_t(x, y) == pytest.approx(want, rel=1e-9, abs=1e-12)
        assert welch_t(y, x) == pytest.approx(-want, rel=1e-9, abs=1e-12)


def test_welch_t_edges() -> None:
    assert welch_t([1.0, 1.0], [1.0, 1.0]) == 0.0
    assert welch_t([2.0, 2.0], [1.0, 1.0]) == math.inf
    assert welch_t([0.0, 0.0], [1.0, 1.0]) == -math.inf


def test_fixed_input_has_weight_four() -> None:
    assert hamming_weight(PRESENT_SBOX[FIXED ^ KEY]) == 4


def test_unprotected_device_fails() -> None:
    rng = random.Random(1)
    sets = [collect(rng, 50, FIXED, KEY, 4, 1.0, False) for _ in range(2)]
    tvals, leaky = tvla(sets)
    assert leaky == [0]
    assert all(abs(v) < 4.5 for row in tvals for v in row[1:])


def test_t_grows_as_the_root_of_n() -> None:
    # Expected t is 2 / sqrt(1/n + 2/n): fixed variance 1, random variance 1 + Var(HW) = 2.
    rng = random.Random(2)
    n = 200
    ts = [tvla([collect(rng, n, FIXED, KEY, 2, 1.0, False)])[0][0][0] for _ in range(20)]
    assert statistics.mean(ts) == pytest.approx(2 * math.sqrt(n / 3), rel=0.1)


def test_masked_device_first_and_second_order() -> None:
    rng = random.Random(3)
    sets = [collect(rng, 1000, FIXED, KEY, 4, 1.0, True) for _ in range(2)]
    assert tvla(sets)[1] == []
    second = [
        ([[v] for v in centred_products(f, 0, 1)], [[v] for v in centred_products(r, 0, 1)])
        for f, r in sets
    ]
    tvals, leaky = tvla(second)
    assert leaky == [0]
    # E[(HW(x xor m) - 2)(HW(m) - 2)] = 1 - HW(x)/2 = -1 for the fixed x = F, and 0 for random x.
    assert all(row[0] < 0 for row in tvals)


def test_second_order_expectation_exact() -> None:
    for x in range(16):
        e = sum((hamming_weight(x ^ m) - 2) * (hamming_weight(m) - 2) for m in range(16)) / 16
        assert e == 1 - hamming_weight(x) / 2
    assert sum(1 - hamming_weight(x) / 2 for x in range(16)) == 0


def test_no_false_alarms_on_noise() -> None:
    rng = random.Random(4)
    over2 = over45 = total = 0
    for _ in range(100):
        f = [[rng.gauss(0, 1) for _ in range(20)] for _ in range(30)]
        r = [[rng.gauss(0, 1) for _ in range(20)] for _ in range(30)]
        row = tvla([(f, r)])[0][0]
        total += len(row)
        over2 += sum(abs(v) > 2 for v in row)
        over45 += sum(abs(v) > 4.5 for v in row)
    assert over45 == 0
    # With 30 traces per group the t law has heavier tails than the normal law (0.0455).
    assert 0.03 < over2 / total < 0.08
