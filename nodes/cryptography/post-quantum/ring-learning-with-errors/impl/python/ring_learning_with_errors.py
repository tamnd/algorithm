# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-learning-with-errors/. The authors are listed in prov/4YZXDV.jsonl.
"""Ring-LWE over R_q = Z_q[x]/(x^n + 1) with a negacyclic number theoretic transform.

Polynomials are lists of n coefficients in [0, q), lowest degree first.
mul_schoolbook() is the O(n^2) product in R_q (x^n = -1).
ntt() and intt() are the O(n log n) negacyclic NTT for a prime q = 1 mod 2n:
Cooley-Tukey butterflies with the powers of a primitive 2n-th root of unity
psi in bit-reversed order, and Gentleman-Sande butterflies for the inverse.
sample_ring_lwe() returns (a, b = a s + e) with small s and e.

For study only. The code is not constant time, uses the random module, and
runs only on toy or textbook parameters. Use a FIPS 140 validated ML-KEM
module for real data.
"""

import random
from typing import List, Sequence, Tuple

Poly = List[int]


def mul_schoolbook(a: Sequence[int], b: Sequence[int], q: int) -> Poly:
    """a b in Z_q[x]/(x^n + 1). Cost: n^2 multiplications mod q."""
    n = len(a)
    c = [0] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n):
            k = i + j
            if k < n:
                c[k] += a[i] * b[j]
            else:
                c[k - n] -= a[i] * b[j]  # x^n = -1
    return [x % q for x in c]


def rotation_matrix(a: Sequence[int], q: int) -> List[List[int]]:
    """The n x n matrix of multiplication by a: column j holds x^j a mod (x^n + 1)."""
    n = len(a)
    cols = []
    col = list(a)
    for _ in range(n):
        cols.append([x % q for x in col])
        col = [(-col[-1]) % q] + col[:-1]  # multiply by x: shift, wrap with a sign
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def bit_reverse(i: int, bits: int) -> int:
    r = 0
    for _ in range(bits):
        r = (r << 1) | (i & 1)
        i >>= 1
    return r


def primitive_root_2n(n: int, q: int) -> int:
    """The least psi in Z_q with psi^n = -1, a primitive 2n-th root of unity.

    n must be a power of 2 and q a prime with q = 1 mod 2n.
    """
    if (q - 1) % (2 * n):
        raise ValueError("q must be 1 mod 2n")
    for g in range(2, q):
        psi = pow(g, (q - 1) // (2 * n), q)
        if pow(psi, n, q) == q - 1:
            return psi
    raise ValueError("no root found")


def ntt_tables(n: int, q: int, psi: int) -> Tuple[Poly, Poly]:
    """Powers psi^brv(i) and psi^(-brv(i)) for i < n, brv on log2 n bits."""
    bits = n.bit_length() - 1
    inv = pow(psi, -1, q)
    fwd = [pow(psi, bit_reverse(i, bits), q) for i in range(n)]
    bwd = [pow(inv, bit_reverse(i, bits), q) for i in range(n)]
    return fwd, bwd


def ntt(a: Sequence[int], q: int, fwd: Sequence[int]) -> Poly:
    """Forward negacyclic NTT, output in bit-reversed order.

    Entry i of the output is a(psi^(2 brv(i) + 1)), the value of a at one
    root of x^n + 1. Cost: (n/2) log2 n butterflies.
    """
    f = [x % q for x in a]
    n = len(f)
    t, m = n, 1
    while m < n:
        t //= 2
        for i in range(m):
            z = fwd[m + i]
            for j in range(2 * i * t, 2 * i * t + t):
                u, v = f[j], f[j + t] * z % q
                f[j], f[j + t] = (u + v) % q, (u - v) % q
        m *= 2
    return f


def intt(f: Sequence[int], q: int, bwd: Sequence[int]) -> Poly:
    """Inverse of ntt(): Gentleman-Sande butterflies, then a factor 1/n."""
    a = list(f)
    n = len(a)
    t, m = 1, n
    while m > 1:
        h = m // 2
        j1 = 0
        for i in range(h):
            z = bwd[h + i]
            for j in range(j1, j1 + t):
                u, v = a[j], a[j + t]
                a[j] = (u + v) % q
                a[j + t] = (u - v) * z % q
            j1 += 2 * t
        t *= 2
        m = h
    n_inv = pow(n, -1, q)
    return [x * n_inv % q for x in a]


def mul_ntt(a: Sequence[int], b: Sequence[int], q: int, fwd: Sequence[int], bwd: Sequence[int]) -> Poly:
    """a b in R_q by NTT, pointwise product and inverse NTT. Cost: O(n log n)."""
    fa, fb = ntt(a, q, fwd), ntt(b, q, fwd)
    return intt([x * y % q for x, y in zip(fa, fb)], q, bwd)


def small_poly(n: int, bound: int, q: int, rng: random.Random) -> Poly:
    """Coefficients uniform in [-bound, bound], stored mod q."""
    return [rng.randint(-bound, bound) % q for _ in range(n)]


def sample_ring_lwe(
    n: int, q: int, bound: int, rng: random.Random, s: Sequence[int] = None
) -> Tuple[Poly, Poly, Poly, Poly]:
    """One Ring-LWE sample (a, b = a s + e) in R_q, with s and e small.

    The secret is in normal form (small coefficients), as in the schemes.
    Returns (a, b, s, e).
    """
    if s is None:
        s = small_poly(n, bound, q, rng)
    a = [rng.randrange(q) for _ in range(n)]
    e = small_poly(n, bound, q, rng)
    b = [(x + y) % q for x, y in zip(mul_schoolbook(a, s, q), e)]
    return a, b, list(s), e


def as_lwe_samples(a: Sequence[int], b: Sequence[int], q: int) -> Tuple[List[List[int]], Poly]:
    """One Ring-LWE sample as n plain LWE samples (A, b) with A the rotation matrix of a."""
    return rotation_matrix(a, q), list(b)
