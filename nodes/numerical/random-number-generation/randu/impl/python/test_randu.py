# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randu/. The authors are listed in prov/352H47.jsonl.

import random

import pytest

from randu import A, M, randu_next, randu_plane, randu_seed, randu_stream, randu_uniform


def test_trace_of_the_page() -> None:
    assert randu_stream(1, 6) == [65539, 393225, 1769499, 7077969, 26542323, 95552217]
    assert randu_stream(123456789, 4) == [1663592255, 280507837, 1743102263, 1491592101]


def test_shift_form_equals_product() -> None:
    rng = random.Random(65539)
    for x in [1, 3, M - 1, M - 3] + [rng.randrange(1, M, 2) for _ in range(3000)]:
        assert randu_next(x) == A * x % M


def test_square_of_multiplier() -> None:
    assert A * A % M == (6 * A - 9) % M == 393225


def test_fifteen_planes() -> None:
    xs = randu_stream(123456789, 100000)
    planes = {randu_plane(xs[i], xs[i + 1], xs[i + 2]) for i in range(len(xs) - 2)}
    assert planes == set(range(-5, 10))


def test_period_is_two_to_the_29() -> None:
    # The period equals the order of A modulo 2^31, a power of 2.
    assert pow(A, 2**29, M) == 1
    assert pow(A, 2**28, M) != 1


def test_period_by_brute_force_for_small_moduli() -> None:
    for e in range(3, 17):
        m = 2**e
        for a in sorted({3, 11, 19, A % m, m - 5}):  # each is 3 mod 8, as A is
            x, steps = a * 1 % m, 1
            while x != 1:
                x = a * x % m
                steps += 1
            assert steps == 2 ** (e - 2)


def test_lowest_bits_are_not_random() -> None:
    xs = randu_stream(12345, 64)
    assert all(x & 1 == 1 for x in xs)
    # x mod 4 alternates because A = 3 mod 4.
    assert [x % 4 for x in xs[:6]] == [(12345 * 3 ** (i + 1)) % 4 for i in range(6)]


def test_seed_rules() -> None:
    with pytest.raises(ValueError):
        randu_seed(0)
    with pytest.raises(ValueError):
        randu_seed(2)
    assert randu_seed(M + 1) == 1


def test_uniform_range() -> None:
    us = [randu_uniform(x) for x in randu_stream(7, 1000)]
    assert all(0.0 < u < 1.0 for u in us)


def test_plane_rejects_non_consecutive() -> None:
    with pytest.raises(ValueError):
        randu_plane(1, 3, 5)
