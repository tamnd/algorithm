# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/number-field-sieve-discrete-logarithm/. The authors are listed in prov/YRSSHK.jsonl.

import random
from math import exp, gcd, isqrt, log

# Monic f1 = x^2 + u x + v such that Z[w] = Z[x]/(f1) is the ring of integers of
# an imaginary quadratic field with class number 1; the discriminants are
# -4, -8, -3, -7, -11, -19, -43, -67 and -163. An element a + b w is the pair (a, b).
QUADRATIC_FIELDS = [(0, 1), (0, 2), (1, 1), (1, 2), (1, 3), (1, 5), (1, 11), (1, 17), (1, 41)]


def norm(z, u: int, v: int) -> int:
    a, b = z
    return a * a - u * a * b + v * b * b


def qmul(x, y, u: int, v: int):
    """x y in Z[w], with w^2 = -u w - v."""
    a, b = x
    c, d = y
    return (a * c - b * d * v, a * d + b * c - b * d * u)


def qdiv(x, y, u: int, v: int):
    """x / y in Z[w] if y divides x, else None."""
    a, b = x
    c, d = y
    n = norm(y, u, v)
    re, im = a * (c - d * u) + b * d * v, b * c - a * d  # x times the conjugate of y
    if re % n or im % n:
        return None
    return (re // n, im // n)


def _primes(bound: int) -> list[int]:
    sieve = bytearray([1]) * (bound + 1)
    out = []
    for i in range(2, bound + 1):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, bound + 1, i):
                sieve[j] = 0
    return out


def _int_factors(m: int) -> dict[int, int]:
    """Factor the integer m >= 1 by trial division; return {prime: exponent}."""
    out: dict[int, int] = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            out[d] = out.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        out[m] = out.get(m, 0) + 1
    return out


