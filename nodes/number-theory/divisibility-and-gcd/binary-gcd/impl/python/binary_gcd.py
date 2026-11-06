# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-gcd/. The authors are listed in prov/NZK9TA.jsonl.

"""Binary GCD (Stein's algorithm).

Computes gcd(a, b) with parity tests, shifts and subtractions only, with no
division. Inputs may be any integers; the result is non-negative, and
gcd(0, 0) = 0. On inputs of at most n binary digits the loop runs at most
2n + 1 times, and each pass costs O(n) bit operations, so the total is
O(n^2) bit operations. Extra space is O(n) bits for the two working values.
"""


def trailing_zeros(x: int) -> int:
    """The exponent of 2 in x, for x > 0: the number of trailing zero digits."""
    return (x & -x).bit_length() - 1


def binary_gcd(a: int, b: int) -> int:
    """Return gcd(a, b) >= 0 using shifts and subtractions."""
    a, b = abs(a), abs(b)  # @line L1
    if a == 0:  # @line L2
        return b
    if b == 0:  # @line L3
        return a
    k = trailing_zeros(a | b)  # @line L4
    a >>= trailing_zeros(a)  # @line L5
    while True:  # @line L6
        b >>= trailing_zeros(b)  # @line L7
        if a > b:  # @line L8
            a, b = b, a
        b -= a  # @line L9
        if b == 0:  # @line L10
            break
    return a << k  # @line L11


def loop_passes(a: int, b: int) -> int:
    """The number of passes of the loop of lines L6 to L10 on (a, b)."""
    a, b = abs(a), abs(b)
    if a == 0 or b == 0:
        return 0
    a >>= trailing_zeros(a)
    passes = 0
    while True:
        passes += 1
        b >>= trailing_zeros(b)
        if a > b:
            a, b = b, a
        b -= a
        if b == 0:
            return passes
