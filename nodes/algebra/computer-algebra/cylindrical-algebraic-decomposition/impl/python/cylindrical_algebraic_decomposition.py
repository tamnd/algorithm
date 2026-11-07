# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cylindrical-algebraic-decomposition/. The authors are listed in prov/P06M5D.jsonl.

"""Cylindrical algebraic decomposition of the plane, exact over Q.

cad(F) takes polynomials in Q[x, y] (dicts from (i, j) to Fractions, meaning
c x^i y^j) and returns an F-sign-invariant cylindrical decomposition of R^2:
a list of columns over the cells of the x-axis, each with its stack of cells
in y, a sample point and the sign vector of F at it.

Algebraic numbers are given by a squarefree defining polynomial over Q and an
isolating interval with rational endpoints. Arithmetic in Q(alpha) uses
dynamic evaluation: when a gcd with the defining polynomial is nontrivial, the
defining polynomial is replaced by the factor that vanishes at alpha.

Cost model: operations in Q on numbers whose size grows with the degrees.
For a product S of total degree D, the projection P has degree O(D^2) and
each stack at most 2D + 1 cells, so there are O(D^3) cells; the number of
field operations is polynomial in D. The bound for n variables, doubly
exponential in n, does not arise here since n = 2.
"""

from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

UPoly = List[Fraction]           # low degree first
BiPoly = Dict[Tuple[int, int], Fraction]
YPoly = List[UPoly]              # polynomial in y with coefficients in Q[x]

# ---------------------------------------------------------------- univariate

def trim(p: Sequence[Fraction]) -> UPoly:
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def uadd(p: UPoly, q: UPoly) -> UPoly:
    n = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def uscale(p: UPoly, c: Fraction) -> UPoly:
    return trim([c * a for a in p])


def umul(p: UPoly, q: UPoly) -> UPoly:
    if not p or not q:
        return []
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                r[i + j] += a * b
    return trim(r)


def udivmod(p: UPoly, q: UPoly) -> Tuple[UPoly, UPoly]:
    p, q = trim(p), trim(q)
    if len(p) < len(q):
        return [], p
    r = list(p)
    out = [Fraction(0)] * (len(p) - len(q) + 1)
    inv = 1 / q[-1]
    for k in range(len(p) - len(q), -1, -1):
        c = r[k + len(q) - 1] * inv
        out[k] = c
        if c:
            for i, b in enumerate(q):
                r[k + i] -= c * b
    return trim(out), trim(r[: len(q) - 1])


def umonic(p: UPoly) -> UPoly:
    p = trim(p)
    return [a / p[-1] for a in p] if p else []


def ugcd(p: UPoly, q: UPoly) -> UPoly:
    p, q = trim(p), trim(q)
    while q:
        p, q = q, udivmod(p, q)[1]
    return umonic(p)


def uderiv(p: UPoly) -> UPoly:
    return trim([i * p[i] for i in range(1, len(p))])


def ueval(p: UPoly, x: Fraction) -> Fraction:
    v = Fraction(0)
    for a in reversed(p):
        v = v * x + a
    return v


def usqfree(p: UPoly) -> UPoly:
    p = trim(p)
    if len(p) <= 1:
        return umonic(p)
    return umonic(udivmod(p, ugcd(p, uderiv(p)))[0])


def sign(v: Fraction) -> int:
    return (v > 0) - (v < 0)


def sturm(p: UPoly) -> List[UPoly]:
    seq = [trim(p), uderiv(p)]
    while seq[-1]:
        seq.append(uscale(udivmod(seq[-2], seq[-1])[1], Fraction(-1)))
    return seq[:-1]


def variations(signs: List[int]) -> int:
    s = [v for v in signs if v]
    return sum(1 for a, b in zip(s, s[1:]) if a != b)


