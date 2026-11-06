# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/garner-algorithm/. The authors are listed in prov/PHSQZC.jsonl.

import math
import random

import pytest

from garner_algorithm import garner, garner_digits, garner_setup


def reference(residues, moduli):
    """The classical CRT sum with Python's pow, used only as the reference."""
    big = math.prod(moduli)
    x = 0
    for v, mi in zip(residues, moduli):
        w = big // mi
        x += v * w * pow(w, -1, mi)
    return x % big


def coprime_moduli(rng, pool, count):
    chosen = []
    for mi in rng.sample(pool, len(pool)):
        if all(math.gcd(mi, mj) == 1 for mj in chosen):
            chosen.append(mi)
        if len(chosen) == count:
            break
    return chosen


POOL = [
    1, 2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 25, 27, 49, 64, 101, 121, 1 << 64, 15, 77, 221,
    10**9 + 7, 998244353, 2**61 - 1, 2**127 - 1, 10**300 + 1, 3**700, 10**400 - 3, 2**521 - 1, 17**250,
]


def test_hac_example():
    ctx = garner_setup([5, 7, 11, 13])
    assert ctx.c == (0, 3, 6, 5)
    assert garner_digits([2, 1, 3, 8], ctx) == [2, 4, 7, 5]
    assert garner([2, 1, 3, 8], ctx) == 2192


def test_rsa_example():
    ctx = garner_setup([61, 53])
    assert ctx.c[1] == 20
    assert garner([pow(2790, 53, 61), pow(2790, 49, 53)], ctx) == 65 == pow(2790, 2753, 3233)


def test_small_cases():
    assert garner([], garner_setup([])) == 0
    assert garner([0], garner_setup([1])) == 0
    assert garner([0, 1], garner_setup([1, 2])) == 1
    assert garner([1, 0], garner_setup([2, 1])) == 1
    ctx = garner_setup([2, 3])
    assert [garner([x % 2, x % 3], ctx) for x in range(6)] == list(range(6))


def test_every_value_small_systems():
    for moduli in ([3, 4, 5], [8, 9, 7], [2, 1, 3], [16, 5, 3, 7], [11, 13, 17]):
        ctx = garner_setup(moduli)
        big = math.prod(moduli)
        for x in range(big):
            assert garner([x % mi for mi in moduli], ctx) == x


def test_random_against_reference():
    rng = random.Random(5)
    count = 0
    for _ in range(600):
        moduli = coprime_moduli(rng, POOL, rng.randrange(1, 9))
        ctx = garner_setup(moduli)
        big = math.prod(moduli)
        for x in (0, 1 % big, big - 1, rng.randrange(big)):
            res = [x % mi for mi in moduli]
            got = garner(res, ctx)
            assert got == x == reference(res, moduli)
            digits = garner_digits(res, ctx)
            assert all(0 <= d < mi for d, mi in zip(digits, moduli))
            count += 1
    assert count >= 2000


def test_random_residues_and_word_primes():
    rng = random.Random(6)
    primes = [p for p in range(10**6, 10**6 + 3000) if all(p % d for d in range(2, 1001))]
    for _ in range(100):
        moduli = rng.sample(primes, rng.randrange(1, 40))
        ctx = garner_setup(moduli)
        res = [rng.randrange(-10**20, 10**20) for _ in moduli]
        x = garner(res, ctx)
        assert 0 <= x < math.prod(moduli)
        assert x == reference([v % mi for v, mi in zip(res, moduli)], moduli)


def test_not_coprime():
    for moduli in ([4, 6], [3, 5, 9], [2, 2], [10**300 + 1, 3, 10**300 + 1], [0, 3], [5, -7]):
        with pytest.raises(ValueError):
            garner_setup(moduli)
    rng = random.Random(7)
    for _ in range(200):
        a, b = rng.randrange(2, 10**6), rng.randrange(2, 10**6)
        moduli = [a, b]
        if math.gcd(a, b) == 1:
            assert garner([1, 1], garner_setup(moduli)) == 1 % (a * b)
        else:
            with pytest.raises(ValueError):
                garner_setup(moduli)


def test_length_mismatch():
    with pytest.raises(ValueError):
        garner([1], garner_setup([3, 5]))
