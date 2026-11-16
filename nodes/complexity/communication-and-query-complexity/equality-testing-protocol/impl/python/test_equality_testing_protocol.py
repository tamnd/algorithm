# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equality-testing-protocol/. The authors are listed in prov/SVFWAE.jsonl.

import random
from fractions import Fraction
from itertools import product

from equality_testing_protocol import (
    equality_test,
    error_probability,
    exchange,
    field_size,
    fingerprint,
    protocol_cost,
    word_length,
)


def naive_is_prime(m: int) -> bool:
    return m >= 2 and all(m % d != 0 for d in range(2, m))


def test_field_size_is_least_prime() -> None:
    for n in range(0, 25):
        q = field_size(n)
        lo = max(2, n * n)
        assert q >= lo and naive_is_prime(q)
        assert not any(naive_is_prime(m) for m in range(lo, q))
        if n >= 2:
            assert q < 2 * n * n


def test_fingerprint_matches_direct_sum() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(0, 12)
        x = [rng.randrange(2) for _ in range(n)]
        q = field_size(n)
        r = rng.randrange(q)
        direct = sum(x[i] * r**i for i in range(n)) % q
        assert fingerprint(x, r, q) == direct


def test_exact_error_on_all_pairs() -> None:
    # Every pair of strings and every random point, for n = 1 to 5:
    # 35 thousand runs of the protocol in all.
    for n in range(1, 6):
        q = field_size(n)
        bound = Fraction(n - 1, q)
        worst = Fraction(0)
        for x in product((0, 1), repeat=n):
            for y in product((0, 1), repeat=n):
                wrong = 0
                for r in range(q):
                    out, transcript = exchange(x, y, r, q)
                    assert len(transcript) == protocol_cost(n)
                    if out != (x == y):
                        wrong += 1
                        assert x != y and out
                err = Fraction(wrong, q)
                assert err <= bound
                worst = max(worst, err)
        # The bound (n - 1) / q is reached for these small n.
        assert worst == bound


def test_worked_example() -> None:
    x = [1, 0, 1, 1, 0]
    y = [1, 0, 0, 1, 1]
    q = field_size(5)
    assert q == 29 and word_length(q) == 5
    bad = [r for r in range(q) if fingerprint(x, r, q) == fingerprint(y, r, q)]
    assert bad == [0, 1, 28]
    assert error_probability(x, y) == Fraction(3, 29)
    assert fingerprint(x, 7, q) == 16 and fingerprint(y, 7, q) == 19
    assert exchange(x, y, 7, q) == (False, "00111" + "10000" + "0")
    assert exchange(x, y, 28, q)[0] is True


def test_random_runs_never_reject_equal_strings() -> None:
    rng = random.Random(2024)
    for _ in range(300):
        n = rng.randrange(1, 80)
        x = [rng.randrange(2) for _ in range(n)]
        out, transcript = equality_test(x, list(x), rng)
        assert out is True
        assert len(transcript) == protocol_cost(n)


def test_exact_error_on_random_long_pairs() -> None:
    rng = random.Random(99)
    n = 32
    q = field_size(n)
    assert q == 1031
    for _ in range(4):
        x = [rng.randrange(2) for _ in range(n)]
        y = list(x)
        y[rng.randrange(n)] ^= 1
        assert error_probability(x, y) <= Fraction(n - 1, q)


def test_cost_table() -> None:
    assert [protocol_cost(n) for n in (5, 8, 16, 32, 64, 100, 1000)] == [11, 15, 19, 23, 27, 29, 41]
    # The protocol is first shorter than the n + 1 bits of the trivial protocol at n = 19.
    assert all(protocol_cost(n) >= n + 1 for n in range(1, 19))
    assert protocol_cost(19) == 19
