# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pratt-certificate/. The authors are listed in prov/QY13TB.jsonl.

"""Pratt certificates of primality.

A certificate for n is a list of entries (p, a, factors), where p is an odd
prime, factors maps each prime q of p - 1 to its exponent, and a satisfies
    a^((p-1)/2) = -1 (mod p),  a^((p-1)/(2q)) != -1 (mod p) for each odd q.
Each odd q of an entry must be the p of an earlier entry, so the list is the
Lucas tree in bottom-up order, with shared primes listed once.

verify_pratt(n, cert) checks a certificate: deterministic, with
O(log n) entries and O((log n)^2) modular multiplications, so O((log n)^4)
bit operations with schoolbook arithmetic on integers of bit length log n.
build_pratt(n) builds one; its cost is dominated by factoring each p - 1.
All loops are iterative; there is no recursion.
"""

import math
import random

Entry = tuple[int, int, dict[int, int]]


def verify_pratt(n: int, cert: list[Entry]) -> bool:
    if n == 2:  # @line L1
        return True
    if n < 3 or n % 2 == 0:  # @line L2
        return False
    proven = {2}  # @line L3
    for p, a, factors in cert:  # @line L4
        prod = 1
        for q, e in factors.items():
            prod *= q**e if e >= 1 else 0
        if p < 3 or p % 2 == 0 or prod != p - 1:  # @line L5
            return False
        if any(q not in proven for q in factors):  # @line L6
            return False
        if pow(a, (p - 1) // 2, p) != p - 1:  # @line L7
            return False
        for q in factors:  # @line L8
            if q != 2 and pow(a, (p - 1) // (2 * q), p) == p - 1:  # @line L9
                return False
        proven.add(p)  # @line L10
    return n in proven  # @line L11


def multiplications(e: int) -> int:
    """Modular multiplications of the left-to-right binary method for x^e."""
    return 0 if e <= 1 else e.bit_length() - 1 + bin(e).count("1") - 1


def verify_cost(cert: list[Entry]) -> int:
    """M(p): the multiplications that verify_pratt does with the binary method."""
    total = 0
    for p, _, factors in cert:
        total += multiplications((p - 1) // 2)
        total += sum(multiplications((p - 1) // (2 * q)) for q in factors if q != 2)
    return total


# Helpers for the builder. They may err (a probable prime that is composite);
# the builder then fails to find a base, so it never returns a false certificate.


def _strong_probable(n: int, a: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def _probable_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    return all(_strong_probable(n, a) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41) if a % n)


def _rho(n: int, rng: random.Random) -> int:
    """A nontrivial factor of the odd composite n (Pollard rho, Brent's cycle)."""
    while True:
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g, r, q = 1, 1, 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
        if g != n:
            return g


def factorize(m: int, rng: random.Random, small: int = 10_000) -> dict[int, int]:
    """Prime factorization of m >= 1: trial division, then Pollard rho."""
    f: dict[int, int] = {}
    for d in (2, 3):
        while m % d == 0:
            f[d] = f.get(d, 0) + 1
            m //= d
    d = 5
    while d <= small and d * d <= m:
        for dd in (d, d + 2):
            while m % dd == 0:
                f[dd] = f.get(dd, 0) + 1
                m //= dd
        d += 6
    stack = [m] if m > 1 else []
    while stack:
        x = stack.pop()
        if _probable_prime(x):
            f[x] = f.get(x, 0) + 1
            continue
        r = math.isqrt(x)
        if r * r == x:
            stack += [r, r]
            continue
        g = _rho(x, rng)
        stack += [g, x // g]
    return f


def build_pratt(n: int, rng: random.Random | None = None, tries: int = 10_000) -> list[Entry] | None:
    """A Pratt certificate for n, or None if n is not prime (or no base is found).

    The result lists every odd prime of the Lucas tree once, children first,
    with the smallest base that works for each prime."""
    rng = rng if rng is not None else random.Random()
    if n == 2:
        return []
    if n < 3 or n % 2 == 0 or not _probable_prime(n):
        return None  # a composite has no certificate; this check only saves time
    order: list[int] = []
    facts: dict[int, dict[int, int]] = {}
    stack = [n]
    while stack:  # depth-first, iterative; each prime is factored once
        p = stack.pop()
        if p in facts:
            continue
        facts[p] = factorize(p - 1, rng)
        order.append(p)
        stack += [q for q in facts[p] if q != 2 and q not in facts]
    cert: list[Entry] = []
    for p in sorted(order):  # every q of p - 1 is smaller than p
        f = facts[p]
        base = 0
        for a in range(2, min(p, 2 + tries)):
            if pow(a, (p - 1) // 2, p) == p - 1 and all(
                pow(a, (p - 1) // (2 * q), p) != p - 1 for q in f if q != 2
            ):
                base = a
                break
        if base == 0:
            return None
        cert.append((p, base, f))
    return cert if verify_pratt(n, cert) else None
