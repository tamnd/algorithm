# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasi-polynomial-discrete-logarithm/. The authors are listed in prov/7RM8BX.jsonl.

import random

# The field F_(q^2) = F_q[i]/(i^2 - nu) for an odd prime q, with elements
# coded as ints a + b q for a + b i. A polynomial over F_(q^2) is a tuple of
# codes, lowest degree first, with no trailing zeros; () is zero. The big
# field is K = F_(q^2)[X]/(I) with I an irreducible factor of h1 X^q - h0.


class Fq2:
    """Tables for F_(q^2), q an odd prime."""

    def __init__(self, q: int):
        if q < 3 or any(q % d == 0 for d in range(2, int(q**0.5) + 1)):
            raise ValueError("q must be an odd prime")
        self.q = q
        n = q * q
        self.n = n
        nu = next(a for a in range(2, q) if pow(a, (q - 1) // 2, q) == q - 1)

        def mul(x: int, y: int) -> int:
            a, b, c, d = x % q, x // q, y % q, y // q
            return (a * c + nu * b * d) % q + q * ((a * d + b * c) % q)

        self.add = [[(x % q + y % q) % q + q * ((x // q + y // q) % q) for y in range(n)] for x in range(n)]
        self.neg = [(-(x % q)) % q + q * ((-(x // q)) % q) for x in range(n)]
        gen = next(x for x in range(1, n) if self._order(x, mul) == n - 1)
        self.exp = [1] * (n - 1)
        for k in range(1, n - 1):
            self.exp[k] = mul(self.exp[k - 1], gen)
        self.log = [0] * n
        for k, x in enumerate(self.exp):
            self.log[x] = k
        self.frob = [0] + [self.exp[self.log[x] * q % (n - 1)] for x in range(1, n)]

    @staticmethod
    def _order(x: int, mul) -> int:
        y, k = x, 1
        while y != 1:
            y, k = mul(y, x), k + 1
        return k

    def mul(self, x: int, y: int) -> int:
        if x == 0 or y == 0:
            return 0
        return self.exp[(self.log[x] + self.log[y]) % (self.n - 1)]

    def inv(self, x: int) -> int:
        return self.exp[(-self.log[x]) % (self.n - 1)]


def _trim(a: list[int]) -> tuple[int, ...]:
    while a and a[-1] == 0:
        a.pop()
    return tuple(a)


def padd(F: Fq2, a, b):
    if len(a) < len(b):
        a, b = b, a
    out = list(a)
    for i, y in enumerate(b):
        out[i] = F.add[out[i]][y]
    return _trim(out)


def psub(F: Fq2, a, b):
    return padd(F, a, tuple(F.neg[y] for y in b))


def pscale(F: Fq2, a, c: int):
    return _trim([F.mul(x, c) for x in a])


def pmul(F: Fq2, a, b):
    if not a or not b:
        return ()
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] = F.add[out[i + j]][F.mul(x, y)]
    return _trim(out)


def pdivmod(F: Fq2, a, m):
    """Quotient and remainder of a by m != 0."""
    r = list(a)
    dm = len(m) - 1
    if len(r) <= dm:
        return (), _trim(r)
    inv = F.inv(m[-1])
    quo = [0] * (len(r) - dm)
    for i in range(len(r) - 1, dm - 1, -1):
        c = F.mul(r[i], inv)
        if c:
            quo[i - dm] = c
            for j in range(dm + 1):
                if m[j]:
                    r[i - dm + j] = F.add[r[i - dm + j]][F.neg[F.mul(c, m[j])]]
    return _trim(quo), _trim(r[:dm])


def pmonic(F: Fq2, a):
    return pscale(F, a, F.inv(a[-1]))


def pgcd(F: Fq2, a, b):
    while b:
        a, b = b, pdivmod(F, a, b)[1]
    return pmonic(F, a) if a else ()


def ppowmod(F: Fq2, a, e: int, m):
    out: tuple[int, ...] = (1,)
    a = pdivmod(F, a, m)[1]
    while e:
        if e & 1:
            out = pdivmod(F, pmul(F, out, a), m)[1]
        a = pdivmod(F, pmul(F, a, a), m)[1]
        e >>= 1
    return out


def peval(F: Fq2, a, x: int) -> int:
    out = 0
    for c in reversed(a):
        out = F.add[F.mul(out, x)][c]
    return out


class QPField:
    """K = F_(q^2)[X]/(I) where I is irreducible of degree k and divides h1 X^q - h0,
    with deg h0, deg h1 <= 2, gcd(h0, h1) = 1, and h1 a product of linear factors."""

    def __init__(self, q: int, k: int, seed: int = 0, h0=None, h1=None):
        """Search h0 and h1 at random with the given seed, or take the given
        h0 (and h1, by default 1); raise ValueError if the given pair has no
        unique irreducible factor of degree k or h1 does not split."""
        if not 2 <= k <= q + 2:
            raise ValueError("need 2 <= k <= q + 2")
        F = Fq2(q)
        self.F, self.q, self.k = F, q, k
        rng = random.Random(seed)
        n = F.n
        xq = (0,) * q + (1,)
        fixed = h0 is not None
        while True:
            if fixed:
                h0, h1 = _trim(list(h0)), _trim(list(h1 or (1,)))
                if len(h0) > 3 or not 1 <= len(h1) <= 3 or len(split_linear(F, h1)[2]) != 1:
                    raise ValueError("need deg h0, deg h1 <= 2 and h1 a product of linear factors")
            else:
                dh1 = rng.choice([d for d in (0, 1, 2) if q + d >= k])
                h1 = (1,)
                for _ in range(dh1):
                    h1 = pmul(F, h1, (rng.randrange(n), 1))
                h0 = _trim([rng.randrange(n) for _ in range(3)])
            if not h0 or len(pgcd(F, h0, h1)) != 1:
                if fixed:
                    raise ValueError("need gcd(h0, h1) = 1")
                continue
            big = psub(F, pmul(F, h1, xq), h0)
            part = pgcd(F, big, psub(F, ppowmod(F, (0, 1), n**k, big), (0, 1)))
            for d in range(1, k):
                if k % d == 0 and len(part) > 1:
                    part = pdivmod(F, part, pgcd(F, part, psub(F, ppowmod(F, (0, 1), n**d, part), (0, 1))))[0]
            if len(part) - 1 == k:
                self.h0, self.h1, self.I = h0, h1, part
                return
            if fixed:
                raise ValueError("h1 X^q - h0 has no unique irreducible factor of degree k")

    def size(self) -> int:
        return self.F.n**self.k

    def encode(self, a) -> int:
        return sum(c * self.F.n**j for j, c in enumerate(a))

    def decode(self, v: int):
        c = []
        while v:
            c.append(v % self.F.n)
            v //= self.F.n
        return tuple(c)

    def mul(self, a, b):
        return pdivmod(self.F, pmul(self.F, a, b), self.I)[1]

    def pow(self, a, e: int):
        return ppowmod(self.F, a, e, self.I)


def split_linear(F: Fq2, a):
    """Write a != 0 as c * prod (X + beta)^(e_beta) * rest with rest monic and
    without roots in F_(q^2); return (c, e, rest), e indexed by beta."""
    e = [0] * F.n
    c = a[-1]
    a = pmonic(F, a)
    for beta in range(F.n):
        if len(a) == 1:
            break
        while len(a) > 1 and peval(F, a, F.neg[beta]) == 0:
            a = pdivmod(F, a, (beta, 1))[0]
            e[beta] += 1
    return c, e, a


def coset_representatives(F: Fq2) -> list[tuple[int, int, int, int]]:
    """Matrices (a, b, c, d), one for each coset of PGL2(F_(q^2)) / PGL2(F_q),
    up to the scaling of all four entries by F_(q^2)^*: q^3 + q matrices."""
    q, n = F.q, F.n
    fq = list(range(q))  # F_q inside F_(q^2)
    reps = []
    deltas = sorted({min(F.mul(lam, x) for lam in fq[1:]) for x in range(1, n)})
    for delta in deltas:  # Y = X + b, Z = delta
        bs = sorted({min(F.add[b][F.mul(al, delta)] for al in fq) for b in range(n)})
        reps += [(1, b, 0, delta) for b in bs]
    norm1 = [x for x in range(1, n) if F.mul(F.frob[x], x) == 1]
    ts = sorted({min(F.mul(z, t) for z in norm1) for t in range(1, n)})
    w = q  # the element i, not in F_q
    for t in ts:  # Y = X + phi(1), Z = i X + phi(i), phi(x) = s x + t x^q
        for s in range(n):
            reps.append((1, F.add[s][t], w, F.add[F.mul(s, w)][F.mul(t, F.frob[w])]))
    return reps


def _int_factors(m: int) -> dict[int, int]:
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


def _solve(rels, rho: int, mod: int) -> list[int] | None:
    """Gauss-Jordan elimination modulo mod = rho^f with unit pivots; None if a column has no unit pivot."""
    rows = [[x % mod for x in e] + [v % mod] for e, v in rels]
    t = len(rels[0][0])
    for j in range(t):  # @line L18
        piv = next((i for i in range(j, len(rows)) if rows[i][j] % rho), None)
        if piv is None:
            return None
        rows[j], rows[piv] = rows[piv], rows[j]  # @line L19
        inv = pow(rows[j][j], -1, mod)
        rows[j] = [x * inv % mod for x in rows[j]]
        for i in range(len(rows)):
            if i != j and rows[i][j]:
                c = rows[i][j]
                rows[i] = [(x - c * y) % mod for x, y in zip(rows[i], rows[j])]
    return [rows[j][t] for j in range(t)]  # @line L20


def qp_dlog(g: int, h: int, r: int, K: QPField, seed: int = 0) -> int | None:
    """Discrete logarithm in K^* = (F_(q^2)[X]/(I))^* with relations from the
    systematic equation X^q - X = prod over alpha in F_q of (X - alpha).

    Field elements are ints in [1, q^(2k)) whose base-q^2 digits are the codes
    of the coefficients of a polynomial in X of degree below k. Return the x in
    [0, r) with g^x = h, or None if h is not a power of g.
    Precondition: g has order exactly r and h != 0.
    The factor base is the q^2 monic linear polynomials; the descent of this
    toy version stops at degree 2 (shifts of the target must split into
    linear factors and irreducible quadratics that one homography removes).
    Raises ValueError if r < 1 or g or h is not a reduced nonzero element.
    Cost: heuristic (log Q)^(O(log log Q)) for Q = q^(2k) with the full
    descent; this toy version uses O(q^5) operations in F_(q^2) for the
    relations, O(q^6) for the linear algebra, random shifts for the targets
    and O(Q^(1/2)) integer divisions to factor Q - 1.
    """
    F, n, k = K.F, K.F.n, K.k
    if r < 1 or not (0 < g < K.size()) or not (0 < h < K.size()):
        raise ValueError("need r >= 1 and reduced nonzero g, h")
    gp, hp = K.decode(g), K.decode(h)
    if K.pow(hp, r) != (1,):  # @line L1
        return None
    if hp == (1,):  # @line L2
        return 0
    rng = random.Random(seed)
    order = K.size() - 1
    fac = _int_factors(order)
    gamma = next(c for c in (K.decode(v) for v in range(n, K.size())) if all(K.pow(c, order // p) != (1,) for p in fac))  # @line L3
    parts = {p: p**e for p, e in fac.items() if r % p == 0}
    ell = 1
    for mq in parts.values():
        ell *= mq
    omega = K.pow(gamma, order // (n - 1))[0]  # a generator of F_(q^2)^*
    log_const = [0] * n
    c = 1
    for j in range(n - 1):
        log_const[c] = j * (order // (n - 1)) % ell
        c = F.mul(c, omega)
    h0, h1 = K.h0, K.h1
    ch1, eh1, _ = split_linear(F, h1)  # h1 = ch1 prod (X + beta)^(eh1)
    rels: list[tuple[list[int], int]] = []  # @line L4
    elim: dict[tuple[int, ...], tuple[list[int], int]] = {}
    for a, b, c, d in coset_representatives(F):  # @line L5
        y, z = _trim([b, a]), _trim([d, c])
        rm = psub(F, pmul(F, padd(F, pscale(F, h0, F.frob[a]), pscale(F, h1, F.frob[b])), z),
                  pmul(F, y, padd(F, pscale(F, h0, F.frob[c]), pscale(F, h1, F.frob[d]))))  # @line L6
        e = list(eh1)
        v = -log_const[ch1]
        for f in [z] + [psub(F, y, pscale(F, z, al)) for al in range(F.q)]:
            if len(f) == 1:
                v -= log_const[f[0]]
            else:
                e[F.mul(f[0], F.inv(f[1]))] += 1
                v -= log_const[f[1]]
        c0, er, rest = split_linear(F, rm)
        row = [x - y2 for x, y2 in zip(e, er)]
        if len(rest) == 1:  # @line L7
            rels.append((row, (v + log_const[c0]) % ell))
        elif len(rest) == 3:  # @line L8
            elim.setdefault(rest, (row, (v + log_const[c0]) % ell))
    lam: list[int] | None = None
    need = n + 10  # rows needed before the next try of SOLVE
    while lam is None:  # @line L9
        m = rng.randrange(order)
        cz, ez, rest = split_linear(F, K.pow(gamma, m))
        if len(rest) != 1:
            continue
        rels.append((ez, (m - log_const[cz]) % ell))  # @line L10
        if len(rels) < need:
            continue
        need = len(rels) + max(10, n // 4)
        lam = [0] * n
        modulus = 1
        for p, mq in parts.items():
            sol = _solve(rels, p, mq)
            if sol is None:  # @line L11
                lam = None
                break
            lam = [x + modulus * ((s - x) * pow(modulus, -1, mq) % mq) for x, s in zip(lam, sol)]
            modulus *= mq
    logs = []
    for yy in (gp, hp):  # @line L12
        while True:
            m = rng.randrange(order)
            cz, ez, rest = split_linear(F, K.mul(yy, K.pow(gamma, m)))  # @line L13
            quads = []
            for qq in elim:
                while len(rest) > 1 and not pdivmod(F, rest, qq)[1]:
                    rest = pdivmod(F, rest, qq)[0]
                    quads.append(qq)
            if len(rest) == 1:  # @line L14
                break
        total = log_const[cz] + sum(u * w for u, w in zip(ez, lam))
        for qq in quads:
            row, v = elim[qq]
            total += sum(u * w for u, w in zip(row, lam)) - v  # @line L15
        logs.append((total - m) % ell)
    cc = ell // r  # @line L16
    u = logs[0] // cc
    return logs[1] // cc * pow(u, -1, r) % r  # @line L17
