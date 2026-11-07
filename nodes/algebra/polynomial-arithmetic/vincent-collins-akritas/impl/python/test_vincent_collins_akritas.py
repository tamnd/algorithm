# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vincent-collins-akritas/. The authors are listed in prov/S6W6AA.jsonl.
"""Tests for the Vincent-Collins-Akritas method.

Real root isolation needs an ordered field, so the inputs are over Z and
over Q (Fraction); prime fields Z/pZ have no order and are not used. The
oracle is an independent Sturm sequence count in exact rational arithmetic.
"""

from __future__ import annotations

import random
from fractions import Fraction
from math import comb

import pytest

from vincent_collins_akritas import (
    _descartes_test,
    _taylor_shift,
    isolate_real_roots,
    square_free_part,
    vca_isolate,
)

# ------------------------------------------------------------ the oracle


def _trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def _rem(a, b):
    a = [Fraction(x) for x in a]
    while len(a) >= len(b) and a:
        q = a[-1] / b[-1]
        s = len(a) - len(b)
        for i, y in enumerate(b):
            a[s + i] -= q * y
        a = _trim(a)
    return a


def _sturm(f):
    seq = [_trim([Fraction(x) for x in f])]
    d = _trim([i * seq[0][i] for i in range(1, len(seq[0]))])
    if not d:
        return seq
    seq.append(d)
    while True:
        r = _rem(seq[-2], seq[-1])
        if not r:
            return seq
        seq.append([-x for x in r])


def _ev(a, x):
    s = Fraction(0)
    for c in reversed(a):
        s = s * x + c
    return s


def _var(vals):
    v = [x for x in vals if x != 0]
    return sum(1 for i in range(len(v) - 1) if (v[i] > 0) != (v[i + 1] > 0))


def _count(seq, lo, hi):
    """Distinct roots in (lo, hi] by Sturm; lo, hi not multiple roots."""
    return _var([_ev(p, lo) for p in seq]) - _var([_ev(p, hi) for p in seq])


def _total(seq):
    neg = _var([p[-1] * (-1) ** (len(p) - 1) for p in seq])
    pos = _var([p[-1] for p in seq])
    return neg - pos


def _sqfree(f):
    """f / gcd(f, f') over Q, computed with the oracle's own remainders."""
    a = _trim([Fraction(x) for x in f])
    b = _trim([i * a[i] for i in range(1, len(a))])
    g = a
    while b:
        g, b = b, _rem(g, b)
    q = [Fraction(0)] * (len(a) - len(g) + 1)
    r = list(a)
    while len(r) >= len(g):
        c = r[-1] / g[-1]
        s = len(r) - len(g)
        q[s] = c
        for i, y in enumerate(g):
            r[s + i] -= c * y
        r = _trim(r)
    assert not r
    return q


def _check(f, out):
    """The output isolates exactly the distinct real roots of f.

    Endpoints of open intervals may be roots that are reported as exact
    points; the Sturm count on (lo, hi] is corrected for that.
    """
    h = _sqfree(f)
    seq = _sturm(h)
    assert len(out) == _total(seq)
    for lo, hi in out:
        if lo == hi:
            assert _ev(h, lo) == 0
        else:
            assert lo < hi
            inside = _count(seq, lo, hi) - (1 if _ev(h, hi) == 0 else 0)
            assert inside == 1
    for (lo1, hi1), (lo2, hi2) in zip(out, out[1:]):
        assert hi1 <= lo2
        if lo1 == hi1 and lo2 == hi2:
            assert lo1 < lo2
    for lo, hi in out:
        if lo < hi:
            for r in (lo, hi):
                if _ev(h, r) == 0:
                    assert (r, r) in out


def _from_roots(roots):
    """Primitive integer polynomial with the given rational roots."""
    f = [Fraction(1)]
    for r in roots:
        g = [Fraction(0)] * (len(f) + 1)
        for i, x in enumerate(f):
            g[i + 1] += x
            g[i] -= r * x
        f = g
    den = 1
    for x in f:
        den = den * x.denominator
    return [int(x * den) for x in f]


def _contains(out, r):
    return sum(1 for lo, hi in out if (lo == hi == r) or lo < r < hi)


# ------------------------------------------------------------ helpers


def test_taylor_shift_against_binomial_expansion():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(0, 9)
        a = [rng.randint(-20, 20) for _ in range(n + 1)]
        c = rng.choice([-3, -1, 1, 2, 5])
        ref = [0] * (n + 1)
        for i, x in enumerate(a):
            for j in range(i + 1):
                ref[j] += x * comb(i, j) * c ** (i - j)
        assert _taylor_shift(a, c) == ref


def test_descartes_test_is_an_upper_bound_with_parity():
    rng = random.Random(12)
    for _ in range(300):
        roots = [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(rng.randint(1, 5))]
        roots = sorted(set(roots))
        a = _from_roots(roots)
        inside = sum(1 for r in roots if 0 < r < 1)
        v = _descartes_test(a)
        assert v >= inside and (v - inside) % 2 == 0


# ------------------------------------------------------------ worked examples


def test_worked_example_cubic():
    out = vca_isolate([1, -3, 0, 1])
    assert out == [
        (Fraction(-4), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(2)),
    ]


