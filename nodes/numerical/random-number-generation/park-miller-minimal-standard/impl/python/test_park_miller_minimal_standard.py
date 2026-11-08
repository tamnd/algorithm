# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/park-miller-minimal-standard/. The authors are listed in prov/HR4MZ7.jsonl.

import random

import pytest

from park_miller_minimal_standard import (
    A,
    M,
    park_miller_next,
    park_miller_seed,
    park_miller_stream,
    park_miller_uniform,
)


def test_trace_of_the_page() -> None:
    assert park_miller_stream(1, 7) == [
        16807, 282475249, 1622650073, 984943658, 1144108930, 470211272, 101027544,
    ]


def test_published_check_value() -> None:
    # Park and Miller (1988): from x0 = 1, x10000 = 1043618065.
    assert park_miller_stream(1, 10000)[-1] == 1043618065
    # The C++ standard gives 399268537 for the 10000th value of minstd_rand (a = 48271).
    assert park_miller_stream(1, 10000, a=48271)[-1] == 399268537


def test_against_direct_product() -> None:
    rng = random.Random(16807)
    xs = [1, 2, 127772, 127773, 127774, M - 2, M - 1] + [rng.randrange(1, M) for _ in range(2000)]
    for a in (16807, 48271):
        for x in xs:
            assert park_miller_next(x, a) == a * x % M


def test_largest_state_needs_the_correction() -> None:
    assert park_miller_next(M - 1) == M - A


def test_schrage_on_small_primes_exhaustively() -> None:
    primes = [p for p in range(5, 400) if all(p % d for d in range(2, int(p**0.5) + 1))]
    for m in primes:
        for a in range(2, m):
            if m % a > m // a:
                continue
            for x in range(1, m):
                assert park_miller_next(x, a, m) == a * x % m


def test_multiplier_is_a_primitive_root() -> None:
    n = M - 1
    factors = [2, 3, 7, 11, 31, 151, 331]
    prod = 2 * 9 * 7 * 11 * 31 * 151 * 331
    assert prod == n
    for a in (16807, 48271):
        assert pow(a, n, M) == 1
        assert all(pow(a, n // p, M) != 1 for p in factors)


def test_full_period_by_brute_force_for_small_primes() -> None:
    for m, a in ((31, 3), (101, 2), (1009, 11)):
        x = park_miller_seed(1, m)
        seen = {x}
        x = park_miller_next(x, a, m)
        steps = 1
        while x != 1:
            seen.add(x)
            x = park_miller_next(x, a, m)
            steps += 1
        is_root = all(pow(a, (m - 1) // p, m) != 1 for p in range(2, m) if (m - 1) % p == 0 and all(p % d for d in range(2, p)))
        assert is_root
        assert steps == m - 1 and len(seen) == m - 1


def test_forbidden_seed() -> None:
    with pytest.raises(ValueError):
        park_miller_seed(0)
    with pytest.raises(ValueError):
        park_miller_seed(M)
    assert park_miller_seed(M + 5) == 5


def test_uniform_range_and_chi_square() -> None:
    xs = park_miller_stream(12345, 20000)
    us = [park_miller_uniform(x) for x in xs]
    assert all(0.0 < u < 1.0 for u in us)
    counts = [0] * 10
    for u in us:
        counts[int(u * 10)] += 1
    expected = len(us) / 10
    chi2 = sum((c - expected) ** 2 / expected for c in counts)
    assert chi2 < 27.88  # the 0.999 quantile of chi-square with 9 degrees of freedom
