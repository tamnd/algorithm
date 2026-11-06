# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-primality-test/. The authors are listed in prov/12XYK5.jsonl.

import math
import random

import pytest

from lucas_primality_test import (
    distinct_prime_factors,
    is_prime_lucas,
    lucas_primality_test,
    lucas_witnesses,
    verify_lucas_witnesses,
)

LIMIT = 100_000
CARMICHAEL = (561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 825265, 321197185, 5394826801)
# Smallest strong pseudoprimes to the first 1 to 7 prime bases.
PSI = (2047, 1373653, 25326001, 3215031751, 2152302898747, 3474749660383, 341550071728321)
SMALL_PRIMES = [p for p in range(2, 10_000) if all(p % d for d in range(2, math.isqrt(p) + 1))]


def sieve(limit: int) -> bytearray:
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, math.isqrt(limit) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(is_p[i * i :: i]))
    return is_p


def trial_division_is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def miller_rabin(n: int, rng: random.Random, rounds: int = 30) -> bool:
    """An independent probable prime test for large n."""
    if n < 4:
        return n >= 2
    if n % 2 == 0:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def test_example_1009_and_561() -> None:
    assert distinct_prime_factors(1008) == [2, 3, 7]
    assert lucas_witnesses(1009, [2, 3, 7]) == {2: 11, 3: 2, 7: 2}
    assert pow(2, 504, 1009) == 1 and pow(11, 504, 1009) == 1008
    assert pow(2, 336, 1009) == 374 and pow(2, 144, 1009) == 105
    assert lucas_primality_test(1009, [7, 3, 2]) is True
    # 561: the base 2 passes the Fermat test and 2^280 = 1, then 3 divides 561.
    assert pow(2, 560, 561) == 1 and pow(2, 280, 561) == 1 and pow(3, 560, 561) == 375
    assert lucas_witnesses(561, [2, 5, 7]) is None


def test_against_trial_division_up_to_limit() -> None:
    is_p = sieve(LIMIT)
    for n in range(LIMIT + 1):
        assert is_prime_lucas(n) == bool(is_p[n]), n
    for n in range(0, 3000):
        assert is_prime_lucas(n) == trial_division_is_prime(n)


def test_certificates_verify() -> None:
    for n in range(3, 5000):
        primes = distinct_prime_factors(n - 1)
        w = lucas_witnesses(n, primes)
        if w is None:
            assert not trial_division_is_prime(n)
        else:
            assert trial_division_is_prime(n)
            assert verify_lucas_witnesses(n, primes, w)
    assert not verify_lucas_witnesses(1009, [2, 3, 7], {2: 2, 3: 2, 7: 2})
    assert not verify_lucas_witnesses(561, [2, 5, 7], {2: 5, 5: 2, 7: 2})


def test_hard_composites() -> None:
    for n in CARMICHAEL + PSI:
        assert lucas_primality_test(n, distinct_prime_factors(n - 1)) is False, n
    for n in (4, 6, 9, 25, 3**10, 2**20, 7919**2, 65537 * 65539):
        assert lucas_primality_test(n, distinct_prime_factors(n - 1)) is False


def test_large_primes_and_composites_with_factored_n_minus_1() -> None:
    rng = random.Random(5)
    for digits in (30, 100, 200, 300):
        primes_found = composites_found = tries = 0
        while tries < 3000 and (primes_found < 1 or composites_found < 3):
            tries += 1
            primes = sorted(set(rng.sample(SMALL_PRIMES[1:], 4)) | {2})
            m = 2
            while m < 10 ** (digits - 1):
                m *= rng.choice(primes)
            n = m + 1
            qs = distinct_prime_factors_from(m, primes)
            probable = miller_rabin(n, rng)
            assert lucas_primality_test(n, qs) is probable
            if probable:
                w = lucas_witnesses(n, qs)
                assert w is not None and verify_lucas_witnesses(n, qs, w)
                primes_found += 1
            else:
                composites_found += 1
        assert primes_found >= 1 and composites_found >= 3, digits
    # Fermat primes and a few Proth-style primes with n - 1 a power of 2 times a prime.
    for k in range(5):
        assert lucas_primality_test(2 ** (2**k) + 1, [2]) is True
    for k in range(5, 10):
        assert lucas_primality_test(2 ** (2**k) + 1, [2]) is False
    assert lucas_primality_test(3 * 2**189 + 1, [2, 3]) is True
    assert lucas_primality_test(3 * 2**190 + 1, [2, 3]) is miller_rabin(3 * 2**190 + 1, rng)


def distinct_prime_factors_from(m: int, primes: list[int]) -> list[int]:
    return [q for q in primes if m % q == 0]


def test_bad_factor_lists() -> None:
    with pytest.raises(ValueError):
        lucas_primality_test(1009, [2, 3])  # 7 is missing
    with pytest.raises(ValueError):
        lucas_primality_test(1009, [2, 3, 7, 5])  # 5 does not divide 1008
    with pytest.raises(ValueError):
        lucas_primality_test(1009, [2, 2, 3, 7])
    with pytest.raises(ValueError):
        distinct_prime_factors(0)
    assert lucas_primality_test(2, []) is True
    assert lucas_primality_test(1, []) is False
    assert lucas_primality_test(0, []) is False
