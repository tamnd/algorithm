# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-fraction-decomposition/. The authors are listed in prov/P053GE.jsonl.

import random
from fractions import Fraction as Fr

import pytest

from partial_fraction_decomposition import partial_fractions


class GF:
    """Z/pZ for p = 7."""

    p = 7

    def __init__(self, v):
        self.v = v.v if isinstance(v, GF) else v % GF.p

    def __add__(self, o):
        return GF(self.v + GF(o).v)

    __radd__ = __add__

    def __sub__(self, o):
        return GF(self.v - GF(o).v)

    def __rsub__(self, o):
        return GF(GF(o).v - self.v)

    def __mul__(self, o):
        return GF(self.v * GF(o).v)

    __rmul__ = __mul__

    def __neg__(self):
        return GF(-self.v)

    def __truediv__(self, o):
        o = GF(o)
        if o.v == 0:
            raise ZeroDivisionError
        return GF(self.v * pow(o.v, GF.p - 2, GF.p))

    def __eq__(self, o):
        return self.v == GF(o).v

    def __hash__(self):
        return self.v


# independent helpers, written separately from the module under test
def ev(f, x):
    s = 0 * x
    for c in reversed(f):
        s = s * x + c
    return s


def mul(f, g):
    if not f or not g:
        return []
    h = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            h[i + j] = h[i + j] + a * b
    while h and h[-1] == 0:
        h.pop()
    return h


def power(f, e):
    out = [1]
    for _ in range(e):
        out = mul(out, f)
    return out


def solve(rows, rhs):
    """Unique solution of a square linear system by Gauss-Jordan elimination."""
    n = len(rows)
    m = [list(r) + [v] for r, v in zip(rows, rhs)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        pv = m[col][col]
        m[col] = [v / pv for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                fac = m[r][col]
                m[r] = [a - fac * b for a, b in zip(m[r], m[col])]
    return [m[i][n] for i in range(n)]


def brute(a, factors, field):
    """Solve a = q b + sum a_ij b / b_i^j for the coefficients, as a linear system."""
    b = [field(1)]
    for bi, ei in factors:
        b = mul(b, power(bi, ei))
    d = len(b) - 1
    dq = max(0, len(a) - 1 - d + 1) if len(a) > d else 0
    cols = []  # each column is a polynomial, the coefficient of one unknown
    labels = []
    for k in range(dq):
        cols.append(mul([0] * k + [field(1)], b))
        labels.append(("q", k))
    for i, (bi, ei) in enumerate(factors):
        for j in range(1, ei + 1):
            cof = [field(1)]
            for i2, (b2, e2) in enumerate(factors):
                cof = mul(cof, power(b2, e2 - j if i2 == i else e2))
            for k in range(len(bi) - 1):
                cols.append(mul([0] * k + [field(1)], cof))
                labels.append((i, j, k))
    n = len(cols)
    size = max(n, len(a))
    rows = [[(c[r] if r < len(c) else field(0)) for c in cols] for r in range(size)]
    rhs = [(a[r] if r < len(a) else field(0)) for r in range(size)]
    sol = solve(rows[:n], rhs[:n]) if n else []
    assert all(sum((row[k] * sol[k] for k in range(n)), field(0)) == v for row, v in zip(rows[n:], rhs[n:]))
    q, parts = [field(0)] * dq, {}
    for lab, v in zip(labels, sol):
        if lab[0] == "q":
            q[lab[1]] = v
        else:
            i, j, k = lab
            parts.setdefault((i, j), [field(0)] * (len(factors[i][0]) - 1))[k] = v
    tr = lambda f: [c for c in f] if not f or f[-1] != 0 else tr(f[:-1])
    return tr(q), {key: tr(v) for key, v in parts.items()}


def fill(parts, factors):
    return {(i, j): parts.get((i, j), []) for i, (_, e) in enumerate(factors) for j in range(1, e + 1)}


def test_worked_example():
    # (x^5 + 2) / ((x - 1)^2 (x^2 + 1))
    a = [Fr(2), 0, 0, 0, 0, Fr(1)]
    factors = [([Fr(-1), Fr(1)], 2), ([Fr(1), 0, Fr(1)], 1)]
    q, parts = partial_fractions(a, factors)
    assert q == [Fr(2), Fr(1)]
    assert parts[(0, 2)] == [Fr(3, 2)]
    assert parts[(0, 1)] == [Fr(1)]
    assert parts[(1, 1)] == [Fr(-1, 2), Fr(1)]


def test_edges():
    lin = [Fr(-3), Fr(1)]
    assert partial_fractions([], [(lin, 2)]) == ([], {(0, 2): [], (0, 1): []})
    assert partial_fractions([Fr(5)], [(lin, 1)]) == ([], {(0, 1): [Fr(5)]})
    assert partial_fractions([Fr(1), Fr(2)], []) == ([Fr(1), Fr(2)], {})
    # numerator a multiple of the denominator: only a polynomial part
    q, parts = partial_fractions(mul([Fr(1), Fr(1)], power(lin, 3)), [(lin, 3)])
    assert q == [Fr(1), Fr(1)] and all(v == [] for v in parts.values())
    with pytest.raises(ValueError):
        partial_fractions([Fr(1)], [([Fr(2)], 1)])
    with pytest.raises(ValueError):
        partial_fractions([Fr(1)], [([Fr(-1), Fr(1)], 1), ([Fr(-2), Fr(1), Fr(1)], 1)])  # x - 1 divides x^2 + x - 2


def random_factors(rng, field, roots):
    rs = rng.sample(roots, rng.randint(1, 4))
    factors, k = [], 0
    while k < len(rs):
        g = rng.randint(1, 2)
        bi = [field(1)]
        for c in rs[k : k + g]:
            bi = mul(bi, [field(-c), field(1)])
        factors.append((bi, rng.randint(1, 3)))
        k += g
    if field is Fr and rng.random() < 0.5:
        factors.append(([Fr(rng.randint(1, 5)), Fr(0), Fr(1)], rng.randint(1, 2)))  # x^2 + c, no rational root
    return factors


@pytest.mark.parametrize("field", [Fr, GF])
def test_random_against_linear_algebra_and_points(field):
    rng = random.Random(1873 if field is Fr else 77)
    roots = list(range(-6, 0)) + list(range(1, 7)) if field is Fr else list(range(7))
    for _ in range(500):
        factors = random_factors(rng, field, roots)
        b = [field(1)]
        for bi, ei in factors:
            b = mul(b, power(bi, ei))
        a = [field(rng.randint(-9, 9)) for _ in range(rng.randint(0, len(b) + 2))]
        while a and a[-1] == 0:
            a.pop()
        q, parts = partial_fractions(a, factors)
        for (i, j), aij in parts.items():
            assert len(aij) < len(factors[i][0])
        bq, bparts = brute(a, factors, field)
        assert q == bq
        assert fill(parts, factors) == fill(bparts, factors)
        pts = range(-12, 13) if field is Fr else range(7)
        for x0 in pts:
            x = field(x0)
            if ev(b, x) == 0:
                continue
            rhs = ev(q, x)
            for (i, j), aij in parts.items():
                rhs = rhs + ev(aij, x) / ev(power(factors[i][0], j), x)
            assert rhs == ev(a, x) / ev(b, x)
