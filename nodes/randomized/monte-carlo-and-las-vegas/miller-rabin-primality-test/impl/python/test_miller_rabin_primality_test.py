# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-rabin-primality-test/. The authors are listed in prov/HSYVA5.jsonl.

import random
from fractions import Fraction
from math import gcd

from miller_rabin_primality_test import decompose, is_strong_probable_prime, miller_rabin, strong_sequence

LIMIT = 2000


def sieve(n: int) -> list[bool]:
    is_p = [False, False] + [True] * (n - 1)
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return is_p


IS_PRIME = sieve(10000)


def factor(n: int) -> list[int]:
    """Prime factors with multiplicity, by trial division."""
    out, p = [], 2
    while p * p <= n:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def phi(n: int) -> int:
    out = n
    for p in set(factor(n)):
        out = out // p * (p - 1)
    return out


def v2(x: int) -> int:
    return (x & -x).bit_length() - 1


def odd_part(x: int) -> int:
    return x >> v2(x)


def strong_liar_by_definition(n: int, a: int) -> bool:
    """a^d = 1 or a^(2^j d) = -1 for some 0 <= j < s, straight from the definition."""
    s, d = decompose(n)
    if pow(a, d, n) == 1:
        return True
    return any(pow(a, 2**j * d, n) == n - 1 for j in range(s))


def jacobi_by_factoring(a: int, n: int) -> int:
    """The Jacobi symbol as a product of Legendre symbols from Euler's criterion."""
    out = 1
    for p in factor(n):
        r = pow(a, (p - 1) // 2, p)
        out *= 0 if r == 0 else (1 if r == 1 else -1)
    return out


def euler_liar(a: int, n: int) -> bool:
    j = jacobi_by_factoring(a, n)
    return j != 0 and pow(a, (n - 1) // 2, n) == j % n


def monier_count(n: int) -> int:
    """Monier's formula for the number of strong liars of an odd composite n."""
    primes = sorted(set(factor(n)))
    k = len(primes)
    nu = min(v2(p - 1) for p in primes)
    prod = 1
    for p in primes:
        prod *= gcd(odd_part(n - 1), odd_part(p - 1))
    return (1 + (2 ** (k * nu) - 1) // (2**k - 1)) * prod


def odd_composites(limit: int) -> list[int]:
    return [n for n in range(9, limit, 2) if not IS_PRIME[n]]


def test_primes_pass_every_base() -> None:
    for n in range(5, LIMIT, 2):
        if IS_PRIME[n]:
            assert all(is_strong_probable_prime(n, a) for a in range(1, n))


def test_small_inputs() -> None:
    rng = random.Random(0)
    assert [n for n in range(0, 30) if miller_rabin(n, 5, rng)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


LIAR_COUNTS = {n: sum(1 for a in range(1, n) if is_strong_probable_prime(n, a)) for n in odd_composites(LIMIT)}


def test_liars_match_definition() -> None:
    for n in odd_composites(700):
        liars = [a for a in range(1, n) if is_strong_probable_prime(n, a)]
        assert liars == [a for a in range(1, n) if strong_liar_by_definition(n, a)]


def test_liar_counts_match_monier() -> None:
    for n, count in LIAR_COUNTS.items():
        assert count == monier_count(n)


def test_quarter_bound_and_where_it_is_reached() -> None:
    reached = []
    for n, count in LIAR_COUNTS.items():
        ratio = Fraction(count, phi(n))
        if n == 9:
            assert count == 2 and phi(9) == 6  # 2 > 6/4, the one exception
            assert 4 * count <= n - 1
            continue
        assert ratio <= Fraction(1, 4)
        if ratio == Fraction(1, 4):
            reached.append(n)
        # Over the bases {2, ..., n-2} used by the algorithm.
        assert Fraction(count - 2, n - 3) <= Fraction(1, 4)
    assert reached == [15, 91, 703, 1891]


def test_strong_liars_are_euler_liars() -> None:
    for n in odd_composites(800):
        strong = {a for a in range(1, n) if is_strong_probable_prime(n, a)}
        euler = {a for a in range(1, n) if euler_liar(a, n)}
        assert strong <= euler
        if n % 4 == 3:
            assert strong == euler
    strong45 = {a for a in range(1, 45) if is_strong_probable_prime(45, a)}
    euler45 = {a for a in range(1, 45) if euler_liar(a, 45)}
    assert sorted(euler45 - strong45) == [19, 26]


CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911]


def test_carmichael_numbers() -> None:
    # Korselt's criterion by brute force: squarefree, composite, p - 1 | n - 1.
    found = []
    for n in range(3, 10000, 2):
        f = factor(n)
        if len(f) >= 2 and len(set(f)) == len(f) and all((n - 1) % (p - 1) == 0 for p in f):
            found.append(n)
    assert found == CARMICHAEL
    expected = {561: 10, 1105: 30, 1729: 162, 2465: 70, 2821: 270, 6601: 330, 8911: 1782}
    for n in CARMICHAEL:
        # The Fermat test passes for every base coprime to n.
        assert all(pow(a, n - 1, n) == 1 for a in range(1, n) if gcd(a, n) == 1)
        liars = sum(1 for a in range(1, n) if is_strong_probable_prime(n, a))
        assert liars == expected[n] == monier_count(n)
        assert 4 * liars <= phi(n)


def test_traces() -> None:
    assert decompose(561) == (4, 35)
    assert strong_sequence(561, 2) == [263, 166, 67, 1, 1]
    assert not is_strong_probable_prime(561, 2)
    assert strong_sequence(221, 174)[:2] == [47, 220]
    assert is_strong_probable_prime(221, 174)
    assert strong_sequence(221, 137) == [188, 205, 35]
    assert not is_strong_probable_prime(221, 137)
    assert strong_sequence(97, 5) == [28, 8, 64, 22, 96, 1]
    assert pow(2, 1023, 2047) == 1 and is_strong_probable_prime(2047, 2)
    assert min(n for n in odd_composites(2100) if is_strong_probable_prime(n, 2)) == 2047
    assert strong_sequence(1373653, 2)[:2] == [890592, 1373652]
    assert is_strong_probable_prime(1373653, 2) and is_strong_probable_prime(1373653, 3)
    assert 1373653 == 829 * 1657


def test_random_rounds() -> None:
    rng = random.Random(42)
    for n in range(2, LIMIT):
        assert miller_rabin(n, 20, rng) == IS_PRIME[n]
    # On 561 a random base from {2, ..., 559} is a liar with probability 8/558.
    trials = 20000
    passed = sum(miller_rabin(561, 1, rng) for _ in range(trials))
    assert abs(passed / trials - 8 / 558) < 0.006
