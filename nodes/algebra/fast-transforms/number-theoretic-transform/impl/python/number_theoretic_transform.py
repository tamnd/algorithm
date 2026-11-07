# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/number-theoretic-transform/. The authors are listed in prov/7AWXWS.jsonl.

# Primes p = c * 2^k + 1 with the primitive root 3, as (p, g, k).
NTT_PRIMES = [(998244353, 3, 23), (167772161, 3, 25), (469762049, 3, 26)]


def root_of_unity(n: int, p: int, g: int) -> int:
    """Return g^((p-1)/n) mod p, a primitive n-th root of unity modulo p.

    Precondition: p is prime, g is a primitive root modulo p, and n divides
    p - 1; otherwise ValueError.
    """
    if n < 1 or (p - 1) % n:
        raise ValueError("n must divide p - 1")
    return pow(g, (p - 1) // n, p)  # @line L4


def ntt(x: list[int], w: int, p: int) -> None:
    """Replace x by X[k] = sum of x[j] * w^(j*k) mod p, in place.

    Precondition: n = len(x) is a power of two, p is an odd prime, and w has
    order n modulo p. Cost: n lg n additions and (n/2) lg n multiplications
    modulo p, n/2 - 1 more for the table, and O(n) index steps.
    """
    n = len(x)
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    t = n.bit_length() - 1
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):  # @line L10
        if j < rev[j]:
            x[j], x[rev[j]] = x[rev[j]], x[j]
    table = [1] * max(n // 2, 1)  # @line L11
    for k in range(1, n // 2):
        table[k] = table[k - 1] * w % p
    h = 1  # @line L12
    while h < n:  # @line L13
        step = n // (2 * h)
        for s in range(0, n, 2 * h):  # @line L14
            for k in range(h):  # @line L15
                u = x[s + k]  # @line L16
                v = table[k * step] * x[s + k + h] % p  # @line L16
                x[s + k] = (u + v) % p  # @line L17
                x[s + k + h] = (u - v) % p  # @line L17
        h *= 2  # @line L18


def multiply_mod(a: list[int], b: list[int], p: int = 998244353, g: int = 3) -> list[int]:
    """Return the coefficients of a(t) * b(t) modulo the prime p.

    Precondition: g is a primitive root modulo p, and the least power of two
    n >= len(a) + len(b) - 1 divides p - 1. Cost: three NTTs of length n,
    n pointwise products and n scalings, so O(n log n) operations modulo p.
    """
    if not a or not b:
        return []
    m = len(a) + len(b) - 1  # @line L1
    n = 1  # @line L2
    while n < m:
        n *= 2
    if (p - 1) % n:  # @line L3
        raise ValueError("p - 1 is not divisible by the transform length")
    w = root_of_unity(n, p, g)
    fa = [v % p for v in a] + [0] * (n - len(a))  # @line L5
    fb = [v % p for v in b] + [0] * (n - len(b))  # @line L5
    ntt(fa, w, p)  # @line L6
    ntt(fb, w, p)  # @line L6
    fc = [u * v % p for u, v in zip(fa, fb)]  # @line L7
    ntt(fc, pow(w, -1, p), p)  # @line L8
    n_inv = pow(n, -1, p)
    return [fc[j] * n_inv % p for j in range(m)]  # @line L9


def multiply_exact(a: list[int], b: list[int]) -> list[int]:
    """Return the exact integer coefficients of a(t) * b(t).

    Uses the three primes of NTT_PRIMES and the Chinese remainder theorem.
    Precondition: every coefficient c of the product has |c| < P/2, where P
    is the product of the three primes (about 7.9 * 10^25); this holds when
    min(len(a), len(b)) * max|a| * max|b| < P/2. Length limit: 2^23.
    """
    if not a or not b:
        return []
    res = [multiply_mod(a, b, p, g) for p, g, _ in NTT_PRIMES]
    (p1, _, _), (p2, _, _), (p3, _, _) = NTT_PRIMES
    big = p1 * p2 * p3
    inv1 = pow(p1, -1, p2)
    inv12 = pow(p1 * p2, -1, p3)
    out = []
    for r1, r2, r3 in zip(*res):
        # Garner's mixed-radix form: c = r1 + p1 * (y2 + p2 * y3).
        y2 = (r2 - r1) * inv1 % p2
        c12 = r1 + p1 * y2
        y3 = (r3 - c12) * inv12 % p3
        c = c12 + p1 * p2 * y3
        out.append(c - big if c > big // 2 else c)
    return out
