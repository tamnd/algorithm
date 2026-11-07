# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-polynomial/. The authors are listed in prov/RVZNCP.jsonl.

import random
from fractions import Fraction
from typing import Any, Dict, Tuple

import pytest

from dense_polynomial import DensePoly, from_dict, zero_of

# Oracle: distributed polynomials as dicts {exponent tuple: nonzero coefficient}.
D = Dict[Tuple[int, ...], Any]


def d_clean(a: D) -> D:
    return {k: v for k, v in a.items() if v != 0}


def d_add(a: D, b: D, s: int = 1) -> D:
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + s * v
    return d_clean(r)


def d_mul(a: D, b: D) -> D:
    r: D = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(x + y for x, y in zip(k1, k2))
            r[k] = r.get(k, 0) + v1 * v2
    return d_clean(r)


def d_main_deg(a: D) -> int:
    return max((k[-1] for k in a), default=-1)


def d_lc(a: D) -> D:
    """Leading coefficient in the last (main) variable, as a dict with exponent 0 there."""
    m = d_main_deg(a)
    return {k[:-1] + (0,): v for k, v in a.items() if k[-1] == m}


def d_subs_main(a: D, u: D) -> D:
    """Substitute u (free of the main variable) for the main variable."""
    n = len(next(iter(a))) if a else 0
    r: D = {}
    for k, v in a.items():
        term: D = {k[:-1] + (0,): v}
        for _ in range(k[-1]):
            term = d_mul(term, u)
        r = d_add(r, term)
    return r


def rand_dict(rng: random.Random, n: int, deg: int, terms: int, frac: bool) -> D:
    d: D = {}
    for _ in range(terms):
        k = tuple(rng.randint(0, deg) for _ in range(n))
        v = Fraction(rng.randint(-5, 5), rng.randint(1, 3)) if frac else rng.randint(-5, 5)
        d[k] = d.get(k, 0) + v
    return d_clean(d)


def test_worked_examples() -> None:
    # (x^2 + 1) y^2 + 3x in Q[x][y]: outer list indexed by the power of y
    f = from_dict({(2, 2): Fraction(1), (0, 2): Fraction(1), (1, 0): Fraction(3)}, 2, Fraction(0))
    assert [p.c for p in f.c] == [[0, 3], [], [1, 0, 1]]
    f.check_invariant()
    # pseudo-division over Z: a = x^3 + 2x + 1, b = 2x + 1
    a = DensePoly([1, 2, 0, 1], 0)
    b = DensePoly([1, 2], 0)
    q, r = a.pseudo_divmod(b)
    assert q.c == [9, -2, 4] and r.c == [-1]
    assert (q * b + r).c == a.scale(8).c
    # schoolbook product and Horner
    assert (DensePoly([1, 1], 0) * DensePoly([-1, 1], 0)).c == [-1, 0, 1]
    assert DensePoly([1, 2, 3], 0).evaluate(2) == 17


def test_edge_cases() -> None:
    z = DensePoly([], 0)
    assert z.degree() == -1 and z.is_zero() and z == 0
    assert DensePoly([0, 0, 0], 0).c == []
    assert (z * DensePoly([1, 2], 0)).c == []
    assert (DensePoly([1, 2], 0) - DensePoly([1, 2], 0)).c == []
    assert DensePoly([5], 0).derivative().c == []
    assert z.evaluate(3) == 0
    c = DensePoly([7], 0)
    q, r = DensePoly([1, 2, 3], 0).pseudo_divmod(c)  # 7^3 a = q * 7
    assert q.c == [49, 98, 147] and r.c == []
    q, r = DensePoly([4], 0).pseudo_divmod(DensePoly([1, 1], 0))  # deg a < deg b
    assert q.c == [] and r.c == [4]
    with pytest.raises(ZeroDivisionError):
        c.pseudo_divmod(z)
    zz = zero_of(3, Fraction(0))
    assert zz.is_zero() and zz.to_dict() == {}
    zz.check_invariant()
    # zero divisors are not an issue for Z, but cancellation at inner levels is
    p = from_dict({(1, 1): 1, (0, 1): 1}, 2, 0)  # (x + 1) y
    m = from_dict({(1, 1): -1, (0, 1): -1, (0, 0): 2}, 2, 0)
    s = p + m
    assert s.degree() == 0 and s.to_dict() == {(0, 0): 2}
    s.check_invariant()


