# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-exponentiation/. The authors are listed in prov/D262EM.jsonl.

import random

import pytest

from binary_exponentiation import binary_exponentiation, multiplication_count


def naive_power_mod(x: int, e: int, m: int) -> int:
    """x**e mod m by e multiplications with exact Python integers (small e only)."""
    p = 1
    for _ in range(e):
        p *= x
    return p % m


def test_example() -> None:
    assert binary_exponentiation(3, 200, 1009) == 985
    assert multiplication_count(200) == 10


def test_edges() -> None:
    assert binary_exponentiation(0, 0, 7) == 1
    assert binary_exponentiation(5, 0, 1) == 0
    assert binary_exponentiation(0, 5, 7) == 0
    assert binary_exponentiation(1, 10**30, 13) == 1
    assert binary_exponentiation(12, 1, 13) == 12
    assert binary_exponentiation(12, 2, 13) == 1
    assert binary_exponentiation(-2, 3, 7) == (-8) % 7
    assert binary_exponentiation(2, 4, 8) == 0
    for m in (1, 2, 4, 8, 1024, 2**64):
        for x in (0, 1, m - 1, m, m + 1, -1):
            for e in range(0, 12):
                assert binary_exponentiation(x, e, m) == naive_power_mod(x, e, m)


def test_carmichael() -> None:
    assert binary_exponentiation(7, 560, 561) == 1


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        binary_exponentiation(2, -1, 5)
    with pytest.raises(ValueError):
        binary_exponentiation(2, 3, 0)


def test_counts() -> None:
    for e in range(1, 2000):
        assert multiplication_count(e) <= 2 * (e.bit_length() - 1) + 1
    assert multiplication_count(2**20) == 21
    assert multiplication_count(2**20 - 1) == 2 * 19 + 1


def test_random_small_against_naive() -> None:
    rng = random.Random(4637)
    for _ in range(2000):
        m = rng.choice([1, 2, 3, 4, 16, 97, 100, 101, 561, 1009, rng.randint(1, 10**6)])
        x = rng.randint(-(10**6), 10**6)
        e = rng.randint(0, 60)
        assert binary_exponentiation(x, e, m) == naive_power_mod(x, e, m)


def test_random_large_against_pow() -> None:
    rng = random.Random(9151)
    p = 2**521 - 1  # a Mersenne prime
    for _ in range(500):
        m = rng.choice([p, 2**rng.randint(1, 700), rng.randint(2, 10**300), rng.randint(1, 10**300) * 2 + 1])
        x = rng.randint(-(10**400), 10**400)
        e = rng.randint(0, 10**300)
        assert binary_exponentiation(x, e, m) == pow(x, e, m)


def test_fermat_on_prime() -> None:
    rng = random.Random(77)
    p = 2**127 - 1
    for _ in range(200):
        a = rng.randint(1, p - 1)
        assert binary_exponentiation(a, p - 1, p) == 1
