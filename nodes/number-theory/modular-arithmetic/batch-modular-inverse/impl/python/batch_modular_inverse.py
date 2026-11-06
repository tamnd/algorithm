# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-modular-inverse/. The authors are listed in prov/ZYDK39.jsonl.

"""Batch modular inverse (Montgomery's trick).

Inverts k residues modulo the same m >= 1 with one extended Euclidean
inversion and 3(k - 1) modular multiplications. A forward pass stores the
prefix products z_i = x_1 ... x_i mod m. One inversion gives the inverse of
the full product. A backward pass peels off one factor at a time.

If some x_i shares a factor with m, the full product is not invertible. Then
the function raises NotInvertible, which carries g = gcd(z_k, m) > 1, a
divisor of m. Python integers have arbitrary size, so m may have any number
of digits.
"""

from typing import List, Sequence, Tuple


class NotInvertible(ValueError):
    """Some residue shares a factor with the modulus; g = gcd(product, m) > 1."""

    def __init__(self, g: int, m: int):
        super().__init__(f"the product is not invertible modulo {m}: gcd is {g}")
        self.g = g
        self.m = m


def inverse_and_gcd(a: int, m: int) -> Tuple[int, int]:
    """Return (g, u) with g = gcd(a, m) and u * a = g mod m, by the extended
    Euclidean algorithm with a loop. For g = 1, u is the inverse of a."""
    r0, r1 = m, a % m
    u0, u1 = 0, 1  # invariant: r_i = u_i * a (mod m)
    while r1 != 0:
        t = r0 // r1
        r0, r1 = r1, r0 - t * r1
        u0, u1 = u1, u0 - t * u1
    return r0, u0 % m


def batch_inverse(xs: Sequence[int], m: int) -> List[int]:
    """Return [x^(-1) mod m for x in xs], or raise NotInvertible."""
    if m < 1:
        raise ValueError("the modulus must be a positive integer")
    k = len(xs)
    if k == 0:  # @line L1
        return []
    x = [v % m for v in xs]
    z = [0] * k
    z[0] = x[0] % m  # @line L2
    for i in range(1, k):  # @line L3
        z[i] = z[i - 1] * x[i] % m  # @line L4
    g, q = inverse_and_gcd(z[k - 1], m)  # @line L5
    if g != 1:  # @line L6
        raise NotInvertible(g, m)
    y = z  # the prefix products are overwritten from the top down
    for i in range(k - 1, 0, -1):  # @line L7
        y[i] = q * z[i - 1] % m  # @line L8
        q = q * x[i] % m  # @line L9
    y[0] = q  # @line L10
    return y  # @line L11
