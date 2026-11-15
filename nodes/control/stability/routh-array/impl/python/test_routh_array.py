# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/routh-array/. The authors are listed in prov/43YJD3.jsonl.

import random
from fractions import Fraction

import ctlmat as cm
from routh_array import EpsFrac, hurwitz_determinants, is_hurwitz, rhp_count, routh_array

# Root counts from floating point roots. A root with |Re| below AXIS is
# taken to lie on the imaginary axis. polyroots is accurate to about 1e-8
# for double roots and 1e-5 for triple roots, so AXIS = 1e-3 is safe for the
# small integer polynomials used here.
AXIS = 1e-3


def real_parts(c):
    return [z.real for z in cm.polyroots(c)]


def rhp_true(c):
    return sum(1 for x in real_parts(c) if x > AXIS)


def random_poly(rng, lo=-3, hi=3, max_degree=6):
    n = rng.randint(1, max_degree)
    c = [rng.randint(lo, hi) for _ in range(n + 1)]
    while c[0] == 0:
        c[0] = rng.randint(lo, hi)
    return c


def test_check_value():
    r = routh_array([1, 1, 2, 8])
    assert r.first_column == [1, 1, -6, 8]
    assert r.regular and r.sign_changes == 2
    assert rhp_count([1, 1, 2, 8]) == 2 == rhp_true([1, 1, 2, 8])
    assert not is_hurwitz([1, 1, 2, 8])
    assert r.table() == [[1, 2], [1, 8], [-6], [8]]


