# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weil-descent-attack/. The authors are listed in prov/83GQX3.jsonl.

import random
from math import isqrt

# Weil descent for n = 2 in odd characteristic. K = F_(q^2) = F_q[t]/(t^2 - nu)
# with q an odd prime and nu the least non-residue; an element u + v t of K is
# the pair (u, v), and its Frobenius conjugate is (u, -v). The curve
#   E: y^2 = (x^2 - s x + t0)(x - beta) over K, with s, t0 in F_q and beta not in F_q,
# is covered by the genus 2 curve
#   C0: Y^2 = H(u) = -(T - 2u) G(u) over F_q, T = beta + beta^q, N = beta^(q+1),
#   G(u) = (N - u^2)^2 - s (N - u^2)(T - 2u) + t0 (T - 2u)^2,
# through phi(u, Y) = ((N - u^2)/(T - 2u), Y (u - beta)/(T - 2u)^2). A point R of
# E(K) goes to psi(R) = D + D^sigma in J(F_q), where D is the class of phi^*(R)
# minus 2 infinity, and the logarithm is then found by index calculus in J(F_q).
# Divisor classes are Mumford pairs (a, b) of coefficient lists, lowest first.


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


def sqrt_mod(c: int, q: int) -> int | None:
    """A square root of c mod the odd prime q (Tonelli-Shanks), or None."""
    c %= q
    if c == 0:
        return 0
    if pow(c, (q - 1) // 2, q) != 1:
        return None
    m, s = q - 1, 0
    while m % 2 == 0:
        m, s = m // 2, s + 1
    z = next(z for z in range(2, q) if pow(z, (q - 1) // 2, q) == q - 1)
    e, w, t, x = s, pow(z, m, q), pow(c, m, q), pow(c, (m + 1) // 2, q)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2, i = t2 * t2 % q, i + 1
        bb = pow(w, 1 << (e - i - 1), q)
        e, w, t, x = i, bb * bb % q, t * bb * bb % q, x * bb % q
    return x


class Fq:
    """The prime field F_q; elements are ints in [0, q)."""

    def __init__(self, q: int):
        self.q, self.zero, self.one = q, 0, 1

    def add(self, x, y):
        return (x + y) % self.q

    def sub(self, x, y):
        return (x - y) % self.q

    def mul(self, x, y):
        return x * y % self.q

    def inv(self, x):
        return pow(x, -1, self.q)

    def lift(self, c: int):
        return c % self.q


class Fq2:
    """K = F_q[t]/(t^2 - nu); elements are pairs (u, v)."""

    def __init__(self, q: int, nu: int):
        self.q, self.nu, self.zero, self.one = q, nu, (0, 0), (1, 0)

    def add(self, x, y):
        return (x[0] + y[0]) % self.q, (x[1] + y[1]) % self.q

    def sub(self, x, y):
        return (x[0] - y[0]) % self.q, (x[1] - y[1]) % self.q

    def mul(self, x, y):
        q = self.q
        return (x[0] * y[0] + self.nu * x[1] * y[1]) % q, (x[0] * y[1] + x[1] * y[0]) % q

    def inv(self, x):
        q = self.q
        n = pow((x[0] * x[0] - self.nu * x[1] * x[1]) % q, -1, q)
        return x[0] * n % q, (-x[1]) * n % q

    def lift(self, c: int):
        return c % self.q, 0

    def conj(self, x):
        return x[0], (-x[1]) % self.q

    def norm(self, x) -> int:
        return (x[0] * x[0] - self.nu * x[1] * x[1]) % self.q

    def sqrt(self, x):
        q = self.q
        u, v = x
        if v == 0:
            s = sqrt_mod(u, q)
            return (s, 0) if s is not None else (0, sqrt_mod(u * pow(self.nu, -1, q), q))
        n = sqrt_mod(self.norm(x), q)
        if n is None:
            return None
        for sg in (n, q - n):
            s = sqrt_mod((u + sg) * pow(2, -1, q), q)
            if s:
                return s, v * pow(2 * s, -1, q) % q
        return None


# polynomials over a field F: lists of elements, lowest degree first, trimmed


def ptrim(F, a):
    a = list(a)
    while a and a[-1] == F.zero:
        a.pop()
    return a


def padd(F, a, b):
    n = max(len(a), len(b))
    return ptrim(F, [F.add(a[i] if i < len(a) else F.zero, b[i] if i < len(b) else F.zero) for i in range(n)])


def psub(F, a, b):
    n = max(len(a), len(b))
    return ptrim(F, [F.sub(a[i] if i < len(a) else F.zero, b[i] if i < len(b) else F.zero) for i in range(n)])


def pmul(F, a, b):
    if not a or not b:
        return []
    out = [F.zero] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = F.add(out[i + j], F.mul(x, y))
    return ptrim(F, out)


def pscale(F, a, c):
    return ptrim(F, [F.mul(x, c) for x in a])


def pdivmod(F, a, m):
    r = list(a)
    inv = F.inv(m[-1])
    quo = [F.zero] * max(0, len(a) - len(m) + 1)
    for i in range(len(quo) - 1, -1, -1):
        c = F.mul(r[i + len(m) - 1], inv)
        quo[i] = c
        for j, y in enumerate(m):
            r[i + j] = F.sub(r[i + j], F.mul(c, y))
    return ptrim(F, quo), ptrim(F, r[: len(m) - 1])


def pxgcd(F, a, b):
    """(g, x, y) with x a + y b = g and g monic, for a, b not both zero."""
    r0, r1, x0, x1, y0, y1 = a, b, [F.one], [], [], [F.one]
    while r1:
        qt, r = pdivmod(F, r0, r1)
        r0, r1 = r1, r
        x0, x1 = x1, psub(F, x0, pmul(F, qt, x1))
        y0, y1 = y1, psub(F, y0, pmul(F, qt, y1))
    c = F.inv(r0[-1])
    return pscale(F, r0, c), pscale(F, x0, c), pscale(F, y0, c)


def peval(F, a, x):
    out = F.zero
    for c in reversed(a):
        out = F.add(F.mul(out, x), c)
    return out


# the Jacobian of Y^2 = H(u), deg H = 5, by Cantor's algorithm


def jac_add(F, H, D1, D2):
    (a1, b1), (a2, b2) = D1, D2
    d1, e1, e2 = pxgcd(F, a1, a2)
    if len(d1) == 1:  # coprime supports: d = 1, s1 = e1, s2 = e2, s3 = 0
        a = pmul(F, a1, a2)
        b = pdivmod(F, padd(F, pmul(F, pmul(F, e1, a1), b2), pmul(F, pmul(F, e2, a2), b1)), a)[1]
    else:
        d, c1, c2 = pxgcd(F, d1, padd(F, b1, b2))
        s1, s2 = pmul(F, c1, e1), pmul(F, c1, e2)
        a = pdivmod(F, pmul(F, a1, a2), pmul(F, d, d))[0]
        num = padd(F, padd(F, pmul(F, pmul(F, s1, a1), b2), pmul(F, pmul(F, s2, a2), b1)), pmul(F, c2, padd(F, pmul(F, b1, b2), H)))
        b = pdivmod(F, pdivmod(F, num, d)[0], a)[1]
    while len(a) > 3:
        a = pdivmod(F, psub(F, H, pmul(F, b, b)), a)[0]
        a = pscale(F, a, F.inv(a[-1]))
        b = pdivmod(F, ptrim(F, [F.sub(F.zero, c) for c in b]), a)[1]
    return a, b


def jac_neg(F, D):
    return D[0], ptrim(F, [F.sub(F.zero, c) for c in D[1]])


def jac_mul(F, H, k: int, D):
    R = ([F.one], [])
    while k:
        if k & 1:
            R = jac_add(F, H, R, D)
        D = jac_add(F, H, D, D)
        k >>= 1
    return R


def jac_doublings(F, H, D, m: int) -> list:
    """D, 2 D, 4 D, ... with enough terms for any multiplier below m."""
    out = [D]
    for _ in range(max(1, m.bit_length()) - 1):
        out.append(jac_add(F, H, out[-1], out[-1]))
    return out


def jac_mul_table(F, H, k: int, tab: list):
    R, i = ([F.one], []), 0
    while k:
        if k & 1:
            R = jac_add(F, H, R, tab[i])
        k, i = k >> 1, i + 1
    return R


class WeilCurve:
    """E: y^2 = (x^2 - s x + t0)(x - beta) over F_(q^2) and its genus 2 cover C0 over F_q."""

    def __init__(self, q: int, s: int, t0: int, beta: tuple[int, int]):
        if q < 3 or not _is_prime(q):
            raise ValueError("q must be an odd prime")
        nu = next(c for c in range(2, q) if pow(c, (q - 1) // 2, q) == q - 1) if q > 3 else 2
        self.q, self.F, self.K = q, Fq(q), Fq2(q, nu)
        K, F = self.K, self.F
        self.s, self.t0 = s % q, t0 % q
        self.beta = (beta[0] % q, beta[1] % q)
        if self.beta[1] == 0:
            raise ValueError("beta must lie outside F_q")
        if (self.s * self.s - 4 * self.t0) % q == 0:
            raise ValueError("x^2 - s x + t0 has a double root")
        b = self.beta
        gb = K.add(K.sub(K.mul(b, b), K.mul(K.lift(self.s), b)), K.lift(self.t0))
        if gb == K.zero:
            raise ValueError("beta is a root of x^2 - s x + t0")
        # f(x) = x^3 + a2 x^2 + a4 x + a6 over K
        self.a2 = K.sub(K.lift(-self.s), b)
        self.a4 = K.add(K.lift(self.t0), K.mul(K.lift(self.s), b))
        self.a6 = K.mul(K.lift(-self.t0), b)
        self.T, self.N = 2 * b[0] % q, K.norm(b)
        T, N = self.T, self.N
        m = [N, 0, q - 1]  # N - u^2
        l = [T, q - 2]  # T - 2u
        G = padd(F, padd(F, pmul(F, m, m), pscale(F, pmul(F, m, l), (-self.s) % q)), pscale(F, pmul(F, l, l), self.t0))
        self.H = pscale(F, pmul(F, l, G), q - 1)  # @line L1
        dH = ptrim(F, [i * c % q for i, c in enumerate(self.H)][1:])
        if len(self.H) != 6 or len(pxgcd(F, self.H, dH)[0]) != 1:
            raise ValueError("H is not squarefree of degree 5")
        self.HK = [K.lift(c) for c in self.H]

    # E(K)
    def f(self, x):
        K = self.K
        return K.add(K.mul(K.add(K.mul(K.add(x, self.a2), x), self.a4), x), self.a6)

    def on_curve(self, P) -> bool:
        return P is None or self.K.mul(P[1], P[1]) == self.f(P[0])

    def neg(self, P):
        return None if P is None else (P[0], self.K.sub(self.K.zero, P[1]))

    def add(self, P, Q):
        K = self.K
        if P is None:
            return Q
        if Q is None:
            return P
        (x1, y1), (x2, y2) = P, Q
        if x1 == x2:
            if K.add(y1, y2) == K.zero:
                return None
            num = K.add(K.add(K.mul(K.lift(3), K.mul(x1, x1)), K.mul(K.lift(2), K.mul(self.a2, x1))), self.a4)
            lam = K.mul(num, K.inv(K.add(y1, y1)))
        else:
            lam = K.mul(K.sub(y2, y1), K.inv(K.sub(x2, x1)))
        x3 = K.sub(K.sub(K.sub(K.mul(lam, lam), self.a2), x1), x2)
        return x3, K.sub(K.mul(lam, K.sub(x1, x3)), y1)

    def smul(self, k: int, P):
        R = None
        while k:
            if k & 1:
                R = self.add(R, P)
            P = self.add(P, P)
            k >>= 1
        return R

    def order_e(self) -> int:
        """#E(F_(q^2)) by counting, O(q^2) operations (a toy step)."""
        K, q, n = self.K, self.q, 1
        for u in range(q):
            for v in range(q):
                z = self.f((u, v))
                n += 1 if z == K.zero else (2 if pow(K.norm(z), (q - 1) // 2, q) == 1 else 0)
        return n

    def order_j(self) -> int:
        """#J(F_q) from #C0(F_q) and #C0(F_(q^2)) by counting (a toy step)."""
        F, K, q = self.F, self.K, self.q
        n1 = 1
        for u in range(q):
            z = peval(F, self.H, u)
            n1 += 1 if z == 0 else (2 if pow(z, (q - 1) // 2, q) == 1 else 0)
        n2 = 1
        for u in range(q):
            for v in range(q):
                z = peval(K, self.HK, (u, v))
                n2 += 1 if z == K.zero else (2 if pow(K.norm(z), (q - 1) // 2, q) == 1 else 0)
        a1 = n1 - q - 1
        a2 = (a1 * a1 - (q * q + 1 - n2)) // 2
        return 1 + a1 + a2 + q * a1 + q * q

    def point_order(self, P, n: int) -> int:
        for r, _ in _factor(n):
            while n % r == 0 and self.smul(n // r, P) is None:
                n //= r
        return n

    def random_point(self, rng: random.Random):
        while True:
            x = (rng.randrange(self.q), rng.randrange(self.q))
            y = self.K.sqrt(self.f(x))
            if y is not None:
                return (x, y) if rng.randrange(2) else self.neg((x, y))

    # the descent map psi: E(K) -> J(F_q)
    def phi(self, u, Y):
        """The point of E over the point (u, Y) of C0 with u in K, T - 2u != 0."""
        K = self.K
        d = K.sub(K.lift(self.T), K.mul(K.lift(2), u))
        x = K.mul(K.sub(K.lift(self.N), K.mul(u, u)), K.inv(d))
        return x, K.mul(K.mul(Y, K.sub(u, self.beta)), K.inv(K.mul(d, d)))

    def psi(self, R):
        K, F = self.K, self.F
        if R is None or R[0] == self.beta:  # @line L10
            return [1], []
        xr, yr = R
        A = [K.sub(K.mul(xr, K.lift(self.T)), K.lift(self.N)), K.mul(K.lift(-2), xr), K.one]  # @line L11
        _, inv, _ = pxgcd(K, [K.sub(K.zero, self.beta), K.one], A)
        l = [K.lift(self.T), K.lift(-2)]
        B = pdivmod(K, pmul(K, pscale(K, pmul(K, l, l), yr), inv), A)[1]
        D = (ptrim(K, A), B)
        Ds = ([K.conj(c) for c in D[0]], [K.conj(c) for c in D[1]])
        a, b = jac_add(K, self.HK, D, Ds)  # @line L12
        if any(c[1] for c in a + b):
            raise AssertionError("trace not defined over F_q")
        return [c[0] for c in a], [c[0] for c in b]


def factor_base(W: WeilCurve) -> dict[int, int]:
    """u0 -> Y0 for every u0 in F_q with H(u0) a square, Y0 the smaller root."""
    fb = {}
    for u in range(W.q):
        y = sqrt_mod(peval(W.F, W.H, u), W.q)
        if y is not None:
            fb[u] = min(y, (-y) % W.q)
    return fb


def jac_decompose(W: WeilCurve, D, fb: dict[int, int]) -> dict[int, int] | None:
    """A row e with D = sum of e_u (u - u0, Y0) if the a-polynomial of D splits, or None."""
    q, F = W.q, W.F
    a, b = D
    if len(a) == 1:
        return {}
    if len(a) == 2:
        u0, Y = (-a[0]) % q, peval(F, b, (-a[0]) % q)
        return {u0: 1 if Y == fb[u0] else -1}
    w = sqrt_mod(a[1] * a[1] - 4 * a[0], q)
    if w is None:
        return None
    half = pow(2, -1, q)
    row: dict[int, int] = {}
    for u0 in sorted({(-a[1] - w) * half % q, (-a[1] + w) * half % q}):
        Y = peval(F, b, u0)
        row[u0] = (1 if Y == fb[u0] else -1) * (2 if w == 0 else 1)
    return row


def gaudry_log(W: WeilCurve, D1, D2, r: int, nj: int, fb: dict[int, int], rng: random.Random) -> int:
    """log_D1 D2 mod r in J(F_q) by index calculus on degree one divisors.
    Precondition: D1 has prime order r, r divides nj = #J(F_q) exactly once, D2 in <D1>."""
    F, H = W.F, W.H
    cols = sorted(fb)  # @line L13
    idx = {u: i for i, u in enumerate(cols)}
    m, us = nj // r, cols[0]
    t1, t2 = jac_doublings(F, H, D1, r), jac_doublings(F, H, D2, r)
    tu = jac_doublings(F, H, jac_mul(F, H, r, ([(-us) % W.q, 1], ptrim(F, [fb[us]]))), m)
    piv: dict[int, tuple[list[int], dict[int, int]]] = {}
    av: list[int] = []
    bv: list[int] = []
    while True:  # @line L14
        a, b = rng.randrange(r), rng.randrange(r)  # @line L15
        R = jac_add(F, H, jac_add(F, H, jac_mul_table(F, H, a, t1), jac_mul_table(F, H, b, t2)), jac_mul_table(F, H, rng.randrange(m), tu))
        e = jac_decompose(W, R, fb)  # @line L16
        if e is None:  # @line L17
            continue
        j = len(av)
        av.append(a)
        bv.append(b)
        v = [0] * len(cols)
        for u, c in e.items():
            v[idx[u]] = c % r
        comb = {j: 1}
        for col in range(len(cols)):  # @line L18
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
            A = sum(c * av[k] for k, c in comb.items()) % r
            C = sum(c * bv[k] for k, c in comb.items()) % r
            if C:  # @line L19
                return (-A) * pow(C, -1, r) % r
        else:
            inv = pow(v[lead], -1, r)  # @line L20
            piv[lead] = ([c * inv % r for c in v], {k: c * inv % r for k, c in comb.items() if c})


def bsgs(W: WeilCurve, P, Q, m: int) -> int | None:
    """x in [0, m) with x P = Q in E(K) for P of order m, or None."""
    s = isqrt(m - 1) + 1
    table: dict = {}
    T = None
    for i in range(s):
        table.setdefault(T, i)
        T = W.add(T, P)
    step, T = W.neg(W.smul(s, P)), Q
    for j in range(s + 1):
        if T in table:
            return (j * s + table[T]) % m
        T = W.add(T, step)
    return None


def weil_descent_log(W: WeilCurve, P, Q, seed: int = 0, ne: int | None = None, nj: int | None = None) -> int | None:
    """The x in [0, ord P) with x P = Q in E(F_(q^2)), or None if Q is not in <P>.

    The group is E(F_(q^2)), of order about q^2; a group operation costs O(1)
    operations in F_(q^2), O(log(q)^2) bit operations. psi costs O(1)
    operations in F_(q^2). For the prime r > q with r || ord P, r^2 not
    dividing #J(F_q) and psi(P_r) != 0 (there is at most one), the index
    calculus in J(F_q) makes an expected O(q) draws (heuristic: about half of
    the reduced divisors split), each O(log q) Jacobian operations of O(1)
    operations in F_q, and the dense elimination costs O(q^3) operations mod
    r. Other prime powers r^e go to baby-step giant-step, O(r^(e/2)) group
    operations. Counting the two group orders is a toy O(q^2) step.
    """
    if not (W.on_curve(P) and W.on_curve(Q)):
        raise ValueError("points must lie on the curve")
    rng = random.Random(seed)
    if ne is None:
        ne = W.order_e()
    n = W.point_order(P, ne)
    if W.smul(n, Q) is not None:  # @line L2
        return None
    fb: dict[int, int] | None = None
    x, mod = 0, 1
    for r, e in _factor(n):  # @line L3
        re = r**e
        Pr, Qr = W.smul(n // re, P), W.smul(n // re, Q)  # @line L4
        big = e == 1 and r > W.q
        if big:
            if nj is None:
                nj = W.order_j()
            DP = W.psi(Pr)
        if big and nj % (r * r) != 0 and DP != ([1], []):  # @line L5
            if fb is None:
                fb = factor_base(W)
            y = gaudry_log(W, DP, W.psi(Qr), r, nj, fb, rng)  # @line L6
            if W.smul(y, Pr) != Qr:  # @line L7
                return None
            xr = y
        else:
            xr = bsgs(W, Pr, Qr, re)  # @line L8
            if xr is None:
                return None
        x += mod * ((xr - x) * pow(mod, -1, re) % re)  # @line L9
        mod *= re
    return x % n
