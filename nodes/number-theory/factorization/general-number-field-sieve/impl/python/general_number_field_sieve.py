# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/general-number-field-sieve/. The authors are listed in prov/H28VR1.jsonl.

from math import gcd, isqrt, log2

# Polynomials are lists of integers, lowest degree first. An element of
# Z[alpha] = Z[x]/(f) for a monic f of degree d is a list of d integers.


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


def evaluate(f: list[int], x: int, mod: int = 0) -> int:
    """f(x), or f(x) mod `mod` if mod > 0, by Horner's rule."""
    v = 0
    for c in reversed(f):
        v = v * x + c
        if mod:
            v %= mod
    return v


def homogeneous(f: list[int], a: int, b: int) -> int:
    """F(a, b) = b^d f(a/b), the norm of a - b alpha for a monic f."""
    d = len(f) - 1
    return sum(c * a**i * b ** (d - i) for i, c in enumerate(f))


def derivative(f: list[int]) -> list[int]:
    return [i * c for i, c in enumerate(f)][1:]


def mulmod(u: list[int], v: list[int], f: list[int], mod: int = 0) -> list[int]:
    """u v in Z[x]/(f), with coefficients reduced modulo `mod` if mod > 0.

    Precondition: f is monic of degree d, and u, v have length d."""
    d = len(f) - 1
    w = [0] * (2 * d - 1)
    for i, x in enumerate(u):
        if x:
            for j, y in enumerate(v):
                w[i + j] += x * y
    for k in range(2 * d - 2, d - 1, -1):
        c = w[k]
        if c:
            for j in range(d):
                w[k - d + j] -= c * f[j]
    w = w[:d]
    return [x % mod for x in w] if mod else w


def powmod(u: list[int], e: int, f: list[int], mod: int) -> list[int]:
    """u^e in (Z/mod)[x]/(f), by binary exponentiation."""
    d = len(f) - 1
    r = [1] + [0] * (d - 1)
    while e:
        if e & 1:
            r = mulmod(r, u, f, mod)
        u = mulmod(u, u, f, mod)
        e >>= 1
    return r


def base_m(n: int, d: int, m: int = 0) -> tuple[list[int], int]:
    """The base-m expansion f of n, with f(m) = n, and m.

    Precondition: d >= 2 and n > 2^(2 d^2) or so, so that the leading digit is
    1. By default m = floor(n^(1/d)); then m^d <= n < (m + 1)^d < 2 m^d."""
    if m <= 0:
        m = iroot(n, d)
    f, x = [], n
    for _ in range(d):
        f.append(x % m)
        x //= m
    f.append(x)
    return f, m


def balanced_base_m(n: int, d: int, m: int) -> list[int]:
    """The base-m expansion of n with digits in (-m/2, m/2], so f(m) = n."""
    f, x = [], n
    for _ in range(d):
        c = x % m
        if c > m // 2:
            c -= m
        f.append(c)
        x = (x - c) // m
    f.append(x)
    return f


def select_polynomial(n: int, d: int, tries: int = 64) -> tuple[list[int], int]:
    """A monic f of degree d and an m with f(m) = n, chosen among the balanced
    base-m expansions for m = floor(n^(1/d)), m - 1, ..., with the smallest
    largest coefficient. Smaller coefficients give smaller norms F(a, b)."""
    m0 = iroot(n, d)
    best: tuple[int, list[int], int] | None = None
    for m in range(m0, max(m0 - tries, 1), -1):
        f = balanced_base_m(n, d, m)
        if f[-1] != 1:
            continue
        size = max(abs(c) for c in f[:-1])
        if best is None or size < best[0]:
            best = (size, f, m)
    if best is None:
        return base_m(n, d, m0)
    return best[1], best[2]


def is_inert(f: list[int], p: int) -> bool:
    """True if the monic f of prime degree d is irreducible modulo the prime p.

    For a prime d, f is irreducible modulo p if and only if it has no root
    modulo p and x^(p^d) = x in F_p[x]/(f)."""
    d = len(f) - 1
    if any(evaluate(f, r, p) == 0 for r in range(p)):
        return False
    x = [0, 1] + [0] * (d - 2)
    return powmod(x, p**d, f, p) == x


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


def factor_bases(f: list[int], bound: int, chars: int):
    """Rational primes p <= bound, algebraic pairs (p, r) with f(r) = 0 mod p,
    and `chars` quadratic characters (q, s): primes q > bound with a simple
    root s of f modulo q."""
    fp = derivative(f)
    primes = primes_up_to(bound)
    pairs = [(p, r) for p in primes for r in range(p) if evaluate(f, r, p) == 0]
    qchars: list[tuple[int, int]] = []
    q = bound
    while len(qchars) < chars:
        q += 1
        if all(q % p for p in primes_up_to(isqrt(q))):
            for s in range(q):
                if evaluate(f, s, q) == 0 and evaluate(fp, s, q) != 0:
                    qchars.append((q, s))
                    if len(qchars) == chars:
                        break
    return primes, pairs, qchars


