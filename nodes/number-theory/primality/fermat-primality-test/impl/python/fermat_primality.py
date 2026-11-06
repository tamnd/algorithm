# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermat-primality-test/. The authors are listed in prov/8TFPRS.jsonl.

"""Fermat primality test.

fermat_primality_test(n, k) returns False when n is certainly not prime and
True when n is probably prime. The answer False is always right. For an odd
composite n that is not a Carmichael number, each round answers "probably
prime" with probability below 1/2, so k rounds err with probability below
2^-k. A Carmichael number passes every round whose base is coprime to n.

Cost: k modular exponentiations with an exponent of about lg n binary digits,
O(k (log n)^3) bit operations with schoolbook arithmetic. Integers are of
arbitrary precision (Python int).
"""

import random


def is_fermat_witness(a: int, n: int) -> bool:
    """True when a^(n-1) mod n is not 1, which proves that n > 1 is composite."""
    return pow(a, n - 1, n) != 1


def fermat_primality_test(n: int, k: int = 20, rng: random.Random | None = None) -> bool:
    """Return False if n is not prime, True if n is probably prime (k >= 1 rounds)."""
    if n < 4:  # @line L1
        return n >= 2
    if n % 2 == 0:  # @line L2
        return False
    rng = rng if rng is not None else random.Random()
    for _ in range(k):  # @line L3
        a = rng.randint(2, n - 2)  # @line L4
        if pow(a, n - 1, n) != 1:  # @line L5
            return False
    return True  # @line L6


def fermat_test_bases(n: int, bases: list[int]) -> bool:
    """The same test with the given bases in place of random ones.

    Each base is reduced modulo n; the bases 0, 1 and n - 1 modulo n are skipped
    because they test nothing (0 is not coprime to n, the other two always pass).
    """
    if n < 4:
        return n >= 2
    if n % 2 == 0:
        return False
    for a in bases:
        a %= n
        if a in (0, 1, n - 1):
            continue
        if pow(a, n - 1, n) != 1:
            return False
    return True