def nfs_polynomials(p: int) -> tuple[int, int, int, int]:
    """Return (u, v, c, d) with f1 = x^2 + u x + v from QUADRATIC_FIELDS, d >= 1 and
    c^2 + u c d + v d^2 = p, so that f1 and f2 = d x - c have the common root
    c / d modulo p. Raise ValueError if p splits in none of the nine fields."""
    for u, v in QUADRATIC_FIELDS:
        disc = u * u - 4 * v
        if p == 2 or pow(disc % p, (p - 1) // 2, p) != 1:
            continue
        d = 1
        while 4 * p + disc * d * d >= 0:
            t = isqrt(4 * p + disc * d * d)
            if t * t == 4 * p + disc * d * d:
                return u, v, (t - u * d) // 2, d
            d += 1
    raise ValueError("p splits in no imaginary quadratic field of class number 1 in the list")


def _unit_powers(u: int, v: int):
    """The units of Z[w] as the powers e^0, e^1, ... of a generator e."""
    units = [(a, b) for a in range(-2, 3) for b in range(-2, 3) if norm((a, b), u, v) == 1]
    best: list = []
    for e in units:
        pw = [(1, 0)]
        while True:
            nxt = qmul(pw[-1], e, u, v)
            if nxt == (1, 0):
                break
            pw.append(nxt)
        if len(pw) > len(best):
            best = pw
    return best


def _algebraic_primes(bound: int, u: int, v: int, units) -> list[tuple[int, int]]:
    """One generator for each prime ideal of Z[w] of norm <= bound."""
    disc = 4 * v - u * u  # minus the discriminant, > 0
    ymax = isqrt(4 * bound // disc) + 1
    xmax = isqrt(bound) + abs(u) * ymax + 1
    elems = [(x, y) for y in range(-ymax, ymax + 1) for x in range(-xmax, xmax + 1) if 0 < norm((x, y), u, v) <= bound]
    norms = {norm(z, u, v) for z in elems}
    rprimes = set(_primes(bound))
    out = set()
    for z in elems:
        n = norm(z, u, v)
        inert = z[1] == 0 and z[0] in rprimes and z[0] not in norms
        if n in rprimes or inert:
            out.add(max(qmul(z, e, u, v) for e in units))
    return sorted(out, key=lambda z: (norm(z, u, v), z))


def _split_int(n: int, plist: list[int]) -> tuple[list[int], int]:
    e = [0] * len(plist)
    for i, q in enumerate(plist):
        while n % q == 0:
            n //= q
            e[i] += 1
    return e, n


def _solve(rels, q: int, mod: int) -> list[int] | None:
    """Solve sum_j e_j lambda_j = k (mod mod) for all relations, mod = q^f.

    Gauss-Jordan elimination with pivots that are units modulo q. Return the
    unique solution, or None if some column has no unit pivot.
    """
    rows = [[x % mod for x in e] + [k % mod] for e, k in rels]
    t = len(rels[0][0])
    for j in range(t):  # @line L19
        piv = next((i for i in range(j, len(rows)) if rows[i][j] % q), None)
        if piv is None:
            return None
        rows[j], rows[piv] = rows[piv], rows[j]  # @line L20
        inv = pow(rows[j][j], -1, mod)
        rows[j] = [x * inv % mod for x in rows[j]]
        for i in range(len(rows)):
            if i != j and rows[i][j]:
                c = rows[i][j]
                rows[i] = [(x - c * y) % mod for x, y in zip(rows[i], rows[j])]
    return [rows[j][t] for j in range(t)]  # @line L21


def _reduce(v1, v2):
    """Lagrange reduction of a basis of a lattice in Z^2."""
    def dot(x, y):
        return x[0] * y[0] + x[1] * y[1]
    while True:
        if dot(v2, v2) < dot(v1, v1):
            v1, v2 = v2, v1
        n1 = dot(v1, v1)
        mu = (2 * dot(v1, v2) + n1) // (2 * n1)
        if mu == 0:
            return v1, v2
        v2 = (v2[0] - mu * v1[0], v2[1] - mu * v1[1])


def nfs_dlog(g: int, h: int, r: int, p: int, seed: int = 0, bound: int | None = None) -> int | None:
    """Number field sieve with a quadratic field for log_g h in (Z/pZ)^*.

    Return the x in [0, r) with g^x = h mod p, or None if h is not a power of g.
    Precondition: p is prime, 0 < g, h < p and g has order exactly r.
    The algebraic side is Z[x]/(x^2 + u x + v), a ring of integers with class
    number 1 in which p splits; the rational side is f2 = d x - c with
    c, d about p^(1/2). The factor bases hold the primes up to `bound` on both
    sides, with bound clipped to [1, (p - 1) / 2].
    Raises ValueError if r < 1, g or h is out of range, or p >= 3 splits in
    none of the nine fields of QUADRATIC_FIELDS.
    Cost: heuristic L_p(1/2, c) operations for this degree 2 version, against
    L_p(1/3, (64/9)^(1/3)) for the general number field sieve; it also spends
    O(p^(1/2)) integer divisions to factor p - 1 and to find c and d.
    """
    if r < 1 or not (0 < g < p) or not (0 < h < p):
        raise ValueError("need r >= 1 and 0 < g, h < p")
    if pow(h, r, p) != 1:  # @line L1
        return None
    if h == 1:  # @line L2
        return 0
    rng = random.Random(seed)
    order = p - 1
    fac = _int_factors(order)
    gamma = next(c for c in range(2, p) if all(pow(c, order // q, p) != 1 for q in fac))  # @line L3
    parts = {q: q**e for q, e in fac.items() if r % q == 0}
    ell = 1
    for m in parts.values():
        ell *= m
    u, v, c, d = nfs_polynomials(p)
    s = c * pow(d, -1, p) % p  # the common root of f1 and f2 modulo p
    if bound is None:
        bound = round(3 * exp(0.5 * (log(p) * log(log(p))) ** 0.5))
    bound = max(1, min(bound, (p - 1) // 2))
    rat = _primes(bound)  # @line L4
    units = _unit_powers(u, v)
    pis = _algebraic_primes(bound, u, v, units)
    pinorm = [norm(z, u, v) for z in pis]
    # columns: [-1, rational primes] then [unit e, algebraic primes, the constant d]
    images = [(units[1][0] + units[1][1] * s) % p] + [(a + b * s) % p for a, b in pis] + [d % p]
    nrat, nalg = 1 + len(rat), len(images)
    ncol = nrat + nalg

    def rat_split(n: int):
        e, rest = _split_int(abs(n), rat)
        return [1 if n < 0 else 0] + e, rest

    def alg_split(z):
        e = [0] * len(pis)
        n = norm(z, u, v)
        for i, (pi, npi) in enumerate(zip(pis, pinorm)):
            while n % npi == 0:
                w = qdiv(z, pi, u, v)
                if w is None:
                    break
                z, n = w, n // npi
                e[i] += 1
        return (units.index(z), e) if n == 1 else None

    def balanced(z: int) -> int:
        return z - p if 2 * z > p else z

    rels: list[tuple[list[int], int]] = []
    width = max(10, 2 * ncol)
    for b in range(1, width + 1):
        for a in range(-width, width + 1):  # @line L5
            if len(rels) >= 2 * ncol or gcd(a, b) != 1:
                continue
            n2 = a * d + b * c  # @line L6
            if n2 % p == 0:
                continue
            er, rest = rat_split(n2)
            fa = alg_split((a, b)) if rest == 1 else None
            if fa is not None:  # @line L7
                rels.append((er + [-fa[0]] + [-x for x in fa[1]] + [-1], 0))
    lam: list[int] | None = None
    while lam is None:  # @line L8
        m = rng.randrange(order)
        j = rng.randrange(nalg + 1)
        z = pow(gamma, m, p) * (images[j] if j < nalg else 1) % p  # @line L9
        er, rest = rat_split(balanced(z))
        if rest != 1:
            continue
        row = er + [0] * nalg
        if j < nalg:
            row[nrat + j] = -1
        rels.append((row, m % ell))  # @line L10
        if len(rels) < ncol + 10:
            continue
        lam = [0] * ncol
        modulus = 1
        for q, mq in parts.items():
            sol = _solve(rels, q, mq)
            if sol is None:  # @line L11
                lam = None
                break
            lam = [x + modulus * ((y - x) * pow(modulus, -1, mq) % mq) for x, y in zip(lam, sol)]
            modulus *= mq
    lam_rat, lam_alg = lam[:nrat], lam[nrat:]
    medium = [q for q in _primes(bound * bound) if q > bound]

    def special_q(qq: int) -> int | None:
        # find (a, b) with qq^k exactly dividing a d + b c and both sides smooth
        if d % qq:
            b1, b2 = _reduce((qq, 0), (-c * pow(d, -1, qq) % qq, 1))
        else:
            b1, b2 = _reduce((1, 0), (0, qq))
        for i in range(-4, 5):
            for k in range(-4, 5):
                a, b = i * b1[0] + k * b2[0], i * b1[1] + k * b2[1]
                if b < 0:
                    a, b = -a, -b
                if b == 0 or gcd(a, b) != 1:
                    continue
                n2 = a * d + b * c
                if n2 % p == 0:
                    continue
                mult = 0
                while n2 % qq == 0:
                    n2 //= qq
                    mult += 1
                if any(mult % q == 0 for q in parts):
                    continue
                er, rest = rat_split(n2)
                fa = alg_split((a, b)) if rest == 1 else None
                if fa is None:
                    continue
                right = lam_alg[-1] + fa[0] * lam_alg[0] + sum(x * y for x, y in zip(fa[1], lam_alg[1:-1]))
                left = sum(x * y for x, y in zip(er, lam_rat))
                return (right - left) * pow(mult, -1, ell) % ell
        return None

    logs = []
    for y in (g, h):  # @line L12
        while True:
            m = rng.randrange(order)
            z = balanced(y * pow(gamma, m, p) % p)  # @line L13
            er, rest = rat_split(z)
            em, rest = _split_int(rest, medium)
            if rest != 1:
                continue
            total = sum(x * w for x, w in zip(er, lam_rat))
            for qq, mult in zip(medium, em):
                if mult:
                    lq = special_q(qq)  # @line L14
                    if lq is None:
                        break
                    total += mult * lq
            else:  # @line L15
                break
        logs.append((total - m) % ell)  # @line L16
    c = ell // r  # @line L17
    w = logs[0] // c
    return logs[1] // c * pow(w, -1, r) % r  # @line L18
