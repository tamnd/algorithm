# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segmented-sieve/. The authors are listed in prov/ZW0DHJ.jsonl.

import random

from segmented_sieve import segmented_sieve


def is_prime_by_trial_division(m: int) -> bool:
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


LIMIT = 20000
PRIME = [is_prime_by_trial_division(m) for m in range(LIMIT + 1)]


def oracle(low: int, high: int) -> list[int]:
    if high <= LIMIT:
        return [m for m in range(max(low, 0), high + 1) if PRIME[m]]
    return [m for m in range(max(low, 2), high + 1) if is_prime_by_trial_division(m)]


def test_example() -> None:
    assert segmented_sieve(100, 130, 16) == [101, 103, 107, 109, 113, 127]
    assert segmented_sieve(10**9, 10**9 + 100, 101) == [
        10**9 + 7, 10**9 + 9, 10**9 + 21, 10**9 + 33, 10**9 + 87, 10**9 + 93, 10**9 + 97,
    ]


def test_edges() -> None:
    assert segmented_sieve(0, 0) == []
    assert segmented_sieve(0, 1) == []
    assert segmented_sieve(1, 1) == []
    assert segmented_sieve(-10, 2) == [2]
    assert segmented_sieve(2, 2) == [2]
    assert segmented_sieve(0, 10, 1) == [2, 3, 5, 7]
    assert segmented_sieve(5, 4) == []
    assert segmented_sieve(114, 126, 3) == []


def test_every_upper_end_up_to_2000_from_0_and_1() -> None:
    for high in range(2001):
        assert segmented_sieve(0, high, 37) == oracle(0, high)
        assert segmented_sieve(1, high, 64) == oracle(1, high)


def test_length_one_segments() -> None:
    for m in range(2001):
        assert segmented_sieve(m, m) == ([m] if PRIME[m] else [])
    for high in range(0, 2001, 97):
        assert segmented_sieve(0, high, 1) == oracle(0, high)


def test_block_ends_on_primes_and_prime_squares() -> None:
    for q in (2, 3, 5, 7, 11, 13, 31, 97, 101):
        for edge in (q, q * q):
            for low in (2, edge - 5, edge - 1, edge, edge + 1):
                if low < 0:
                    continue
                high = edge + 60
                for block in (edge - low + 1, edge - low, 1, 2, 7):
                    if block >= 1:
                        assert segmented_sieve(low, high, block) == oracle(low, high)
    # the upper end is the square of a prime, so the base list must include that prime
    for q in (2, 3, 5, 7, 11, 13, 97, 139):
        assert segmented_sieve(q * q - 30, q * q, 8) == oracle(q * q - 30, q * q)


def test_random_intervals() -> None:
    rng = random.Random(1977)
    for _ in range(150):
        low = rng.randint(0, LIMIT)
        high = rng.randint(low, min(LIMIT, low + 3000))
        block = rng.randint(1, 500)
        assert segmented_sieve(low, high, block) == oracle(low, high)
    for _ in range(15):
        low = rng.randint(10**6, 10**10)
        high = low + rng.randint(0, 300)
        assert segmented_sieve(low, high, rng.randint(1, 400)) == oracle(low, high)
