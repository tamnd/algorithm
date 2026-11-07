# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multimodular-determinant/. The authors are listed in prov/BETBZR.jsonl.

"""Determinant of an integer matrix by elimination modulo many primes and the Chinese remainder theorem."""

from math import isqrt

_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_prime(n: int) -> bool:
    """Miller-Rabin with the first 13 prime bases, deterministic for n < 3.3 * 10^24."""
    if n < 2:
        return False
    for q in _BASES:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(n: int) -> int:
    """Return the least prime that is at least n."""
    n = max(n, 2)
    while not is_prime(n):
        n += 1
    return n


def hadamard_int(a: list[list[int]]) -> int:
    """Return floor(sqrt(prod of squared row norms)), an integer bound on |det a|."""
    prod = 1
    for row in a:
        prod *= sum(v * v for v in row)
    return isqrt(prod)


def det_mod_p(a: list[list[int]], p: int) -> int:
    """Determinant of a square integer matrix modulo the prime p, by Gaussian elimination with row swaps."""
    n = len(a)
    m = [[v % p for v in row] for row in a]
    det = 1
    for k in range(n):
        piv = next((i for i in range(k, n) if m[i][k] != 0), None)
        if piv is None:
            return 0
        if piv != k:
            m[k], m[piv] = m[piv], m[k]
            det = -det
        det = det * m[k][k] % p
        inv = pow(m[k][k], -1, p)
        for i in range(k + 1, n):
            f = m[i][k] * inv % p
            if f:
                ri, rk = m[i], m[k]
                for j in range(k + 1, n):
                    ri[j] = (ri[j] - f * rk[j]) % p
    return det % p


def multimodular_det_trace(a: list[list[int]], start: int = 1 << 31) -> tuple[int, list[int]]:
    """Return (det a, the primes used), using the primes at least start in increasing order."""
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("the matrix must be square")
    if n == 0:  # @line L1
        return 1, []
    h = hadamard_int(a)  # @line L2
    big_m, r, p = 1, 0, next_prime(start)  # @line L3
    used: list[int] = []
    while big_m <= 2 * h:  # @line L4
        d = det_mod_p(a, p)  # @line L5
        r += big_m * ((d - r) * pow(big_m, -1, p) % p)  # @line L6
        big_m *= p
        used.append(p)
        p = next_prime(p + 1)  # @line L7
    if r > big_m // 2:  # @line L8
        r -= big_m
    return r, used  # @line L9


def multimodular_det(a: list[list[int]], start: int = 1 << 31) -> int:
    """Return the determinant of the square integer matrix a.

    The determinant is computed modulo successive primes p >= start until their
    product M exceeds twice the Hadamard bound H, then reconstructed by the
    Chinese remainder theorem as the residue of absolute value at most M/2.
    """
    return multimodular_det_trace(a, start)[0]