def test_row_lengths_and_leading_zeros():
    for n in range(0, 8):
        c = [1] + list(range(1, n + 1))
        r = routh_array(c)
        assert len(r.rows) == n + 1
        assert [len(row) for row in r.rows] == [(n - i) // 2 + 1 for i in range(n + 1)]
    assert routh_array([0, 0, 1, 1, 2, 8]).first_column == [1, 1, -6, 8]


def test_zero_polynomial_raises():
    for c in ([0], [0, 0, 0], []):
        try:
            routh_array(c)
        except ValueError:
            pass
        else:
            raise AssertionError("no ValueError for %r" % (c,))


def test_constant_and_degree_one():
    assert routh_array([5]).sign_changes == 0 and is_hurwitz([5])
    assert is_hurwitz([2, 3]) and not is_hurwitz([2, -3]) and rhp_count([2, -3]) == 1


def test_scaling_does_not_change_the_count():
    rng = random.Random(7)
    for _ in range(200):
        c = random_poly(rng)
        k = rhp_count(c)
        assert rhp_count([-x for x in c]) == k
        assert rhp_count([Fraction(3, 2) * x for x in c]) == k


def test_float_and_fraction_input_are_exact():
    r = routh_array([1.0, 0.5, 0.75, 0.125])
    assert r.regular
    assert r.first_column == [1, Fraction(1, 2), Fraction(1, 2), Fraction(1, 8)]
    assert all(isinstance(x, Fraction) for x in r.first_column)
    r2 = routh_array([Fraction(1), Fraction(1, 2), Fraction(3, 4), Fraction(1, 8)])
    assert r.first_column == r2.first_column


def test_gain_range_third_order():
    # s^3 + 3 s^2 + 2 s + K is Hurwitz if and only if 0 < K < 6.
    for k2 in range(-4, 17):
        K = Fraction(k2, 2)
        assert is_hurwitz([1, 3, 2, K]) == (0 < K < 6)
    r = routh_array([1, 3, 2, 6])
    assert r.events == [("zero_row", 2, [3, 0, 6])]
    assert r.first_column == [1, 3, 6, 6]
    assert r.sign_changes == 0 and not is_hurwitz([1, 3, 2, 6])
    roots = cm.polyroots([1, 3, 2, 6])
    assert abs(roots[0] + 3) < 1e-9
    assert all(abs(z.real) < 1e-9 and abs(abs(z.imag) - 2 ** 0.5) < 1e-9 for z in roots[1:])


def test_epsilon_example():
    c = [1, 2, 2, 4, 11, 10]
    r = routh_array(c)
    assert r.events == [("epsilon", 2)]
    assert r.signs == [1, 1, 1, -1, 1, 1]
    assert r.sign_changes == 2 == rhp_true(c)
    # Row s^2 starts with (4 eps - 12) / eps.
    e = r.rows[3][0]
    assert isinstance(e, EpsFrac) and e.num == [-12, 4] and e.den == [0, 1]


def test_more_examples_from_the_page():
    r = routh_array([1, 10, 35, 50, 24])
    assert r.first_column == [1, 10, 30, 42, 24] and is_hurwitz([1, 10, 35, 50, 24])
    r = routh_array([1, 2, 3, 4, 5])
    assert r.first_column == [1, 2, 1, -6, 5] and r.sign_changes == 2 == rhp_true([1, 2, 3, 4, 5])


def test_hurwitz_determinants_are_products_of_the_first_column():
    assert hurwitz_determinants([1, 1, 2, 8]) == [1, -6, -48]
    assert hurwitz_determinants([1, 10, 35, 50, 24]) == [10, 300, 12600, 302400]
    rng = random.Random(11)
    checked = 0
    for _ in range(400):
        c = random_poly(rng, -5, 5)
        r = routh_array(c)
        if not r.regular:
            continue
        col = r.first_column[1:]
        prod, want = Fraction(1), []
        for x in col:
            prod *= x
            want.append(prod)
        assert hurwitz_determinants(c) == want
        checked += 1
    assert checked > 200


def test_random_polynomials_against_roots():
    # The verdict and the count agree with the roots when no root is near
    # the imaginary axis. Polynomials with a root within 1e-6 of the axis
    # are skipped, as the area rules ask.
    rng = random.Random(20261115)
    used = eps_used = 0
    for _ in range(1500):
        c = random_poly(rng)
        re = real_parts(c)
        if min(abs(x) for x in re) < 1e-6:
            continue
        r = routh_array(c)
        assert r.sign_changes == sum(1 for x in re if x > 0), c
        assert is_hurwitz(c) == all(x < 0 for x in re), c
        if is_hurwitz(c):
            assert all(x * c[0] > 0 for x in c), c
        used += 1
        eps_used += r.used_epsilon
    assert used > 1000 and eps_used > 50


def test_zero_rows_keep_the_count_and_find_the_axis_roots():
    # With zero rows and no epsilon, the count is exact even with roots on
    # the axis, and the axis roots of p are those of the first auxiliary
    # polynomial.
    rng = random.Random(5)
    seen = 0
    for _ in range(3000):
        c = random_poly(rng)
        r = routh_array(c)
        if r.regular or r.used_epsilon:
            continue
        re = real_parts(c)
        if any(AXIS <= abs(x) < 1e-2 for x in re):
            continue
        assert r.sign_changes == rhp_true(c), c
        aux = r.events[0][2]
        on_axis_p = sum(1 for x in re if abs(x) < AXIS)
        on_axis_aux = sum(1 for x in real_parts(aux) if abs(x) < AXIS)
        assert on_axis_p == on_axis_aux, c
        assert not is_hurwitz(c)
        seen += 1
    assert seen > 300


def test_built_zero_rows():
    # (s^2 + 1)(s + 1)(s - 2): one root in the right half plane and two on the axis.
    c = cm.polymul(cm.polymul([1, 0, 1], [1, 1]), [1, -2])
    r = routh_array(c)
    assert any(e[0] == "zero_row" for e in r.events)
    assert r.sign_changes == 1
    # (s^2 - 1)(s^2 + 4): roots symmetric about the origin, one in the right half plane.
    c = cm.polymul([1, 0, -1], [1, 0, 4])
    r = routh_array(c)
    assert r.events[0][0] == "zero_row" and r.sign_changes == 1


def test_epsilon_with_axis_roots_can_overcount():
    # The page warns that the epsilon method is proved only when p has no
    # root on the imaginary axis. Here p = (s^2 + 1)(s^3 + 2 s + 1) has two
    # roots in the right half plane, but the epsilon array shows 4 sign
    # changes. The Hurwitz verdict (False) is still right.
    c = [1, 0, 3, 1, 2, 1]
    assert cm.polymul([1, 0, 1], [1, 0, 2, 1]) == c
    r = routh_array(c)
    assert r.used_epsilon
    assert rhp_true(c) == 2 and r.sign_changes == 4
    assert not is_hurwitz(c)
