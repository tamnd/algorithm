# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coppersmith-discrete-logarithm/. The authors are listed in prov/TEVZ61.jsonl.

import random
from math import log

# A polynomial over F_2 is an int: bit i is the coefficient of x^i.


def pmul(a: int, b: int) -> int:
    """Product of two polynomials over F_2 (carry-less multiplication)."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def pdivmod(a: int, m: int) -> tuple[int, int]:
    """Quotient and remainder of a by m != 0 over F_2."""
    q = 0
    dm = m.bit_length()
    while a.bit_length() >= dm:
        s = a.bit_length() - dm
        q ^= 1 << s
        a ^= m << s
    return q, a


def pgcd(a: int, b: int) -> int:
    """Greatest common divisor of two polynomials over F_2."""
    while b:
        a, b = b, pdivmod(a, b)[1]
    return a


def fmul(a: int, b: int, f: int) -> int:
    """Product of a and b in F_2[x]/(f)."""
    return pdivmod(pmul(a, b), f)[1]


def fpow(a: int, e: int, f: int) -> int:
    """a^e in F_2[x]/(f) by square and multiply."""
    out = 1
    a = pdivmod(a, f)[1]
    while e:
        if e & 1:
            out = fmul(out, a, f)
        a = fmul(a, a, f)
        e >>= 1
    return out


def spread(a: int, k: int) -> int:
    """a(x^(2^k)), which equals a(x)^(2^k) over F_2."""
    out = 0
    i = 0
    while a:
        if a & 1:
            out |= 1 << (i << k)
        a >>= 1
        i += 1
    return out


def irreducibles(dmax: int) -> list[int]:
    """All irreducible polynomials over F_2 of degree 1 to dmax, by a sieve on products."""
    red = set()
    irr: list[int] = []
    for p in range(2, 1 << (dmax + 1)):
        if p not in red:
            irr.append(p)
        for s in irr:
            if (s.bit_length() - 1) + (p.bit_length() - 1) > dmax:
                break
            red.add(pmul(s, p))
    return irr


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


def _split(y: int, base: list[int]) -> tuple[list[int], int]:
    """Divide y by the members of base as often as possible; return (exponents, cofactor)."""
    e = [0] * len(base)
    for i, s in enumerate(base):
        while True:
            q, rem = pdivmod(y, s)
            if rem:
                break
            y = q
            e[i] += 1
    return e, y


def _solve(rels: list[tuple[list[int], int]], q: int, mod: int) -> list[int] | None:
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


def coppersmith_dlog(g: int, h: int, r: int, f: int, seed: int = 0, b: int | None = None) -> int | None:
    """Coppersmith's index calculus for log_g h in F_(2^n)^* = (F_2[x]/(f))^*.

    Field elements are ints in [1, 2^n) read as polynomials, n = deg f.
    Return the x in [0, r) with g^x = h, or None if h is not a power of g.
    Precondition: f = x^n + f1 is irreducible over F_2, g != 0 has order
    exactly r, and h != 0.
    The factor base holds the irreducible polynomials of degree at most b,
    by default b = round(0.974 n^(1/3) (ln n)^(2/3)).
    Raises ValueError if deg f < 1, r < 1, or g or h is not a reduced nonzero element.
    Cost: heuristic L_q(1/3, (32/9)^(1/3)) bit operations for q = 2^n when
    deg f1 is small; this toy version also spends O(2^(n/2)) integer
    divisions to factor 2^n - 1 and find a generator.
    """
    n = f.bit_length() - 1
    if n < 1 or r < 1 or not (0 < g < 1 << n) or not (0 < h < 1 << n):
        raise ValueError("need deg f >= 1, r >= 1 and reduced nonzero g, h")
    if fpow(h, r, f) != 1:  # @line L1
        return None
    if h == 1:  # @line L2
        return 0
    rng = random.Random(seed)
    order = (1 << n) - 1
    fac = _int_factors(order)
    gamma = next(c for c in range(1, 1 << n) if all(fpow(c, order // q, f) != 1 for q in fac))  # @line L3
    parts = {q: q**e for q, e in fac.items() if r % q == 0}
    ell = 1
    for m in parts.values():
        ell *= m
    if b is None:
        b = round(0.974 * n ** (1 / 3) * log(n) ** (2 / 3))
    b = max(1, min(n - 1, b))
    big = min(n - 1, 2 * b)
    irr = irreducibles(max(big, 1))
    base = [s for s in irr if s.bit_length() - 1 <= b]  # @line L4
    large = [s for s in irr if b < s.bit_length() - 1 <= big]
    k = 0
    while (2 << (2 * k)) * b <= n:  # 2^k is about (n / b)^(1/2)
        k += 1
    two_k = 1 << k
    ell_l = -(-n // two_k)
    f1 = f ^ (1 << n)
    shift = two_k * ell_l - n

    def frob(a: int, bb: int) -> int:
        # D = a(x^(2^k)) x^(2^k l - n) f1 + bb(x^(2^k)), congruent to (a x^l + bb)^(2^k)
        return pmul(pmul(spread(a, k), 1 << shift), f1) ^ spread(bb, k)

    rels: list[tuple[list[int], int]] = []
    for a in range(1, 1 << b):  # @line L5
        for bb in range(1 << b):
            if len(rels) >= 2 * len(base) or pgcd(a, bb) != 1:
                continue
            c = pmul(a, 1 << ell_l) ^ bb  # @line L6
            d = frob(a, bb)
            if pdivmod(c, f)[1] == 0:
                continue
            ec, rc = _split(c, base)
            ed, rd = _split(d, base)
            if rc == 1 and rd == 1:  # @line L7
                rels.append(([two_k * u - v for u, v in zip(ec, ed)], 0))
    lam: list[int] | None = None
    while lam is None:  # @line L8
        m = rng.randrange(order)
        e, rest = _split(fpow(gamma, m, f), base)  # @line L9
        if rest != 1:
            continue
        rels.append((e, m))
        if len(rels) < len(base) + 10:  # @line L10
            continue
        lam = [0] * len(base)
        modulus = 1
        for q, mq in parts.items():
            sol = _solve(rels, q, mq)
            if sol is None:  # @line L11
                lam = None
                break
            lam = [a + modulus * ((s - a) * pow(modulus, -1, mq) % mq) for a, s in zip(lam, sol)]
            modulus *= mq
    inv_two_k = pow(two_k, -1, ell)

    def special_q(gq: int) -> int | None:
        # find C = A x^l + B with gq^a exactly dividing C, C / gq^a and D smooth
        for a in range(1, 1 << b):
            quo, rem = pdivmod(pmul(a, 1 << ell_l), gq)
            for t in range(4):
                bb = rem ^ pmul(gq, t)
                c = pmul(a, 1 << ell_l) ^ bb  # c = gq * (quo + t)
                if c == 0 or pdivmod(c, f)[1] == 0:
                    continue
                mult = 0
                while pdivmod(c, gq)[1] == 0:
                    c = pdivmod(c, gq)[0]
                    mult += 1
                if any(mult % q == 0 for q in parts):
                    continue
                ec, rc = _split(c, base)
                ed, rd = _split(frob(a, bb), base)
                if rc == 1 and rd == 1:
                    lc = sum(u * v for u, v in zip(ec, lam))
                    ld = sum(u * v for u, v in zip(ed, lam))
                    return (inv_two_k * ld - lc) * pow(mult, -1, ell) % ell
        return None

    logs = []
    for y in (g, h):  # @line L12
        while True:
            m = rng.randrange(order)
            dvec, rest = _split(fmul(y, fpow(gamma, m, f), f), base)  # @line L13
            elarge, rest = _split(rest, large)
            if rest != 1:
                continue
            total = sum(u * v for u, v in zip(dvec, lam))
            for gq, mult in zip(large, elarge):
                if mult:
                    lg = special_q(gq)  # @line L14
                    if lg is None:
                        break
                    total += mult * lg
            else:  # @line L15
                break
        logs.append((total - m) % ell)  # @line L16
    c = ell // r  # @line L17
    u = logs[0] // c
    return logs[1] // c * pow(u, -1, r) % r  # @line L18
