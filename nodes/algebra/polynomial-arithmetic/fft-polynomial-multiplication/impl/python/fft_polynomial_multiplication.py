# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fft-polynomial-multiplication/. The authors are listed in prov/WT2CHV.jsonl.

"""Polynomial multiplication by the fast Fourier transform.

Polynomials are coefficient lists, lowest degree first, normalized (no zero
on top; the zero polynomial is []). The exact transform works over Z/pZ for
a prime p with 2^k | p - 1 (a number-theoretic transform). Products over Z,
over Z/mZ for any m, and over Q are reduced to it by several primes and the
Chinese remainder theorem. A floating point version over C is included for
comparison. Costs are in ring operations of Z/pZ: O(N log N) for N >= m + n - 1.
"""

from __future__ import annotations

import cmath
from fractions import Fraction
from math import lcm
from typing import List, Sequence

# Primes p = c 2^k + 1 with a primitive root g, for the exact transform.
NTT_PRIMES = [(998244353, 3), (167772161, 3), (469762049, 3), (754974721, 11)]


def _normalize(c: List) -> List:
    while c and c[-1] == 0:
        c.pop()
    return c


def ntt(a: List[int], omega: int, p: int) -> None:
    """In-place DFT of a, of length N = 2^k, at the powers of omega modulo p.

    Precondition: omega^N = 1 and omega^(N/2) = -1 modulo p.
    Cost: (N/2) log2 N butterflies, each 2 multiplications and 2 additions.
    """
    n = len(a)
    j = 0
    for i in range(1, n):  # @line F1: bit-reversal permutation
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2  # @line F2
    while length <= n:  # @line F3
        w_len = pow(omega, n // length, p)  # @line F4
        half = length // 2
        for s in range(0, n, length):  # @line F5
            w = 1  # @line F6
            for k in range(half):  # @line F7
                t = w * a[s + k + half] % p  # @line F8
                x = a[s + k]
                a[s + k] = (x + t) % p  # @line F9
                a[s + k + half] = (x - t) % p
                w = w * w_len % p  # @line F10
        length <<= 1  # @line F11


def multiply_mod(a: Sequence[int], b: Sequence[int], p: int = 998244353, g: int = 3) -> List[int]:
    """The product a b over Z/pZ by the number-theoretic transform.

    Precondition: p is prime, g generates (Z/pZ)^*, and 2^k divides p - 1 for
    the power of two N >= len(a) + len(b) - 1. Cost: O(N log N) operations mod p.
    """
    m, n = len(a), len(b)
    if m == 0 or n == 0:  # @line L1
        return []
    size = 1
    while size < m + n - 1:  # @line L2
        size <<= 1
    if (p - 1) % size:
        raise ValueError("p - 1 is not divisible by the transform length")
    fa = [x % p for x in a] + [0] * (size - m)  # @line L3
    fb = [x % p for x in b] + [0] * (size - n)
    omega = pow(g, (p - 1) // size, p)
    ntt(fa, omega, p)  # @line L4
    ntt(fb, omega, p)
    for i in range(size):  # @line L5
        fa[i] = fa[i] * fb[i] % p
    ntt(fa, pow(omega, p - 2, p), p)  # @line L6
    inv = pow(size, p - 2, p)
    c = [x * inv % p for x in fa[: m + n - 1]]
    return _normalize(c)  # @line L7


def _is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.4 * 10^14."""
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for b in (2, 3, 5, 7, 11, 13, 17):
        x = pow(b, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _primitive_root(p: int) -> int:
    """The least generator of (Z/pZ)^* for a prime p with p - 1 = c 2^k, c small."""
    m, factors, q = p - 1, [2], 3
    while m % 2 == 0:
        m //= 2
    while q * q <= m:
        if m % q == 0:
            factors.append(q)
            while m % q == 0:
                m //= q
        q += 2
    if m > 1:
        factors.append(m)
    g = 2
    while any(pow(g, (p - 1) // f, p) == 1 for f in factors):
        g += 1
    return g


MAX_LOG = 20  # the extra primes support transform lengths up to 2^20


def _crt_primes(count: int, size: int) -> List[tuple]:
    """count primes p with size | p - 1, each with a primitive root."""
    if size > 1 << MAX_LOG:
        raise ValueError("transform length too large")
    out = [(p, g) for p, g in NTT_PRIMES if (p - 1) % size == 0][:count]
    c = 1
    while len(out) < count:
        p = (c << MAX_LOG) + 1
        if _is_prime(p) and all(p != q for q, _ in out):
            out.append((p, _primitive_root(p)))
        c += 1
    return out


def multiply_int(a: Sequence[int], b: Sequence[int]) -> List[int]:
    """The product a b over Z, exact, by several NTT primes and the CRT.

    Enough primes are used so that their product exceeds twice the bound
    min(m, n) max|a_i| max|b_j| on the absolute value of a coefficient.
    Cost: O(N log N) operations modulo each of the O(1 + log(bound) / 30) primes.
    """
    if not a or not b:
        return []
    bound = min(len(a), len(b)) * max(abs(x) for x in a) * max(abs(x) for x in b)
    size = 1
    while size < len(a) + len(b) - 1:
        size <<= 1
    count, prod = 0, 1
    for p, _ in NTT_PRIMES:
        if prod > 2 * bound:
            break
        count, prod = count + 1, prod * p
    if prod <= 2 * bound:
        count = (2 * bound).bit_length() // 20 + 1
    primes = _crt_primes(count, size)
    residues, mods, prod = [], [], 1
    for p, g in primes:
        residues.append(multiply_mod(a, b, p, g) + [0] * (len(a) + len(b) - 1))
        mods.append(p)
        prod *= p
    out = []
    for i in range(len(a) + len(b) - 1):
        x, mod = 0, 1
        for r, p in zip(residues, mods):
            # Garner step: x = x + mod * ((r_i - x) / mod mod p)
            t = (r[i] - x) * pow(mod, p - 2, p) % p
            x += mod * t
            mod *= p
        if x > prod // 2:
            x -= prod
        out.append(x)
    return _normalize(out)


def multiply_mod_any(a: Sequence[int], b: Sequence[int], m: int) -> List[int]:
    """The product a b over Z/mZ for any modulus m >= 2, through Z."""
    c = multiply_int([x % m for x in a], [x % m for x in b])
    return _normalize([x % m for x in c])


def multiply_fraction(a: Sequence[Fraction], b: Sequence[Fraction]) -> List[Fraction]:
    """The product a b over Q: clear denominators, multiply over Z, divide back."""
    if not a or not b:
        return []
    da = lcm(*[Fraction(x).denominator for x in a])
    db = lcm(*[Fraction(x).denominator for x in b])
    ia = [int(Fraction(x) * da) for x in a]
    ib = [int(Fraction(x) * db) for x in b]
    c = multiply_int(ia, ib)
    return [Fraction(x, da * db) for x in c]


def multiply_complex(a: Sequence[int], b: Sequence[int]) -> List[int]:
    """The product a b over Z by a floating point FFT over C, rounded.

    Correct only while the rounding error stays below 1/2; for 53-bit doubles
    this holds in practice when N max|a_i| max|b_j| is well below 2^50.
    """
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return []
    size = 1
    while size < m + n - 1:
        size <<= 1

    def fft(v: List[complex], sign: int) -> None:
        j = 0
        for i in range(1, size):
            bit = size >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j:
                v[i], v[j] = v[j], v[i]
        length = 2
        while length <= size:
            half = length // 2
            for k in range(half):
                w = cmath.exp(sign * 2j * cmath.pi * k / length)
                for s in range(0, size, length):
                    t = w * v[s + k + half]
                    x = v[s + k]
                    v[s + k] = x + t
                    v[s + k + half] = x - t
            length <<= 1

    fa = [complex(x) for x in a] + [0j] * (size - m)
    fb = [complex(x) for x in b] + [0j] * (size - n)
    fft(fa, -1)
    fft(fb, -1)
    fc = [x * y for x, y in zip(fa, fb)]
    fft(fc, 1)
    return _normalize([round(x.real / size) for x in fc[: m + n - 1]])
