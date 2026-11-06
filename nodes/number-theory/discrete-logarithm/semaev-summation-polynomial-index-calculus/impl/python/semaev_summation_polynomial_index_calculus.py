# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semaev-summation-polynomial-index-calculus/. The authors are listed in prov/WAPFC0.jsonl.

import random
from math import isqrt

# The curve E: y^2 = x^3 + a x + b lies over F_(p^2) = F_p[t]/(t^2 - nu) with
# p > 3 prime and nu the least quadratic non-residue mod p. A field element
# u + v t is the pair (u, v); a point is a pair of field elements, or None for
# the point at infinity O. The factor base is the set of points whose x lies
# in F_p, one point P_x for each such x, and a relation writes a point as
# P_x1 +- P_x2 or as +- P_x, which the summation polynomial S3 detects.

Fe = tuple[int, int]
Point = tuple[Fe, Fe] | None


def _is_prime(m: int) -> bool:
    return m >= 2 and all(m % d for d in range(2, isqrt(m) + 1))


def _factor(m: int) -> list[tuple[int, int]]:
    out, d = [], 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            out.append((d, e))
        d += 1
    if m > 1:
        out.append((m, 1))
    return out


def sqrt_mod(c: int, p: int) -> int | None:
    """A square root of c mod the odd prime p (Tonelli-Shanks), or None."""
    c %= p
    if c == 0:
        return 0
    if pow(c, (p - 1) // 2, p) != 1:
        return None
    q, s = p - 1, 0
    while q % 2 == 0:
        q, s = q // 2, s + 1
    z = next(z for z in range(2, p) if pow(z, (p - 1) // 2, p) == p - 1)
    m, w, t, x = s, pow(z, q, p), pow(c, q, p), pow(c, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2, i = t2 * t2 % p, i + 1
        bb = pow(w, 1 << (m - i - 1), p)
        m, w, t, x = i, bb * bb % p, t * bb * bb % p, x * bb % p
    return x


# Polynomials over F_p are lists of ints, lowest degree first, trimmed.


def _trim(f: list[int]) -> list[int]:
    while f and f[-1] == 0:
        f.pop()
    return f


def _pmul(f: list[int], g: list[int], p: int) -> list[int]:
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, x in enumerate(f):
        for j, y in enumerate(g):
            out[i + j] = (out[i + j] + x * y) % p
    return _trim(out)


def _padd(f: list[int], g: list[int], p: int) -> list[int]:
    out = [0] * max(len(f), len(g))
    for i, x in enumerate(f):
        out[i] = x
    for i, y in enumerate(g):
        out[i] = (out[i] + y) % p
    return _trim(out)


def _pmod(f: list[int], m: list[int], p: int) -> list[int]:
    r = list(f)
    inv = pow(m[-1], -1, p)
    while len(r) >= len(m):
        c = r[-1] * inv % p
        shift = len(r) - len(m)
        for j, y in enumerate(m):
            r[shift + j] = (r[shift + j] - c * y) % p
        _trim(r)
    return r


def _pgcd(f: list[int], g: list[int], p: int) -> list[int]:
    while g:
        f, g = g, _pmod(f, g, p)
    if not f:
        return []
    inv = pow(f[-1], -1, p)
    return [x * inv % p for x in f]


def _ppowmod(f: list[int], e: int, m: list[int], p: int) -> list[int]:
    out, f = [1], _pmod(f, m, p)
    while e:
        if e & 1:
            out = _pmod(_pmul(out, f, p), m, p)
        f = _pmod(_pmul(f, f, p), m, p)
        e >>= 1
    return out


def _peval(f: list[int], x: int, p: int) -> int:
    out = 0
    for c in reversed(f):
        out = (out * x + c) % p
    return out


def roots_mod(f: list[int], p: int, rng: random.Random) -> list[int]:
    """The distinct roots in F_p of a nonzero f, sorted (Cantor-Zassenhaus)."""
    f = _trim([c % p for c in f])
    g = _pgcd(f, _padd(_ppowmod([0, 1], p, f, p), [0, p - 1], p), p) if len(f) > 1 else [1]
    out, todo = [], [g]
    while todo:
        h = todo.pop()
        if len(h) <= 1:
            continue
        if len(h) == 2:
            out.append((-h[0]) * pow(h[1], -1, p) % p)
            continue
        while True:
            d = rng.randrange(p)
            s = _pgcd(h, _padd(_ppowmod([d, 1], (p - 1) // 2, h, p), [p - 1], p), p)
            if 1 < len(s) < len(h):
                break
        quo = _pdiv_exact(h, s, p)
        todo.extend([s, quo])
    return sorted(out)


def _pdiv_exact(f: list[int], m: list[int], p: int) -> list[int]:
    r, inv = list(f), pow(m[-1], -1, p)
    q = [0] * (len(f) - len(m) + 1)
    for i in range(len(q) - 1, -1, -1):
        c = r[i + len(m) - 1] * inv % p
        q[i] = c
        for j, y in enumerate(m):
            r[i + j] = (r[i + j] - c * y) % p
    return _trim(q)


class Curve:
    """E: y^2 = x^3 + a x + b over F_(p^2), with a and b given as pairs (u, v)."""

    def __init__(self, p: int, a: Fe, b: Fe):
        if p <= 3 or not _is_prime(p):
            raise ValueError("p must be a prime > 3")
        self.p = p
        self.nu = next(c for c in range(2, p) if pow(c, (p - 1) // 2, p) == p - 1)
        self.a = (a[0] % p, a[1] % p)
        self.b = (b[0] % p, b[1] % p)
        a3 = self.mul(self.mul(self.a, self.a), self.a)
        if self.add_f(self.mul((4, 0), a3), self.mul((27, 0), self.mul(self.b, self.b))) == (0, 0):
            raise ValueError("singular curve")

    # field arithmetic in F_(p^2)
    def add_f(self, x: Fe, y: Fe) -> Fe:
        return (x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p

    def sub_f(self, x: Fe, y: Fe) -> Fe:
        return (x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p

    def mul(self, x: Fe, y: Fe) -> Fe:
        p = self.p
        return (x[0] * y[0] + self.nu * x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p

    def inv(self, x: Fe) -> Fe:
        p = self.p
        n = pow((x[0] * x[0] - self.nu * x[1] * x[1]) % p, -1, p)
        return x[0] * n % p, (-x[1]) * n % p

    def is_square(self, x: Fe) -> bool:
        n = (x[0] * x[0] - self.nu * x[1] * x[1]) % self.p
        return n == 0 or pow(n, (self.p - 1) // 2, self.p) == 1

    def sqrt(self, x: Fe) -> Fe | None:
        p = self.p
        u, v = x
        if v == 0:
            s = sqrt_mod(u, p)
            if s is not None:
                return s, 0
            return 0, sqrt_mod(u * pow(self.nu, -1, p), p)
        n = sqrt_mod(u * u - self.nu * v * v, p)
        if n is None:
            return None
        for sg in (n, p - n):
            s = sqrt_mod((u + sg) * pow(2, -1, p), p)
            if s:
                return s, v * pow(2 * s, -1, p) % p
        return None

    def rhs(self, x: Fe) -> Fe:
        return self.add_f(self.mul(self.add_f(self.mul(x, x), self.a), x), self.b)

    # the group E(F_(p^2))
    def on_curve(self, P: Point) -> bool:
        return P is None or self.mul(P[1], P[1]) == self.rhs(P[0])

    def neg(self, P: Point) -> Point:
        return None if P is None else (P[0], ((-P[1][0]) % self.p, (-P[1][1]) % self.p))

    def add(self, P: Point, Q: Point) -> Point:
        if P is None:
            return Q
        if Q is None:
            return P
        (x1, y1), (x2, y2) = P, Q
        if x1 == x2:
            if self.add_f(y1, y2) == (0, 0):
                return None
            lam = self.mul(self.add_f(self.mul((3, 0), self.mul(x1, x1)), self.a), self.inv(self.add_f(y1, y1)))
        else:
            lam = self.mul(self.sub_f(y2, y1), self.inv(self.sub_f(x2, x1)))
        x3 = self.sub_f(self.sub_f(self.mul(lam, lam), x1), x2)
        return x3, self.sub_f(self.mul(lam, self.sub_f(x1, x3)), y1)

    def smul(self, k: int, P: Point) -> Point:
        """k P by double and add, for k >= 0."""
        R: Point = None
        while k:
            if k & 1:
                R = self.add(R, P)
            P = self.add(P, P)
            k >>= 1
        return R

    def order(self) -> int:
        """#E(F_(p^2)) by counting, O(p^2) field operations (a toy step)."""
        p, n = self.p, 1
        for u in range(p):
            for v in range(p):
                z = self.rhs((u, v))
                n += 1 if z == (0, 0) else (2 if self.is_square(z) else 0)
        return n

    def random_point(self, rng: random.Random) -> Point:
        while True:
            x = (rng.randrange(self.p), rng.randrange(self.p))
            y = self.sqrt(self.rhs(x))
            if y is not None:
                return (x, y) if rng.randrange(2) else self.neg((x, y))

    def point_order(self, P: Point, N: int) -> int:
        n = N
        for r, _ in _factor(N):
            while n % r == 0 and self.smul(n // r, P) is None:
                n //= r
        return n


def factor_base(E: Curve) -> dict[int, Point]:
    """P_x = (x, y_x) for every x in F_p with x^3 + a x + b a square in F_(p^2)."""
    fb = {}
    for x in range(E.p):
        y = E.sqrt(E.rhs((x, 0)))
        if y is not None:
            fb[x] = ((x, 0), min(y, E.neg(((x, 0), y))[1]))
    return fb


def s3(E: Curve, x1: Fe, x2: Fe, x3: Fe) -> Fe:
    """Semaev's third summation polynomial at (x1, x2, x3)."""
    m, ad, sb = E.mul, E.add_f, E.sub_f
    d = sb(x1, x2)
    t1 = m(m(d, d), m(x3, x3))
    t2 = m((2, 0), m(ad(m(ad(x1, x2), ad(m(x1, x2), E.a)), m((2, 0), E.b)), x3))
    w = sb(m(x1, x2), E.a)
    t3 = sb(m(w, w), m(m((4, 0), E.b), ad(x1, x2)))
    return ad(sb(t1, t2), t3)


def decompose(E: Curve, R: Point, fb: dict[int, Point], rng: random.Random) -> dict[int, int] | None:
    """A row e with R = sum of e_x P_x and |e| of weight at most 2, or None.
    Deterministic in R: the internal randomness only affects the time."""
    p = E.p
    if R is None:  # @line L16
        return None
    xr = R[0]
    if xr[1] == 0 and xr[0] in fb:
        return {xr[0]: 1 if fb[xr[0]] == R else -1}
    m, a, b = E.mul, E.a, E.b
    # @line L17
    # S3(x1, x2, xr) in s1 = x1 + x2 and s2 = x1 x2 is
    # xr^2 s1^2 - 2 xr s1 s2 + s2^2 - (2 a xr + 4 b) s1 - (4 xr^2 + 2 a) s2 + a^2 - 4 b xr.
    k11 = m(xr, xr)
    k12 = m((p - 2, 0), xr)
    k1 = E.sub_f((0, 0), E.add_f(m((2, 0), m(a, xr)), m((4, 0), b)))
    k2 = E.sub_f((0, 0), E.add_f(m((4, 0), k11), m((2, 0), a)))
    k0 = E.sub_f(m(a, a), m((4, 0), m(b, xr)))
    # G1 = c1(s1) s2 + c0(s1) and G0 = s2^2 + d1(s1) s2 + d0(s1)
    c1 = _trim([k2[1], k12[1]])
    c0 = _trim([k0[1], k1[1], k11[1]])
    d1 = _trim([k2[0], k12[0]])
    d0 = _trim([k0[0], k1[0], k11[0]])
    neg = [(-c) % p for c in _pmul(c0, c1, p)]
    rho = _padd(_padd(_pmul(c0, c0, p), _pmul(neg, d1, p), p), _pmul(_pmul(c1, c1, p), d0, p), p)
    cands = roots_mod(rho, p, rng) if rho else range(p)
    sols = set()
    for s1 in cands:  # @line L18
        C1, C0 = _peval(c1, s1, p), _peval(c0, s1, p)
        D1, D0 = _peval(d1, s1, p), _peval(d0, s1, p)
        if C1:
            s2s = [(-C0) * pow(C1, -1, p) % p]
        elif C0 == 0:
            w = sqrt_mod(D1 * D1 - 4 * D0, p)
            s2s = [] if w is None else [(-D1 - w) * pow(2, -1, p) % p, (-D1 + w) * pow(2, -1, p) % p]
        else:
            s2s = []
        for s2 in s2s:
            if (s2 * s2 + D1 * s2 + D0) % p == 0 and (C1 * s2 + C0) % p == 0:
                sols.add((s1, s2))
    half = pow(2, -1, p)
    for s1, s2 in sorted(sols):
        w = sqrt_mod(s1 * s1 - 4 * s2, p)
        if w is None:
            continue
        x1, x2 = (s1 - w) * half % p, (s1 + w) * half % p
        if x1 not in fb or x2 not in fb:  # @line L19
            continue
        P1, P2 = fb[x1], fb[x2]
        for e1, e2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):  # @line L20
            S = E.add(P1 if e1 == 1 else E.neg(P1), P2 if e2 == 1 else E.neg(P2))
            if S == R:
                row: dict[int, int] = {}
                row[x1] = row.get(x1, 0) + e1
                row[x2] = row.get(x2, 0) + e2
                return {x: c for x, c in row.items() if c}
    return None  # @line L21


def relation_log(E: Curve, P: Point, Q: Point, r: int, fb: dict[int, Point], rng: random.Random) -> int:
    """log_P Q mod r by summation polynomial index calculus.
    Precondition: P has prime order r, r divides #E(F_(p^2)) exactly once, Q in <P>,
    and the factor base fb is nonempty."""
    cols = sorted(fb)  # @line L8
    idx = {x: i for i, x in enumerate(cols)}
    piv: dict[int, tuple[list[int], dict[int, int]]] = {}
    av: list[int] = []
    bv: list[int] = []
    while True:  # @line L9
        a, b = rng.randrange(r), rng.randrange(r)  # @line L10
        R = E.add(E.add(E.smul(a, P), E.smul(b, Q)), E.smul(r, E.random_point(rng)))
        e = decompose(E, R, fb, rng)  # @line L11
        if e is None:
            continue
        j = len(av)
        av.append(a)
        bv.append(b)
        v = [0] * len(cols)
        for x, c in e.items():
            v[idx[x]] = c % r
        comb = {j: 1}
        for col in range(len(cols)):  # @line L12
            f = v[col]
            if f and col in piv:
                pv, pc = piv[col]
                for k in range(col, len(cols)):
                    if pv[k]:
                        v[k] = (v[k] - f * pv[k]) % r
                for k, c in pc.items():
                    comb[k] = (comb.get(k, 0) - f * c) % r
        lead = next((k for k in range(len(cols)) if v[k]), None)
        if lead is None:
            A = sum(c * av[k] for k, c in comb.items()) % r  # @line L13
            C = sum(c * bv[k] for k, c in comb.items()) % r
            if C:  # @line L14
                return (-A) * pow(C, -1, r) % r
        else:
            inv = pow(v[lead], -1, r)  # @line L15
            piv[lead] = ([c * inv % r for c in v], {k: c * inv % r for k, c in comb.items() if c})


def bsgs(E: Curve, P: Point, Q: Point, m: int) -> int | None:
    """x in [0, m) with x P = Q for P of order m, or None."""
    s = isqrt(m - 1) + 1
    table: dict = {}
    T: Point = None
    for i in range(s):
        table.setdefault(T, i)
        T = E.add(T, P)
    step, T = E.neg(E.smul(s, P)), Q
    for j in range(s + 1):
        if T in table:
            return (j * s + table[T]) % m
        T = E.add(T, step)
    return None


def summation_index_calculus(E: Curve, P: Point, Q: Point, seed: int = 0, N: int | None = None) -> int | None:
    """The x in [0, ord P) with x P = Q, or None if Q is not in <P>.

    The group is E(F_(p^2)) of order N, about p^2, and one group operation
    costs O(1) operations in F_(p^2), O(log(p)^2) bit operations. For each
    prime r with r dividing ord P and r^2 not dividing N, the relation step
    makes an expected O(p) decomposition attempts (heuristic: about half of
    the points decompose), each O(log N) group operations and O(log p) field
    operations for the roots, and the dense elimination costs O(p^3)
    operations mod r. Other prime powers r^e go to baby-step giant-step,
    O(r^(e/2)) group operations.
    """
    if not (E.on_curve(P) and E.on_curve(Q)):
        raise ValueError("points must lie on the curve")
    rng = random.Random(seed)
    if N is None:
        N = E.order()  # @line L1
    n = E.point_order(P, N)
    if E.smul(n, Q) is not None:  # @line L2
        return None
    fb: dict[int, Point] | None = None
    x, mod = 0, 1
    for r, e in _factor(n):  # @line L3
        re = r**e
        Pr, Qr = E.smul(n // re, P), E.smul(n // re, Q)  # @line L4
        if N % (r * r) == 0:  # @line L5
            xr = bsgs(E, Pr, Qr, re)
            if xr is None:
                return None
        else:  # @line L6
            if fb is None:
                fb = factor_base(E)
                if not fb:
                    raise ValueError("empty factor base")
            xr = relation_log(E, Pr, Qr, r, fb, rng)
        x += mod * ((xr - x) * pow(mod, -1, re) % re)  # @line L7
        mod *= re
    return x % n