def int_poly(p: UPoly) -> List[int]:
    """A positive multiple of p with coprime integer coefficients (same signs everywhere)."""
    den = 1
    for c in p:
        den = den * c.denominator // gcd_int(den, c.denominator)
    q = [int(c * den) for c in p]
    g = 0
    for c in q:
        g = gcd_int(g, c)
    return [c // g for c in q] if g else q


def gcd_int(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def isign(q: List[int], x: Fraction) -> int:
    """Sign of q(x) for x = n/e, from the integer e^k q(n/e) with e > 0."""
    n, e = x.numerator, x.denominator
    k = len(q) - 1
    ep = [1] * (k + 1)
    for i in range(1, k + 1):
        ep[i] = ep[i - 1] * e
    v = 0
    for i in range(k, -1, -1):
        v = v * n + q[i] * ep[k - i]
    return (v > 0) - (v < 0)


class SturmCounter:
    """Sturm sequence of a squarefree p, with sign variations cached by point."""

    def __init__(self, p: UPoly):
        self.seq = [int_poly(q) for q in sturm(p)]
        self.cache: Dict[Fraction, int] = {}

    def var(self, x: Fraction) -> int:
        if x not in self.cache:
            self.cache[x] = variations([isign(q, x) for q in self.seq])
        return self.cache[x]

    def count(self, a: Fraction, b: Fraction) -> int:
        """Distinct real roots in (a, b); a and b are not roots."""
        return self.var(a) - self.var(b)


def isolate(p: UPoly) -> List[Tuple[Fraction, Fraction]]:
    """Disjoint open intervals with non-root rational endpoints, one per real root of squarefree p."""
    p = trim(p)
    if len(p) <= 1:
        return []
    sc = SturmCounter(p)
    B = 1 + max(abs(c / p[-1]) for c in p[:-1])
    out, stack = [], [(-B, B)]
    while stack:
        a, b = stack.pop()
        k = sc.count(a, b)
        if k == 0:
            continue
        if k == 1:
            out.append((a, b))
            continue
        m, w = (a + b) / 2, (b - a) / 4
        while ueval(p, m) == 0:
            m, w = m + w, w / 2
        stack += [(a, m), (m, b)]
    return sorted(out)


def interpolate(xs: List[Fraction], ys: List[Fraction]) -> UPoly:
    """Newton interpolation through the points (xs[i], ys[i])."""
    coef = list(ys)
    n = len(xs)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (xs[i] - xs[i - j])
    p: UPoly = []
    for i in range(n - 1, -1, -1):
        p = uadd(umul(p, [-xs[i], Fraction(1)]), [coef[i]])
    return p


def det_int(M: List[List[int]]) -> int:
    """Determinant of an integer matrix by Bareiss fraction-free elimination."""
    M = [row[:] for row in M]
    n, sgn, prev = len(M), 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            piv = next((r for r in range(k + 1, n) if M[r][k] != 0), None)
            if piv is None:
                return 0
            M[k], M[piv] = M[piv], M[k]
            sgn = -sgn
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sgn * M[n - 1][n - 1]


def sylvester_res(a: List[Fraction], b: List[Fraction]) -> Fraction:
    """Resultant of a and b with formal degrees len(a)-1 and len(b)-1."""
    m, n = len(a) - 1, len(b) - 1
    if m == 0:
        return a[0] ** n
    if n == 0:
        return b[0] ** m
    la = lb = 1
    for c in a:
        la = la * c.denominator // gcd_int(la, c.denominator)
    for c in b:
        lb = lb * c.denominator // gcd_int(lb, c.denominator)
    ai, bi = [int(c * la) for c in reversed(a)], [int(c * lb) for c in reversed(b)]
    N = m + n
    rows = [[0] * i + ai + [0] * (N - m - 1 - i) for i in range(n)]
    rows += [[0] * i + bi + [0] * (N - n - 1 - i) for i in range(m)]
    return Fraction(det_int(rows), la ** n * lb ** m)


# ---------------------------------------------------------------- bivariate

def to_ypoly(f: BiPoly) -> YPoly:
    if not f:
        return []
    dy = max(j for _, j in f)
    out: YPoly = [[] for _ in range(dy + 1)]
    for (i, j), c in f.items():
        col = out[j] + [Fraction(0)] * (i + 1 - len(out[j]))
        col[i] += c
        out[j] = trim(col)
    while out and not out[-1]:
        out.pop()
    return out


def ymul(A: YPoly, B: YPoly) -> YPoly:
    if not A or not B:
        return []
    out: YPoly = [[] for _ in range(len(A) + len(B) - 1)]
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            out[i + j] = uadd(out[i + j], umul(a, b))
    return out


def content(A: YPoly) -> UPoly:
    g: UPoly = []
    for c in A:
        g = ugcd(g, c)
    return g


def primitive(A: YPoly) -> YPoly:
    g = content(A)
    return [udivmod(c, g)[0] for c in A] if A else []


def yderiv(A: YPoly) -> YPoly:
    out = [uscale(A[j], Fraction(j)) for j in range(1, len(A))]
    while out and not out[-1]:
        out.pop()
    return out


def prem(A: YPoly, B: YPoly) -> YPoly:
    """Pseudo-remainder of A by B in Q[x][y]."""
    R = [list(c) for c in A]
    lb, db = B[-1], len(B) - 1
    while len(R) - 1 >= db and R:
        lr, shift = R[-1], len(R) - 1 - db
        R = [umul(c, lb) for c in R]
        for j, c in enumerate(B):
            R[j + shift] = uadd(R[j + shift], uscale(umul(c, lr), Fraction(-1)))
        while R and not R[-1]:
            R.pop()
    return R


def ygcd(A: YPoly, B: YPoly) -> YPoly:
    """Primitive gcd in Q[x][y] of primitive A and B, by the primitive remainder sequence."""
    A, B = primitive(A), primitive(B)
    while B and len(B) > 1:
        A, B = B, primitive(prem(A, B))
    if B:            # a nonzero constant in y: the gcd is 1
        return [[Fraction(1)]]
    return A


def yeval_x(A: YPoly, x0: Fraction) -> List[Fraction]:
    return [ueval(c, x0) for c in A]


def res_y(A: YPoly, B: YPoly) -> UPoly:
    """res_y(A, B) in Q[x], by evaluation at x = 0, 1, ... and interpolation."""
    dA = max(len(c) for c in A) - 1
    dB = max(len(c) for c in B) - 1
    D = (len(A) - 1) * dB + (len(B) - 1) * dA
    xs = [Fraction(k) for k in range(D + 1)]
    return interpolate(xs, [sylvester_res(yeval_x(A, x0), yeval_x(B, x0)) for x0 in xs])

# ---------------------------------------------------------------- algebraic points

class RealAlg:
    """A real algebraic number: squarefree p over Q with one root alpha in (a, b), or exact."""

    def __init__(self, p: UPoly, a: Fraction, b: Fraction, exact: Optional[Fraction] = None):
        self.p, self.a, self.b, self.exact = umonic(p), a, b, exact
        self._src: Optional[UPoly] = None
        if exact is not None:
            self.p, self.a, self.b = [-exact, Fraction(1)], exact, exact

    @staticmethod
    def rational(r: Fraction) -> "RealAlg":
        return RealAlg([-r, Fraction(1)], r, r, r)

    def refine(self, steps: int = 1) -> None:
        """Halve the isolating interval `steps` times, with integer sign evaluation."""
        for _ in range(steps):
            if self.exact is not None:
                return
            if self._src is not self.p:
                self._src, self._pi = self.p, int_poly(self.p)
                self._sa = isign(self._pi, self.a)
            m = (self.a + self.b) / 2
            v = isign(self._pi, m)
            if v == 0:
                self.__init__(self.p, m, m, m)
                return
            if v == self._sa:
                self.a = m
            else:
                self.b = m

    def has_root(self, g: UPoly) -> bool:
        """For a divisor g of p: does g vanish at alpha?"""
        if self.exact is not None:
            return ueval(g, self.exact) == 0
        return sign(ueval(g, self.a)) * sign(ueval(g, self.b)) < 0

    def reduce(self, q: UPoly) -> UPoly:
        q = trim(q)
        return q if len(q) < len(self.p) else udivmod(q, self.p)[1]

    def is_zero(self, q: UPoly) -> bool:
        q = trim(q)
        if not q:
            return True
        if self.exact is not None:
            return ueval(q, self.exact) == 0
        lo, hi = interval_eval(q, self.a, self.b)
        if lo > 0 or hi < 0:          # the interval already proves q(alpha) != 0
            return False
        g = ugcd(self.p, q)
        if len(g) <= 1:
            return False
        if self.has_root(g):
            self.p = g
            return True
        self.p = udivmod(self.p, g)[0]
        return False

    def inverse(self, q: UPoly) -> UPoly:
        """Inverse of q modulo p; q must be nonzero at alpha (checked first with is_zero)."""
        g = ugcd(self.p, q)
        if len(g) > 1:                 # q vanishes at other roots of p only: drop them
            self.p = udivmod(self.p, g)[0]
        r0, r1, s0, s1 = self.p, self.reduce(q), [], [Fraction(1)]
        while len(r1) > 1:
            quo, rem = udivmod(r0, r1)
            r0, r1, s0, s1 = r1, rem, s1, uadd(s0, uscale(umul(quo, s1), Fraction(-1)))
        return self.reduce(uscale(s1, 1 / r1[0]))

    def sign_of(self, q: UPoly) -> int:
        q = trim(q)
        if self.exact is not None:
            return sign(ueval(q, self.exact))
        if self.is_zero(q):
            return 0
        while True:
            lo, hi = interval_eval(q, self.a, self.b)
            if lo > 0 or hi < 0:
                return 1 if lo > 0 else -1
            self.refine(4)


def ipow(lo: int, hi: int, k: int) -> Tuple[int, int]:
    """Bounds of x^k for x in [lo, hi]."""
    if k == 0:
        return 1, 1
    a, b = lo ** k, hi ** k
    if k % 2 == 0 and lo < 0 < hi:
        return 0, max(a, b)
    return min(a, b), max(a, b)


def scaled(a: Fraction, b: Fraction) -> Tuple[int, int, int]:
    """[a, b] = [A, B] / D with integers A, B and D > 0."""
    D = a.denominator * b.denominator // gcd_int(a.denominator, b.denominator)
    return int(a * D), int(b * D), D


def interval_eval(q: UPoly, a: Fraction, b: Fraction) -> Tuple[int, int]:
    """A positive multiple of an enclosure of q over [a, b]; only its sign pattern is used."""
    qi = int_poly(trim(q))
    A, B, D = scaled(a, b)
    k = len(qi) - 1
    lo = hi = 0
    for i, c in enumerate(qi):
        if c:
            pl, ph = ipow(A, B, i)
            w = D ** (k - i)
            lo, hi = (lo + c * pl * w, hi + c * ph * w) if c > 0 else (lo + c * ph * w, hi + c * pl * w)
    return lo, hi


def interval_eval2(f: BiPoly, X: Tuple[Fraction, Fraction], Y: Tuple[Fraction, Fraction]) -> Tuple[int, int]:
    """A positive multiple of an enclosure of f over the box X x Y."""
    den = 1
    for c in f.values():
        den = den * c.denominator // gcd_int(den, c.denominator)
    A1, B1, D1 = scaled(*X)
    A2, B2, D2 = scaled(*Y)
    dx = max(i for i, _ in f)
    dy = max(j for _, j in f)
    lo = hi = 0
    for (i, j), c in f.items():
        c = int(c * den)
        xl, xh = ipow(A1, B1, i)
        yl, yh = ipow(A2, B2, j)
        ps = [xl * yl, xl * yh, xh * yl, xh * yh]
        pl, ph = min(ps), max(ps)
        w = D1 ** (dx - i) * D2 ** (dy - j)
        lo, hi = (lo + c * pl * w, hi + c * ph * w) if c > 0 else (lo + c * ph * w, hi + c * pl * w)
    return lo, hi


# ---------------------------------------------------------------- polynomials over Q(alpha)

def a_trim(al: RealAlg, g: List[UPoly]) -> List[UPoly]:
    g = [al.reduce(c) for c in g]
    while g and (not g[-1] or al.is_zero(g[-1])):
        g.pop()
    return [al.reduce(c) for c in g]


def a_monic(al: RealAlg, g: List[UPoly]) -> List[UPoly]:
    inv = al.inverse(g[-1])
    return [al.reduce(umul(c, inv)) for c in g]


def a_divmod(al: RealAlg, A: List[UPoly], B: List[UPoly]) -> Tuple[List[UPoly], List[UPoly]]:
    """Division in Q(alpha)[y]; B is trimmed, so its leading coefficient is nonzero at alpha."""
    A = a_trim(al, A)
    B = a_monic(al, a_trim(al, B))
    R = list(A)
    Q: List[UPoly] = [[] for _ in range(max(len(A) - len(B) + 1, 0))]
    while len(R) >= len(B) and R:
        c, k = R[-1], len(R) - len(B)
        Q[k] = c
        for i, b in enumerate(B):
            R[i + k] = al.reduce(uadd(R[i + k], uscale(umul(c, b), Fraction(-1))))
        R = a_trim(al, R)
    return Q, R


def a_gcd(al: RealAlg, A: List[UPoly], B: List[UPoly]) -> List[UPoly]:
    A, B = a_trim(al, A), a_trim(al, B)
    while B:
        A, B = B, a_divmod(al, A, B)[1]
    return a_monic(al, A) if A else []


def a_deriv(al: RealAlg, A: List[UPoly]) -> List[UPoly]:
    return a_trim(al, [uscale(A[j], Fraction(j)) for j in range(1, len(A))])


def a_eval(al: RealAlg, A: List[UPoly], y0: Fraction) -> UPoly:
    v: UPoly = []
    for c in reversed(A):
        v = al.reduce(uadd(uscale(v, y0), c))
    return v


class AlgSturm:
    """Sturm sequence over Q(alpha) of a squarefree g, with variations cached by point."""

    def __init__(self, al: RealAlg, g: List[UPoly]):
        self.al = al
        self.seq = [a_trim(al, g), a_deriv(al, g)]
        while self.seq[-1]:
            self.seq.append([uscale(x, Fraction(-1)) for x in a_divmod(al, self.seq[-2], self.seq[-1])[1]])
        self.seq = self.seq[:-1]
        self.cache: Dict[Fraction, int] = {}

    def var(self, y0: Fraction) -> int:
        if y0 not in self.cache:
            self.cache[y0] = variations([self.al.sign_of(a_eval(self.al, q, y0)) for q in self.seq])
        return self.cache[y0]

    def count(self, c: Fraction, d: Fraction) -> int:
        """Distinct roots in (c, d) of g over Q(alpha); c, d are not roots."""
        return self.var(c) - self.var(d)


def norm_in_y(al: RealAlg, g: List[UPoly]) -> UPoly:
    """N(y) = res_x(p(x), g(x, y)): its roots contain the roots of g over every root of p."""
    ex = max(len(c) for c in g)
    D = (len(al.p) - 1) * (len(g) - 1)
    ys = [Fraction(k) for k in range(D + 1)]
    vals = []
    for y0 in ys:
        col = [Fraction(0)] * ex
        for j, c in enumerate(g):
            for i, v in enumerate(c):
                col[i] += v * y0 ** j
        vals.append(sylvester_res(list(al.p), col))
    return interpolate(ys, vals)

# ---------------------------------------------------------------- the decomposition

def yun(f: UPoly) -> List[UPoly]:
    """Yun's squarefree decomposition: the nonconstant a_i with f = c * prod a_i^i."""
    f = umonic(f)
    if len(f) <= 1:
        return []
    g = ugcd(f, uderiv(f))
    c = udivmod(f, g)[0]
    d = uadd(udivmod(uderiv(f), g)[0], uscale(uderiv(c), Fraction(-1)))
    out = []
    while len(c) > 1:
        a = ugcd(c, d)
        if len(a) > 1:
            out.append(a)
        c = udivmod(c, a)[0]
        d = uadd(udivmod(d, a)[0], uscale(uderiv(c), Fraction(-1)))
    return out


def projection(F: List[BiPoly]) -> Tuple[YPoly, UPoly, List[UPoly]]:
    """S = squarefree part of the primitive part of prod F, P = the squarefree projection in Q[x],
    and the squarefree factors of the projection polynomials, used as small defining polynomials."""
    prod: YPoly = [[Fraction(1)]]
    factors: List[UPoly] = []
    for f in F:
        A = to_ypoly(f)
        if not A:
            continue
        factors.append(content(A))
        prod = ymul(prod, primitive(A))
    S = primitive(prod)
    if len(S) > 1:
        G = ygcd(S, yderiv(S))
        if len(G) > 1:
            S = primitive(ydivexact(S, G))
        factors.append(S[-1])
        factors.append(res_y(S, yderiv(S)))
    P: UPoly = [Fraction(1)]
    basis: List[UPoly] = []
    for q in factors:
        if len(trim(q)) > 1:
            P = umul(P, q)
            basis += yun(q)
    return S, usqfree(P), sorted(basis, key=len)


def ydivexact(A: YPoly, B: YPoly) -> YPoly:
    """Exact quotient A / B in Q[x][y] when B divides A."""
    R = [list(c) for c in A]
    Q: YPoly = [[] for _ in range(len(A) - len(B) + 1)]
    lb = B[-1]
    for k in range(len(A) - len(B), -1, -1):
        c, r = udivmod(R[k + len(B) - 1], lb)
        assert not r
        Q[k] = c
        for j, b in enumerate(B):
            R[j + k] = uadd(R[j + k], uscale(umul(c, b), Fraction(-1)))
    return Q


class Cell:
    def __init__(self, kind: Tuple[int, int], x, y, signs: Tuple[int, ...]):
        self.kind, self.x, self.y, self.signs = kind, x, y, signs

    def __repr__(self) -> str:
        return f"Cell({self.kind}, {self.signs})"


def sign_at(f: BiPoly, al: RealAlg, y) -> int:
    """Sign of f(alpha, y), for y rational or y = (Ns, c, d, g) a section of the stack."""
    fa = a_trim(al, to_ypoly(f)) if f else []
    if not fa:
        return 0
    if isinstance(y, Fraction):
        return al.sign_of(a_eval(al, fa, y))
    return section_sign(f, fa, al, *y)


def section_sign(f: BiPoly, fa: List[UPoly], al: RealAlg, Ns: UPoly, c: Fraction, d: Fraction,
                 g: List[UPoly]) -> int:
    """Sign of f at (alpha, beta), beta the only root of Ns and of g(alpha, y) in (c, d)."""
    if al.exact is not None:        # rational x: work with f(x0, y) in Q[y]
        q = trim([c0[0] if c0 else Fraction(0) for c0 in fa])
        G = ugcd(q, Ns)
        if len(G) > 1 and SturmCounter(G).count(c, d) >= 1:
            return 0
        while True:
            lo, hi = interval_eval(q, c, d)
            if lo > 0 or hi < 0:
                return 1 if lo > 0 else -1
            m = (c + d) / 2
            v = ueval(Ns, m)
            if v == 0:
                return sign(ueval(q, m))
            if sign(v) == sign(ueval(Ns, c)):
                c = m
            else:
                d = m
    lo, hi = interval_eval2(f, (al.a, al.b), (c, d))
    if lo > 0 or hi < 0:
        return 1 if lo > 0 else -1
    G = a_gcd(al, fa, g)
    if len(G) > 1 and AlgSturm(al, G).count(c, d) >= 1:
        return 0
    yl, yh = c, d
    while True:
        lo, hi = interval_eval2(f, (al.a, al.b), (yl, yh))
        if lo > 0 or hi < 0:
            return 1 if lo > 0 else -1
        al.refine()
        if yl != yh:
            m = (yl + yh) / 2
            v = ueval(Ns, m)
            if v == 0:
                yl = yh = m
            elif sign(v) == sign(ueval(Ns, yl)):
                yl = m
            else:
                yh = m


def stack_over(F: List[BiPoly], S: YPoly, al: RealAlg) -> List[Tuple[str, object]]:
    """The y-cells over the point alpha: sectors with rational samples, sections as (Ns, c, d)."""
    if len(S) <= 1:
        return [("sector", Fraction(0))]
    if al.exact is not None:        # rational x: the stack of S(x0, y) in Q[y]
        Ns = usqfree([ueval(c, al.exact) for c in S])
        sections = isolate(Ns)
        g = [[v] if v else [] for v in Ns]
    else:
        Ns, g, sections = algebraic_sections(S, al)
    if not sections:
        return [("sector", Fraction(0))]
    out: List[Tuple[str, object]] = [("sector", sections[0][0] - 1)]
    for c, d in sections:
        out.append(("section", (Ns, c, d, g)))
        out.append(("sector", d))
    out[-1] = ("sector", sections[-1][1] + 1)
    return out


def algebraic_sections(S: YPoly, al: RealAlg) -> Tuple[UPoly, List[UPoly], List[Tuple[Fraction, Fraction]]]:
    """Roots of S(alpha, y) for irrational alpha: the norm, the squarefree stack polynomial, the intervals."""
    g = a_trim(al, S)
    g = a_divmod(al, g, a_gcd(al, g, a_deriv(al, g)))[0]
    g = a_monic(al, a_trim(al, g))
    if len(g) <= 1:
        return [Fraction(1)], g, []
    Ns = usqfree(norm_in_y(al, g))
    st = AlgSturm(al, g)
    return Ns, g, [(c, d) for c, d in isolate(Ns) if st.count(c, d) == 1]


def cad(F: List[BiPoly]) -> Tuple[List[Tuple[str, object, List[Cell]]], UPoly, YPoly]:
    """Cylindrical F-sign-invariant decomposition of R^2.

    Returns the columns (kind, x sample, cells), the projection polynomial P(x)
    and the lifting polynomial S(x, y). Precondition: F is a list of
    polynomials over Q. Cost: polynomial in the degrees, for fixed n = 2.
    """
    S, P, basis = projection(F)  # @line L1
    xs: List[Tuple[str, RealAlg]] = []
    roots = isolate(P)  # @line L2
    if not roots:
        xs.append(("sector", RealAlg.rational(Fraction(0))))
    else:
        xs.append(("sector", RealAlg.rational(roots[0][0] - 1)))
        for k, (a, b) in enumerate(roots):  # @line L3
            # the smallest squarefree projection factor with a root in (a, b) defines alpha
            p = next(q for q in basis if sign(ueval(q, a)) * sign(ueval(q, b)) < 0)
            al = RealAlg(p, a, b)
            al.refine(24)
            xs.append(("section", al))
            nxt = roots[k + 1][0] if k + 1 < len(roots) else b + 2
            xs.append(("sector", RealAlg.rational((b + nxt) / 2)))
    columns = []
    for i, (kx, al) in enumerate(xs):  # @line L4
        ys = stack_over(F, S, al)  # @line L5
        cells = []
        for j, (ky, y) in enumerate(ys):  # @line L6
            signs = tuple(sign_at(f, al, y) for f in F)  # @line L7
            cells.append(Cell((i, j), al, y, signs))
        columns.append((kx, al, cells))
    return columns, P, S  # @line L8
