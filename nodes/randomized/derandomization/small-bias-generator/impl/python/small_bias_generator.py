# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/small-bias-generator/. The authors are listed in prov/4KEFV4.jsonl.

"""The powering construction of Alon, Goldreich, Hastad and Peralta.

A seed is a pair (x, y) of elements of the field GF(2^m). Output bit i, for
i = 0, 1, ..., n - 1, is the inner product over GF(2) of the bit vectors of
x^i and y. Every nonempty parity of the n output bits has bias at most
(n - 1) / 2^m over a uniform seed.
"""

from functools import lru_cache


def _poly_mod(a: int, b: int) -> int:
    """Remainder of the GF(2) polynomial a modulo the nonzero polynomial b."""
    db = b.bit_length() - 1
    while a and a.bit_length() - 1 >= db:
        a ^= b << (a.bit_length() - 1 - db)
    return a


@lru_cache(maxsize=None)
def irreducible_polynomial(m: int) -> int:
    """The smallest irreducible GF(2) polynomial of degree m, as a bit mask.

    The search uses trial division by every polynomial of degree 1 to m // 2.
    It is meant for m up to about 24.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    for p in range((1 << m) | 1, 1 << (m + 1), 2):
        if all(_poly_mod(p, d) != 0 for d in range(2, 1 << (m // 2 + 1))):
            return p
    raise AssertionError("an irreducible polynomial of each degree exists")


def gf_mul(a: int, b: int, m: int) -> int:
    """Product of a and b in GF(2^m), with the modulus irreducible_polynomial(m)."""
    poly = irreducible_polynomial(m)
    top = 1 << m
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & top:
            a ^= poly
    return result


def inner_product(a: int, b: int) -> int:
    """Inner product over GF(2) of the bit vectors of a and b."""
    return bin(a & b).count("1") & 1


def small_bias_generator(seed: int, n: int, m: int) -> list[int]:
    """Stretch a 2m-bit seed to n bits. The high m bits are x, the low m bits are y."""
    if m < 1 or not 0 <= seed < 1 << (2 * m):
        raise ValueError("the seed must have 2m bits, with m >= 1")
    x = seed >> m  # @line L1
    y = seed & ((1 << m) - 1)  # @line L2
    z = 1  # @line L3: z = x^i, and x^0 = 1 also for x = 0
    bits = []
    for _ in range(n):  # @line L4
        bits.append(inner_product(z, y))  # @line L5
        z = gf_mul(z, x, m)  # @line L6
    return bits  # @line L7


def powering_bits(x: int, y: int, n: int, m: int) -> list[int]:
    """The n output bits for the seed (x, y), with 0 <= x, y < 2^m."""
    if m < 1 or not (0 <= x < 1 << m and 0 <= y < 1 << m):
        raise ValueError("x and y must be elements of GF(2^m)")
    return small_bias_generator((x << m) | y, n, m)


def field_degree_for(n: int, eps: float) -> int:
    """The least m >= 1 with (n - 1) / 2^m <= eps. The seed length is 2m."""
    if n < 1 or eps <= 0:
        raise ValueError("need n >= 1 and eps > 0")
    m = 1
    while (n - 1) > eps * (1 << m):
        m += 1
    return m
