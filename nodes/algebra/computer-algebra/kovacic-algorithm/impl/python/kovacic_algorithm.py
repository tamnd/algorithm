# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kovacic-algorithm/. The authors are listed in prov/0QX1QC.jsonl.
"""Kovacic's algorithm for y'' = r y with r in Q(x), in exact rational arithmetic.

Polynomials are lists of Fractions, lowest degree first; rational functions
are pairs (num, den) in lowest terms with monic den. kovacic(s, t) looks at
r = s/t and returns (case, F), where F = [F_0, ..., F_m] lists the rational
coefficients of a polynomial F(w) = sum F_i w^i, monic in w, whose roots w
solve the Riccati equation w' + w^2 = r, so that y = exp(integral of w) is a
Liouvillian solution. It returns None when the equation has no Liouvillian
solution.

Scope: the poles of r must be rational (the denominator must split into
linear factors over Q), else ValueError. Case 1 may need square roots of
rational numbers; a family whose exponent sum is an integer only through
cancelling irrational square roots, or a pole of order 4 or more with an
irrational leading square root, raises NotImplementedError, since the
answer would need algebraic numbers.
"""
from fractions import Fraction
from itertools import product
from math import comb, factorial, isqrt

# ---------- polynomials over Q ----------


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    n = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def scale(p, c):
    return trim([c * a for a in p])


def sub(p, q):
    return add(p, scale(q, -1))


def mul(p, q):
    if not p or not q:
        return []
    r = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                r[i + j] += a * b
    return trim(r)


def deriv(p):
    return trim([i * p[i] for i in range(1, len(p))])


def shift(p, h):
    """p(x + h)."""
    if not p or h == 0:
        return list(p)
    r = [Fraction(0)] * len(p)
    for j, c in enumerate(p):
        if c:
            hp = Fraction(1)
            for k in range(j, -1, -1):
                r[k] += c * comb(j, k) * hp
                hp *= h
    return trim(r)


def divmod_poly(p, q):
    p = trim(p)
    quo = [Fraction(0)] * max(len(p) - len(q) + 1, 0)
    while p and len(p) >= len(q):
        c = Fraction(p[-1]) / q[-1]
        k = len(p) - len(q)
        quo[k] = c
        p = sub(p, scale([0] * k + q, c))
    return trim(quo), p


def gcd_poly(p, q):
    p, q = trim(p), trim(q)
    while q:
        p, q = q, divmod_poly(p, q)[1]
    return scale(p, Fraction(1) / p[-1]) if p else []


