# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/continued-fraction-factorization/. The authors are listed in prov/ZB7C0A.jsonl.

from math import exp, gcd, isqrt, log

MULTIPLIERS = (1, 3, 5, 7, 11, 13, 15, 17, 19, 21, 23, 29, 31, 33, 35, 37)


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


def factor_base(d: int, bound: int) -> list[int]:
    """-1, 2 and the odd primes p <= bound with p | d or d a square modulo p."""
    base = [-1, 2]
    for p in primes_up_to(bound)[1:]:
        if d % p == 0 or pow(d % p, (p - 1) // 2, p) == 1:
            base.append(p)
    return base


def exponents(v: int, base: list[int]) -> list[int] | None:
    """The exponents of v over the factor base, or None if v is not smooth."""
    e = [0] * len(base)
    if v < 0:
        e[0], v = 1, -v
    for j in range(1, len(base)):
        p = base[j]
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


def cfrac(n: int, k: int = 1, bound: int = 0, extra: int = 10, limit: int = 0) -> int:
    """Morrison-Brillhart continued fraction factorization of n with multiplier k.

    Precondition: n >= 3 odd, not a prime power, k >= 1, k * n not a square.
    It expands sqrt(k n) until it has len(base) + extra smooth residues
    (-1)^i Q_i, or `limit` steps, then combines them by linear algebra over GF(2).
    Returns a proper factor of n, or 1 if this multiplier fails.
    Cost: heuristically L_n[1/2, sqrt(2)] steps with the best bound and trial
    division; the elimination costs O(K^3 / w) for K primes in the base.
    """
    if n < 3 or k < 1:
        raise ValueError("need n >= 3 and k >= 1")
    d = k * n  # @line L1
    a0 = isqrt(d)
    if a0 * a0 == d:
        raise ValueError("k * n must not be a perfect square")
    if bound <= 0:
        ln = log(n)
        bound = max(30, int(exp(0.5 * (ln * log(ln)) ** 0.5)))
    base = factor_base(d, bound)
    if limit <= 0:
        limit = 2000 * len(base) + 10000
    p, q_prev, q = a0, 1, d - a0 * a0  # @line L2
    a_prev, a = 1, a0 % n
    rels: list[tuple[int, list[int]]] = []
    i = 1
    while len(rels) < len(base) + extra and i < limit:  # @line L3
        e = exponents(q if i % 2 == 0 else -q, base)  # @line L4
        if e is not None:
            rels.append((a, e))
        b = (a0 + p) // q  # @line L5
        p_new = b * q - p
        q_prev, q = q, q_prev + b * (p - p_new)
        p = p_new
        a_prev, a = a, (b * a + a_prev) % n
        i += 1
    vectors = [sum((c & 1) << j for j, c in enumerate(e)) for _, e in rels]
    for mask in dependencies(vectors):  # @line L6
        x, total = 1, [0] * len(base)  # @line L7
        for j, (aj, e) in enumerate(rels):
            if mask >> j & 1:
                x = x * aj % n
                total = [s + c for s, c in zip(total, e)]
        y = 1
        for pj, c in zip(base[1:], total[1:]):
            y = y * pow(pj, c // 2, n) % n
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


def _split(m: int) -> int:
    """A proper factor of a composite m with no prime factor below 100.

    A perfect power r^e is split by r. Otherwise CFRAC runs with the multipliers
    in turn. Trial division is the last resort."""
    for e in range(2, m.bit_length() // 6 + 2):
        r = iroot(m, e)
        if r**e == m:
            return r
    for k in MULTIPLIERS:
        if gcd(k, m) > 1:
            continue
        s = isqrt(k * m)
        if s * s == k * m:
            continue
        g = cfrac(m, k)
        if g > 1:
            return g
    d = 101
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division removes the primes below 100, then each composite part is split
    by CFRAC. A loop with an explicit stack replaces recursion."""
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
