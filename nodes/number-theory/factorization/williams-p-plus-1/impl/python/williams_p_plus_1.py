# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/williams-p-plus-1/. The authors are listed in prov/XKCQGC.jsonl.

from math import gcd, isqrt


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


def lucas_v(v: int, m: int, n: int) -> int:
    """V_m(v) mod n for the Lucas sequence V_0 = 2, V_1 = v, V_(k+1) = v V_k - V_(k-1).

    Precondition: m >= 1, n >= 2. It keeps the pair (V_j, V_(j+1)) and reads the
    binary digits of m from the top (a binary Lucas chain).
    Cost: 2 multiplications modulo n per binary digit of m."""
    x, y = v % n, (v * v - 2) % n  # @line K1
    for b in bin(m)[3:]:  # @line K2
        if b == "1":
            x, y = (x * y - v) % n, (y * y - 2) % n  # @line K3
        else:
            x, y = (x * x - 2) % n, (x * y - v) % n  # @line K4
    return x  # @line K5


def williams_p_plus_1(n: int, bound: int, seed: int) -> int:
    """Stage 1 of Williams' p + 1 method. Return g = gcd(V_M(seed) - 2, n), where
    M is the product of the largest powers q^e <= bound of the primes q <= bound.

    Precondition: n >= 3, bound >= 1, 0 <= seed < n. The result g divides n. If a
    prime p | n does not divide seed^2 - 4 and p - (D/p) divides M, with D =
    seed^2 - 4 and (D/p) the Legendre symbol, then p divides g.
    Cost: about 2.9 * bound multiplications modulo n, plus a sieve up to bound.
    """
    if n < 3 or bound < 1 or not 0 <= seed < n:
        raise ValueError("need n >= 3, bound >= 1 and 0 <= seed < n")
    v = seed  # @line L1
    for q in primes_up_to(bound):  # @line L2
        qe = q  # @line L3
        while qe * q <= bound:
            qe *= q
        v = lucas_v(v, qe, n)  # @line L4
    g = gcd(v - 2, n)  # @line L5
    return g  # @line L6


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


def _split(m: int) -> int:
    """A proper factor of a composite m with no prime factor below 100.

    Stage 1 runs with the exponents q, one prime at a time (q^k <= m), and a gcd
    after each step, over all primes q <= sqrt(m). If p is the smallest prime
    factor of m and p does not divide seed^2 - 4, then p - (D/p) divides the
    exponent by the end, so the gcd becomes p or m. When it jumps from 1 to m in
    one step, the next seed is tried. Trial division is the last resort."""
    limit = isqrt(m)
    primes = _primes_to(limit)
    for seed in range(3, 40):
        g = gcd(seed * seed - 4, m)
        if 1 < g < m:
            return g
        v = seed
        for q in primes:
            if q > limit:
                break
            qk = q
            while qk <= m:
                v = lucas_v(v, q, m)
                g = gcd(v - 2, m)
                if 1 < g < m:
                    return g
                if g == m:
                    break
                qk *= q
            if g == m:
                break
    d = 101
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division removes the primes below 100, then each composite part is split
    by the p + 1 method. A loop with an explicit stack replaces recursion."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    for d in range(2, 100):
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
