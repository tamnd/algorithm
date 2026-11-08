# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-grid-quadrature/. The authors are listed in prov/W6G1K4.jsonl.

import math
import random
from fractions import Fraction
from itertools import product

import pytest

from sparse_grid_quadrature import (
    clenshaw_curtis_rule,
    multi_indices,
    newton_cotes_rule,
    points_at_level,
    smolyak_quadrature,
    sparse_grid,
)


def monomials(s, deg):
    return [k for k in product(range(deg + 1), repeat=s) if sum(k) <= deg]


def box_moment(k, a, b):
    v = Fraction(1)
    for kj, lo, hi in zip(k, a, b):
        v *= (Fraction(hi) ** (kj + 1) - Fraction(lo) ** (kj + 1)) / (kj + 1)
    return v


def mono(k):
    def f(x):
        v = 1
        for xj, kj in zip(x, k):
            v = v * xj ** kj
        return v
    return f


def test_multi_indices_match_brute_force():
    for s in (1, 2, 3, 4):
        for lo, hi in ((s, s), (s, s + 3), (s + 1, s + 4), (s + 2, s + 2)):
            got = sorted(multi_indices(s, lo, hi))
            want = sorted(i for i in product(range(1, hi + 1), repeat=s) if lo <= sum(i) <= hi)
            assert got == want
    assert list(multi_indices(3, 1, 2)) == []


def test_one_dimensional_rules():
    for i in range(1, 7):
        m = points_at_level(i)
        cc = clenshaw_curtis_rule(i)
        assert len(cc) == m and abs(sum(w for _, _, w in cc) - 1) < 1e-15
        assert all(w > 0 for _, _, w in cc)
        for k in range(m + 1):  # exact for degree m (m odd)
            assert abs(sum(w * x ** k for _, x, w in cc) - 1 / (k + 1)) < 1e-14
        if i <= 3:
            assert abs(sum(w * x ** (m + 1) for _, x, w in cc) - 1 / (m + 2)) > 1e-6
        if i <= 5:
            nc = newton_cotes_rule(i)
            for k in range(m + 1):
                assert sum(w * x ** k for _, x, w in nc) == Fraction(1, k + 1)
            assert sum(w * x ** (m + 1) for _, x, w in nc) != Fraction(1, m + 2)
        # nesting: every key of level i - 1 occurs at level i, with the same point
        if i > 1:
            prev = {k: x for k, x, _ in clenshaw_curtis_rule(i - 1)}
            cur = {k: x for k, x, _ in cc}
            assert all(k in cur and cur[k] == x for k, x in prev.items())


def test_point_counts_match_published_tables():
    # numbers of points of the Clenshaw-Curtis sparse grid, levels l = q - s = 0, 1, ...
    table = {
        1: [1, 3, 5, 9, 17],
        2: [1, 5, 13, 29, 65, 145],
        3: [1, 7, 25, 69, 177, 441],
        10: [1, 21, 221, 1581],
    }
    for s, counts in table.items():
        assert [len(sparse_grid(s, s + l)) for l in range(len(counts))] == counts


def test_exact_for_total_degree_2l_plus_1_in_fractions():
    for s in (2, 3):
        for l in range(0, 4):
            deg = 2 * l + 1
            for k in monomials(s, deg):
                v = smolyak_quadrature(mono(k), [0] * s, [1] * s, s + l, newton_cotes_rule)
                assert v == box_moment(k, [0] * s, [1] * s), (s, l, k)


def test_degree_bound_is_attained():
    # x1^2 x2^2 has total degree 4 = 2(q - s) + 2 for s = 2, q = 3
    k = (2, 2)
    v = smolyak_quadrature(mono(k), [0, 0], [1, 1], 3, newton_cotes_rule)
    assert v != Fraction(1, 9)
    # the missing term is -Delta^2(x^2) Delta^2(x^2) = -(1/3 - 1/4)^2
    assert v == Fraction(1, 9) - Fraction(1, 12) ** 2


def test_weights_sum_to_one_and_turn_negative():
    for s in (1, 2, 3, 4):
        for l in range(4):
            g = sparse_grid(s, s + l, newton_cotes_rule)
            assert sum(w for _, _, w in g) == 1
    g = sparse_grid(5, 8)
    assert any(w < 0 for _, _, w in g)
    assert sum(abs(w) for _, _, w in g) > 10


