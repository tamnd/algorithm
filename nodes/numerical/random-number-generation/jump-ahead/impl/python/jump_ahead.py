# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-ahead/. The authors are listed in prov/CRH15P.jsonl.

"""Jump-ahead for linear generators: affine maps modulo m, and F2-linear maps."""

from typing import Callable, List


def lcg_jump_coefficients(m: int, a: int, c: int, n: int) -> tuple:
    """Return (A, C) with f^n(s) = (A s + C) mod m for f(s) = (a s + c) mod m."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    big_a, big_c = 1 % m, 0  # @line L1
    b, d = a % m, c % m  # @line L2
    while n > 0:  # @line L3
        if n & 1:  # @line L4
            big_a, big_c = (b * big_a) % m, (b * big_c + d) % m
        b, d = (b * b) % m, (b * d + d) % m  # @line L5
        n >>= 1  # @line L6
    return big_a, big_c


def lcg_jump(m: int, a: int, c: int, s: int, n: int) -> int:
    """The state n steps after s for the LCG (m, a, c)."""
    big_a, big_c = lcg_jump_coefficients(m, a, c, n)
    return (big_a * s + big_c) % m  # @line L7


def leapfrog_parameters(m: int, a: int, c: int, p: int) -> tuple:
    """Multiplier and increment of the LCG that outputs every p-th state."""
    return lcg_jump_coefficients(m, a, c, p)


# ---- polynomials over GF(2) as Python ints (bit j = coefficient of x^j) ----

def gf2_mulmod(u: int, v: int, mod: int) -> int:
    """u * v mod `mod` in GF(2)[x]."""
    k = mod.bit_length() - 1
    r = 0
    while v:
        if v & 1:
            r ^= u
        v >>= 1
        u <<= 1
        if (u >> k) & 1:
            u ^= mod
    return r


def gf2_xpow_mod(n: int, mod: int) -> int:
    """x^n mod `mod` in GF(2)[x], by square and multiply."""
    k = mod.bit_length() - 1
    if k < 1:
        raise ValueError("modulus must have degree at least 1")
    result = 1
    base = 2 if k > 1 else 2 ^ mod  # x reduced modulo mod
    while n > 0:
        if n & 1:
            result = gf2_mulmod(result, base, mod)
        base = gf2_mulmod(base, base, mod)
        n >>= 1
    return result


def berlekamp_massey_gf2(bits: List[int]) -> int:
    """Connection polynomial of least degree generating `bits`, as an int.

    The returned polynomial is the reciprocal form x^L * C(1/x), that is, the
    characteristic polynomial of the recurrence, with bit j the coefficient of x^j.
    """
    n = len(bits)
    c, b = [1] + [0] * n, [1] + [0] * n
    length, m = 0, 1
    for i in range(n):
        d = bits[i]
        for j in range(1, length + 1):
            d ^= c[j] & bits[i - j]
        if d == 0:
            m += 1
            continue
        t = c[:]
        for j in range(n + 1 - m):
            c[j + m] ^= b[j]
        if 2 * length <= i:
            length, b, m = i + 1 - length, t, 1
        else:
            m += 1
    poly = 0
    for j in range(length + 1):
        if c[j]:
            poly |= 1 << (length - j)
    return poly


def f2_jump(step: Callable[[int], int], charpoly: int, state: int, n: int) -> int:
    """The state n steps after `state` for an F2-linear transition `step`.

    `step` maps a packed state to the next one and must be linear over GF(2):
    step(x ^ y) == step(x) ^ step(y). `charpoly` is a polynomial with
    charpoly(A) = 0 for the transition matrix A, for example its characteristic
    polynomial.
    """
    r = gf2_xpow_mod(n, charpoly)  # @line L8
    t = 0  # @line L9
    for j in range(r.bit_length() - 1, -1, -1):  # @line L10
        t = step(t)  # @line L11
        if (r >> j) & 1:  # @line L12
            t ^= state
    return t  # @line L13


def f2_jump_by_polynomial(step: Callable[[int], int], jump_poly: int, state: int) -> int:
    """Apply a precomputed jump polynomial in ascending order, as in published jump constants."""
    t, s = 0, state
    j = 0
    while jump_poly >> j:
        if (jump_poly >> j) & 1:
            t ^= s
        s = step(s)
        j += 1
    return t


# ---- two F2-linear transitions used in the tests and examples ----

M32 = 0xFFFFFFFF
M64 = 0xFFFFFFFFFFFFFFFF


def xorshift32_step(x: int) -> int:
    """Marsaglia's xorshift with shifts (13, 17, 5) on a 32-bit word."""
    x ^= (x << 13) & M32
    x ^= x >> 17
    x ^= (x << 5) & M32
    return x


def xoshiro256_step(packed: int) -> int:
    """The linear engine of xoshiro256 on four 64-bit words packed little-end first."""
    s0 = packed & M64
    s1 = (packed >> 64) & M64
    s2 = (packed >> 128) & M64
    s3 = (packed >> 192) & M64
    t = (s1 << 17) & M64
    s2 ^= s0
    s3 ^= s1
    s1 ^= s2
    s0 ^= s3
    s2 ^= t
    s3 = ((s3 << 45) | (s3 >> 19)) & M64
    return s0 | (s1 << 64) | (s2 << 128) | (s3 << 192)


def output_bits(step: Callable[[int], int], state: int, count: int) -> List[int]:
    """The lowest bit of `count` successive states, starting with `state`."""
    out = []
    for _ in range(count):
        out.append(state & 1)
        state = step(state)
    return out