def smooth_exponents(v: int, primes: list[int]) -> list[int] | None:
    """Exponents of |v| over primes, or None if |v| is not smooth over them."""
    v = abs(v)
    if v == 0:
        return None
    e = [0] * len(primes)
    for i, p in enumerate(primes):
        while v % p == 0:
            v //= p
            e[i] += 1
        if v == 1:
            return e
    return e if v == 1 else None


def find_relations(n, f, m, primes, pairs, need, width, max_b):
    """Pairs (a, b) with gcd(a, b) = 1, b >= 1, |a| <= width, such that a - b m
    and F(a, b) are both smooth over primes. Line sieving on both sides, one b
    at a time, with logarithms; candidates are confirmed by trial division."""
    rels = []
    size = 2 * width + 1
    for b in range(1, max_b + 1):  # @line L3
        rat = [0] * size
        alg = [0] * size
        for p in primes:
            lg = p.bit_length()
            for i in range((b * m + width) % p, size, p):
                rat[i] += lg
        for p, r in pairs:
            lg = p.bit_length()
            for i in range((b * r + width) % p, size, p):
                alg[i] += lg
        slack = 2 * primes[-1].bit_length() + 2
        for i in range(size):
            a = i - width
            u = a - b * m
            v = homogeneous(f, a, b)
            if u == 0 or v == 0 or gcd(a, b) != 1:
                continue
            if rat[i] < abs(u).bit_length() - slack or alg[i] < abs(v).bit_length() - slack:
                continue
            eu = smooth_exponents(u, primes)  # @line L4
            if eu is None:
                continue
            ev = smooth_exponents(v, primes)
            if ev is None:
                continue
            rels.append((a, b, u, eu, v, ev))
            if len(rels) >= need:
                return rels
    return rels


