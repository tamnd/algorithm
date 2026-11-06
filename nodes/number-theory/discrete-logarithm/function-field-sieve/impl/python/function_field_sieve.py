# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/function-field-sieve/. The authors are listed in prov/AJXW0K.jsonl.

import random
from math import isqrt

# A polynomial over F_p is a tuple of coefficients, lowest degree first, with
# no trailing zeros; () is the zero polynomial.


def _trim(a: list[int]) -> tuple[int, ...]:
    while a and a[-1] == 0:
        a.pop()
    return tuple(a)


def padd(a, b, p: int):
    """a + b over F_p."""
    if len(a) < len(b):
        a, b = b, a
    out = list(a)
    for i, y in enumerate(b):
        out[i] = (out[i] + y) % p
    return _trim(out)


def pscale(a, c: int, p: int):
    """c a over F_p."""
    return _trim([x * c % p for x in a])


def pmul(a, b, p: int):
    """a b over F_p, schoolbook."""
    if not a or not b:
        return ()
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return _trim([x % p for x in out])


def pdivmod(a, m, p: int):
    """Quotient and remainder of a by m != 0 over F_p."""
    r = list(a)
    dm = len(m) - 1
    if len(r) <= dm:
        return (), _trim(r)
    inv = pow(m[-1], -1, p)
    q = [0] * (len(r) - dm)
    low = m[:dm]
    for i in range(len(r) - 1, dm - 1, -1):
        c = r[i] * inv % p
        if c:
            q[i - dm] = c
            k = i - dm
            for j, y in enumerate(low):
                if y:
                    r[k + j] = (r[k + j] - c * y) % p
    return _trim(q), _trim(r[:dm])


def pmod(a, m, p: int):
    return pdivmod(a, m, p)[1]


def pmonic(a, p: int):
    return pscale(a, pow(a[-1], -1, p), p)


def pgcd(a, b, p: int):
    """Monic greatest common divisor over F_p (gcd(0, 0) = 0)."""
    while b:
        a, b = b, pmod(a, b, p)
    return pmonic(a, p) if a else ()


def fmul(a, b, f, p: int):
    return pmod(pmul(a, b, p), f, p)


def fpow(a, e: int, f, p: int):
    """a^e modulo f over F_p by square and multiply."""
    out: tuple[int, ...] = (1,)
    a = pmod(a, f, p)
    while e:
        if e & 1:
            out = fmul(out, a, f, p)
        a = fmul(a, a, f, p)
        e >>= 1
    return out


def compose(a, b, p: int):
    """a(b(t)) over F_p by Horner's rule."""
    out: tuple[int, ...] = ()
    for c in reversed(a):
        out = padd(pmul(out, b, p), (c,), p)
    return out


def monics(deg: int, p: int):
    """All monic polynomials of degree exactly deg over F_p."""
    for v in range(p**deg):
        c = []
        for _ in range(deg):
            c.append(v % p)
            v //= p
        yield tuple(c) + (1,)


def irreducibles(dmax: int, p: int) -> list[tuple[int, ...]]:
    """Monic irreducible polynomials over F_p of degree 1 to dmax, by trial division."""
    irr: list[tuple[int, ...]] = []
    for d in range(1, dmax + 1):
        small = [s for s in irr if 2 * (len(s) - 1) <= d]
        for a in monics(d, p):
            if all(pdivmod(a, s, p)[1] for s in small):
                irr.append(a)
    return irr


def encode(a, p: int) -> int:
    """The int with base-p digits a_0, a_1, ..."""
    return sum(c * p**i for i, c in enumerate(a))


def decode(v: int, p: int):
    c = []
    while v:
        c.append(v % p)
        v //= p
    return tuple(c)


