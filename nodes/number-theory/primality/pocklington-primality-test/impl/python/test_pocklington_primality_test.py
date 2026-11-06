# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pocklington-primality-test/. The authors are listed in prov/1J28JY.jsonl.

import math
import random

import pytest

from pocklington_primality_test import COMPOSITE, PRIME, UNKNOWN, bls_cube_root_test, factored_part, pocklington, verify_certificate

LIMIT = 100_000


def is_prime_td(n: int) -> bool:
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


def factorize(n: int) -> dict[int, int]:
    f: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def strong_probable(n: int, a: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def probably_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    return all(strong_probable(n, a) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41))


def smallest_sufficient_part(n: int, cube: bool = False) -> dict[int, int]:
    """Prime powers of n - 1, largest first, until F^2 > n (or F^3 >= n)."""
    full = factorize(n - 1)
    part: dict[int, int] = {}
    f = 1
    for q in sorted(full, key=lambda q: -(q ** full[q])):
        part[q] = full[q]
        f *= q ** full[q]
        if (f**3 >= n) if cube else (f * f > n):
            break
    return part


M127 = 2**127 - 1
M521 = 2**521 - 1
M607 = 2**607 - 1
CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361]
STRONG_PSP = [2047, 1373653, 25326001, 3215031751, 2152302898747, 3474749660383, 341550071728321, 3825123056546413051]


def test_example_1000003() -> None:
    n = 1000003
    assert is_prime_td(166667) and (n - 1) == 6 * 166667 and 166667**2 > n
    assert pow(2, n - 1, n) == 1 and pow(2, 6, n) == 64 and math.gcd(63, n) == 1
    assert verify_certificate(n, {166667: 1}, {166667: 2})
    verdict, bases = pocklington(n, {166667: 1}, rng=random.Random(1))
    assert verdict == PRIME and verify_certificate(n, {166667: 1}, bases)


def test_example_561() -> None:
    assert pow(2, 280, 561) == 1 and math.gcd(pow(2, 280, 561) - 1, 561) == 561
    assert pow(5, 280, 561) == 67 and math.gcd(66, 561) == 33
    for seed in range(20):
        verdict, ev = pocklington(561, {2: 4, 5: 1}, rng=random.Random(seed))
        assert verdict in (COMPOSITE, UNKNOWN)
        if "factor" in ev:
            assert 561 % ev["factor"] == 0 and 1 < ev["factor"] < 561


def test_small_and_even_and_bad_input() -> None:
    assert pocklington(2, {})[0] == PRIME and pocklington(3, {})[0] == PRIME
    assert pocklington(0, {})[0] == COMPOSITE and pocklington(1, {})[0] == COMPOSITE
    assert pocklington(4, {})[0] == COMPOSITE and pocklington(10**6, {})[0] == COMPOSITE
    with pytest.raises(ValueError):
        pocklington(1000003, {2: 1, 3: 1})  # F = 6 is too small
    with pytest.raises(ValueError):
        pocklington(101, {3: 1})  # 3 does not divide 100


def test_all_n_up_to_limit_full_factorization() -> None:
    rng = random.Random(2)
    for n in range(5, LIMIT + 1, 2):
        verdict, ev = pocklington(n, factorize(n - 1), tries=30, rng=rng)
        if is_prime_td(n):
            assert verdict == PRIME, n
            assert verify_certificate(n, factorize(n - 1), ev)
        else:
            assert verdict in (COMPOSITE, UNKNOWN), n


def test_all_n_up_to_limit_partial_factorization() -> None:
    rng = random.Random(3)
    unknown = 0
    for n in range(5, LIMIT + 1, 2):
        part = smallest_sufficient_part(n)
        assert factored_part(part) ** 2 > n
        verdict, ev = pocklington(n, part, tries=30, rng=rng)
        if is_prime_td(n):
            assert verdict == PRIME, n
            assert verify_certificate(n, part, ev)
        else:
            assert verdict != PRIME, n
            unknown += verdict == UNKNOWN
            if "factor" in ev:
                assert n % ev["factor"] == 0 and 1 < ev["factor"] < n
    assert unknown < 50


def test_bls_cube_root_variant() -> None:
    rng = random.Random(4)
    for n in range(5, 30_000, 2):
        part = smallest_sufficient_part(n, cube=True)
        verdict, ev = bls_cube_root_test(n, part, tries=30, rng=rng)
        if is_prime_td(n):
            assert verdict == PRIME, n
        else:
            assert verdict != PRIME, n
            if "factor" in ev:
                assert n % ev["factor"] == 0 and 1 < ev["factor"] < n, (n, ev)


def test_certificate_rejects_wrong_data() -> None:
    n = 1000003
    assert not verify_certificate(n, {166667: 1}, {166667: n - 1})  # (n-1)^6 = 1
    assert not verify_certificate(n, {2: 1, 3: 1}, {2: 2, 3: 2})  # F too small
    assert not verify_certificate(1000001, {2: 1}, {2: 3})


def test_carmichael_and_strong_pseudoprimes_never_proved() -> None:
    rng = random.Random(5)
    for n in CARMICHAEL + STRONG_PSP:
        part = smallest_sufficient_part(n)
        verdict, ev = pocklington(n, part, tries=30, rng=rng)
        assert verdict in (COMPOSITE, UNKNOWN), n


def test_proth_and_large_primes() -> None:
    rng = random.Random(6)
    n = 3 * 2**534 + 1  # 162 digits, n - 1 = 3 * 2^534
    verdict, ev = pocklington(n, {2: 534}, rng=rng)
    assert verdict == PRIME and verify_certificate(n, {2: 534}, ev)
    # Build primes n = 2 k q + 1 from a known large prime q, as in Maurer's method.
    found = 0
    for q in (M127, M521, M607):
        for k in range(1, 4000):
            n = 2 * k * q + 1
            if probably_prime(n):
                verdict, ev = pocklington(n, {q: 1}, rng=rng)
                assert verdict == PRIME and verify_certificate(n, {q: 1}, ev)
                found += 1
                break
    assert found == 3


def test_large_composites_never_proved() -> None:
    rng = random.Random(7)
    checked = 0
    for k in range(1, 300):
        n = 2 * k * M521 + 1
        if probably_prime(n):
            continue
        verdict, _ = pocklington(n, {M521: 1}, tries=5, rng=rng)
        assert verdict in (COMPOSITE, UNKNOWN)
        checked += 1
    assert checked > 250
    # Squares of large primes: n - 1 = (p - 1)(p + 1) has a large power of 2.
    p = 3 * 2**534 + 1
    for n, part in [
        (M521**2, {2: 522}),
        (M607**2, {2: 608}),
        (p * p, {2: 535, 3: 1}),
    ]:
        assert (n - 1) % factored_part(part) == 0 and factored_part(part) ** 2 > n
        assert pocklington(n, part, rng=rng)[0] == COMPOSITE


def test_random_large_inputs_against_probable_prime() -> None:
    rng = random.Random(8)
    for _ in range(300):
        n = rng.randrange(10**9, 10**11) | 1
        part = smallest_sufficient_part(n)
        verdict, ev = pocklington(n, part, tries=30, rng=rng)
        if is_prime_td(n):
            assert verdict == PRIME
        else:
            assert verdict != PRIME
