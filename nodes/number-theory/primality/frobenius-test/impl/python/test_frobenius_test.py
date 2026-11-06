# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frobenius-test/. The authors are listed in prov/3WFYQX.jsonl.

import math
import random

import pytest

from frobenius import _mul
from frobenius_test import (
    TRIAL_BOUND,
    choose_parameters,
    frobenius_test,
    is_probable_prime,
    jacobi,
    power_of_x,
    primes_up_to,
    quadratic_frobenius,
)

LIMIT = 10**5
MERSENNE_PRIME_EXPONENTS = (2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279)


def sieve(m: int) -> bytearray:
    is_p = bytearray([1]) * (m + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, math.isqrt(m) + 1):
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(range(i * i, m + 1, i)))
    return is_p


def reference_is_probable_prime(n: int, rng: random.Random, rounds: int = 20) -> bool:
    """Miller-Rabin with random bases, used only as a reference for large n."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
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


def allowed(n: int, a: int, b: int) -> bool:
    delta = a * a - 4 * b
    return math.gcd(delta * b, n) == 1 and jacobi(delta, n) == -1 and jacobi(b, n) == 1


def test_against_trial_division_up_to_limit() -> None:
    is_p = sieve(LIMIT)
    rng = random.Random(1)
    for n in range(LIMIT + 1):
        assert frobenius_test(n, rng) == bool(is_p[n]), n


def test_quadratic_step_against_trial_division() -> None:
    # With trial division only by 2, every odd non-square n >= 9 reaches the
    # Frobenius step. Primes must pass; with this seed no composite does.
    is_p = sieve(LIMIT)
    rng = random.Random(2)
    for n in range(LIMIT + 1):
        assert frobenius_test(n, rng, bound=2) == bool(is_p[n]), n


def test_small_and_special_values() -> None:
    rng = random.Random(3)
    assert [frobenius_test(n, rng) for n in range(6)] == [False, False, True, True, False, True]
    for n in (2**40, 3**30, 50021**2, 1000003**2, 2**61 * 3):
        assert not frobenius_test(n, rng), n
    with pytest.raises(ValueError):
        frobenius_test(101, rng, bound=1)
    with pytest.raises(ValueError):
        jacobi(3, 10)


def test_jacobi_against_euler_criterion() -> None:
    for p in primes_up_to(400)[1:]:
        for a in range(-50, 3 * p):
            e = pow(a, (p - 1) // 2, p)
            assert jacobi(a, p) == (0 if a % p == 0 else (1 if e == 1 else -1))
    for n in range(1, 200, 2):
        for a in range(n):
            j = 1
            m, d = n, 3
            while m > 1:  # multiply the symbols of the prime factors
                while d * d <= m and m % d:
                    d += 2
                q = m if d * d > m else d
                m //= q
                e = pow(a, (q - 1) // 2, q)
                j *= 0 if a % q == 0 else (1 if e == 1 else -1)
            assert jacobi(a, n) == j


def test_power_of_x_against_repeated_products() -> None:
    rng = random.Random(4)
    for _ in range(1000):
        n, e = rng.randrange(2, 200), rng.randrange(0, 300)
        a, b = rng.randrange(-5, n), rng.randrange(-5, n)
        r = (1 % n, 0)
        for _ in range(e):
            r = _mul(r, (0, 1), n, a, b)
        assert power_of_x(e, n, a, b) == r


def test_primes_always_pass_every_allowed_polynomial() -> None:
    for p in (11, 13, 97, 101):
        for a in range(1, p):
            for b in range(1, p):
                if allowed(p, a, b):
                    assert quadratic_frobenius(p, a, b), (p, a, b)
                    assert power_of_x(p, p, a, b) == (a % p, p - 1)  # x^p = a - x


def test_worked_examples() -> None:
    # n = 97 and x^2 - x + 2: x^49 = 83, 83^2 = 2, and x^147 = 69, 8, 64, 22, 96.
    assert allowed(97, 1, 2)
    assert power_of_x(49, 97, 1, 2) == (83, 0) and 83 * 83 % 97 == 2
    z = power_of_x(147, 97, 1, 2)
    chain = []
    for _ in range(5):
        chain.append(z[0])
        z = ((z[0] * z[0] - 2 * z[1] * z[1]) % 97, (2 * z[0] * z[1] + z[1] * z[1]) % 97)
    assert chain == [69, 8, 64, 22, 96] and 97 * 97 - 1 == 2**6 * 147
    # 5777 = 53 * 109 passes for x^2 - x - 1 but fails for most polynomials.
    assert 5777 == 53 * 109 and allowed(5777, 1, -1)
    assert quadratic_frobenius(5777, 1, -1)
    rng = random.Random(5)
    passed = total = 0
    for _ in range(2000):
        params = choose_parameters(5777, rng)
        if isinstance(params, int):
            assert 5777 % params == 0
            continue
        total += 1
        passed += quadratic_frobenius(5777, *params)
    assert passed <= total // 500
    # 35 has small factors; x^2 - x + 1 and x^2 + x + 1 are its only liars.
    liars = [(a, b) for a in range(1, 35) for b in range(1, 35) if allowed(35, a, b) and quadratic_frobenius(35, a, b)]
    assert liars == [(1, 1), (34, 1)]


def test_carmichael_and_strong_pseudoprimes() -> None:
    rng = random.Random(6)
    hard = [561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 825265, 321197185, 5394826801]
    hard += [2047, 3277, 4033, 4681, 8321, 1373653, 25326001, 3215031751, 2152302898747]
    hard += [3474749660383, 341550071728321, 3825123056546413051, 318665857834031151167461]
    hard += [5459, 5777, 10877, 16109, 18971, 22499, 24569, 25199, 40309, 58519, 75077, 97439]
    for n in hard:
        assert not any(frobenius_test(n, rng, bound=2) for _ in range(3)), n
        assert not frobenius_test(n, rng), n


def test_large_known_primes_and_composites() -> None:
    rng = random.Random(7)
    for p in MERSENNE_PRIME_EXPONENTS:
        assert is_probable_prime(2**p - 1, 2, rng), p
    assert is_probable_prime(10**100 + 267, 2, rng)
    for p in (67, 523, 1277):
        assert not frobenius_test(2**p - 1, rng), p  # composite, M_1277 has no known factor
    for k in (5, 6, 7, 8, 9, 10):
        assert not frobenius_test(2 ** (2**k) + 1, rng), k
    # A Carmichael number (6k + 1)(12k + 1)(18k + 1) of about 180 digits.
    k = 10**60
    while True:
        k += 1
        fs = (6 * k + 1, 12 * k + 1, 18 * k + 1)
        if all(reference_is_probable_prime(f, rng, 8) for f in fs):
            break
    n = fs[0] * fs[1] * fs[2]
    assert all(pow(base, n - 1, n) == 1 for base in (2, 3, 5, 7))
    assert not frobenius_test(n, rng)
    assert all(frobenius_test(f, rng) for f in fs)


def test_random_large_inputs() -> None:
    rng = random.Random(8)
    for digits in (20, 50, 100, 300):
        for _ in range(30):
            n = rng.randrange(10 ** (digits - 1), 10**digits) | 1
            assert frobenius_test(n, rng) == reference_is_probable_prime(n, rng)
    for _ in range(3):
        ps = []
        while len(ps) < 2:
            x = rng.randrange(10**149, 10**150) | 1
            if reference_is_probable_prime(x, rng):
                ps.append(x)
        assert frobenius_test(ps[0], rng) and frobenius_test(ps[1], rng)
        assert not frobenius_test(ps[0] * ps[1], rng)
        assert not frobenius_test(ps[0] ** 2, rng)
    assert TRIAL_BOUND == 50000