def relation_vector(rel, primes, pairs, index, qchars) -> int:
    """The GF(2) vector of a relation: the sign of a - b m, the rational
    exponents, the sign of F(a, b), the exponents of the first degree prime ideals (p, r) with
    a = b r mod p, and the quadratic characters (a - b s / q)."""
    a, b, u, eu, v, ev = rel
    bits = [1 if u < 0 else 0, 1 if v < 0 else 0] + [e & 1 for e in eu]
    alg = [0] * len(pairs)
    for p, e in zip(primes, ev):
        if e:
            r = a * pow(b, -1, p) % p
            alg[index[(p, r)]] = e & 1
    bits += alg
    for q, s in qchars:
        bits.append(1 if pow((a - b * s) % q, (q - 1) // 2, q) == q - 1 else 0)
    return sum(c << k for k, c in enumerate(bits))


def product_in_order(elements: list[list[int]], f: list[int]) -> list[int]:
    """The product of elements of Z[alpha], by a balanced product tree."""
    level = elements
    while len(level) > 1:
        level = [mulmod(level[i], level[i + 1], f) if i + 1 < len(level) else level[i]
                 for i in range(0, len(level), 2)]
    return level[0]


def inert_prime(f: list[int], start: int, tries: int = 2000) -> int:
    """The least prime p > start with p = 3 mod 4 and f irreducible modulo p,
    or 0 if none is found among `tries` candidates. Then F_p[x]/(f) is the
    field with q = p^d elements, and q = 3 mod 4 when d is odd."""
    p = start + 1
    for _ in range(tries):
        if p % 4 == 3 and all(p % t for t in range(2, isqrt(p) + 1)) and is_inert(f, p):
            return p
        p += 1
    return 0


def algebraic_sqrt(gamma: list[int], f: list[int], p: int) -> list[int] | None:
    """delta in Z[alpha] with delta^2 = gamma, or None.

    Precondition: f monic of odd prime degree d, p an inert prime with
    p = 3 mod 4 not dividing the norm of gamma. Computes r = gamma^(-1/2) in
    F_q with q = p^d by one power, lifts it to Z/p^k by Newton's iteration
    r <- r (3 - gamma r^2) / 2, and checks delta = gamma r with symmetric
    coefficients exactly. Gives up when p^k passes a bound on the size."""
    d = len(f) - 1
    q = p**d
    g0 = [c % p for c in gamma]
    r = powmod(g0, (3 * q - 5) // 4, f, p)
    if mulmod(mulmod(r, r, f, p), g0, f, p) != [1] + [0] * (d - 1):
        return None
    limit = 4 * max(abs(c) for c in gamma) + 4
    mod = p
    while mod < limit:
        mod = mod * mod
        g = [c % mod for c in gamma]
        t = mulmod(mulmod(r, r, f, mod), g, f, mod)
        t = [(-c) % mod for c in t]
        t[0] = (t[0] + 3) % mod
        half = pow(2, -1, mod)
        r = [c * half % mod for c in mulmod(r, t, f, mod)]
        delta = mulmod(g, r, f, mod)
        delta = [c - mod if c > mod // 2 else c for c in delta]
        if mulmod(delta, delta, f) == gamma:
            return delta
    return None


def default_bound(n: int) -> int:
    """A smoothness bound for this toy sieve, tuned by experiment for n
    between 2^20 and 2^64: about 200 at 2^20, 900 at 2^40, 6000 at 2^64."""
    return max(150, int(200 * 2 ** ((n.bit_length() - 20) / 9)))


def gnfs(n: int, d: int = 3, bound: int = 0, width: int = 0, chars: int = 0,
         extra: int = 10, m: int = 0, max_b: int = 0) -> int:
    """A proper factor of the odd composite n by the general number field sieve.

    Precondition: n odd, not a prime power and not a perfect power, d in {3, 5},
    and n large enough that the base-m polynomial is monic. Returns a proper
    factor of n, or 1 on failure. Cost: heuristically L_n[1/3, (64/9)^(1/3)]
    with the right choices of d, bound and the sieve region as n grows; this
    toy version uses a fixed small degree."""
    f, m = base_m(n, d, m) if m > 0 else select_polynomial(n, d)  # @line L1
    if f[-1] != 1:
        return 1
    if bound <= 0:
        bound = default_bound(n)
    if width <= 0:
        width = 3 * bound
    if chars <= 0:
        chars = 2 * n.bit_length() // 3 + 10
    if max_b <= 0:
        max_b = 5 * bound
    for p in primes_up_to(max(bound, 2 * chars)):
        if n % p == 0:
            return p if p < n else 1
    g = gcd(evaluate(derivative(f), m), n)
    if 1 < g < n:
        return g
    p_inert = inert_prime(f, max(bound, 2 * chars) + 200)
    if p_inert == 0:
        return 1  # no inert prime: f is probably reducible over Q
    primes, pairs, qchars = factor_bases(f, bound, chars)  # @line L2
    index = {pr: k for k, pr in enumerate(pairs)}
    cols = 2 + len(primes) + len(pairs) + len(qchars)
    rels = find_relations(n, f, m, primes, pairs, cols + extra, width, max_b)
    vectors = [relation_vector(r, primes, pairs, index, qchars) for r in rels]  # @line L5
    fp = derivative(f)
    fpm = evaluate(derivative(f), m, n)
    for mask in dependencies(vectors):  # @line L6
        chosen = [r for k, r in enumerate(rels) if mask >> k & 1]
        total = [0] * len(primes)
        for _, _, _, eu, _, _ in chosen:
            total = [x + y for x, y in zip(total, eu)]
        x = fpm  # @line L7
        for p, e in zip(primes, total):
            x = x * pow(p, e // 2, n) % n
        elems = [[a, -b] + [0] * (len(f) - 3) for a, b, _, _, _, _ in chosen]
        gamma = product_in_order(elems + [fp, fp], f)
        delta = algebraic_sqrt(gamma, f, p_inert)  # @line L8
        if delta is None:
            continue
        y = evaluate(delta, m, n)
        g = gcd(x - y, n)  # @line L9
        if 1 < g < n:
            return g
    return 1  # @line L10


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


_SMALL = primes_up_to(1000)


def _split(m: int) -> int:
    """A proper factor of a composite m with no prime factor below 1000.

    A perfect power r^e is split by r. Otherwise the number field sieve runs
    with m = floor(m^(1/3)) and then smaller bases and larger bounds. Odd trial
    division is the last resort, so the function always returns."""
    for e in range(2, m.bit_length() // 9 + 2):
        r = iroot(m, e)
        if r**e == m:
            return r
    bound = default_bound(m)
    for k in range(4):
        g = gnfs(m, 3, bound, extra=10 + 20 * k)
        if 1 < g < m:
            return g
        bound += bound // 2
    d = 1001
    while m % d:
        d += 2
    return d


def factorize(n: int) -> list[int]:
    """Prime factors of n >= 1 in non-decreasing order, with multiplicity.

    Trial division removes the primes below 1000, then each composite part is
    split by the number field sieve. A loop with an explicit stack replaces
    recursion."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    out: list[int] = []
    for p in _SMALL:
        if p * p > n:
            break
        while n % p == 0:
            out.append(p)
            n //= p
    stack = [n]
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if m < 1000 * 1000 or is_probable_prime(m):
            out.append(m)
            continue
        g = _split(m)
        stack.extend((g, m // g))
    return sorted(out)
