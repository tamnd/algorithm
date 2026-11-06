# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baillie-psw/. The authors are listed in prov/33QWDT.jsonl.

import math
import random

import pytest

from baillie_psw import (
    baillie_psw,
    is_strong_lucas_probable_prime,
    is_strong_probable_prime,
    jacobi,
    lucas_uvq,
    selfridge_parameters,
)

LIMIT = 100_000
# Strong pseudoprimes to the first m prime bases (smallest for each m); all are
# also strong pseudoprimes to the base 2.
PSI = (
    2047,
    1373653,
    25326001,
    3215031751,
    2152302898747,
    3474749660383,
    341550071728321,
    3825123056546413051,
    318665857834031151167461,
    3317044064679887385961981,
)
# The strong Lucas pseudoprimes with Selfridge's parameters below 10^5.
STRONG_LUCAS_PSEUDOPRIMES = (5459, 5777, 10877, 16109, 18971, 22499, 24569, 25199, 40309, 58519, 75077, 97439)
MERSENNE_PRIME_EXPONENTS = (521, 607, 1279, 2203)


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


def reference_is_probable_prime(n: int, rng: random.Random, rounds: int = 30) -> bool:
    """Miller-Rabin with random bases, as an independent check for large n."""
    if n < 4:
        return n >= 2
    if n % 2 == 0:
        return False
    return all(is_strong_probable_prime(n, rng.randrange(2, n - 1)) for _ in range(rounds))


def test_against_trial_division_up_to_limit() -> None:
    is_p = sieve(LIMIT)
    for n in range(LIMIT + 1):
        assert baillie_psw(n) == bool(is_p[n]), n
    for n in range(0, 2000):
        assert baillie_psw(n) == trial_division_is_prime(n)


def test_small_and_special_values() -> None:
    assert [n for n in range(-5, 30) if baillie_psw(n)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for n in (4, 6, 100, 2**40, 3**20, 101**2, 7919**2, 9973**3):
        assert baillie_psw(n) is False


def test_jacobi_against_euler_criterion() -> None:
    is_p = sieve(2000)
    for p in range(3, 2000, 2):
        if is_p[p]:
            for a in range(-30, 60):
                want = pow(a % p, (p - 1) // 2, p)
                want = -1 if want == p - 1 else want
                assert jacobi(a, p) == want
    # Multiplicativity in the lower argument.
    for n in range(1, 400, 2):
        for m in range(1, 60, 2):
            for a in range(-10, 30):
                assert jacobi(a, n * m) == jacobi(a, n) * jacobi(a, m)


def test_lucas_sequences_against_the_recurrence() -> None:
    for n in (3, 7, 9, 15, 21, 101, 561, 2047):
        for p, q in ((1, -1), (1, 2), (3, 1), (1, -3), (2, 5)):
            u_seq, v_seq = [0, 1], [2, p]
            for _ in range(80):
                u_seq.append(p * u_seq[-1] - q * u_seq[-2])
                v_seq.append(p * v_seq[-1] - q * v_seq[-2])
            for k in range(1, 80):
                assert lucas_uvq(n, p, q, k) == (u_seq[k] % n, v_seq[k] % n, pow(q, k, n) % n)


def test_selfridge_parameters() -> None:
    assert selfridge_parameters(127) == (5, 1, -1)
    assert selfridge_parameters(2047) == (5, 1, -1)
    assert selfridge_parameters(5459) == (-7, 1, 2)
    assert selfridge_parameters(21) is None  # (5/21) = 1, (-7/21) = 0 with 7 < 21
    rng = random.Random(3)
    for _ in range(2000):
        n = rng.randrange(3, 10**9) | 1
        if math.isqrt(n) ** 2 == n:
            continue
        params = selfridge_parameters(n)
        if params is None:
            continue
        d, p, q = params
        assert d % 4 == 1 and jacobi(d, n) == -1 and p == 1 and 4 * q == 1 - d


def test_strong_pseudoprimes_to_base_2_are_rejected() -> None:
    is_p = sieve(LIMIT * 10)
    spsp2 = [n for n in range(3, LIMIT * 10, 2) if not is_p[n] and is_strong_probable_prime(n, 2)]
    assert len(spsp2) == 46 and spsp2[:3] == [2047, 3277, 4033]
    for n in spsp2 + list(PSI):
        assert is_strong_probable_prime(n, 2)
        assert baillie_psw(n) is False, n


def test_strong_lucas_pseudoprimes_are_rejected() -> None:
    is_p = sieve(LIMIT)
    found = []
    for n in range(5, LIMIT, 2):
        if is_p[n] or math.isqrt(n) ** 2 == n:
            continue
        params = selfridge_parameters(n)
        if params is not None and is_strong_lucas_probable_prime(n, params[1], params[2]):
            found.append(n)
    assert tuple(found) == STRONG_LUCAS_PSEUDOPRIMES
    for n in found:
        assert not is_strong_probable_prime(n, 2)
        assert baillie_psw(n) is False


def test_carmichael_numbers_are_rejected() -> None:
    carmichael = (561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 825265, 321197185, 5394826801)
    for n in carmichael:
        assert baillie_psw(n) is False
    # A large Carmichael number (6k + 1)(12k + 1)(18k + 1) with three prime factors.
    rng = random.Random(7)
    k = 10**60
    while True:
        k += 1
        a, b, c = 6 * k + 1, 12 * k + 1, 18 * k + 1
        if all(reference_is_probable_prime(x, rng, 8) for x in (a, b, c)):
            break
    n = a * b * c
    assert all(pow(base, n - 1, n) == 1 for base in (2, 3, 5, 7))
    assert baillie_psw(n) is False
    assert baillie_psw(a) and baillie_psw(b) and baillie_psw(c)


def test_large_known_primes_and_composites() -> None:
    for p in MERSENNE_PRIME_EXPONENTS:
        assert baillie_psw(2**p - 1) is True
    # Composite Mersenne numbers with a prime exponent and composite Fermat
    # numbers are strong pseudoprimes to the base 2, so the Lucas part must
    # reject them. M_1277 has no known factor.
    for p in (11, 23, 29, 523, 1277):
        n = 2**p - 1
        assert is_strong_probable_prime(n, 2)
        assert baillie_psw(n) is False
    for k in (5, 6, 7, 8, 9, 10):
        n = 2 ** (2**k) + 1
        assert is_strong_probable_prime(n, 2)
        assert baillie_psw(n) is False
    assert (2**512 + 1) % 2424833 == 0 and (2**1024 + 1) % 45592577 == 0


def test_random_large_inputs() -> None:
    rng = random.Random(11)
    for digits in (20, 50, 100, 300):
        for _ in range(40):
            n = rng.randrange(10 ** (digits - 1), 10**digits) | 1
            assert baillie_psw(n) == reference_is_probable_prime(n, rng)
    # Products of two random probable primes of about 150 digits.
    for _ in range(3):
        ps = []
        while len(ps) < 2:
            x = rng.randrange(10**149, 10**150) | 1
            if reference_is_probable_prime(x, rng):
                ps.append(x)
        assert baillie_psw(ps[0]) and baillie_psw(ps[1])
        assert baillie_psw(ps[0] * ps[1]) is False
        assert baillie_psw(ps[0] ** 2) is False


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        jacobi(3, 4)
    with pytest.raises(ValueError):
        lucas_uvq(7, 1, -1, 0)