def test_random_polynomials_against_exact_moments():
    rng = random.Random(7)
    for case in range(500):
        s = rng.randint(1, 4)
        l = rng.randint(0, 3)
        deg = 2 * l + 1
        terms = [(Fraction(rng.randint(-9, 9), rng.randint(1, 9)), rng.choice(monomials(s, deg))) for _ in range(rng.randint(1, 4))]
        a = [Fraction(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(s)]
        b = [lo + Fraction(rng.randint(-6, 6), rng.randint(1, 4)) for lo in a]
        exact = sum(c * box_moment(k, a, b) for c, k in terms)

        def f(x, terms=terms):
            return sum(c * mono(k)(x) for c, k in terms)

        if case % 2 == 0:
            assert smolyak_quadrature(f, a, b, s + l, newton_cotes_rule) == exact
        else:
            fa = [float(t) for t in a]
            fb = [float(t) for t in b]
            v = smolyak_quadrature(lambda x: float(f(x)), fa, fb, s + l)
            scale = sum(abs(c) * box_moment(k, [0] * s, [1] * s) for c, k in terms)
            scale *= max([1] + [abs(t) for t in a + b]) ** deg * max([1] + [abs(t) for t in a + b]) ** s
            assert abs(v - float(exact)) <= 1e-12 * float(scale) + 1e-14


def test_dimension_one_is_the_one_dimensional_rule():
    for q in range(1, 6):
        g = sparse_grid(1, q)
        r = clenshaw_curtis_rule(q)
        assert sorted((k[0], x[0], w) for k, x, w in g) == sorted(r)


def test_smooth_integrand_in_five_and_ten_dimensions():
    for s, l, tol in ((5, 3, 1e-10), (10, 3, 1e-10)):
        exact = (s * (math.exp(1 / s) - 1)) ** s
        f = lambda x: math.exp(sum(x) / len(x))
        errs = [abs(smolyak_quadrature(f, [0] * s, [1] * s, s + k) - exact) for k in range(l + 1)]
        assert all(errs[k + 1] < errs[k] / 100 for k in range(l))
        assert errs[-1] < tol
    # 241 sparse points in 5 dimensions against the 3^5 = 243 point product rule
    s = 5
    exact = (s * (math.exp(1 / s) - 1)) ** s
    r = clenshaw_curtis_rule(2)
    prod = 0.0
    for combo in product(r, repeat=s):
        w = 1.0
        for c in combo:
            w *= c[2]
        prod += w * math.exp(sum(c[1] for c in combo) / s)
    sparse = smolyak_quadrature(lambda x: math.exp(sum(x) / 5), [0] * 5, [1] * 5, 8)
    assert len(sparse_grid(5, 8)) == 241
    assert abs(sparse - exact) < abs(prod - exact) / 1000


def test_kink_converges_slowly():
    s = 3
    exact = (1.5 ** 4 - 3 * 0.5 ** 4) / 24
    f = lambda x: max(sum(x) - 1.5, 0.0)
    errs = [abs(smolyak_quadrature(f, [0] * s, [1] * s, s + l) - exact) for l in range(1, 7)]
    assert min(errs) > 1e-4


def test_edges_and_counts():
    calls = [0]

    def f(x):
        calls[0] += 1
        return math.cos(sum(x))

    assert smolyak_quadrature(f, [0.0, 1.0], [1.0, 1.0], 4) == 0 and calls[0] == 0
    v = smolyak_quadrature(f, [0.0, 0.0], [1.0, 2.0], 5)
    assert calls[0] == len(sparse_grid(2, 5)) == 29
    assert abs(smolyak_quadrature(f, [1.0, 0.0], [0.0, 2.0], 5) + v) < 1e-15
    exact = math.cos(1) + math.cos(2) - 1 - math.cos(3)  # integral of cos(x + y) over [0,1] x [0,2]
    assert abs(v - exact) < 1e-6
    with pytest.raises(ValueError):
        smolyak_quadrature(f, [0.0, 0.0], [1.0, math.inf], 3)
    with pytest.raises(ValueError):
        smolyak_quadrature(f, [0.0, 0.0], [1.0, 1.0], 1)
    with pytest.raises(ValueError):
        smolyak_quadrature(f, [0.0], [1.0, 1.0], 3)
