# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-modular-inverse/. The authors are listed in prov/ZYDK39.jsonl.

import math
import random

import pytest

from batch_modular_inverse import NotInvertible, batch_inverse, inverse_and_gcd


def reference(xs, m):
    """Python's pow, used only as the reference."""
    return [pow(x, -1, m) for x in xs]


def unit(rng, m):
    while True:
        x = rng.randrange(m)
        if math.gcd(x, m) == 1:
            return x


MODULI = (
    [1, 2, 3, 4, 8, 16, 1 << 64, 6, 15, 21, 101, 1009, 65536, 2**61 - 1, 2**127 - 1, 10**9 + 7, 998244353]
    + [10**300 + 1, 3**700, 2**1000, 10**400 - 3, 2**521 - 1]
)


def test_worked_example():
    assert batch_inverse([3, 7, 10, 25], 101) == [34, 29, 91, 97]
    assert batch_inverse([], 101) == []
    assert batch_inverse([1], 101) == [1]
    assert batch_inverse([100], 101) == [100]


def test_not_invertible_example():
    with pytest.raises(NotInvertible) as info:
        batch_inverse([2, 7, 6], 15)
    assert info.value.g == 3


def test_inverse_and_gcd():
    rng = random.Random(1)
    for m in MODULI:
        for _ in range(50):
            a = rng.randrange(m)
            g, u = inverse_and_gcd(a, m)
            assert g == math.gcd(a, m)
            assert (u * a - g) % m == 0


def test_moduli_one_and_two():
    assert batch_inverse([0, 0, 0], 1) == [0, 0, 0]
    assert batch_inverse([1, 1], 2) == [1, 1]
    with pytest.raises(NotInvertible):
        batch_inverse([1, 0], 2)


def test_random_against_pow():
    rng = random.Random(2)
    count = 0
    for m in MODULI:
        for _ in range(40):
            k = rng.choice([1, 2, 3, 5, 17, 64])
            xs = [unit(rng, m) for _ in range(k)]
            if m > 1:
                xs[rng.randrange(k)] = 1
                xs[rng.randrange(k)] = m - 1
            assert batch_inverse(xs, m) == reference(xs, m)
            count += 1
    for _ in range(500):
        m = rng.randrange(1, 10**rng.randrange(1, 40))
        xs = [unit(rng, m) for _ in range(rng.randrange(0, 30))]
        assert batch_inverse(xs, m) == reference(xs, m)
        count += 1
    assert count >= 1000


def test_all_units_small_moduli():
    for m in range(1, 200):
        xs = [x for x in range(m) if math.gcd(x, m) == 1]
        assert batch_inverse(xs, m) == reference(xs, m)


def test_non_invertible_elements():
    rng = random.Random(3)
    for m in MODULI + [rng.randrange(4, 10**50) for _ in range(30)]:
        if m < 4:
            continue
        for _ in range(20):
            xs = [rng.randrange(m) for _ in range(rng.randrange(1, 20))]
            bad = [x for x in xs if math.gcd(x, m) != 1]
            prod = 1
            for x in xs:
                prod = prod * x % m
            if bad:
                with pytest.raises(NotInvertible) as info:
                    batch_inverse(xs, m)
                g = info.value.g
                assert g == math.gcd(prod, m) and g > 1 and m % g == 0
            else:
                assert batch_inverse(xs, m) == reference(xs, m)
        xs = [unit(rng, m) for _ in range(10)]
        xs[rng.randrange(10)] = 0
        with pytest.raises(NotInvertible) as info:
            batch_inverse(xs, m)
        assert info.value.g == m


def test_unreduced_and_negative_inputs():
    rng = random.Random(4)
    for _ in range(200):
        m = rng.randrange(2, 10**30)
        xs = [unit(rng, m) + m * rng.randrange(-5, 5) for _ in range(8)]
        assert batch_inverse(xs, m) == reference([x % m for x in xs], m)


def test_bad_modulus():
    with pytest.raises(ValueError):
        batch_inverse([1], 0)
