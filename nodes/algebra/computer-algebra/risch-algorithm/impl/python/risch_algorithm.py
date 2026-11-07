# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/risch-algorithm/. The authors are listed in prov/GY4RMM.jsonl.
"""The Risch algorithm for one exponential monomial over Q(x).

Input: b in Q[x] of degree at least 1, so that t = exp(b) is a monomial over
Q(x) with t' = b' t, and an integrand
    f = sum over k of f_k t^k,   f_k in Q(x), k in Z
(a Laurent polynomial in t). Output: None if f has no elementary integral,
otherwise (ys, R, (A, D)) with
    integral of f = sum over k != 0 of y_k t^k + R + integral of A / D,
where y_k, R are in Q(x) and D is squarefree, so that the last integral is a
sum of logarithms (found by the Rothstein-Trager method, not done here).

Polynomials are lists of Fractions, low degree first; a rational function is
a pair (num, den). Cost model: operations in Q. The work is polynomial in the
degrees of b, of the numerators and of the denominators (proved); the size of
the rational numbers is not bounded here.
"""

from __future__ import annotations

from fractions import Fraction as Q


def norm(a):
    a = [Q(c) for c in a]
    while a and a[-1] == 0:
        a.pop()
    return a


def deg(a):
    return len(a) - 1  # -1 for the zero polynomial


def add(a, b):
    n = max(len(a), len(b))
    return norm([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def scale(a, c):
    return norm([c * x for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    if not a or not b:
        return []
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] += x * y
    return norm(out)


def divmod_p(a, b):
    a, q = list(a), [Q(0)] * max(len(a) - len(b) + 1, 0)
    while len(a) >= len(b) and a:
        c, s = a[-1] / b[-1], len(a) - len(b)
        q[s] = c
        for i, y in enumerate(b):
            a[i + s] -= c * y
        a = norm(a)
    return norm(q), a


def exquo(a, b):
    q, r = divmod_p(a, b)
    assert not r
    return q


def gcd(a, b):
    a, b = norm(a), norm(b)
    while b:
        a, b = b, divmod_p(a, b)[1]
    return scale(a, 1 / a[-1]) if a else []


def deriv(a):
    return norm([i * a[i] for i in range(1, len(a))])


def ext_euclid(a, b, c):
    """(s, t) with s a + t b = c and deg s < deg b; gcd(a, b) must divide c."""
    r0, r1, s0, s1 = norm(a), norm(b), [Q(1)], []
    while r1:  # invariant: s_i a = r_i mod b
        q, r = divmod_p(r0, r1)
        r0, r1, s0, s1 = r1, r, s1, sub(s0, mul(q, s1))
    g = r0
    q, r = divmod_p(c, g)
    assert not r
    s = divmod_p(mul(s0, q), b)[1] if deg(b) > 0 else []
    t = exquo(sub(c, mul(s, a)), b)
    return s, t


def rat_add(x, y):
    n = add(mul(x[0], y[1]), mul(y[0], x[1]))
    d = mul(x[1], y[1])
    g = gcd(n, d) if n else d
    return (exquo(n, g), exquo(d, g)) if n else ([], [Q(1)])


def rat_deriv(x):
    n, d = x
    return rat_add((mul(deriv(n), d), mul(d, d)), (scale(mul(n, deriv(d)), -1), mul(d, d)))


def hermite_reduce(A, D):
    """(R, (A2, D2)) with A / D = R' + A2 / D2 and D2 squarefree (Mack's linear version)."""
    P, A = divmod_p(A, D)  # polynomial part, integrated directly
    g = (norm([0] + [c / (i + 1) for i, c in enumerate(P)]), [Q(1)])
    Dm = gcd(D, deriv(D))
    Ds = exquo(D, Dm)
    while deg(Dm) > 0:
        Dm2 = gcd(Dm, deriv(Dm))
        Dms = exquo(Dm, Dm2)
        B, C = ext_euclid(scale(exquo(mul(Ds, deriv(Dm)), Dm), -1), Dms, A)
        A = sub(C, exquo(mul(deriv(B), Ds), Dms))
        g = rat_add(g, (B, Dm))
        Dm = Dm2
    return g, (A, Ds)


def rde_poly_coeff(fk, gk):
    """Rational y with y' + fk y = gk, fk in Q[x] of degree m >= 0; None if none.

    The solution is unique because y' + fk y = 0 has no nonzero rational solution.
    """
    a, d = gk
    if not a:
        return ([], [Q(1)])
    g0 = gcd(a, d)
    a, d = exquo(a, g0), exquo(d, g0)
    h = gcd(d, deriv(d))                                  # @line L4
    c, r = divmod_p(mul(a, mul(h, h)), d)
    if r:                                                 # a simple pole in gk
        return None
    # h q' + (fk h - h') q = c, an operator that raises the degree by m + deg h
    lead = sub(mul(fk, h), deriv(h))
    shift, lc = deg(lead), lead[-1]
    q = []
    while c:                                              # @line L5
        j = deg(c) - shift
        if j < 0:
            return None
        coef = c[-1] / lc
        mono = [Q(0)] * j + [coef]
        q = add(q, mono)
        c = sub(c, add(mul(h, deriv(mono)), mul(lead, mono)))
    gq = gcd(q, h) if q else h
    return (exquo(q, gq), exquo(h, gq)) if q else ([], [Q(1)])


def risch_exp(b, f):
    """Integrate f = {k: (num, den)} in Q(x)[t, 1/t] with t = exp(b)."""
    b = norm(b)
    assert deg(b) >= 1
    db = deriv(b)
    ys = {}
    for k in sorted(f):                                   # @line L1
        if k == 0 or not norm(f[k][0]):
            continue
        y = rde_poly_coeff(scale(db, k), (norm(f[k][0]), norm(f[k][1])))  # @line L2
        if y is None:
            return None                                   # @line L3
        ys[k] = y
    A, D = f.get(0, ([], [Q(1)]))                         # @line L6
    A, D = norm(A), norm(D)
    if not A:
        return ys, ([], [Q(1)]), ([], [Q(1)])
    R, rest = hermite_reduce(A, D)                        # @line L7
    return ys, R, rest                                    # @line L8
