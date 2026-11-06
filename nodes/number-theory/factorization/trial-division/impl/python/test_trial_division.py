# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trial-division/. The authors are listed in prov/1TKFVE.jsonl.

import math
import random

import pytest

from trial_division import trial_division

MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
CARMICHAEL = [561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657,
              52633, 62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461,
              252601, 278545, 294409, 314821, 334153, 340561, 399001, 410041, 449065,
              488881, 512461, 3215031751]


def is_prime(n: int) -> bool:
    """Miller-Rabin with the 13 prime bases up to 41: deterministic for n < 3.3 * 10^24."""
    assert n < 3317044064679887385961981
    if n < 2:
        return False
    for p in MR_BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in MR_BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def random_prime(rng: random.Random, bits: int) -> int:
    while True:
        p = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p):
            return p


def next_prime(x: int) -> int:
    x += 1
    while not is_prime(x):
        x += 1
    return x


def check(n: int) -> None:
    f = trial_division(n)
    assert math.prod(f) == n
    assert all(is_prime(p) for p in f)
    assert f == sorted(f)


def test_example() -> None:
    assert trial_division(9100) == [2, 2, 5, 5, 7, 13]


def test_edges() -> None:
    with pytest.raises(ValueError):
        trial_division(0)
    with pytest.raises(ValueError):
        trial_division(-6)
    assert trial_division(1) == []
    assert trial_division(2) == [2]
    assert trial_division(3) == [3]
    assert trial_division(4) == [2, 2]
    assert trial_division(1000003) == [1000003]
    assert trial_division(2**31 - 1) == [2**31 - 1]
    assert trial_division(2**40) == [2] * 40
    assert trial_division(3**25) == [3] * 25
    assert trial_division(65537**2) == [65537, 65537]
    assert trial_division(101**3) == [101] * 3
    assert trial_division(999983 * 1000003) == [999983, 1000003]


def test_all_small() -> None:
    spf = list(range(100001))
    for i in range(2, 317):
        if spf[i] == i:
            for j in range(i * i, 100001, i):
                if spf[j] == j:
                    spf[j] = i
    for n in range(1, 100001):
        f = trial_division(n)
        assert math.prod(f) == n
        expected, m = [], n
        while m > 1:
            expected.append(spf[m])
            m //= spf[m]
        assert f == expected


def test_carmichael() -> None:
    for n in CARMICHAEL:
        check(n)


def test_random_semiprimes_and_close_primes() -> None:
    rng = random.Random(1975)
    for bits in range(2, 21):
        for _ in range(3):
            p, q = random_prime(rng, bits), random_prime(rng, bits)
            assert trial_division(p * q) == sorted([p, q])
        p = random_prime(rng, bits)
        q = next_prime(p)
        assert trial_division(p * q) == [p, q]


def test_random_smooth() -> None:
    rng = random.Random(4554)
    primes = [p for p in range(2, 1000) if is_prime(p)]
    for k in range(1, 40):
        f = sorted(rng.choice(primes) for _ in range(k))
        assert trial_division(math.prod(f)) == f
