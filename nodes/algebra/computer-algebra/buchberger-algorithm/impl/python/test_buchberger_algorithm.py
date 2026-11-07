# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buchberger-algorithm/. The authors are listed in prov/EG385B.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from buchberger_algorithm import buchberger, normal_form, order_key, reduced_basis, s_polynomial

P = 101


class Fp:
    """An element of Z/101Z, for the tests."""

    __slots__ = ("v",)

    def __init__(self, v: int) -> None:
        self.v = v % P

    @staticmethod
    def _c(o: object) -> int:
        return o.v if isinstance(o, Fp) else int(o)  # type: ignore[arg-type]

    def __add__(self, o: object) -> "Fp":
        return Fp(self.v + self._c(o))

    __radd__ = __add__

    def __sub__(self, o: object) -> "Fp":
        return Fp(self.v - self._c(o))

    def __rsub__(self, o: object) -> "Fp":
        return Fp(self._c(o) - self.v)

    def __mul__(self, o: object) -> "Fp":
        return Fp(self.v * self._c(o))

    __rmul__ = __mul__

    def __neg__(self) -> "Fp":
        return Fp(-self.v)

    def __truediv__(self, o: object) -> "Fp":
        return Fp(self.v * pow(self._c(o), P - 2, P))

    def __rtruediv__(self, o: object) -> "Fp":
        return Fp(self._c(o) * pow(self.v, P - 2, P))

    def __eq__(self, o: object) -> bool:
        return self.v == self._c(o) % P

    def __hash__(self) -> int:
        return self.v


# ---------------------------------------------------------------- independent reference code


def ref_reduce(f, G, key):
    """Remainder by G, written independently of the module: sorted term lists."""
    terms = {m: c for m, c in f.items() if c != 0}
    rem = {}
    gl = []
    for g in G:
        lm = max(g, key=key)
        gl.append((lm, g[lm], g))
    while terms:
        m = max(terms, key=key)
        c = terms[m]
        hit = None
        for lm, lc, g in gl:
            if all(x >= y for x, y in zip(m, lm)):
                hit = (lm, lc, g)
                break
        if hit is None:
            rem[m] = c
            del terms[m]
            continue
        lm, lc, g = hit
        q = tuple(x - y for x, y in zip(m, lm))
        f2 = c / lc
        for e, d in g.items():
            mm = tuple(x + y for x, y in zip(e, q))
            terms[mm] = terms.get(mm, 0) - f2 * d
            if terms[mm] == 0:
                del terms[mm]
    return rem


def monomials_of_degree(n, d):
    for c in itertools.combinations_with_replacement(range(n), d):
        e = [0] * n
        for i in c:
            e[i] += 1
        yield tuple(e)


def in_span(vectors, target, one):
    """Is target in the span of vectors (dicts monomial -> coeff)? Gaussian elimination."""
    rows = []  # list of (pivot, dict)
    for v in vectors:
        v = {m: c for m, c in v.items() if c != 0}
        for piv, r in rows:
            if piv in v:
                c = v[piv] / r[piv]
                for m, d in r.items():
                    v[m] = v.get(m, 0) - c * d
                    if v[m] == 0:
                        del v[m]
        if v:
            rows.append((max(v), v))
    t = {m: c for m, c in target.items() if c != 0}
    for piv, r in rows:
        if piv in t:
            c = t[piv] / r[piv]
            for m, d in r.items():
                t[m] = t.get(m, 0) - c * d
                if t[m] == 0:
                    del t[m]
    return not t


def mono_mul(f, m):
    return {tuple(a + b for a, b in zip(e, m)): c for e, c in f.items()}


def poly_mul(f, g):
    h = {}
    for a, c in f.items():
        for b, d in g.items():
            m = tuple(x + y for x, y in zip(a, b))
            h[m] = h.get(m, 0) + c * d
            if h[m] == 0:
                del h[m]
    return h


def poly_add(f, g):
    h = dict(f)
    for m, c in g.items():
        h[m] = h.get(m, 0) + c
        if h[m] == 0:
            del h[m]
    return h