def _divisors(m):
    m, out, d = abs(m), set(), 1
    while d * d <= m:
        if m % d == 0:
            out.update((d, m // d))
        d += 1
    return sorted(out)


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def rational_roots(p):
    p = trim(p)
    roots = []
    if p and p[0] == 0:
        roots.append(Fraction(0))
        while p and p[0] == 0:
            p = p[1:]
    if len(p) <= 1:
        return roots
    den = 1
    for c in p:
        c = Fraction(c)
        den = den * c.denominator // _gcd(den, c.denominator)
    z = [int(Fraction(c) * den) for c in p]
    g = 0
    for c in z:
        g = _gcd(g, c)
    z = [c // g for c in z]
    deg = len(z) - 1
    for u in _divisors(z[0]):
        for v in _divisors(z[-1]):
            if _gcd(u, v) != 1:
                continue
            for su in (u, -u):
                acc, up, vp = 0, 1, v ** deg
                for c in z:
                    acc += c * up * vp
                    up *= su
                    vp //= v
                if acc == 0:
                    roots.append(Fraction(su, v))
    return roots


def poles(t):
    """{c: multiplicity} for the roots of t, which must split over Q."""
    t = trim(t)
    out = {}
    for c in rational_roots(t):
        lin = [-c, Fraction(1)]
        while True:
            q, rem = divmod_poly(t, lin)
            if rem:
                break
            out[c] = out.get(c, 0) + 1
            t = q
    if len(t) != 1:
        raise ValueError("the poles of r must be rational")
    return out


# ---------- rational functions ----------


def rf(num, den=None):
    num = trim([Fraction(c) for c in num])
    den = [Fraction(1)] if den is None else trim([Fraction(c) for c in den])
    if not num:
        return ([], [Fraction(1)])
    g = gcd_poly(num, den)
    num, den = divmod_poly(num, g)[0], divmod_poly(den, g)[0]
    c = den[-1]
    return (scale(num, 1 / c), scale(den, 1 / c))


def rf_add(a, b):
    return rf(add(mul(a[0], b[1]), mul(b[0], a[1])), mul(a[1], b[1]))


def rf_mul(a, b):
    return rf(mul(a[0], b[0]), mul(a[1], b[1]))


def rf_scale(a, c):
    return rf(scale(a[0], Fraction(c)), a[1])


def rf_der(a):
    return rf(sub(mul(deriv(a[0]), a[1]), mul(a[0], deriv(a[1]))), mul(a[1], a[1]))


def rf_inv(a):
    return rf(a[1], a[0])


def rf_sum(items):
    out = rf([])
    for a in items:
        out = rf_add(out, a)
    return out


def pole_term(coef, c, k):
    """coef / (x - c)^k."""
    den = [Fraction(1)]
    for _ in range(k):
        den = mul(den, [-c, Fraction(1)])
    return rf([coef], den)


ZERO = ([], [Fraction(1)])

# ---------- series ----------


def series_div(a, b, n):
    a = [Fraction(c) for c in a] + [Fraction(0)] * n
    out = []
    for k in range(n):
        v = a[k] - sum(out[i] * b[k - i] for i in range(max(0, k - len(b) + 1), k))
        out.append(v / b[0])
    return out


def rational_sqrt(q):
    q = Fraction(q)
    if q < 0:
        return None
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    return Fraction(a, b) if a * a == q.numerator and b * b == q.denominator else None


def sqrt_series(s, n):
    a0 = rational_sqrt(s[0])
    if a0 is None:
        raise NotImplementedError("leading square root is irrational")
    a = [a0]
    for k in range(1, n):
        a.append((s[k] - sum(a[i] * a[k - i] for i in range(1, k))) / (2 * a0))
    return a


def laurent_at(s, t, c, m, n):
    """r = sum L[k] (x - c)^(k - m), for k < n."""
    sc, tc = shift(s, c), shift(t, c)
    return series_div(sc, tc[m:], n)


def laurent_at_infinity(s, t, n):
    """r = sum M[k] x^(-o - k) with o = deg t - deg s the order at infinity, for k < n."""
    return series_div(list(reversed(s)), list(reversed(t)), n)


def squarefree_part(q):
    """(rational part, squarefree integer D) with sqrt(q) = part * sqrt(D)."""
    q = Fraction(q)
    if q == 0:
        return Fraction(0), 1
    num = q.numerator * q.denominator
    sign = -1 if num < 0 else 1
    num, D, f = abs(num), 1, 2
    part = 1
    while f * f <= num:
        while num % (f * f) == 0:
            num //= f * f
            part *= f
        f += 1
    D = sign * num
    return Fraction(part, q.denominator), D


# ---------- linear ODEs: polynomial solutions ----------


def nullspace(rows, ncols):
    rows = [list(r) for r in rows if any(r)]
    pivots, rank = [], 0
    for col in range(ncols):
        piv = next((i for i in range(rank, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = Fraction(1) / rows[rank][col]
        rows[rank] = [a * inv for a in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        pivots.append(col)
        rank += 1
    basis = []
    for free in range(ncols):
        if free in pivots:
            continue
        v = [Fraction(0)] * ncols
        v[free] = Fraction(1)
        for i, pc in enumerate(pivots):
            v[pc] = -rows[i][free]
        basis.append(v)
    return basis


def solve_columns(cols):
    height = max((len(c) for c in cols), default=0)
    rows = [[c[e] if e < len(c) else Fraction(0) for c in cols] for e in range(height)]
    basis = nullspace(rows, len(cols))
    return trim(basis[0]) if basis else None


def poly_solution(coeffs, d):
    """A nonzero polynomial P of degree <= d with sum coeffs[k] P^(k) = 0, or None."""
    den = [Fraction(1)]
    for a in coeffs:
        den = divmod_poly(mul(den, a[1]), gcd_poly(den, a[1]))[0]
    nums = [divmod_poly(mul(a[0], den), a[1])[0] for a in coeffs]
    cols = []
    for j in range(d + 1):
        mono, col = [Fraction(0)] * j + [Fraction(1)], []
        for k, nk in enumerate(nums):
            col = add(col, mul(nk, mono))
            mono = deriv(mono)
        cols.append(col)
    return solve_columns(cols)


# ---------- the three cases ----------


def _alpha_pm(b):
    """1/2 +- sqrt(1 + 4b)/2 as surds (p, q, D) meaning p + q sqrt(D)."""
    part, D = squarefree_part(1 + 4 * Fraction(b))
    if D == 1:
        return [(Fraction(1, 2) + part / 2, Fraction(0), 1), (Fraction(1, 2) - part / 2, Fraction(0), 1)]
    if part == 0:
        return [(Fraction(1, 2), Fraction(0), 1)] * 2
    return [(Fraction(1, 2), part / 2, D), (Fraction(1, 2), -part / 2, D)]


def case1_local(s, t, P, o):
    """For each pole and for infinity: a list of (sqrt part, alpha) choices."""
    local = []
    for c, m in sorted(P.items()):
        if m == 1:
            local.append([(ZERO, (Fraction(1), Fraction(0), 1))])
        elif m == 2:
            b = laurent_at(s, t, c, m, 1)[0]
            local.append([(ZERO, al) for al in _alpha_pm(b)])
        else:
            v = m // 2
            L = laurent_at(s, t, c, m, v)
            a = sqrt_series(L, v - 1) if v >= 2 else []
            sq_poly = a[:v - 1]
            sq = rf_sum([pole_term(a[k], c, v - k) for k in range(v - 1)])
            b = L[v - 1] - sum(sq_poly[i] * sq_poly[v - 1 - i] for i in range(v)
                               if i < len(sq_poly) and v - 1 - i < len(sq_poly))
            # leading coefficient a_0 of sqrt(r) itself
            a0 = sqrt_series(L, 1)[0]
            local.append([(sq, ((v + b / a0) / 2, Fraction(0), 1)),
                          (rf_scale(sq, -1), ((v - b / a0) / 2, Fraction(0), 1))])
    if o > 2:
        local.append([(ZERO, (Fraction(0), Fraction(0), 1)), (ZERO, (Fraction(1), Fraction(0), 1))])
    elif o == 2:
        b = Fraction(s[-1]) / t[-1]
        local.append([(ZERO, al) for al in _alpha_pm(b)])
    else:
        v = -o // 2
        M = laurent_at_infinity(s, t, v + 2)
        a = sqrt_series(M, v + 1)
        sq = rf([a[v - i] for i in range(v + 1)])
        b = M[v + 1] - sum(a[i] * a[v + 1 - i] for i in range(1, v + 1))
        local.append([(sq, ((b / a[0] - v) / 2, Fraction(0), 1)),
                      (rf_scale(sq, -1), ((-b / a[0] - v) / 2, Fraction(0), 1))])
    return local


def case1(s, t, P, o, r, trace):
    local = case1_local(s, t, P, o)  # @line L4
    for choice in product(*local):  # @line L5
        *at_poles, at_inf = choice
        p = at_inf[1][0] - sum(al[0] for _, al in at_poles)
        irr = {}
        for sign, (_, al) in [(1, at_inf)] + [(-1, x) for x in at_poles]:
            if al[1]:
                irr[al[2]] = irr.get(al[2], 0) + sign * al[1]
        if any(irr.values()):
            continue
        if p.denominator != 1 or p < 0:
            continue
        if irr:
            raise NotImplementedError("family needs algebraic numbers")
        d = int(p)
        w = rf_sum(  # @line L6
            [sq for sq, _ in choice] +
            [pole_term(al[0], c, 1) for (c, _), (_, al) in zip(sorted(P.items()), at_poles)])
        rest = rf_add(rf_add(rf_der(w), rf_mul(w, w)), rf_scale(r, -1))
        Pd = poly_solution([rest, rf_scale(w, 2), rf([1])], d)  # @line L7
        if trace is not None:
            trace.append((1, d, w, Pd))
        if Pd is not None:
            w1 = rf_add(w, rf(deriv(Pd), Pd))
            return [rf_scale(w1, -1), rf([1])]
    return None


def _ints(values):
    out = []
    for v in values:
        if v.denominator == 1 and v not in out:
            out.append(v)
    return out


def _sqrt_terms(b, mult):
    """[m * sqrt(1 + 4b) for m in mult], keeping only rational values."""
    q = rational_sqrt(1 + 4 * Fraction(b))
    if q is None:
        return [Fraction(0)] if 0 in mult else []
    return [m * q for m in mult]


def case2(s, t, P, o, r, trace):
    local = []
    for c, m in sorted(P.items()):
        if m == 1:
            local.append([Fraction(4)])
        elif m == 2:
            b = laurent_at(s, t, c, m, 1)[0]
            local.append(_ints([2 + x for x in _sqrt_terms(b, [0, 2, -2])]))
        else:
            local.append([Fraction(m)])
    if o > 2:
        e_inf = [Fraction(0), Fraction(2), Fraction(4)]
    elif o == 2:
        e_inf = _ints([2 + x for x in _sqrt_terms(Fraction(s[-1]) / t[-1], [0, 2, -2])])
    else:
        e_inf = [Fraction(o)]
    cs = sorted(P)
    for ei in e_inf:
        for es in product(*local):
            d2 = ei - sum(es)
            if d2 < 0 or d2 % 2 != 0:
                continue
            d = int(d2 // 2)
            th = rf_sum([pole_term(e / 2, c, 1) for e, c in zip(es, cs)])
            th1, th2 = rf_der(th), rf_der(rf_der(th))
            c1 = rf_sum([rf_scale(rf_mul(th, th), 3), rf_scale(th1, 3), rf_scale(r, -4)])
            c0 = rf_sum([th2, rf_scale(rf_mul(th, th1), 3), rf_mul(th, rf_mul(th, th)),
                         rf_scale(rf_mul(r, th), -4), rf_scale(rf_der(r), -2)])
            Pd = poly_solution([c0, c1, rf_scale(th, 3), rf([1])], d)
            if trace is not None:
                trace.append((2, d, th, Pd))
            if Pd is not None:
                phi = rf_add(th, rf(deriv(Pd), Pd))
                const = rf_sum([rf_scale(rf_der(phi), Fraction(1, 2)),
                                rf_scale(rf_mul(phi, phi), Fraction(1, 2)), rf_scale(r, -1)])
                return [const, rf_scale(phi, -1), rf([1])]
    return None


def case3(s, t, P, o, r, trace):
    cs = sorted(P)
    S = [Fraction(1)]
    for c in cs:
        S = mul(S, [-c, Fraction(1)])
    S1 = deriv(S)
    S2r = divmod_poly(mul(mul(S, S), r[0]), r[1])
    assert not S2r[1]
    S2r = S2r[0]
    gamma = Fraction(s[-1]) / t[-1] if o == 2 else Fraction(0)
    for n in (4, 6, 12):  # @line L3
        ks = [Fraction(12 * k, n) for k in range(-n // 2, n // 2 + 1)]
        local = []
        for c in cs:
            if P[c] == 1:
                local.append([Fraction(12)])
            else:
                b = laurent_at(s, t, c, 2, 1)[0]
                local.append(_ints([6 + x for x in _sqrt_terms(b, ks)]))
        e_inf = _ints([6 + x for x in _sqrt_terms(gamma, ks)])
        for ei in e_inf:
            for es in product(*local):
                dd = Fraction(n, 12) * (ei - sum(es))
                if dd < 0 or dd.denominator != 1:
                    continue
                d = int(dd)
                # S * theta as a polynomial
                Sth = []
                for e, c in zip(es, cs):
                    Sth = add(Sth, scale(divmod_poly(S, [-c, Fraction(1)])[0], Fraction(n, 12) * e))
                seqs, cols = [], []
                for j in range(d + 1):
                    Pi = {n + 1: [], n: [Fraction(0)] * j + [Fraction(-1)]}
                    for i in range(n, -1, -1):
                        Pi[i - 1] = add(add(scale(mul(S, deriv(Pi[i])), -1),
                                            mul(sub(scale(S1, n - i), Sth), Pi[i])),
                                        scale(mul(S2r, Pi[i + 1]), -(n - i) * (i + 1)))
                    seqs.append(Pi)
                    cols.append(Pi[-1])
                v = solve_columns(cols)
                if trace is not None:
                    trace.append((3, n, d, v))
                if v is not None:
                    F = []
                    for i in range(n + 1):
                        Pi = []
                        for j, vj in enumerate(v):
                            Pi = add(Pi, scale(seqs[j][i], vj))
                        Sp = [Fraction(1)]
                        for _ in range(i):
                            Sp = mul(Sp, S)
                        F.append(rf(scale(mul(Sp, Pi), Fraction(1, factorial(n - i)))))
                    lead = rf_inv(F[-1])
                    return [rf_mul(f, lead) for f in F]
    return None


def kovacic(s, t, trace=None):
    """Liouvillian solutions of y'' = (s/t) y: (case, F) or None."""
    r = rf(s, t)  # @line L1
    s, t = r
    P = poles(t)
    o = len(t) - len(s) if s else 10 ** 9
    cond1 = all(m == 1 or m % 2 == 0 for m in P.values()) and (o % 2 == 0 or o > 2)
    cond2 = any(m == 2 or (m % 2 == 1 and m > 2) for m in P.values())
    cond3 = all(m <= 2 for m in P.values()) and o >= 2
    for case, ok, run in ((1, cond1, case1), (2, cond2, case2), (3, cond3, case3)):  # @line L2
        if not ok:
            continue
        F = run(s, t, P, o, r, trace)  # lines L3 to L7, in case1, case2 and case3
        if F is not None:
            return case, F  # @line L8
    return None  # @line L9


# ---------- an independent check ----------


def verify(s, t, F):
    """True if every root w of F solves w' + w^2 = s/t: F divides F_x + F_w (r - w^2).

    Denominators are cleared first, so the test is a pseudo-division in w with
    polynomial coefficients in x and needs no gcd computations.
    """
    s = trim([Fraction(c) for c in s])
    t = trim([Fraction(c) for c in t])
    m = len(F) - 1
    D = [Fraction(1)]
    for f in F:
        D = mul(D, divmod_poly(f[1], gcd_poly(D, f[1]))[0])
    P = [mul(f[0], divmod_poly(D, f[1])[0]) for f in F]
    dD = deriv(D)

    def coef(k):
        return P[k] if 0 <= k <= m else []

    # G = D^2 t (F_x + F_w (s/t - w^2)), coefficient of w^k
    G = [add(add(mul(t, sub(mul(deriv(coef(k)), D), mul(coef(k), dD))),
                 scale(mul(mul(coef(k + 1), D), s), k + 1)),
             scale(mul(mul(coef(k - 1), D), t), -(k - 1)))
         for k in range(m + 2)]
    lead = P[m]
    for k in range(len(G) - 1, m - 1, -1):
        c = G[k]
        if c:
            G = [mul(g, lead) for g in G]
            for i in range(m + 1):
                G[k - m + i] = sub(G[k - m + i], mul(c, P[i]))
        G = G[:k]
    return all(not g for g in G)
