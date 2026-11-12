# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/macwilliams-identity/. The authors are listed in prov/1E7DCT.jsonl.

"""The MacWilliams identity W_{C-perp}(x, y) = (1/|C|) W_C(x + (q - 1) y, x - y) for linear
codes over GF(p), p prime. Words are tuples of ints in range(p).

A homogeneous polynomial sum_i c_i x^(n - i) y^i of degree n is stored as [c_0, ..., c_n].
"""

from fractions import Fraction
from itertools import product
from math import comb


def span(gen: list[tuple[int, ...]], p: int) -> list[tuple[int, ...]]:
    """All words m G of the code with generator rows gen over GF(p) (as a set, sorted)."""
    n = len(gen[0])
    words = {tuple(sum(a * g[j] for a, g in zip(m, gen)) % p for j in range(n))
             for m in product(range(p), repeat=len(gen))}
    return sorted(words)


def dual_code(words: list[tuple[int, ...]], n: int, p: int) -> list[tuple[int, ...]]:
    """C-perp by brute force: every word with zero inner product with every codeword."""
    return [u for u in product(range(p), repeat=n)
            if all(sum(a * b for a, b in zip(u, c)) % p == 0 for c in words)]


def weight_distribution(words: list[tuple[int, ...]], n: int) -> list[int]:
    """[A_0, ..., A_n]: A_i is the number of codewords of weight i."""
    a = [0] * (n + 1)
    for w in words:
        a[sum(1 for s in w if s)] += 1
    return a


def poly_mul(f: list[int], g: list[int]) -> list[int]:
    """Product of two homogeneous polynomials in x, y given by coefficient lists."""
    h = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                h[i + j] += a * b
    return h


def poly_pow(f: list[int], e: int) -> list[int]:
    out = [1]
    for _ in range(e):
        out = poly_mul(out, f)
    return out


def macwilliams_transform(a: list[int], q: int, size: int) -> list[Fraction]:
    """Substitute x -> x + (q - 1) y and y -> x - y in W(x, y) = sum_i a_i x^(n - i) y^i,
    and divide by size = |C|. Returns the coefficients of the result."""
    n = len(a) - 1
    sx = [1, q - 1]   # x + (q - 1) y
    sy = [1, -1]      # x - y
    total = [0] * (n + 1)
    for i, ai in enumerate(a):
        if ai:
            term = poly_mul(poly_pow(sx, n - i), poly_pow(sy, i))
            for k, c in enumerate(term):
                total[k] += ai * c
    return [Fraction(t, size) for t in total]


def krawtchouk(n: int, k: int, x: int, q: int = 2) -> int:
    return sum((-1) ** j * (q - 1) ** (k - j) * comb(x, j) * comb(n - x, k - j) for j in range(k + 1))


def macwilliams_krawtchouk(a: list[int], q: int, size: int) -> list[Fraction]:
    """The same transform in Krawtchouk form: B_k = (1/|C|) sum_i A_i K_k(i)."""
    n = len(a) - 1
    return [Fraction(sum(ai * krawtchouk(n, k, i, q) for i, ai in enumerate(a)), size) for k in range(n + 1)]


def hamming_code_weights(n: int) -> list[Fraction]:
    """Closed form for the binary Hamming code of length n = 2^r - 1:
    A(z) = ((1 + z)^n + n (1 - z)(1 - z^2)^((n - 1)/2)) / (n + 1)."""
    p1 = [comb(n, i) for i in range(n + 1)]
    m = (n - 1) // 2
    p2 = [0] * (n + 1)
    for j in range(m + 1):
        c = comb(m, j) * (-1) ** j * n
        p2[2 * j] += c        # times 1
        p2[2 * j + 1] -= c    # times -z
    return [Fraction(x + y, n + 1) for x, y in zip(p1, p2)]


def simplex_generator(r: int) -> list[tuple[int, ...]]:
    """Binary simplex code of length 2^r - 1: columns are all nonzero r-bit vectors."""
    n = 2 ** r - 1
    return [tuple((j >> i) & 1 for j in range(1, n + 1)) for i in range(r)]
