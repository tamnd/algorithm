# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-rabin/. The authors are listed in prov/T1483D.jsonl.

"""Miller-Rabin primality test.

miller_rabin(n, k) returns False when n is certainly not prime and True when
n is probably prime. The answer False is always right. For an odd composite n,
each round answers "probably prime" with probability below 1/4 (Monier-Rabin),
so k rounds err with probability below 4^-k, whatever n is.

Cost: k modular exponentiations with an exponent of about lg n binary digits,
O(k (log n)^3) bit operations with schoolbook arithmetic. Integers are of
arbitrary precision (Python int).
"""

import random

# The first twelve primes are a witness set for every odd composite n < 2^64,
# since the smallest strong pseudoprime to all of them is
# 318665857834031151167461 > 2^64 (Sorenson and Webster 2017), while the
# smallest one to the first eleven is 3825123056546413051 < 2^64.
FIRST_12_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def split_power_of_two(m: int) -> tuple[int, int]:
    """Return (s, d) with m = 2^s * d and d odd, for m >= 1."""
    s = 0
    while m % 2 == 0:
        m //= 2
        s += 1
    return s, m


def is_strong_probable_prime(n: int, a: int) -> bool:
    """True when the odd n >= 3 passes the strong test with the base a.

    The base is reduced modulo n. A base that is 0 modulo n is treated as
    passing, because it tests nothing.
    """
    a %= n
    if a == 0:
        return True
    s, d = split_power_of_two(n - 1)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def miller_rabin(n: int, k: int = 20, rng: random.Random | None = None) -> bool:
    """Return False if n is not prime, True if n is probably prime (k >= 1 rounds)."""
    if n < 4:  # @line L1
        return n >= 2
    if n % 2 == 0:  # @line L2
        return False
    s, d = split_power_of_two(n - 1)  # @line L3
    rng = rng if rng is not None else random.Random()
    for _ in range(k):  # @line L4
        a = rng.randint(2, n - 2)  # @line L5
        x = pow(a, d, n)  # @line L6
        if x == 1 or x == n - 1:  # @line L7
            continue
        for _ in range(s - 1):  # @line L8
            x = x * x % n  # @line L9
            if x == n - 1:  # @line L10
                break
        else:
            return False  # @line L11
    return True  # @line L12


def miller_rabin_bases(n: int, bases: tuple[int, ...] | list[int]) -> bool:
    """The same test with the given bases in place of random ones."""
    if n < 4:
        return n >= 2
    if n % 2 == 0:
        return False
    return all(is_strong_probable_prime(n, a) for a in bases)


def is_prime_u64(n: int) -> bool:
    """Deterministic primality for 0 <= n < 2^64 with the first twelve prime bases."""
    if n < 0 or n >= 1 << 64:
        raise ValueError("n must be in [0, 2^64)")
    for p in FIRST_12_PRIMES:
        if n % p == 0:
            return n == p
    if n < 2:
        return False
    return miller_rabin_bases(n, FIRST_12_PRIMES)
