# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solovay-strassen/. The authors are listed in prov/4S0832.jsonl.

import math
import random
from fractions import Fraction

from solovay_strassen import euler_test_bases, is_euler_witness, jacobi, solovay_strassen

LIMIT = 100_000


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


def jacobi_by_definition(a: int, n: int) -> int:
    """Product of Legendre symbols, each from Euler's criterion."""
    result = 1
    for p, e in factorize(n).items():
        r = pow(a, (p - 1) // 2, p)
        leg = 0 if a % p == 0 else (1 if r == 1 else -1)
        result *= leg**e
    return result


def euler_liars(n: int) -> list[int]:
    return [a for a in range(1, n) if math.gcd(a, n) == 1 and pow(a, (n - 1) // 2, n) == jacobi(a, n) % n]


PRIME_SET = {n for n in range(LIMIT + 1) if trial_division_is_prime(n)}

MERSENNE_521 = 2**521 - 1
MERSENNE_607 = 2**607 - 1
MERSENNE_1279 = 2**1279 - 1  # 386 decimal digits
BIG_PRIMES = [2**61 - 1, 2**127 - 1, 2**255 - 19, 3 * 2**534 + 1, MERSENNE_521, MERSENNE_607, MERSENNE_1279]
BIG_COMPOSITES = [
    MERSENNE_521 * MERSENNE_607,  # 339 decimal digits
    MERSENNE_607 * MERSENNE_1279,  # 569 decimal digits
    MERSENNE_521**2,
    2**1277 - 1,  # composite, no factor known
    3**401,
    10**300 + 1,
]
# A Carmichael number (6t + 1)(12t + 1)(18t + 1) with three prime factors of 30 digits.
T = 10**29 + 18555
CHERNICK = (6 * T + 1) * (12 * T + 1) * (18 * T + 1)
CARMICHAEL_SMALL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361]
# Smallest strong pseudoprimes to the first t prime bases.
STRONG_PSP = {
    2047: [2],
    1373653: [2, 3],
    25326001: [2, 3, 5],
    3215031751: [2, 3, 5, 7],
    2152302898747: [2, 3, 5, 7, 11],
    3474749660383: [2, 3, 5, 7, 11, 13],
    341550071728321: [2, 3, 5, 7, 11, 13, 17],
    3825123056546413051: [2, 3, 5, 7, 11, 13, 17, 19, 23],
}


def test_jacobi_matches_definition() -> None:
    for n in range(1, 400, 2):
        for a in range(-5, 2 * n + 3):
            assert jacobi(a, n) == jacobi_by_definition(a % n, n), (a, n)
    assert jacobi(13, 561) == -1 and jacobi(7, 561) == 1 and jacobi(2, 561) == 1


def test_example_561() -> None:
    assert pow(2, 280, 561) == 1 and not is_euler_witness(2, 561)
    assert pow(7, 280, 561) == 67 and is_euler_witness(7, 561)
    assert pow(13, 280, 561) == 1 and is_euler_witness(13, 561)
    liars = euler_liars(561)
    assert len(liars) == 80
    assert sum(1 for a in range(1, 561) if math.gcd(a, 561) == 1) == 320


def test_hac_example_65_and_91() -> None:
    assert euler_liars(65) == [1, 8, 14, 18, 47, 51, 57, 64]
    assert not is_euler_witness(9, 91)
    assert len(euler_liars(91)) == 18


def test_small_and_even() -> None:
    rng = random.Random(1)
    assert [solovay_strassen(n, 5, rng) for n in range(5)] == [False, False, True, True, False]
    for n in range(4, 2000, 2):
        assert solovay_strassen(n, 5, rng) is False


def test_zero_jacobi_pitfall() -> None:
    # 3^4 = 81 = 0 (mod 9) and (3/9) = 0: without line L6 the base 3 would pass.
    assert pow(3, 4, 9) == 0 and jacobi(3, 9) == 0
    assert is_euler_witness(3, 9) and is_euler_witness(6, 9)
    # The only Euler liars for 9 are 1 and 8, so every base in [2, 7] is a witness.
    assert euler_liars(9) == [1, 8]
    rng = random.Random(9)
    for _ in range(200):
        assert solovay_strassen(9, 1, rng) is False
    assert euler_test_bases(9, [3]) is False


def test_all_n_up_to_limit_against_trial_division() -> None:
    rng = random.Random(2024)
    passed_composites = []
    for n in range(LIMIT + 1):
        got = solovay_strassen(n, 4, rng)
        if n in PRIME_SET:
            assert got is True, n
        elif got:
            passed_composites.append(n)
    for n in passed_composites:
        assert n % 2 == 1 and not trial_division_is_prime(n)
    assert len(passed_composites) <= 10


def test_fixed_bases_match_definition() -> None:
    bases = [2, 3, 5, 7]
    for n in range(5, LIMIT + 1, 2):
        want = n in PRIME_SET
        if not want:
            want = all(
                math.gcd(a, n) == 1 and pow(a, (n - 1) // 2, n) == jacobi_by_definition(a, n) % n
                for a in bases
                if a % n not in (0, 1, n - 1)
            )
        assert euler_test_bases(n, bases) == want, n
    base2 = [n for n in range(3, LIMIT, 2) if n not in PRIME_SET and euler_test_bases(n, [2])]
    assert len(base2) == 36 and base2[:3] == [561, 1105, 1729]


def test_liars_form_subgroup_of_at_most_half() -> None:
    for n in range(9, 1200, 2):
        if n in PRIME_SET:
            continue
        liars = set(euler_liars(n))
        phi = sum(1 for a in range(1, n) if math.gcd(a, n) == 1)
        assert 2 * len(liars) <= phi
        assert phi % len(liars) == 0
        for a in list(liars)[:12]:
            for b in list(liars)[:12]:
                assert a * b % n in liars
        assert 1 in liars and n - 1 in liars
        assert Fraction(len(liars) - 2, n - 3) < Fraction(1, 2)
        strong = {a for a in range(1, n) if strong_probable(n, a)}
        fermat = {a for a in range(1, n) if pow(a, n - 1, n) == 1}
        assert strong <= liars <= fermat


def strong_probable(n: int, a: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def test_bound_attained_by_1729() -> None:
    liars = euler_liars(1729)
    assert 2 * len(liars) == sum(1 for a in range(1, 1729) if math.gcd(a, 1729) == 1) == 1296


def test_carmichael_numbers_are_caught() -> None:
    rng = random.Random(7)
    for n in CARMICHAEL_SMALL:
        assert solovay_strassen(n, 40, rng) is False
    assert solovay_strassen(CHERNICK, 40, rng) is False


def test_one_round_frequency_on_561() -> None:
    rng = random.Random(3)
    trials = 4000
    hits = sum(solovay_strassen(561, 1, rng) for _ in range(trials))
    assert abs(hits / trials - 78 / 558) < 0.03


def test_large_primes_and_composites() -> None:
    rng = random.Random(4)
    for p in BIG_PRIMES:
        assert solovay_strassen(p, 5, rng) is True
    for c in BIG_COMPOSITES:
        assert solovay_strassen(c, 5, rng) is False


def test_strong_pseudoprimes_to_small_bases() -> None:
    rng = random.Random(6)
    for n, bases in STRONG_PSP.items():
        assert all(strong_probable(n, a) for a in bases)
        # A strong pseudoprime base a is an Euler pseudoprime base a.
        assert euler_test_bases(n, bases) is True
        assert solovay_strassen(n, 40, rng) is False


def test_random_odd_numbers_against_trial_division() -> None:
    rng = random.Random(8)
    wrong: list[int] = []
    for _ in range(600):
        n = rng.randrange(10**9, 10**10) | 1
        got = solovay_strassen(n, 10, rng)
        if trial_division_is_prime(n):
            assert got is True
        else:
            if got:
                wrong.append(n)
    # Each composite passes 10 rounds with probability below 2^-10.
    assert len(wrong) <= 2