@pytest.mark.parametrize("n,frac", [(1, True), (1, False), (2, True), (2, False), (3, False)])
def test_random_against_distributed_oracle(n: int, frac: bool) -> None:
    rng = random.Random(1000 * n + frac)
    base = Fraction(0) if frac else 0
    for _ in range(120):
        da = rand_dict(rng, n, rng.randint(0, 4), rng.randint(0, 7), frac)
        db = rand_dict(rng, n, rng.randint(0, 3), rng.randint(0, 6), frac)
        a, b = from_dict(da, n, base), from_dict(db, n, base)
        a.check_invariant()
        assert a.to_dict() == da
        assert (a + b).to_dict() == d_add(da, db)
        assert (a - b).to_dict() == d_add(da, db, -1)
        ab = a * b
        ab.check_invariant()
        assert ab.to_dict() == d_mul(da, db)
        assert a.degree() == d_main_deg(da)
        # derivative in the main variable
        dd = {k[:-1] + (k[-1] - 1,): k[-1] * v for k, v in da.items() if k[-1] > 0}
        assert a.derivative().to_dict() == d_clean(dd)
        # evaluation of the main variable at a polynomial in the other variables
        du = rand_dict(rng, n, 2, 3, frac)
        du = {k[:-1] + (0,): v for k, v in du.items()}
        du = d_clean({k: sum(v for k2, v in du.items() if k2 == k) for k in du})
        u = from_dict({k[:-1]: v for k, v in du.items()}, n - 1, base)
        val = a.evaluate(u)
        got = val.to_dict() if isinstance(val, DensePoly) else ({(): val} if val != 0 else {})
        want = {k[:-1]: v for k, v in d_subs_main(da, du).items()}
        assert got == want
        # pseudo-division: lc(b)^(m - n + 1) a = q b + r, deg r < deg b
        if db:
            q, r = a.pseudo_divmod(b)
            q.check_invariant()
            r.check_invariant()
            e = max(d_main_deg(da) - d_main_deg(db) + 1, 0)
            lhs = da
            for _ in range(e):
                lhs = d_mul(lhs, d_lc(db))
            assert d_add(d_mul(q.to_dict(), db), r.to_dict()) == lhs
            assert r.degree() < b.degree()


def test_pseudo_division_matches_field_division() -> None:
    rng = random.Random(7)
    for _ in range(200):
        a = DensePoly([Fraction(rng.randint(-9, 9)) for _ in range(rng.randint(0, 9))], Fraction(0))
        b = DensePoly([Fraction(rng.randint(-9, 9)) for _ in range(rng.randint(1, 5))], Fraction(0))
        if b.is_zero():
            continue
        q, r = a.pseudo_divmod(b)
        e = max(a.degree() - b.degree() + 1, 0)
        f = b.lc() ** e
        q1, r1 = q.scale(1 / f), r.scale(1 / f)
        assert (q1 * b + r1).c == a.c and r1.degree() < b.degree()


def test_large_dense_product() -> None:
    rng = random.Random(3)
    a = DensePoly([rng.randint(-3, 3) for _ in range(300)] + [1], 0)
    b = DensePoly([rng.randint(-3, 3) for _ in range(200)] + [1], 0)
    p = a * b
    assert p.degree() == 500
    for x in (-2, -1, 0, 1, 2, 3):
        assert p.evaluate(x) == a.evaluate(x) * b.evaluate(x)
