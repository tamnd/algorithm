# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-rabin/. The authors are listed in prov/T1483D.jsonl.

import math
import random
from fractions import Fraction

from miller_rabin import (
    FIRST_12_PRIMES,
    is_prime_u64,
    is_strong_probable_prime,
    miller_rabin,
    miller_rabin_bases,
    split_power_of_two,
)

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


def strong_liar_count(n: int) -> int:
    """Monier's formula for the number of strong liars of an odd composite n."""
    f = factorize(n)
    _, d = split_power_of_two(n - 1)
    r = len(f)
    nu = min(split_power_of_two(p - 1)[0] for p in f)
    t = math.prod(math.gcd(d, p - 1) for p in f)
    return t * (1 + sum(2 ** (j * r) for j in range(nu)))


PRIME_SET = {n for n in range(LIMIT + 1) if trial_division_is_prime(n)}

BIG_PRIMES = [2**61 - 1, 2**127 - 1, 2**255 - 19, 2**256 - 189, 10**100 + 267, 2**521 - 1, 2**607 - 1, 2**1279 - 1]
BIG_COMPOSITES = [
    (2**521 - 1) * (2**607 - 1),
    (2**607 - 1) * (2**1279 - 1),  # 569 decimal digits
    (10**100 + 267) ** 2,
    2**1277 - 1,  # composite, no factor known
    10**300 + 1,
    3**400,
    (2**127 - 1) ** 3,
]
T = 10**29 + 18555
CHERNICK = (6 * T + 1) * (12 * T + 1) * (18 * T + 1)  # Carmichael, three 30-digit primes
CARMICHAEL_SMALL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633, 62745, 63973, 75361]
# psi_k: the smallest strong pseudoprime to all of the first k prime bases.
PSI = {
    1: 2047,
    2: 1373653,
    3: 25326001,
    4: 3215031751,
    5: 2152302898747,
    6: 3474749660383,
    7: 341550071728321,
    8: 341550071728321,
    9: 3825123056546413051,
    10: 3825123056546413051,
    11: 3825123056546413051,
    12: 318665857834031151167461,
    13: 3317044064679887385961981,
}
PRIMES_43 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]


def test_example_trace() -> None:
    assert split_power_of_two(560) == (4, 35)
    assert [pow(2, 35 * 2**j, 561) for j in range(5)] == [263, 166, 67, 1, 1]
    assert is_strong_probable_prime(561, 2) is False
    n = 1373653
    assert n == 829 * 1657 and split_power_of_two(n - 1) == (2, 343413)
    assert [pow(2, 343413 * 2**j, n) for j in range(2)] == [890592, n - 1]
    assert pow(3, 343413, n) == 1
    assert [pow(5, 343413 * 2**j, n) for j in range(3)] == [1199564, 73782, 1370338]
    assert miller_rabin_bases(n, [2, 3]) is True
    assert miller_rabin_bases(n, [2, 3, 5]) is False
    assert is_strong_probable_prime(341, 2) is False and pow(2, 340, 341) == 1
    assert is_strong_probable_prime(2047, 2) is True and is_strong_probable_prime(2047, 3) is False


def test_small_and_even() -> None:
    rng = random.Random(1)
    assert [miller_rabin(n, 5, rng) for n in range(5)] == [False, False, True, True, False]
    for n in range(4, 3000, 2):
        assert miller_rabin(n, 5, rng) is False
        assert is_prime_u64(n) is False
    assert [is_prime_u64(n) for n in range(4)] == [False, False, True, True]


def test_all_n_up_to_limit_against_trial_division() -> None:
    rng = random.Random(2024)
    wrong = []
    for n in range(LIMIT + 1):
        want = n in PRIME_SET
        assert is_prime_u64(n) == want, n
        assert miller_rabin_bases(n, [2, 3]) == want, n  # psi_2 = 1373653 > LIMIT
        got = miller_rabin(n, 3, rng)
        if want:
            assert got is True, n
        elif got:
            wrong.append(n)
    # One-sided error with probability below 4^-3 per odd composite; in fact rare.
    assert all(n % 2 == 1 and n not in PRIME_SET for n in wrong)
    assert len(wrong) <= 3


def test_prime_powers() -> None:
    rng = random.Random(9)
    for p in [3, 5, 7, 11, 13, 101, 65537, 2**31 - 1]:
        for e in range(2, 5):
            assert miller_rabin(p**e, 10, rng) is False
            if p**e < 2**64:
                assert is_prime_u64(p**e) is False
    for e in range(2, 70):
        assert miller_rabin(2**e, 3, rng) is False


def test_liar_count_formula_and_quarter_bound() -> None:
    for n in range(9, 2500, 2):
        if n in PRIME_SET:
            continue
        liars = sum(1 for a in range(1, n) if is_strong_probable_prime(n, a))
        assert liars == strong_liar_count(n), n
        phi = math.prod((p - 1) * p ** (e - 1) for p, e in factorize(n).items())
        if n == 9:
            assert liars == 2 and 4 * liars > phi
        else:
            assert 4 * liars <= phi, n
            assert Fraction(liars - 2, n - 3) < Fraction(1, 4)
    assert strong_liar_count(15) == 2 and strong_liar_count(91) == 18 and strong_liar_count(8911) == 1782


def test_carmichael_numbers_are_caught() -> None:
    rng = random.Random(7)
    for n in CARMICHAEL_SMALL:
        assert miller_rabin(n, 20, rng) is False
        assert is_prime_u64(n) is False
    assert miller_rabin(CHERNICK, 10, rng) is False
    assert pow(2, CHERNICK - 1, CHERNICK) == 1  # a Fermat liar, but not a strong liar
    assert is_strong_probable_prime(CHERNICK, 2) is False


def test_psi_values_and_deterministic_bases() -> None:
    rng = random.Random(6)
    for k, n in PSI.items():
        assert miller_rabin_bases(n, PRIMES_43[:k]) is True, k
        assert miller_rabin_bases(n, PRIMES_43[: k + 1]) is False or PSI.get(k + 1) == n, k
        assert miller_rabin(n, 30, rng) is False
    assert PSI[12] > 2**64
    assert 3825123056546413051 == 149491 * 747451 * 34233211
    assert PSI[12] == 399165290221 * 798330580441
    assert is_prime_u64(3825123056546413051) is False


def test_large_primes_and_composites() -> None:
    rng = random.Random(4)
    for p in BIG_PRIMES:
        assert miller_rabin(p, 5, rng) is True
    for c in BIG_COMPOSITES:
        assert miller_rabin(c, 5, rng) is False
    assert is_prime_u64(2**61 - 1) and is_prime_u64(2**64 - 59)
    assert not is_prime_u64(2**64 - 1) and not is_prime_u64(4294967291 * 4294967279)


def test_random_64_bit_inputs() -> None:
    rng = random.Random(8)
    for _ in range(300):
        n = rng.randrange(1 << 63, 1 << 64)
        assert is_prime_u64(n) == miller_rabin(n, 25, rng)
    # Products of two random 32-bit primes are always rejected.
    primes32 = []
    while len(primes32) < 40:
        c = rng.randrange(1 << 31, 1 << 32) | 1
        if miller_rabin(c, 25, rng):
            primes32.append(c)
    for i in range(0, 40, 2):
        assert is_prime_u64(primes32[i] * primes32[i + 1]) is False


def test_random_10_digit_against_trial_division() -> None:
    rng = random.Random(10)
    for _ in range(500):
        n = rng.randrange(10**9, 10**10) | 1
        want = trial_division_is_prime(n)
        assert is_prime_u64(n) == want
        if want:
            assert miller_rabin(n, 8, rng) is True
