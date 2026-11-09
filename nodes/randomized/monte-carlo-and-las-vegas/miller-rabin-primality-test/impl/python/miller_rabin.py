# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-rabin-primality-test/. The authors are listed in prov/HSYVA5.jsonl.

"""The Miller-Rabin primality test with random bases.

The answer False ("composite") is always correct. The answer True
("probably prime") is wrong with probability at most 4^-k for k rounds.
"""

import random


def decompose(n: int) -> tuple[int, int]:
    """Write n - 1 = 2^s d with d odd; return (s, d). Needs n odd and n >= 3."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return s, d


def is_strong_probable_prime(n: int, a: int) -> bool:
    """True if n passes the strong test to base a (a is a strong liar or n is prime).

    Needs n odd, n >= 5 and 1 <= a <= n - 1.
    """
    s, d = decompose(n)  # @line L2
    x = pow(a, d, n)  # @line L5
    if x == 1 or x == n - 1:  # @line L6
        return True
    for _ in range(s - 1):  # @line L7
        x = x * x % n  # @line L8
        if x == n - 1:  # @line L9
            return True
    return False  # @line L10


def strong_sequence(n: int, a: int) -> list[int]:
    """The values a^d, a^(2d), ..., a^(2^s d) mod n, for examples and tests."""
    s, d = decompose(n)
    x = pow(a, d, n)
    seq = [x]
    for _ in range(s):
        x = x * x % n
        seq.append(x)
    return seq


def miller_rabin(n: int, k: int, rng: random.Random) -> bool:
    """Return False if n is proved composite, True if n passes k random bases."""
    if n in (2, 3):  # @line L1
        return True
    if n < 2 or n % 2 == 0:
        return False
    for _ in range(k):  # @line L3
        a = rng.randint(2, n - 2)  # @line L4
        if not is_strong_probable_prime(n, a):  # lines L5 to L10
            return False
    return True  # @line L11
