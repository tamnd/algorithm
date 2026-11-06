# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apr-cl-primality-test/. The authors are listed in prov/MW7HYF.jsonl.

import random
from math import gcd, lcm, prod

import pytest

from apr_cl_primality_test import (
    T_TABLE,
    aprcl,
    candidate_primes,
    divisor_search,
    extra_check,
    gauss_jacobi_check,
    jacobi_power,
    jacobi_sums,
    jacobi_symbol,
    make_plan,
    plan,
    primitive_root,
    trace,
    unit_w,
)

LIMIT = 100_000

CARMICHAEL = [
    561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041,
    46657, 52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401,
    172081, 188461, 252601, 278545, 294409, 314821, 334153, 340561, 399001,
    410041, 449065, 488881, 512461,
]
# Strong pseudoprimes: to base 2, to bases 2 and 3, to 2, 3, 5, and so on.
STRONG_PSEUDOPRIMES = [
    2047, 3277, 4033, 4681, 8321, 1373653, 25326001, 3215031751,
    2152302898747, 3474749660383, 341550071728321, 3825123056546413051,
    318665857834031151167461, 3317044064679887385961981,
]


def sieve(limit: int) -> bytearray:
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(is_p[i * i :: i]))
    return is_p


def trial_division_is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def miller_rabin(n: int, rng: random.Random, rounds: int = 30) -> bool:
    """A reference probable prime test with random bases."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(n: int, rng: random.Random) -> int:
    while not miller_rabin(n, rng):
        n += 1
    return n


def test_matches_sieve_up_to_limit() -> None:
    is_p = sieve(LIMIT)
    for n in range(LIMIT + 1):
        assert aprcl(n) is bool(is_p[n]), n


def test_small_inputs_and_even_numbers() -> None:
    assert aprcl(-7) is False
    assert aprcl(0) is False
    assert aprcl(1) is False
    assert aprcl(2) is True
    assert aprcl(3) is True
    assert aprcl(4) is False
    for n in (2**64, 2**127, 10**200, 2 * (2**127 - 1)):
        assert aprcl(n) is False


def test_prime_powers() -> None:
    rng = random.Random(1)
    p100 = next_prime(10**99, rng)
    for base, top in ((3, 40), (5, 30), (7, 25), (31, 12), (65537, 5)):
        for e in range(2, top):
            assert aprcl(base**e) is False
    assert aprcl(p100**2) is False
    assert aprcl((2**127 - 1) ** 2) is False
    assert aprcl(1000003**3) is False


def test_carmichael_numbers() -> None:
    for n in CARMICHAEL:
        assert aprcl(n) is False, n
    # A Chernick number (6k+1)(12k+1)(18k+1) of about 180 digits.
    rng = random.Random(2)
    k = 10**59 + 3
    while not all(miller_rabin(a * k + 1, rng) for a in (6, 12, 18)):
        k += 1
    n = (6 * k + 1) * (12 * k + 1) * (18 * k + 1)
    assert pow(2, n - 1, n) == 1
    assert aprcl(n) is False


def test_strong_pseudoprimes() -> None:
    for n in STRONG_PSEUDOPRIMES:
        assert aprcl(n) is False, n


def test_large_primes() -> None:
    rng = random.Random(3)
    for n in (
        2**61 - 1,
        2**89 - 1,
        2**127 - 1,
        10**100 + 267,
        2**521 - 1,
        next_prime(10**199, rng),
    ):
        assert aprcl(n) is True, n


def test_large_composites() -> None:
    rng = random.Random(4)
    p = next_prime(rng.randrange(10**149, 10**150), rng)
    q = next_prime(rng.randrange(10**149, 10**150), rng)
    assert aprcl(p * q) is False
    assert aprcl(2**523 - 1) is False
    assert aprcl(2**512 + 1) is False
    assert aprcl((2**127 - 1) * (2**89 - 1)) is False
    for _ in range(25):
        n = rng.randrange(10**299, 10**300) | 1
        if not miller_rabin(n, rng):
            assert aprcl(n) is False


def test_random_against_miller_rabin() -> None:
    rng = random.Random(5)
    seen_prime = 0
    for digits in (12, 20, 30, 45, 60):
        for _ in range(30):
            n = rng.randrange(10 ** (digits - 1), 10**digits)
            if rng.random() < 0.5:
                n = next_prime(n, rng)
            expected = miller_rabin(n, rng)
            seen_prime += expected
            assert aprcl(n) is expected, n
    assert seen_prime > 50


def test_plan_conditions() -> None:
    for digits in (1, 5, 30, 100, 300, 580):
        n = 10**digits + 1
        primes, s, t = plan(n)
        assert s == prod(primes) and s * s > n
        assert prod(primes[:-1]) ** 2 <= n
        assert t == lcm(*(q - 1 for q in primes))
        assert all(q == 2 or q % 4 == 3 for q in primes)
        assert all(t % (q - 1) == 0 for q in primes)
    with pytest.raises(ValueError):
        plan(10**700)
    with pytest.raises(ValueError):
        make_plan(10**6, (2, 3, 7))
    with pytest.raises(ValueError):
        make_plan(100, (2, 5, 7))


def test_table_is_increasing_and_t_has_one_factor_two() -> None:
    assert list(T_TABLE) == sorted(T_TABLE)
    sizes = []
    for t in T_TABLE:
        assert t % 2 == 0 and t % 4 != 0
        primes = candidate_primes(t)
        assert all(trial_division_is_prime(q) for q in primes if q < 10**6)
        sizes.append(prod(primes))
    assert sizes == sorted(sizes)
    assert sizes[-1] > 10**295


def test_units_w_not_divisible_by_p() -> None:
    for p, k in ((3, 4), (5, 3), (7, 2), (11, 2), (13, 2), (17, 1), (19, 1), (23, 1)):
        for e in range(1, k + 1):
            assert unit_w(p**e, p) % p != 0
    assert unit_w(3, 3) == 2 and unit_w(5, 5) == 1 and unit_w(9, 3) == 5


def test_jacobi_sums_have_norm_q() -> None:
    for q in candidate_primes(450450):
        if q > 3:
            for p in jacobi_sums(q):
                assert gauss_jacobi_check(q, p), (q, p)


def test_jacobi_sum_sizes() -> None:
    for q in (7, 11, 31, 43, 211, 2311):
        sums = jacobi_sums(q)
        for p, coeffs in sums.items():
            m = len(coeffs)
            assert (q - 1) % m == 0 and ((q - 1) // m) % p != 0
            assert sum(coeffs) == q - 2


def test_root_of_unity_for_primes() -> None:
    """For a prime n, S = chi(n)^(-w n): h = -w n ind(n) mod m."""
    rng = random.Random(6)
    for _ in range(40):
        n = next_prime(rng.randrange(10**6, 10**30), rng)
        for q in (7, 11, 31, 43, 71, 127, 211):
            if n % q == 0:
                continue
            g = primitive_root(q)
            ind = next(i for i in range(q - 1) if pow(g, i, q) == n % q)
            for p, coeffs in jacobi_sums(q).items():
                if p == 2:
                    continue
                m = len(coeffs)
                expected = (-unit_w(m, p) * n * ind) % m
                assert jacobi_power(n, q, p) == expected


def test_extra_check() -> None:
    is_p = sieve(20_000)
    uses = 0
    for n in range(5, 20_000, 2):
        if not is_p[n]:
            continue
        for p in (3, 5, 7):
            if n % p and pow(n, p - 1, p * p) == 1:
                uses += 1
                assert extra_check(n, p, set()) is True
        if n % 4 == 1:
            assert extra_check(n, 2, set()) is True
    assert uses > 100
    assert extra_check(25 * 41, 2, set()) is False
    assert extra_check(49 * 49, 2, set()) is False


def test_divisor_search_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(300):
        primes = tuple(sorted(rng.sample([3, 7, 11, 19, 23, 31, 43, 47], 3))) + (2,)
        s = prod(primes)
        t = lcm(*(q - 1 for q in primes))
        n = rng.randrange(3, s * s)
        found = None
        for i in range(1, t):
            r = pow(n, i, s)
            if 1 < r < n and n % r == 0:
                found = r
                break
        assert divisor_search(n, s, t) == found


def test_divisor_search_finds_planted_factor() -> None:
    """If a prime r is a power n^i modulo s, the search finds a factor."""
    s, t = 2 * 3 * 7 * 11 * 31, 30
    hits = 0
    for r in (13, 17, 19, 29, 37, 41, 43, 61, 67, 71):
        for c in range(r + 2, 2 * s, 2):
            n = r * c
            if n < s * s and gcd(n, s * t) == 1:
                if any(pow(n, i, s) == r for i in range(1, t)):
                    hits += 1
                    assert divisor_search(n, s, t) is not None
    assert hits > 50


def test_jacobi_symbol() -> None:
    for n in range(3, 400, 2):
        for a in range(0, 60):
            if gcd(a, n) > 1:
                assert jacobi_symbol(a, n) == 0
            elif trial_division_is_prime(n):
                assert jacobi_symbol(a, n) == (1 if pow(a, (n - 1) // 2, n) == 1 else -1)


def test_worked_example() -> None:
    rep = trace(1999)
    assert rep.primes == (2, 3, 7, 11) and rep.s == 462 and rep.t == 30
    assert jacobi_sums(7)[3] == (2, 0, 3)
    assert jacobi_sums(11)[5] == (2, 4, 0, 1, 2)
    assert primitive_root(7) == 3 and primitive_root(11) == 2
    assert rep.roots == {(3, 7): 1, (5, 11): 3}
    assert rep.signs == {3: 1, 7: 1, 11: -1}
    assert pow(1999, 2, 9) == 1 and pow(1999, 4, 25) == 1
    assert rep.factor is None and aprcl(1999) is True
    assert 1999 % 462 == 151
    bad = trace(1891)
    assert bad.roots[(3, 7)] == -1 and aprcl(1891) is False
