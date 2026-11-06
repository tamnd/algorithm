# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dixon-random-squares/. The authors are listed in prov/11JRDA.jsonl.

import random
from math import exp, gcd, isqrt, log


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


def exponents(v: int, base: list[int]) -> list[int] | None:
    """The exponents of v >= 1 over the primes in base, or None if v is not smooth."""
    e = [0] * len(base)
    for j, p in enumerate(base):
        if v == 1:
            break
        while v % p == 0:
            v //= p
            e[j] += 1
    return e if v == 1 else None


def dependencies(vectors: list[int]) -> list[int]:
    """Subsets (as bit masks over the rows) whose vectors add to zero over GF(2),
    by Gaussian elimination on bit masks. One subset per linearly dependent row."""
    pivots: dict[int, tuple[int, int]] = {}
    found = []
    for j, v in enumerate(vectors):
        h = 1 << j
        while v:
            top = v.bit_length() - 1
            if top not in pivots:
                pivots[top] = (v, h)
                break
            pv, ph = pivots[top]
            v, h = v ^ pv, h ^ ph
        if v == 0:
            found.append(h)
    return found


def default_bound(n: int) -> int:
    """The smoothness bound exp((1/2) (ln n ln ln n)^(1/2)), at least 30."""
    ln = log(n)
    return max(30, int(exp(0.5 * (ln * log(ln)) ** 0.5)))


def dixon(n: int, bound: int = 0, extra: int = 10, limit: int = 0, seed: int = 0) -> int:
    """Dixon's random squares method on n.

    Precondition: n >= 3. It draws random z in [1, n - 1] until it has
    len(base) + extra values z with z^2 mod n smooth over the primes <= bound,
    or `limit` draws, then combines them by linear algebra over GF(2).
    Returns a proper factor of n, or 1 on failure (always 1 for a prime n).
    Cost: with bound about L_n[1/2, 1/2] the expected number of draws is
    L_n[1/2, 3/2 + o(1)] with trial division, each O(len(base)) divisions.
    """
    if n < 3:
        raise ValueError("need n >= 3")
    if bound <= 0:
        bound = default_bound(n)
    if limit <= 0:
        limit = 10**6
    rng = random.Random(seed)
    base = primes_up_to(bound)  # @line L1
    rels: list[tuple[int, list[int]]] = []
    t = 0
    while len(rels) < len(base) + extra and t < limit:  # @line L2
        z = rng.randrange(1, n)  # @line L3
        t += 1
        g = gcd(z, n)
        if g > 1:  # @line L4
            return g
        e = exponents(z * z % n, base)  # @line L5
        if e is not None:
            rels.append((z, e))
    vectors = [sum((c & 1) << j for j, c in enumerate(e)) for _, e in rels]
    for mask in dependencies(vectors):  # @line L6
        x, total = 1, [0] * len(base)  # @line L7
        for j, (zj, e) in enumerate(rels):
            if mask >> j & 1:
                x = x * zj % n
                total = [s + c for s, c in zip(total, e)]
        y = 1
        for p, c in zip(base, total):
            y = y * pow(p, c // 2, n) % n
        g = gcd(x - y, n)  # @line L8
        if 1 < g < n:
            return g
    return 1  # @line L9


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


def iroot(m: int, e: int) -> int:
    """The integer e-th root floor(m^(1/e)) of m >= 0, by Newton's method."""
    if m < 2:
        return m
    x = 1 << ((m.bit_length() + e - 1) // e)
    while True:
        y = ((e - 1) * x + m // x ** (e - 1)) // e
        if y >= x:
            return x
        x = y


_SMALL = primes_up_to(1000)


def _split(m: int) -> int:
    """A proper factor of a composite m with no prime factor below 1000.

    A perfect power r^e is split by r. Otherwise Dixon's method runs with
    seeds 0, 1, 2, ... Trial division is the last resort."""
    for e in range(2, m.bit_length() // 9 + 2):
        r = iroot(m, e)
        if r**e == m:
            return r
    for seed in range(8):
        g = dixon(m, seed=seed)
        if g > 1:
            return g
    d = 1001
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division removes the primes below 1000, then each composite part is
    split by Dixon's method. A loop with an explicit stack replaces recursion."""
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
