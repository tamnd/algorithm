# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euclidean-algorithm/. The authors are listed in prov/4XB0RJ.jsonl.


def euclidean_algorithm(a: int, b: int) -> int:
    """Return gcd(a, b), the greatest common divisor of two integers.

    The result is non-negative. gcd(a, 0) = |a| and gcd(0, 0) = 0.
    Python integers have arbitrary precision. For inputs of at most n bits the
    loop runs O(n) times and the whole call costs O(n^2) bit operations with
    schoolbook division. Extra space: O(1) integers.
    """
    a, b = abs(a), abs(b)  # @line L1
    while b != 0:  # @line L2
        r = a % b  # @line L3
        a = b  # @line L4
        b = r  # @line L5
    return a  # @line L6


def division_steps(a: int, b: int) -> int:
    """Return the number of times the loop of euclidean_algorithm runs on (a, b)."""
    a, b = abs(a), abs(b)
    k = 0
    while b != 0:
        a, b = b, a % b
        k += 1
    return k
