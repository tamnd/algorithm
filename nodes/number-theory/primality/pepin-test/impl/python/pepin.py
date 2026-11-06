# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pepin-test/. The authors are listed in prov/SM5V45.jsonl.

"""Pepin's test for Fermat numbers F_k = 2^(2^k) + 1.

pepin_test(k) returns True exactly when F_k is prime, for every k >= 0. For
k >= 1 it checks 3^((F_k - 1)/2) = -1 (mod F_k) with 2^k - 1 squarings. The
answer is always right: the test is deterministic.

Cost: 2^k - 1 squarings modulo F_k, a number of N = 2^k + 1 binary digits, each
followed by a reduction that needs only shifts, masks and a subtraction.
That is O(N M(N)) bit operations, O(N^3) with schoolbook multiplication.
Integers are of arbitrary precision (Python int).
"""


def reduce_fermat(x: int, e: int) -> int:
    """Return x mod (2^e + 1) for x >= 0, with shifts, masks and subtractions only."""
    f = (1 << e) + 1
    mask = (1 << e) - 1
    sign = 1  # invariant: the input is congruent to sign * x (mod f)
    while x >= f:
        x = (x & mask) - (x >> e)  # x = hi * 2^e + lo = lo - hi (mod 2^e + 1)
        if x < 0:
            x = -x
            sign = -sign
    if sign < 0 and x:
        x = f - x
    return x


def pepin_test(k: int) -> bool:
    """Return True if F_k = 2^(2^k) + 1 is prime, for an integer k >= 0."""
    if k < 0:
        raise ValueError("k must be at least 0")
    if k == 0:  # @line L1
        return True
    e = 1 << k
    f = (1 << e) + 1  # @line L2
    x = 3  # @line L3
    for _ in range(e - 1):  # @line L4
        x = reduce_fermat(x * x, e)  # @line L5
    return x == f - 1  # @line L6


def pepin_residue(k: int, base: int = 3) -> int:
    """base^((F_k - 1)/2) mod F_k, computed by 2^k - 1 squarings."""
    if k < 0:
        raise ValueError("k must be at least 0")
    e = 1 << k
    x = base % ((1 << e) + 1)
    for _ in range(e - 1):
        x = reduce_fermat(x * x, e)
    return x


def is_fermat_number_prime(n: int) -> bool:
    """Primality of a Fermat number n = 2^(2^k) + 1, by Pepin's test."""
    m = n - 1
    if m < 2 or m & (m - 1):
        raise ValueError("n must be of the form 2^(2^k) + 1")
    e = m.bit_length() - 1
    if e & (e - 1):
        raise ValueError("n must be of the form 2^(2^k) + 1")
    return pepin_test(e.bit_length() - 1)
