# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermat-primality-test/. The authors are listed in prov/8TFPRS.jsonl.

import math
import random
from fractions import Fraction

from fermat_primality_test import fermat_primality_test, fermat_test_bases, is_fermat_witness

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


def is_carmichael(n: int) -> bool:
    """Korselt's criterion, from a trial-division factorization."""
    if n < 3 or n % 2 == 0:
        return False
    f = factorize(n)
    return len(f) >= 2 and all(e == 1 for e in f.values()) and all((n - 1) % (p - 1) == 0 for p in f)


PRIMES_TD = [n for n in range(LIMIT + 1) if trial_division_is_prime(n)]
PRIME_SET = set(PRIMES_TD)

MERSENNE_521 = 2**521 - 1
MERSENNE_607 = 2**607 - 1
MERSENNE_1279 = 2**1279 - 1  # 386 decimal digits
BIG_PRIMES = [2**61 - 1, 2**127 - 1, 2**255 - 19, 2**256 - 189, 10**100 + 267, MERSENNE_521, MERSENNE_607, MERSENNE_1279]
BIG_COMPOSITES = [
    MERSENNE_521 * MERSENNE_607,
    MERSENNE_607 * MERSENNE_1279,  # 569 decimal digits
    (10**100 + 267) ** 2,
    2**1277 - 1,  # composite (Lucas-Lehmer), no factor known
    10**300 + 1,
    3**400,
]
# A Carmichael number (6t + 1)(12t + 1)(18t + 1) with three prime factors of 30 digits.
T = 10**29 + 18555
CHERNICK = (6 * T + 1) * (12 * T + 1) * (18 * T + 1)
CARMICHAEL_SMALL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361]
# Strong pseudoprimes to the first prime bases (they are also Fermat pseudoprimes to them).
STRONG_PSP = {
    2047: [2],
    1373653: [2, 3],
    25326001: [2, 3, 5],
    3215031751: [2, 3, 5, 7],
    2152302898747: [2, 3, 5, 7, 11],
    3474749660383: [2, 3, 5, 7, 11, 13],
    341550071728321: [2, 3, 5, 7, 11, 13, 17],
    3825123056546413051: [2, 3, 5, 7, 11, 13, 17, 19, 23],
    318665857834031151167461: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37],
}


def test_example_341() -> None:
    assert pow(2, 340, 341) == 1
    assert pow(3, 340, 341) == 56
    assert fermat_test_bases(341, [2]) is True
    assert fermat_test_bases(341, [3]) is False
    assert is_fermat_witness(3, 341) and not is_fermat_witness(2, 341)
    liars = [a for a in range(1, 341) if pow(a, 340, 341) == 1]
    assert len(liars) == 100
    assert sum(1 for a in range(1, 341) if math.gcd(a, 341) == 1) == 300


def test_small_and_even() -> None:
    rng = random.Random(1)
    assert [fermat_primality_test(n, 5, rng) for n in range(5)] == [False, False, True, True, False]
    for n in range(4, 2000, 2):
        assert fermat_primality_test(n, 5, rng) is False


def test_all_n_up_to_limit_against_trial_division() -> None:
    rng = random.Random(2024)
    passed_composites = []
    for n in range(LIMIT + 1):
        got = fermat_primality_test(n, 4, rng)
        if n in PRIME_SET:
            assert got is True, n
        elif got:
            passed_composites.append(n)
    # One-sided error: only composites can be wrong, and with 4 random rounds
    # only Fermat pseudoprimes to all four bases can pass. Most are Carmichael numbers.
    for n in passed_composites:
        assert n % 2 == 1 and not trial_division_is_prime(n)
    assert len(passed_composites) <= 20


def test_fixed_bases_match_definition() -> None:
    bases = [2, 3, 5]
    for n in range(5, LIMIT + 1, 2):
        want = all(pow(a, n - 1, n) == 1 for a in bases if a % n not in (0, 1, n - 1))
        assert fermat_test_bases(n, bases) == want
    base2 = [n for n in range(3, LIMIT, 2) if n not in PRIME_SET and pow(2, n - 1, n) == 1]
    assert len(base2) == 78 and base2[:3] == [341, 561, 645]


def test_liar_count_formula_and_half_bound() -> None:
    for n in range(9, 1500, 2):
        if n in PRIME_SET:
            continue
        liars = sum(1 for a in range(1, n) if pow(a, n - 1, n) == 1)
        f = factorize(n)
        assert liars == math.prod(math.gcd(n - 1, p - 1) for p in f)
        phi = math.prod((p - 1) * p ** (e - 1) for p, e in f.items())
        if is_carmichael(n):
            assert liars == phi
        else:
            assert 2 * liars <= phi
            assert Fraction(liars - 2, n - 3) < Fraction(1, 2)


def test_carmichael_numbers_pass_coprime_bases() -> None:
    computed = [n for n in range(3, LIMIT + 1) if n not in PRIME_SET and is_carmichael(n)]
    assert computed == CARMICHAEL_SMALL
    rng = random.Random(7)
    for n in CARMICHAEL_SMALL:
        for _ in range(50):
            a = rng.randint(2, n - 2)
            assert (pow(a, n - 1, n) == 1) == (math.gcd(a, n) == 1)


def test_one_round_frequency_on_341() -> None:
    rng = random.Random(3)
    trials = 4000
    hits = sum(fermat_primality_test(341, 1, rng) for _ in range(trials))
    assert abs(hits / trials - 98 / 338) < 0.03


def test_large_primes_and_composites() -> None:
    rng = random.Random(4)
    for p in BIG_PRIMES:
        assert fermat_primality_test(p, 5, rng) is True
    for c in BIG_COMPOSITES:
        assert fermat_primality_test(c, 5, rng) is False


def test_large_carmichael_fools_the_test() -> None:
    rng = random.Random(5)
    # Each round errs with probability above 1 - 10^-29.
    assert fermat_primality_test(CHERNICK, 20, rng) is True
    assert CHERNICK % (6 * T + 1) == 0


def test_strong_pseudoprimes_to_small_bases() -> None:
    rng = random.Random(6)
    for n, bases in STRONG_PSP.items():
        assert fermat_test_bases(n, bases) is True
        if not is_carmichael_big(n):
            assert fermat_primality_test(n, 30, rng) is False


def is_carmichael_big(n: int) -> bool:
    known = {
        3825123056546413051: [149491, 747451, 34233211],
        318665857834031151167461: [399165290221, 798330580441],
    }
    fs = known.get(n) or list(factorize(n))
    assert math.prod(fs) == n
    return all((n - 1) % (p - 1) == 0 for p in fs)


def test_random_odd_numbers_against_trial_division() -> None:
    rng = random.Random(8)
    for _ in range(600):
        n = rng.randrange(10**9, 10**10) | 1
        got = fermat_primality_test(n, 10, rng)
        if trial_division_is_prime(n):
            assert got is True
        elif got:
            assert pow(2, n - 1, n) == 1
