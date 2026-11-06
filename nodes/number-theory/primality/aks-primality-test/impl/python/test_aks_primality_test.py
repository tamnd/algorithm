# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aks-primality-test/. The authors are listed in prov/JR8RT8.jsonl.

import math
import random

from aks_primality_test import (
    aks,
    euler_phi,
    integer_root,
    is_perfect_power,
    lg_squared_floor,
    power_x_plus_a,
    smallest_r,
    step_bound,
)


def is_prime_td(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def naive_power(a: int, n: int, r: int) -> list[int]:
    """(X + a)^n mod (X^r - 1, n) by n multiplications by X + a."""
    f = [0] * r
    f[0] = 1 % n
    for _ in range(n):
        g = [0] * r
        for i, c in enumerate(f):
            g[i] = (g[i] + a * c) % n
            g[(i + 1) % r] = (g[(i + 1) % r] + c) % n
        f = g
    return f


def order(n: int, r: int) -> int:
    x, k = n % r, 1
    while x != 1:
        x = x * n % r
        k += 1
    return k


def test_small_against_trial_division() -> None:
    for n in range(0, 1000):
        assert aks(n) == is_prime_td(n), n


def test_special_inputs() -> None:
    assert [aks(n) for n in (0, 1, 2, 3, 4)] == [False, False, True, True, False]
    for n in (2**10, 3**7, 5**5, 7**4, 101**2, 1009**3, 2**31 - 2, 10**6):
        assert not aks(n), n  # even numbers and prime powers
    for n in (561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 62745, 825265):
        assert not aks(n), n  # Carmichael numbers
    for n in (2047, 3277, 4033, 4681, 8321, 1373653, 25326001, 3215031751):
        assert not aks(n), n  # strong pseudoprimes to small bases
    for n in (7919, 65537, 104729, 1000003):
        assert aks(n), n


def test_random_against_trial_division() -> None:
    rng = random.Random(1)
    for _ in range(20):
        n = rng.randrange(2, 2 * 10**5)
        assert aks(n) == is_prime_td(n), n


def test_large_composites() -> None:
    # No factor below r and not perfect powers: rejected at line L8.
    for n in (
        (10**9 + 7) * (10**9 + 9),
        3825123056546413051,
    ):
        assert not aks(n), n
    rng = random.Random(2)
    primes = [p for p in range(10**5, 10**5 + 3000) if is_prime_td(p)]
    for _ in range(5):
        p, q = rng.sample(primes, 2)
        assert not aks(p * q), (p, q)


def test_congruence_holds_for_large_primes() -> None:
    # A full run on these primes is too slow in Python; check some values of a.
    for p, values in ((10**12 + 39, (1, 2, 3)), (2**61 - 1, (1,))):
        r = smallest_r(p)
        for a in values:
            f = power_x_plus_a(a, p, r)
            target = [0] * r
            target[0] = a
            target[p % r] += 1
            assert f == target


def test_huge_perfect_powers() -> None:
    # Numbers of several hundred digits stop at line L2 before the search for r.
    p = 2**521 - 1  # a Mersenne prime of 157 digits
    q = 10**100 + 267  # a prime of 101 digits
    for n in (p**2, p**3, q**5, (p * q) ** 2, 3**700):
        assert not aks(n)


def test_helpers() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n, r = rng.randrange(2, 300), rng.randrange(2, 30)
        a = rng.randrange(0, n)
        assert power_x_plus_a(a, n, r) == naive_power(a, n, r), (a, n, r)
    for n in range(0, 3000):
        for b in (1, 2, 3, 5):
            x = integer_root(n, b)
            assert x**b <= n < (x + 1) ** b
    big = rng.randrange(10**50, 10**51)
    assert integer_root(big**7, 7) == big and integer_root(big**7 - 1, 7) == big - 1
    assert is_perfect_power(big**3) and not is_perfect_power(big**3 + 1)
    assert [n for n in range(50) if is_perfect_power(n)] == [4, 8, 9, 16, 25, 27, 32, 36, 49]
    for r in range(1, 500):
        assert euler_phi(r) == sum(1 for i in range(1, r + 1) if math.gcd(i, r) == 1)
    assert lg_squared_floor(2**61 - 1) == 3720  # floats round lg n up to 61 here
    assert lg_squared_floor(2**61) == 3721
    for n in range(2, 3000):
        assert lg_squared_floor(n) == math.floor(math.log2(n) ** 2)
        r = smallest_r(n)
        k = lg_squared_floor(n)
        assert math.gcd(r, n) == 1 and order(n, r) > k
        assert all(math.gcd(s, n) > 1 or order(n, s) <= k for s in range(2, r))
        if n > r:
            assert step_bound(n, r) == math.floor(math.sqrt(euler_phi(r)) * math.log2(n))


def test_worked_example() -> None:
    assert smallest_r(31) == 29 and step_bound(31, 29) == 26
    for a in range(1, 27):
        f = power_x_plus_a(a, 31, 29)
        assert f == [a, 0, 1] + [0] * 26  # X^31 = X^2 mod X^29 - 1
    n = 74513  # 269 * 277, the least composite that reaches line L8
    assert smallest_r(n) == 263 and step_bound(n, 263) == 261 and n % 263 == 84
    f = power_x_plus_a(1, n, 263)
    assert f[:3] == [54070, 51917, 12374] and all(f)