def rand_poly(rng, n, maxdeg, nterms, field):
    f = {}
    for _ in range(nterms):
        e = tuple(rng.randint(0, maxdeg) for _ in range(n))
        while sum(e) > maxdeg:
            e = tuple(rng.randint(0, maxdeg) for _ in range(n))
        c = field(rng.randint(-5, 5))
        if c != 0:
            f[e] = f.get(e, 0) + c
            if f[e] == 0:
                del f[e]
    return f


def rand_homog(rng, n, d, nterms, field):
    mons = list(monomials_of_degree(n, d))
    f = {}
    for _ in range(nterms):
        c = field(rng.randint(-4, 4))
        if c != 0:
            m = rng.choice(mons)
            f[m] = f.get(m, 0) + c
            if f[m] == 0:
                del f[m]
    return f


def check_groebner(F, G, order):
    key = order_key(order)
    for g in G:
        assert g and all(c != 0 for c in g.values())
    for i in range(len(G)):
        for j in range(i + 1, len(G)):
            assert ref_reduce(s_polynomial(G[i], G[j], order), G, key) == {}
    for f in F:
        if f:
            assert ref_reduce(f, G, key) == {}


Q = Fraction
X2 = {(3, 0): Q(1), (1, 1): Q(-2)}  # x^3 - 2xy
Y2 = {(2, 1): Q(1), (0, 2): Q(-2), (1, 0): Q(1)}  # x^2 y - 2y^2 + x


def test_worked_example_grlex():
    G = buchberger([X2, Y2], "grlex", product_criterion=False)
    assert len(G) == 5
    check_groebner([X2, Y2], G, "grlex")
    R = reduced_basis(G, "grlex")
    assert R == [{(2, 0): Q(1)}, {(1, 1): Q(1)}, {(0, 2): Q(1), (1, 0): Q(-1, 2)}]


def test_worked_example_lex():
    R = reduced_basis(buchberger([X2, Y2], "lex"), "lex")
    assert R == [{(1, 0): Q(1), (0, 2): Q(-2)}, {(0, 3): Q(1)}]


def test_membership_examples():
    G = reduced_basis(buchberger([X2, Y2], "grlex"), "grlex")
    assert normal_form({(0, 3): Q(1)}, G, "grlex") == {}
    assert normal_form({(1, 0): Q(1), (0, 1): Q(1)}, G, "grlex") == {(1, 0): Q(1), (0, 1): Q(1)}
    assert normal_form({(3, 1): Q(1), (0, 2): Q(1)}, G, "grlex") == {(1, 0): Q(1, 2)}


def test_empty_and_zero():
    assert buchberger([], "lex") == []
    assert buchberger([{}], "grevlex") == []
    assert reduced_basis([], "lex") == []


def test_constant_and_unit_ideal():
    assert reduced_basis(buchberger([{(0, 0): Q(7)}], "lex"), "lex") == [{(0, 0): Q(1)}]
    F = [{(1, 0): Q(1)}, {(1, 0): Q(1), (0, 0): Q(-1)}]  # x and x - 1
    assert reduced_basis(buchberger(F, "grlex"), "grlex") == [{(0, 0): Q(1)}]
    F = [{(1, 1): Q(1), (0, 0): Q(-1)}, {(1, 0): Q(1)}]  # xy - 1 and x
    assert reduced_basis(buchberger(F, "grevlex"), "grevlex") == [{(0, 0): Q(1)}]


def test_single_generator():
    f = {(2, 1): Q(3), (0, 1): Q(1), (0, 0): Q(-2)}
    for order in ("lex", "grlex", "grevlex"):
        G = buchberger([f], order)
        assert G == [f]
        R = reduced_basis(G, order)
        lm = max(f, key=order_key(order))
        assert R == [{m: c / f[lm] for m, c in f.items()}]


def test_cyclic_three_needs_many_steps():
    x, y, z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    one = (0, 0, 0)
    F = [
        {x: Q(1), y: Q(1), z: Q(1)},
        {(1, 1, 0): Q(1), (0, 1, 1): Q(1), (1, 0, 1): Q(1)},
        {(1, 1, 1): Q(1), one: Q(-1)},
    ]
    for order in ("lex", "grevlex"):
        G = buchberger(F, order)
        check_groebner(F, G, order)
    R = reduced_basis(buchberger(F, "lex"), "lex")
    assert R == [{x: Q(1), y: Q(1), z: Q(1)}, {(0, 2, 0): Q(1), (0, 1, 1): Q(1), (0, 0, 2): Q(1)}, {(0, 0, 3): Q(1), one: Q(-1)}]


