# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-exponentiation/. The authors are listed in prov/D262EM.jsonl.


def binary_exponentiation(x: int, e: int, m: int) -> int:
    """Return x**e mod m, in 0 .. m - 1, by right-to-left binary exponentiation.

    Precondition: e >= 0 and m >= 1. The base x can be any integer, also negative.
    The convention x**0 = 1 holds, so the result for e == 0 is 1 % m.
    Cost: floor(lg e) squarings and popcount(e) multiplications modulo m,
    so O(log e) operations on residues; Python integers have no size limit.
    """
    if e < 0:
        raise ValueError("the exponent must be non-negative")
    if m < 1:
        raise ValueError("the modulus must be at least 1")
    r = 1 % m  # @line L1
    b = x % m  # @line L2
    while e > 0:  # @line L3
        if e & 1:  # @line L4
            r = r * b % m
        e >>= 1  # @line L5
        if e > 0:  # @line L6
            b = b * b % m
    return r  # @line L7


def multiplication_count(e: int) -> int:
    """The number of products that binary_exponentiation makes for exponent e >= 0."""
    if e == 0:
        return 0
    return (e.bit_length() - 1) + bin(e).count("1")
