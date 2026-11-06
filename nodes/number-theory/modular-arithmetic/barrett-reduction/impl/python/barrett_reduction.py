# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barrett-reduction/. The authors are listed in prov/MXGY63.jsonl.

"""Barrett reduction: x mod n with two multiplications and shifts, no division.

The modulus n >= 1 has k binary digits, so 2^(k-1) <= n < 2^k. The setup
computes mu = floor(4^k / n) once. Then every x with 0 <= x < 4^k, which
includes every product of two residues in [0, n), is reduced with two
multiplications, two shifts, one subtraction and at most two corrections.
Python integers have arbitrary size, so n may have any number of digits.
"""

from typing import NamedTuple


class Barrett(NamedTuple):
    n: int  # the modulus, n >= 1
    k: int  # the number of binary digits of n
    mu: int  # floor(4^k / n)


def barrett_setup(n: int) -> Barrett:
    """Precompute the constants for the modulus n >= 1."""
    if n < 1:
        raise ValueError("the modulus must be a positive integer")
    k = n.bit_length()  # @line L1
    mu = (1 << (2 * k)) // n  # @line L2
    return Barrett(n, k, mu)


def barrett_reduce(x: int, ctx: Barrett) -> int:
    """Return x mod n for 0 <= x < 4^k."""
    n, k, mu = ctx
    if x < 0 or x >> (2 * k):
        raise ValueError("x must satisfy 0 <= x < 4^k")
    q = ((x >> (k - 1)) * mu) >> (k + 1)  # @line L3
    r = x - q * n  # @line L4
    while r >= n:  # @line L5
        r -= n
    return r  # @line L6


def barrett_mulmod(a: int, b: int, ctx: Barrett) -> int:
    """Return a * b mod n for residues 0 <= a, b < n."""
    return barrett_reduce(a * b, ctx)  # @line L7


def barrett_powmod(base: int, exponent: int, ctx: Barrett) -> int:
    """Return base^exponent mod n by binary exponentiation with Barrett products."""
    if exponent < 0:
        raise ValueError("the exponent must be non-negative")
    result = barrett_reduce(1 % ctx.n, ctx)
    b = base % ctx.n
    while exponent:
        if exponent & 1:
            result = barrett_mulmod(result, b, ctx)
        b = barrett_mulmod(b, b, ctx)
        exponent >>= 1
    return result
