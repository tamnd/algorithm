# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-euclidean-algorithm/. The authors are listed in prov/QQCABS.jsonl.

"""Extended Euclidean algorithm.

Returns (g, x, y) with g = gcd(a, b) >= 0 and a*x + b*y = g, for any
integers a and b. gcd(0, 0) is 0, returned as (0, 1, 0). For a, b >= 1 the
coefficients satisfy |x| <= b/g and |y| <= a/g, and |x| <= b/(2g),
|y| <= a/(2g) unless b divides a. The loop runs O(log min(|a|, |b|)) times;
on inputs of n binary digits it uses O(n^2) bit operations. Extra space is
a constant number of integers no larger than the inputs.
"""


def extended_euclidean_algorithm(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with g = gcd(a, b) >= 0 and a*x + b*y = g."""
    r0, r1 = abs(a), abs(b)  # @line L1
    s0, s1 = 1, 0  # @line L2
    t0, t1 = 0, 1  # @line L3
    while r1 != 0:  # @line L4
        q = r0 // r1  # @line L5
        r0, r1 = r1, r0 - q * r1  # @line L6
        s0, s1 = s1, s0 - q * s1  # @line L7
        t0, t1 = t1, t0 - q * t1  # @line L8
    x = -s0 if a < 0 else s0  # @line L9
    y = -t0 if b < 0 else t0
    return r0, x, y  # @line L10


def modular_inverse(a: int, m: int) -> int:
    """Return the inverse of a modulo m >= 1, in 0..m-1; raise if gcd(a, m) != 1."""
    if m < 1:
        raise ValueError("modulus must be positive")
    g, x, _ = extended_euclidean_algorithm(a, m)
    if g != 1:
        raise ValueError("a is not invertible modulo m")
    return x % m
