# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elliptic-curve-factorization/. The authors are listed in prov/FMGN8V.jsonl.

import random
from math import gcd, isqrt
from typing import Optional

def primes_up_to(b: int) -> list[int]:
    """The primes p <= b, by the sieve of Eratosthenes in O(b log log b) time."""
    if b < 2:
        return []
    sieve = bytearray([1]) * (b + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, isqrt(b) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, b + 1, i)))
    return [i for i in range(b + 1) if sieve[i]]



Point = Optional[tuple[int, int]]  # None is the point at infinity O


class Found(Exception):
    """Raised when an inverse mod n does not exist; g = gcd(d, n) > 1."""

    def __init__(self, g: int) -> None:
        super().__init__(g)
        self.g = g


def inverse(d: int, n: int) -> int:
    """d^(-1) mod n, or raise Found(gcd(d, n)) when d is not invertible."""
    g = gcd(d, n)
    if g != 1:
        raise Found(g)  # @line L6
    return pow(d, -1, n)


def add(p: Point, q: Point, a: int, n: int) -> Point:
    """The sum of two points of y^2 = x^3 + a x + b over Z/nZ, by the chord and
    tangent rules. The cases are told apart modulo n; a denominator that is not
    invertible raises Found. Cost: O(1) multiplications and one inverse mod n."""
    if p is None:
        return q
    if q is None:
        return p
    x1, y1 = p
    x2, y2 = q
    if (x1 - x2) % n:
        lam = (y2 - y1) * inverse(x2 - x1, n) % n
    elif (y1 + y2) % n == 0:
        return None
    else:
        lam = (3 * x1 * x1 + a) * inverse(y1 + y2, n) % n
    x3 = (lam * lam - x1 - x2) % n
    return x3, (lam * (x1 - x3) - y1) % n


def multiply(p: Point, m: int, a: int, n: int) -> Point:
    """[m]p for m >= 1, by left to right double and add with O(log m) additions."""
    r = p
    for bit in bin(m)[3:]:
        r = add(r, r, a, n)
        if bit == "1":
            r = add(r, p, a, n)
    return r


def ecm(n: int, b1: int, b2: int, curves: int, seed: int = 0) -> int:
    """Lenstra's elliptic curve method with a stage two up to b2.

    Precondition: n > 1 odd, gcd(n, 6) = 1, b2 >= b1 >= 2. Returns a proper factor
    of n, or 1 if no curve finds one. Each curve costs O(b1 + pi(b2) + G) point
    additions, where G is the largest gap between primes in (b1, b2], and each
    addition costs O(1) multiplications and one inverse mod n."""
    rng = random.Random(seed)
    small = primes_up_to(b1)
    large = [q for q in primes_up_to(b2) if q > b1]
    gap = max([v - u for u, v in zip(large, large[1:])], default=2)
    for _ in range(curves):  # @line L1
        x, y, a = rng.randrange(n), rng.randrange(n), rng.randrange(n)  # @line L2
        b = (y * y - x * x * x - a * x) % n
        g = gcd(4 * a * a * a + 27 * b * b, n)
        if g == n:  # @line L3
            continue
        if g > 1:
            return g
        try:
            p: Point = (x, y)
            for q in small:  # @line L4
                qe = q
                while qe <= b1:
                    p = multiply(p, q, a, n)
                    qe *= q
                if p is None:
                    break
            if p is None or not large:
                continue
            r = multiply(p, large[0], a, n)  # @line L5
            table: list[Point] = [None, add(p, p, a, n)]  # table[j] = [2j]p
            while len(table) <= gap // 2:
                table.append(add(table[-1], table[1], a, n))
            for i in range(1, len(large)):
                if r is None:
                    break
                r = add(r, table[(large[i] - large[i - 1]) // 2], a, n)
        except Found as f:  # @line L6
            if f.g < n:
                return f.g
    return 1  # @line L7


_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_probable_prime(n: int) -> bool:
    """Strong probable-prime test to the 13 prime bases up to 41.

    It is a proof of primality for n < 3317044064679887385961981 (about 3.3 * 10^24)."""
    if n < 2:
        return False
    for p in _BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
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


_PRIMES: list[int] = primes_up_to(1 << 12)
_PRIME_CAP = 1 << 22


def _primes_to(b: int) -> list[int]:
    """A cached list of primes that covers every prime up to min(b, 2^22)."""
    global _PRIMES
    b = min(b, _PRIME_CAP)
    if _PRIMES[-1] < b:
        _PRIMES = primes_up_to(max(b, 2 * _PRIMES[-1]))
    return _PRIMES

def iroot(m: int, k: int) -> int:
    """The integer k-th root floor(m^(1/k)) of m >= 0, by Newton's method."""
    if m < 2:
        return m
    x = 1 << ((m.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + m // x ** (k - 1)) // k
        if y >= x:
            return x
        x = y


def _split(m: int) -> int:
    """A proper factor of a composite m with no prime factor below 1000.

    A perfect power r^k gives r. Otherwise ECM runs with B1 doubling from 100 and
    B2 = 50 B1, 20 curves per round. Trial division is the last resort."""
    for k in range(2, m.bit_length() + 1):
        r = iroot(m, k)
        if r ** k == m:
            return r
    b1 = 100
    for rnd in range(14):
        g = ecm(m, b1, 50 * b1, 20, seed=rnd)
        if g > 1:
            return g
        b1 *= 2
    d = 1001
    while m % d:
        d += 2
    return d


_SMALL = primes_up_to(1000)


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division removes the primes below 1000, then each composite part is split
    by ECM. A loop with an explicit stack replaces recursion."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    for d in _SMALL:
        if d * d > n:
            break
        while n % d == 0:
            out.append(d)
            n //= d
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_probable_prime(m):
            out.append(m)
            continue
        g = _split(m)
        stack.extend((g, m // g))
    return sorted(out)