def univariate_gcd(a, b):
    """Monic gcd of two dense lists over a field, by Euclid (oracle)."""
    def strip(u):
        while u and u[-1] == 0:
            u.pop()
        return u
    a, b = strip(list(a)), strip(list(b))
    while b:
        r = list(a)
        while len(r) >= len(b) and r:
            c = r[-1] / b[-1]
            s = len(r) - len(b)
            for i, v in enumerate(b):
                r[s + i] = r[s + i] - c * v
            r = strip(r)
        a, b = b, r
    return [v / a[-1] for v in a] if a else []


def test_one_variable_matches_gcd():
    rng = random.Random(11)
    for _ in range(150):
        polys = [[Q(rng.randint(-3, 3)) for _ in range(rng.randint(1, 5))] for _ in range(rng.randint(1, 3))]
        F = [{(i,): c for i, c in enumerate(p) if c != 0} for p in polys]
        g = []
        for p in polys:
            g = univariate_gcd(g, p) if g else univariate_gcd(p, [])
        R = reduced_basis(buchberger(F, "lex"), "lex")
        if not g:
            assert R == []
        else:
            assert R == [{(i,): c for i, c in enumerate(g) if c != 0}]


@pytest.mark.parametrize("order", ["lex", "grlex", "grevlex"])
def test_random_mod_p(order):
    rng = random.Random({"lex": 1, "grlex": 2, "grevlex": 3}[order])
    for _ in range(180):
        n = rng.choice([2, 2, 3])
        F = [rand_poly(rng, n, 3, rng.randint(1, 3), Fp) for _ in range(rng.randint(1, 3))]
        G = buchberger(F, order)
        check_groebner(F, G, order)
        G2 = buchberger(list(reversed(F)), order, product_criterion=False)
        assert reduced_basis(G, order) == reduced_basis(G2, order)


def test_random_rationals():
    rng = random.Random(5)
    for _ in range(60):
        F = [rand_poly(rng, 2, 2, rng.randint(1, 3), Q) for _ in range(rng.randint(1, 3))]
        for order in ("lex", "grevlex"):
            G = buchberger(F, order)
            check_groebner(F, G, order)
            key = order_key(order)
            # elements built as combinations of F reduce to zero
            p = {}
            for f in F:
                p = poly_add(p, poly_mul(f, rand_poly(rng, 2, 2, 2, Q)))
            assert ref_reduce(p, G, key) == {}


def test_homogeneous_membership_agrees_with_linear_algebra():
    rng = random.Random(9)
    for _ in range(70):
        n = 3
        F = [rand_homog(rng, n, 2, rng.randint(2, 4), Fp) for _ in range(rng.randint(1, 3))]
        F = [f for f in F if f]
        if not F:
            continue
        G = buchberger(F, "grevlex")
        for D in (2, 3):
            span = [mono_mul(f, m) for f in F for m in monomials_of_degree(n, D - 2)]
            for t in range(4):
                if t % 2 == 0:
                    p = rand_homog(rng, n, D, 3, Fp)
                else:
                    p = {}
                    for v in span:
                        p = poly_add(p, {m: c * Fp(rng.randint(0, 3)) for m, c in v.items()})
                member = in_span(span, p, Fp(1))
                assert (normal_form(p, G, "grevlex") == {}) == member


def test_nonhomogeneous_linear_algebra_is_sound():
    rng = random.Random(21)
    for _ in range(60):
        F = [rand_poly(rng, 2, 2, 3, Fp) for _ in range(2)]
        F = [f for f in F if f]
        if not F:
            continue
        G = buchberger(F, "grlex")
        span = [mono_mul(f, m) for f in F for d in range(3) for m in monomials_of_degree(2, d)]
        for _ in range(4):
            p = rand_poly(rng, 2, 3, 3, Fp)
            if in_span(span, p, Fp(1)):
                assert normal_form(p, G, "grlex") == {}