def test_lagrange_cubic_close_roots():
    out = vca_isolate([7, -7, 0, 1])
    assert out == [
        (Fraction(-8), Fraction(0)),
        (Fraction(1), Fraction(3, 2)),
        (Fraction(3, 2), Fraction(2)),
    ]


def test_exact_midpoint_roots():
    out = vca_isolate([0, -1, 0, 1])
    assert (Fraction(0), Fraction(0)) in out
    _check([0, -1, 0, 1], out)


# ------------------------------------------------------------ edge cases


def test_constants_and_zero():
    assert vca_isolate([5]) == []
    assert vca_isolate([-3, 0, 0]) == []
    with pytest.raises(ValueError):
        vca_isolate([])
    with pytest.raises(ValueError):
        vca_isolate([0, 0])
    with pytest.raises(ValueError):
        isolate_real_roots([])


def test_degree_one_monic_and_non_monic():
    for f in ([3, 2], [-1, 1], [0, 1], [0, -7], [5, 3], [-6, 4, 0, 0]):
        out = vca_isolate(f)
        _check(f, out)
        assert len(out) == 1


def test_no_real_roots():
    assert vca_isolate([1, 0, 1]) == []
    assert vca_isolate([1, 0, 0, 0, 1]) == []
    assert vca_isolate([2, 1, 1]) == []


def test_non_square_free_rejected_and_reduced():
    f = [0, 0, -1, 1]  # x^2 (x - 1)
    with pytest.raises(ValueError):
        vca_isolate(f)
    out = isolate_real_roots(f)
    _check(f, out)
    assert len(out) == 2
    g = _from_roots([Fraction(1, 2)] * 3 + [Fraction(-2)] * 2 + [Fraction(5)])
    out = isolate_real_roots(g)
    _check(g, out)
    assert len(out) == 3


def test_fraction_coefficients():
    f = [Fraction(-1, 3), Fraction(0), Fraction(3, 4)]  # roots +- 2/3
    out = isolate_real_roots(f)
    assert len(out) == 2
    assert _contains(out, Fraction(2, 3)) == 1
    assert _contains(out, Fraction(-2, 3)) == 1


def test_square_free_part():
    assert square_free_part([0, 0, -1, 1]) == [0, -1, 1]
    assert square_free_part([4, 4, 1]) == [2, 1]
    assert square_free_part([7]) == [1]


# ------------------------------------------------------------ hard inputs


def test_wilkinson_roots_one_to_twelve():
    roots = [Fraction(i) for i in range(1, 13)]
    f = _from_roots(roots)
    out = vca_isolate(f)
    _check(f, out)
    for r in roots:
        assert _contains(out, r) == 1


def test_mignotte_polynomial_close_roots():
    # x^7 - 2 (10 x - 1)^2 has two roots very close to 1/10.
    f = [0] * 8
    f[7] = 1
    for i, c in enumerate([1, -20, 100]):
        f[i] -= 2 * c
    out = vca_isolate(f)
    _check(f, out)
    assert out == [
        (Fraction(819, 8192), Fraction(3277, 32768)),
        (Fraction(3277, 32768), Fraction(1639, 16384)),
        (Fraction(2), Fraction(4)),
    ]


def test_chebyshev_t12_all_roots_real():
    t = [[1], [0, 1]]
    for _ in range(11):
        a, b = t[-2], t[-1]
        c = [0] + [2 * x for x in b]
        for i, x in enumerate(a):
            c[i] -= x
        t.append(c)
    f = t[12]
    out = vca_isolate(f)
    _check(f, out)
    assert len(out) == 12


def test_very_different_degrees_in_one_input():
    f = [-2] + [0] * 29 + [1]  # x^30 - 2
    out = vca_isolate(f)
    _check(f, out)
    assert len(out) == 2


def test_rational_roots_with_large_denominators():
    roots = [Fraction(1, 97), Fraction(2, 97), Fraction(-50, 3), Fraction(13, 7)]
    f = _from_roots(roots)
    out = vca_isolate(f)
    _check(f, out)
    for r in roots:
        assert _contains(out, r) == 1


# ------------------------------------------------------------ random oracle


def test_random_small_polynomials_against_sturm():
    rng = random.Random(2024)
    checked = 0
    for _ in range(700):
        n = rng.randint(1, 6)
        f = [rng.randint(-6, 6) for _ in range(n)] + [rng.choice([-3, -2, -1, 1, 2, 3])]
        out = isolate_real_roots(f)
        _check(f, out)
        checked += 1
    assert checked >= 500


def test_random_products_of_known_roots():
    rng = random.Random(7)
    for _ in range(150):
        roots = sorted({Fraction(rng.randint(-30, 30), rng.randint(1, 6)) for _ in range(rng.randint(1, 6))})
        extra = rng.choice([[], [1, 0, 1], [-2, 0, 1], [3, 1, 1]])
        f = _from_roots(roots)
        if extra:
            g = [0] * (len(f) + len(extra) - 1)
            for i, x in enumerate(f):
                for j, y in enumerate(extra):
                    g[i + j] += x * y
            f = g
        out = isolate_real_roots(f)
        _check(f, out)
        for r in roots:
            assert _contains(out, r) == 1
