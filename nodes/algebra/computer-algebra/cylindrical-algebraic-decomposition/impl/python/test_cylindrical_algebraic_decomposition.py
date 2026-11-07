# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cylindrical-algebraic-decomposition/. The authors are listed in prov/P06M5D.jsonl.

"""Tests for the plane CAD against an exact line-by-line oracle.

On a vertical line x = x0 with x0 rational, the oracle restricts each f to a
univariate polynomial, isolates the real roots of their product with its own
Sturm sequences, and lists the sign vectors along the line from bottom to top.
Sign-invariance and cylindricity say that over every x0 in a sector column this
list equals the column's list of cell sign vectors.
"""

import random
from fractions import Fraction as Fr
from typing import Dict, List, Tuple

from cylindrical_algebraic_decomposition import cad

# ------------------------------------------------------------ independent oracle

def tr(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def ev(p, x):
    v = Fr(0)
    for a in reversed(p):
        v = v * x + a
    return v


def mul(p, q):
    if not p or not q:
        return []
    r = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def rem(p, q):
    r = tr(p)
    while len(r) >= len(q):
        c, k = r[-1] / q[-1], len(r) - len(q)
        for i, b in enumerate(q):
            r[k + i] -= c * b
        r = tr(r)
    return r


def quo(p, q):
    r, out = tr(p), [Fr(0)] * max(len(p) - len(q) + 1, 1)
    while len(r) >= len(q):
        c, k = r[-1] / q[-1], len(r) - len(q)
        out[k] = c
        for i, b in enumerate(q):
            r[k + i] -= c * b
        r = tr(r)
    return tr(out)


def gcd(p, q):
    p, q = tr(p), tr(q)
    while q:
        p, q = q, rem(p, q)
    return p


def der(p):
    return tr([i * p[i] for i in range(1, len(p))])


def sqf(p):
    p = tr(p)
    return quo(p, gcd(p, der(p))) if len(p) > 1 else p


class Sturm:
    """Sturm sequence of the squarefree part of p, for counting roots in (a, b]."""

    def __init__(self, p):
        p = sqf(p)
        self.seq = [p, der(p)] if len(p) > 1 else []
        while self.seq:
            r = [-c for c in rem(self.seq[-2], self.seq[-1])]
            if not r:
                break
            self.seq.append(r)

    def var(self, x):
        s = [v for v in (ev(q, x) for q in self.seq) if v != 0]
        return sum(1 for u, w in zip(s, s[1:]) if (u > 0) != (w > 0))

    def count(self, a, b):
        return self.var(a) - self.var(b) if self.seq else 0


def nroots(p, a, b):
    """Distinct real roots of p in (a, b]."""
    return Sturm(p).count(a, b)


def roots_of(h):
    """Isolating intervals (c, d) of the real roots of squarefree h, with h(c), h(d) nonzero."""
    if len(h) <= 1:
        return []
    B = 1 + sum(abs(c) for c in h[:-1]) / abs(h[-1])
    st = Sturm(h)
    out, todo = [], [(-B, B)]
    while todo:
        a, b = todo.pop()
        k = st.count(a, b)
        if k == 1:
            out.append((a, b))
        elif k > 1:
            m = (a + b) / 2
            if ev(h, m) == 0:
                out.append((m, m))
                e = (b - a) / 1024
                while ev(h, m - e) == 0 or ev(h, m + e) == 0 or st.count(m - e, m + e) > 1:
                    e /= 2
                out[-1] = (m - e, m + e)
                todo += [(a, m - e), (m + e, b)]
            else:
                todo += [(a, m), (m, b)]
    return sorted(out)


def sign_at_root(q, h, c, d):
    """Sign of q at the unique root of squarefree h in (c, d)."""
    q = tr(q)
    if not q:
        return 0
    g = gcd(q, h)
    if len(g) > 1 and nroots(g, c, d) > 0:
        return 0
    while True:                     # q(beta) != 0: shrink (c, d) until q keeps one sign on it
        lo, hi = hull(q, c, d)
        if lo > 0 or hi < 0:
            return 1 if lo > 0 else -1
        m = (c + d) / 2
        if ev(h, m) == 0:
            v = ev(q, m)
            return (v > 0) - (v < 0)
        if (ev(h, m) > 0) == (ev(h, c) > 0):
            c = m
        else:
            d = m


def hull(q, c, d):
    """Bounds of q on [c, d] by interval Horner evaluation."""
    lo = hi = Fr(0)
    for a in reversed(q):
        ps = [lo * c, lo * d, hi * c, hi * d]
        lo, hi = min(ps) + a, max(ps) + a
    return lo, hi


def restrict(f, x0):
    deg = max((j for _, j in f), default=0)
    out = [Fr(0)] * (deg + 1)
    for (i, j), c in f.items():
        out[j] += c * x0 ** i
    return tr(out)


def line_signs(F, x0) -> List[Tuple[int, ...]]:
    qs = [restrict(f, x0) for f in F]
    h = [Fr(1)]
    for q in qs:
        if q:
            h = mul(h, q)
    h = sqf(h)
    iv = roots_of(h)
    sg = lambda y: tuple((ev(q, y) > 0) - (ev(q, y) < 0) for q in qs)
    if not iv:
        return [sg(Fr(0))]
    out = [sg(iv[0][0] - 1)]
    for k, (c, d) in enumerate(iv):
        out.append(tuple(sign_at_root(q, h, c, d) for q in qs))
        nxt = iv[k + 1][0] if k + 1 < len(iv) else d + 2
        out.append(sg((d + nxt) / 2))
    return out


def sign_at_alg(q, P, a, b):
    """Sign of the univariate q at the unique root of squarefree P in (a, b)."""
    return sign_at_root(q, sqf(P), a, b)


def restrict_y(f, y0):
    deg = max((i for i, _ in f), default=0)
    out = [Fr(0)] * (deg + 1)
    for (i, j), c in f.items():
        out[i] += c * y0 ** j
    return tr(out)

# ------------------------------------------------------------ checks

def simple_in(lo, hi, x):
    """A rational with a small denominator in the open interval (lo, hi), near x."""
    n = 1
    while True:
        y = x.limit_denominator(n)
        if lo < y < hi:
            return y
        n *= 4


def runs(seq):
    return [v for i, v in enumerate(seq) if i == 0 or seq[i - 1] != v]


def column_ranges(cols):
    """Rational open x-ranges (lo, hi) inside each sector column; None means unbounded."""
    secs = [(al.a, al.b) for k, al, _ in cols if k == "section"]
    ranges = []
    for i in range(len(secs) + 1):
        lo = secs[i - 1][1] if i > 0 else None
        hi = secs[i][0] if i < len(secs) else None
        ranges.append((lo, hi))
    return ranges


def check(F, rng, probes=1, xs=()):
    cols, P, S = cad(F)
    kinds = [k for k, _, _ in cols]
    assert kinds[0] == "sector" and kinds[-1] == "sector"
    assert all(kinds[i] != kinds[i + 1] for i in range(len(kinds) - 1))
    sectors = [c for c in cols if c[0] == "sector"]
    for (lo, hi), (_, al, cells) in zip(column_ranges(cols), sectors):
        sigs = [c.signs for c in cells]
        assert line_signs(F, al.exact) == sigs
        for _ in range(probes):
            if lo is None and hi is None:
                x0 = Fr(rng.randint(-50, 50), rng.randint(1, 9))
            elif lo is None:
                x0 = hi - Fr(rng.randint(1, 400), rng.randint(1, 40))
            elif hi is None:
                x0 = lo + Fr(rng.randint(1, 400), rng.randint(1, 40))
            elif lo < hi:
                x0 = simple_in(lo, hi, lo + (hi - lo) * Fr(rng.randint(1, 99), 100))
            else:
                continue
            assert line_signs(F, x0) == sigs, (F, x0)
    for k, al, cells in cols:
        if k != "section":
            continue
        assert len(cells) % 2 == 1
        known = [r for r in xs if al.a <= r <= al.b and ev(P, r) == 0]
        if al.exact is not None or known:
            x0 = al.exact if al.exact is not None else known[0]
            # where some f vanishes on the whole line the stack may keep extra
            # sections of S there, so runs of equal sign vectors are merged
            assert runs(line_signs(F, x0)) == runs([c.signs for c in cells])
            continue
        for j, c in enumerate(cells):
            if j % 2 == 0:
                expect = tuple(sign_at_alg(restrict_y(f, c.y), P, al.a, al.b) for f in F)
                assert c.signs == expect
            else:
                assert 0 in c.signs
                for i, s in enumerate(c.signs):
                    if s != 0:
                        assert cells[j - 1].signs[i] == s == cells[j + 1].signs[i]
    return cols


def rand_poly(rng, deg, terms) -> Dict[Tuple[int, int], Fr]:
    mons = [(i, j) for i in range(deg + 1) for j in range(deg + 1 - i)]
    f = {}
    for m in rng.sample(mons, min(terms, len(mons))):
        c = rng.randint(-4, 4)
        if c:
            f[m] = Fr(c)
    return f

# ------------------------------------------------------------ tests

def circle():
    return {(2, 0): Fr(1), (0, 2): Fr(1), (0, 0): Fr(-1)}


def test_worked_example():
    F = [circle(), {(1, 0): Fr(1), (0, 1): Fr(-1)}]
    cols, P, S = cad(F)
    assert P == [Fr(1, 2), Fr(0), Fr(-3, 2), Fr(0), Fr(1)]  # (x^2 - 1)(x^2 - 1/2)
    assert [len(c) for _, _, c in cols] == [3, 5, 7, 5, 7, 5, 7, 5, 3]
    assert sum(len(c) for _, _, c in cols) == 47
    mid = cols[4][2]
    assert [c.signs for c in mid] == [(1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    check(F, random.Random(1))


def test_circle_alone():
    cols, P, S = cad([circle()])
    assert P == [Fr(-1), Fr(0), Fr(1)]
    assert [len(c) for _, _, c in cols] == [1, 3, 5, 3, 1]
    assert sum(len(c) for _, _, c in cols) == 13


def test_edge_cases():
    assert [c.signs for _, _, cs in cad([])[0] for c in cs] == [()]
    cols, _, _ = cad([{(0, 0): Fr(-3)}])
    assert [c.signs for _, _, cs in cols for c in cs] == [(-1,)]
    cols, _, _ = cad([{}])
    assert [c.signs for _, _, cs in cols for c in cs] == [(0,)]
    cols, P, _ = cad([{(1, 0): Fr(1)}])                   # x: one vertical line
    assert P == [Fr(0), Fr(1)] and [len(c) for _, _, c in cols] == [1, 1, 1]
    assert [cs[0].signs for _, _, cs in cols] == [(-1,), (0,), (1,)]
    cols, P, _ = cad([{(0, 1): Fr(1)}])                   # y: one horizontal line
    assert len(cols) == 1 and [c.signs for c in cols[0][2]] == [(-1,), (0,), (1,)]
    check([{(1, 1): Fr(1), (0, 0): Fr(-1)}], random.Random(2))   # hyperbola xy = 1
    check([{(1, 1): Fr(1)}], random.Random(3))                   # xy: content x times y
    check([{(0, 2): Fr(1), (3, 0): Fr(-1), (2, 0): Fr(-1)}], random.Random(4))  # nodal cubic
    check([{(0, 2): Fr(1), (3, 0): Fr(-1)}], random.Random(5))   # cusp
    check([{(0, 2): Fr(1), (0, 0): Fr(-2)}], random.Random(6))   # y^2 = 2, two lines
    check([{(2, 1): Fr(1), (0, 0): Fr(-1)}], random.Random(7))   # x^2 y = 1, vanishing lc
    check([circle(), circle()], random.Random(8))                # repeated input
    check([{(2, 0): Fr(1), (0, 2): Fr(1)}], random.Random(9))    # a single point


def test_lines_rational_sections():
    rng = random.Random(10)
    for _ in range(230):
        F = []
        for _ in range(rng.randint(1, 3)):
            a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)
            if a == 0 and b == 0:
                continue
            F.append({k: Fr(v) for k, v in {(1, 0): a, (0, 1): b, (0, 0): c}.items() if v})
        xs = []          # every critical x of a family of lines is rational
        for f in F:
            if f.get((0, 1), 0) == 0:
                xs.append(-f.get((0, 0), Fr(0)) / f[(1, 0)])
            for g in F:
                a1, b1, c1 = (f.get(m, Fr(0)) for m in [(1, 0), (0, 1), (0, 0)])
                a2, b2, c2 = (g.get(m, Fr(0)) for m in [(1, 0), (0, 1), (0, 0)])
                dd = a1 * b2 - a2 * b1
                if dd:
                    xs.append((b1 * c2 - b2 * c1) / dd)
        cols = check(F, rng, xs=xs)
        for k, al, _ in cols:
            if k == "section":
                assert al.exact is not None or any(al.a <= r <= al.b for r in xs)


def test_random_families():
    rng = random.Random(11)
    count = 0
    for _ in range(220):
        F = [rand_poly(rng, 2, rng.randint(2, 4)) for _ in range(rng.randint(1, 2))]
        check(F, rng)
        count += 1
    assert count == 220      # with 230 line families and 50 cubics: 500 random inputs


def test_random_cubics():
    rng = random.Random(12)
    for _ in range(50):
        check([rand_poly(rng, 3, rng.randint(2, 4))], rng)
