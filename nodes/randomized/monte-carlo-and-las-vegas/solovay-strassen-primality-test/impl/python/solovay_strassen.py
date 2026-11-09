# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solovay-strassen-primality-test/. The authors are listed in prov/XD7T81.jsonl.

"""The Solovay-Strassen primality test with random bases.

The answer False ("composite") is always correct. The answer True
("probably prime") is wrong with probability at most 2^-k for k rounds.
"""

import random


def jacobi(a: int, n: int) -> int:
    """The Jacobi symbol (a/n) for odd n >= 1, without factoring n."""
    a %= n  # @line L8
    t = 1
    while a != 0:  # @line L9
        while a % 2 == 0:  # @line L10
            a //= 2
            if n % 8 in (3, 5):
                t = -t
        a, n = n, a  # @line L11
        if a % 4 == 3 and n % 4 == 3:  # @line L12
            t = -t
        a %= n  # @line L13
    return t if n == 1 else 0  # @line L14


def is_euler_probable_prime(n: int, a: int) -> bool:
    """True if a^((n-1)/2) = (a/n) mod n with (a/n) != 0: a is an Euler liar or n is prime.

    Needs n odd and n >= 3.
    """
    j = jacobi(a, n)  # @line L4
    if j == 0:  # @line L5
        return False
    return pow(a, (n - 1) // 2, n) == j % n  # @line L6


def solovay_strassen(n: int, k: int, rng: random.Random) -> bool:
    """Return False if n is proved composite, True if n passes k random bases."""
    if n in (2, 3):  # @line L1
        return True
    if n < 2 or n % 2 == 0:
        return False
    for _ in range(k):  # @line L2
        a = rng.randint(2, n - 2)  # @line L3
        if not is_euler_probable_prime(n, a):  # lines L4 to L6
            return False
    return True  # @line L7