def ffs_field(p: int, n: int, seed: int = 0):
    """Find monic F1 of degree d = ceil(n^(1/2)) and monic F2 of degree d2 >= n / d
    such that F2(F1(t)) - t has exactly one irreducible factor F of degree n;
    return (F1, F2, F). The degree d2 grows by 1 after every 200 failed tries."""
    if n < 2:
        raise ValueError("need n >= 2")
    rng = random.Random(seed)
    d = isqrt(n - 1) + 1
    d2 = -(-n // d)
    divisors = [k for k in range(1, n) if n % k == 0]
    tries = 0
    while True:
        tries += 1
        if tries % 200 == 0:
            d2 += 1
        f1 = tuple(rng.randrange(p) for _ in range(d)) + (1,)
        f2 = tuple(rng.randrange(p) for _ in range(d2)) + (1,)
        big = padd(compose(f2, f1, p), (0, p - 1), p)
        tpn = fpow((0, 1), p**n, big, p)
        part = pgcd(big, padd(tpn, (0, p - 1), p), p)
        for k in divisors:
            if len(part) <= 1:
                break
            tk = padd(fpow((0, 1), p**k, part, p), (0, p - 1), p)
            part = pdivmod(part, pgcd(part, tk, p), p)[0]
        if len(part) - 1 == n:
            return f1, f2, part


def _split(y, base, p: int):
    """Divide y by the monic members of base as often as possible; return (exponents, cofactor)."""
    e = [0] * len(base)
    for i, s in enumerate(base):
        if len(y) < len(s):
            continue
        while True:
            q, rem = pdivmod(y, s, p)
            if rem:
                break
            y = q
            e[i] += 1
    return e, y


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


def ffs_dlog(g: int, h: int, r: int, p: int, f1, f2, f, seed: int = 0, deg_base: int | None = None) -> int | None:
    """Function field sieve (Joux-Lercier form) for log_g h in F_(p^n)^* = (F_p[t]/(f))^*.

    Field elements are ints in [1, p^n) whose base-p digits are the
    coefficients of a polynomial in t of degree below n = deg f. Return the x
    in [0, r) with g^x = h, or None if h is not a power of g.
    Precondition: p is prime, f1 and f2 are monic, f is irreducible and
    divides f2(f1(t)) - t, g has order exactly r, and h != 0.
    The two factor bases hold the monic irreducibles of degree <= deg_base,
    by default 4, 3 and 2 for p = 2, 3 and 5, and 1 for larger p.
    Raises ValueError if r < 1 or g or h is not a reduced nonzero element.
    Cost: heuristic L_q(1/3, c) bit operations, q = p^n, with c between
    3^(1/3) and (32/9)^(1/3) for p <= L_q(1/3, (4/9)^(1/3)); this toy version
    also spends O((p^n)^(1/2)) integer divisions to factor p^n - 1.
    """
    n = len(f) - 1
    if r < 1 or not (0 < g < p**n) or not (0 < h < p**n):
        raise ValueError("need r >= 1 and reduced nonzero g, h")
    gp, hp = decode(g, p), decode(h, p)
    if fpow(hp, r, f, p) != (1,):  # @line L1
        return None
    if hp == (1,):  # @line L2
        return 0
    rng = random.Random(seed)
    order = p**n - 1
    fac = _int_factors(order)
    gamma = next(c for c in (decode(v, p) for v in range(1, p**n)) if all(fpow(c, order // q, f, p) != (1,) for q in fac))  # @line L3
    parts = {q: q**e for q, e in fac.items() if r % q == 0}
    ell = 1
    for m in parts.values():
        ell *= m
    omega = fpow(gamma, order // (p - 1), f, p)  # a generator of F_p^*, a constant
    log_const = {}
    c, i = 1, 0
    while c not in log_const:
        log_const[c] = i * (order // (p - 1)) % ell  # L(c) mod ell
        c = c * (omega[0] if omega else 0) % p
        i += 1

    def lc_log(a) -> int:
        return log_const[a[-1]]

    if deg_base is None:
        deg_base = {2: 4, 3: 3, 5: 2}.get(p, 1)
    deg_base = max(1, min(deg_base, n - 1))
    irr = irreducibles(2 * deg_base, p)
    base1 = [s for s in irr if len(s) - 1 <= deg_base]  # @line L4
    images2 = [pmod(compose(s, f1, p), f, p) for s in base1]
    base2 = [s for s, w in zip(base1, images2) if w]
    w2 = [w for w in images2 if w]
    t1, t2 = len(base1), len(base2)
    medium = [s for s in irr if deg_base < len(s) - 1 < n]
    d = len(f1) - 1
    e_deg = 1
    while p ** (2 * e_deg + 1) < 8 * (t1 + t2):
        e_deg += 1

    def both_sides(a, b):
        # psi1(G) = A(x) + B(x) F1(x) and psi2(G) = A(F2(y)) + B(F2(y)) y
        return padd(a, pmul(b, f1, p), p), padd(compose(a, f2, p), pmul(compose(b, f2, p), (0, 1), p), p)

    rels: list[tuple[list[int], int]] = []
    pairs = [(a, b) for db in range(e_deg + 1) for b in monics(db, p) for a in map(lambda v: decode(v, p), range(p ** (e_deg + 1)))]
    for a, b in pairs:  # @line L5
        if len(rels) >= 2 * (t1 + t2) or len(pgcd(a, b, p)) != 1:
            continue
        s1, s2 = both_sides(a, b)  # @line L6
        if not s1 or not pmod(s1, f, p):
            continue
        e1, c1 = _split(s1, base1, p)
        e2, c2 = _split(s2, base2, p)
        if len(c1) == 1 and len(c2) == 1:  # @line L7
            rels.append((e1 + [-x for x in e2], (lc_log(c2) - lc_log(c1)) % ell))
    lam: list[int] | None = None
    while lam is None:  # @line L8
        m = rng.randrange(order)
        j = rng.randrange(t2 + 1)
        z = fpow(gamma, m, f, p) if j == t2 else fmul(w2[j], fpow(gamma, m, f, p), f, p)  # @line L9
        e1, c1 = _split(z, base1, p)
        if len(c1) != 1:
            continue
        e2 = [0] * t2
        if j < t2:
            e2[j] = -1
        rels.append((e1 + e2, (m - lc_log(c1)) % ell))  # @line L10
        if len(rels) < t1 + t2 + 10:
            continue
        lam = [0] * (t1 + t2)
        modulus = 1
        for q, mq in parts.items():
            sol = _solve(rels, q, mq)
            if sol is None:  # @line L11
                lam = None
                break
            lam = [x + modulus * ((s - x) * pow(modulus, -1, mq) % mq) for x, s in zip(lam, sol)]
            modulus *= mq
    lam1, lam2 = lam[:t1], lam[t1:]

    def special_q(qq) -> int | None:
        # find G = A(x) + B(x) y with qq^a exactly dividing psi1(G) and both sides smooth
        for db in range(e_deg + 1):
            for b in monics(db, p):
                a0 = pscale(pmod(pmul(b, f1, p), qq, p), p - 1, p)
                for tv in range(p * p):
                    a = padd(a0, pmul(qq, decode(tv, p), p), p)
                    s1, s2 = both_sides(a, b)
                    if not s1 or not pmod(s1, f, p):
                        continue
                    mult = 0
                    while True:
                        qu, rem = pdivmod(s1, qq, p)
                        if rem:
                            break
                        s1 = qu
                        mult += 1
                    if any(mult % q == 0 for q in parts):
                        continue
                    e1, c1 = _split(s1, base1, p)
                    e2, c2 = _split(s2, base2, p)
                    if len(c1) == 1 and len(c2) == 1:
                        right = lc_log(c2) + sum(u * v for u, v in zip(e2, lam2))
                        left = lc_log(c1) + sum(u * v for u, v in zip(e1, lam1))
                        return (right - left) * pow(mult, -1, ell) % ell
        return None

    logs = []
    for y in (gp, hp):  # @line L12
        while True:
            m = rng.randrange(order)
            z = fmul(y, fpow(gamma, m, f, p), f, p)  # @line L13
            e1, rest = _split(z, base1, p)
            em, rest = _split(rest, medium, p)
            if len(rest) != 1:
                continue
            total = lc_log(rest) + sum(u * v for u, v in zip(e1, lam1))
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
    u = logs[0] // c
    return logs[1] // c * pow(u, -1, r) % r  # @line L18
