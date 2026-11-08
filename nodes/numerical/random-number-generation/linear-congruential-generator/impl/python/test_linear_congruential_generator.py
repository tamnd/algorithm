# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-congruential-generator/. The authors are listed in prov/GFMHDY.jsonl.

import random

import pytest

from linear_congruential_generator import (
    LinearCongruentialGenerator,
    hull_dobell,
    minstd,
    period,
    schrage_mulmod,
)


def test_example_trace() -> None:
    g = LinearCongruentialGenerator(16, 5, 3, 0)
    assert [g.next() for _ in range(16)] == [3, 2, 13, 4, 7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0]


def test_minstd_check_values() -> None:
    # Park and Miller (1988); also the C++ requirement for minstd_rand0 and minstd_rand.
    g = minstd(1)
    for _ in range(9999):
        g.next()
    assert g.next() == 1043618065
    g = minstd(1, 48271)
    for _ in range(9999):
        g.next()
    assert g.next() == 399268537


def test_numerical_recipes_ranqd1() -> None:
    g = LinearCongruentialGenerator(2**32, 1664525, 1013904223, 0)
    assert [g.next() for _ in range(6)] == [
        1013904223, 1196435762, 3519870697, 2868466484, 1649599747, 2670642822]


def test_mmix_and_largest_word() -> None:
    m = 2**64
    g = LinearCongruentialGenerator(m, 6364136223846793005, 1442695040888963407, 1)
    assert g.next() == 7806831264735756412
    g.state = m - 1
    x = g.next()
    assert x == (6364136223846793005 * (m - 1) + 1442695040888963407) % m
    g.state = m - 2
    for _ in range(1000):
        u = g.uniform()
        assert 0.0 <= u < 1.0
    h = LinearCongruentialGenerator(m, 1, m - 1, 0)  # steps down by 1
    assert h.next() == m - 1 and h.uniform() < 1.0


def test_seed_zero_forbidden_when_c_is_zero() -> None:
    with pytest.raises(ValueError):
        minstd(0)
    with pytest.raises(ValueError):
        minstd(2**31 - 1)  # reduces to 0
    assert LinearCongruentialGenerator(16, 5, 3, 0).next() == 3


def test_hull_dobell_matches_brute_force() -> None:
    for m in range(2, 65):
        for a in range(1, m):
            for c in range(m):
                assert (period(m, a, c, 0) == m) == hull_dobell(m, a, c), (m, a, c)


def test_park_miller_full_multiplicative_period_small_prime() -> None:
    # m = 31: a has period m - 1 from every nonzero seed iff a is a primitive root.
    roots = {a for a in range(2, 31) if len({pow(a, k, 31) for k in range(30)}) == 30}
    for a in range(2, 31):
        assert (period(31, a, 0, 1) == 30) == (a in roots)
    assert period(2**10, 5, 0, 1) == 2**8 and period(2**10, 5, 0, 2) == 2**7


def test_schrage() -> None:
    m = 2**31 - 1
    rng = random.Random(7)
    for a in (16807, 48271):
        xs = [1, 2, m - 1, m - 2, m // a, m // a + 1] + [rng.randrange(1, m) for _ in range(2000)]
        for x in xs:
            assert schrage_mulmod(a, x, m) == a * x % m
    with pytest.raises(ValueError):
        schrage_mulmod(2**20, 5, m)


def test_randu_three_term_relation() -> None:
    g = LinearCongruentialGenerator(2**31, 65539, 0, 1)
    xs = [g.next() for _ in range(1000)]
    assert all((xs[i + 2] - 6 * xs[i + 1] + 9 * xs[i]) % 2**31 == 0 for i in range(998))


def test_low_bit_periods() -> None:
    g = LinearCongruentialGenerator(2**16, 5, 3, 7)
    xs = [g.next() for _ in range(64)]
    for j in range(4):
        bits = [(x >> j) & 1 for x in xs]
        p = 2 ** (j + 1)
        assert all(bits[i] == bits[i + p] for i in range(64 - p))
        assert any(bits[i] != bits[i + p // 2] for i in range(64 - p))


def test_chi_square_top_bits() -> None:
    g = LinearCongruentialGenerator(2**64, 6364136223846793005, 1442695040888963407, 12345)
    n, k = 16000, 16
    counts = [0] * k
    for _ in range(n):
        counts[g.next() >> 60] += 1
    e = n / k
    chi2 = sum((c - e) ** 2 / e for c in counts)
    assert chi2 < 37.70  # 0.999 quantile of chi-square with 15 degrees of freedom
