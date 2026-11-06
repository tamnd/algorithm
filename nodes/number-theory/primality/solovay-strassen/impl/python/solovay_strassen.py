# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solovay-strassen/. The authors are listed in prov/4S0832.jsonl.

"""Solovay-Strassen primality test.

solovay_strassen(n, k) returns False when n is certainly not prime and True
when n is probably prime. The answer False is always right. For each odd
composite n, each round answers "probably prime" with probability below 1/2,
so k rounds err with probability below 2^-k. The bound depends only on n and
k, not on any assumption about the input.

Cost: per round one Jacobi symbol, O((log n)^2) bit operations, and one
modular exponentiation, O((log n)^3) bit operations with schoolbook
arithmetic. Integers are of arbitrary precision (Python int).
"""

import random


def jacobi(a: int, n: int) -> int:
    """Jacobi symbol (a/n) for odd n >= 1, by the Euclid-like loop with
    quadratic reciprocity. Returns 1, -1 or 0 (0 exactly when gcd(a, n) > 1)."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be odd and positive")
    a %= n
    sign = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                sign = -sign
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            sign = -sign
        a %= n
    return sign if n == 1 else 0


def is_euler_witness(a: int, n: int) -> bool:
    """True when the base a proves the odd number n >= 3 composite:
    (a/n) = 0, or a^((n-1)/2) mod n differs from (a/n) mod n."""
    j = jacobi(a, n)
    return j == 0 or pow(a, (n - 1) // 2, n) != j % n


def solovay_strassen(n: int, k: int = 20, rng: random.Random | None = None) -> bool:
    """Return False if n is not prime, True if n is probably prime (k >= 1 rounds)."""
    if n < 4:  # @line L1
        return n >= 2
    if n % 2 == 0:  # @line L2
        return False
    rng = rng if rng is not None else random.Random()
    for _ in range(k):  # @line L3
        a = rng.randint(2, n - 2)  # @line L4
        j = jacobi(a, n)  # @line L5
        if j == 0:  # @line L6
            return False
        if pow(a, (n - 1) // 2, n) != j % n:  # @line L7
            return False
    return True  # @line L8


def euler_test_bases(n: int, bases: list[int]) -> bool:
    """The same test with given bases in place of random ones. Bases that are
    0, 1 or n - 1 modulo n are skipped, since they test nothing."""
    if n < 4:
        return n >= 2
    if n % 2 == 0:
        return False
    for a in bases:
        if a % n in (0, 1, n - 1):
            continue
        if is_euler_witness(a, n):
            return False
    return True
