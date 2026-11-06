# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-sieve/. The authors are listed in prov/5TWHZJ.jsonl.

from math import exp, gcd, isqrt, log, log2


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


def sqrt_mod(a: int, p: int) -> int:
    """A square root of a modulo an odd prime p, for a quadratic residue a, by Tonelli-Shanks."""
    a %= p
    if a == 0:
        return 0
    q, s = p - 1, 0
    while q % 2 == 0:
        q, s = q // 2, s + 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2, i = t2 * t2 % p, i + 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


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


def default_bound(n: int) -> int:
    """The smoothness bound 3 L_n[1/2, 1/2] = 3 exp((1/2) (ln n ln ln n)^(1/2)), at least 30.

    The factor 3 suits this implementation, which tests candidates by trial division."""
    ln = log(n)
    return max(30, int(3 * exp(0.5 * (ln * log(ln)) ** 0.5)))


def quadratic_sieve(n: int, bound: int = 0, block: int = 0, extra: int = 10, blocks: int = 0) -> int:
    """Pomerance's quadratic sieve with the single polynomial f(t) = (s + t)^2 - n.

    Precondition: n >= 3 odd and not a perfect square. The factor base holds
    -1, 2 and the odd primes p <= bound with (n/p) = 1, extended past bound
    until it has at least 16 entries. It sieves blocks of
    `block` values of t on both sides of 0, with s = isqrt(n), until it has
    len(base) + extra smooth values f(t), or `blocks` pairs of blocks; then
    combines them by linear algebra over GF(2).
    Returns a proper factor of n, or 1 on failure (always 1 for a prime n).
    Cost: heuristically L_n[1/2, 1 + o(1)] with bound about L_n[1/2, 1/2].
    """
    if n < 3 or n % 2 == 0:
        raise ValueError("need an odd n >= 3")
    s = isqrt(n)
    if s * s == n:
        raise ValueError("n must not be a perfect square")
    if bound <= 0:
        bound = default_bound(n)
    if block <= 0:
        block = max(200, 10 * bound)
    if blocks <= 0:
        blocks = 50
    base, roots = [-1, 2], [(2, 1)]  # @line L1
    for p in primes_up_to(max(bound, 1000))[1:]:
        if p > bound and len(base) >= 16:
            break
        if n % p == 0:
            return p if p < n else 1
        if pow(n % p, (p - 1) // 2, p) == 1:
            r = sqrt_mod(n, p)
            base.append(p)
            roots.append((p, r))
            roots.append((p, p - r))
    logs = {p: log2(p) for p in base[1:]}
    slack = 2 * log2(bound) + 2
    rels: list[tuple[int, list[int]]] = []
    seen: set[int] = set()
    j = 0
    while len(rels) < len(base) + extra and j < blocks:  # @line L2
        for lo in (j * block, -(j + 1) * block):  # @line L3
            lo = max(lo, 1 - s)
            hi = lo + block if lo >= 0 else min(lo + block, -j * block)
            if hi <= lo:
                continue
            sieve = [0.0] * (hi - lo)
            for p, r in roots:  # @line L4
                lg = logs[p]
                for i in range((r - s - lo) % p, hi - lo, p):
                    sieve[i] += lg
            for i, acc in enumerate(sieve):  # @line L5
                x = s + lo + i
                v = x * x - n
                if acc >= log2(abs(v)) - slack and x not in seen:
                    e = exponents(v, base)  # @line L6
                    if e is not None:
                        seen.add(x)
                        rels.append((x, e))
        j += 1
    vectors = [sum((c & 1) << k for k, c in enumerate(e)) for _, e in rels]
    for mask in dependencies(vectors):  # @line L7
        x, total = 1, [0] * len(base)
        for k, (xk, e) in enumerate(rels):
            if mask >> k & 1:
                x = x * xk % n
                total = [a + c for a, c in zip(total, e)]
        y = 1
        for p, c in zip(base[1:], total[1:]):
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


def _split(m: int) -> int:
    """A proper factor of a composite m with no prime factor below 100.

    A perfect power r^e is split by r. Otherwise the quadratic sieve runs with
    growing smoothness bounds. Trial division is the last resort."""
    for e in range(2, m.bit_length() // 6 + 2):
        r = iroot(m, e)
        if r**e == m:
            return r
    b = default_bound(m)
    for _ in range(4):
        g = quadratic_sieve(m, b)
        if g > 1:
            return g
        b *= 2
    d = 101
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division removes the primes below 100, then each composite part is
    split by the quadratic sieve. A loop with an explicit stack replaces recursion."""
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
