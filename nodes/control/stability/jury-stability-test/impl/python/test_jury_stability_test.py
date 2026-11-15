# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jury-stability-test/. The authors are listed in prov/7A0696.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

import ctlmat as cm
from jury_stability_test import is_schur, jury_classic, jury_table, outside_count

# A root with ||z| - 1| below EDGE is taken to be too close to the unit
# circle for a floating point check, and the polynomial is skipped.
EDGE = 1e-6


def moduli(c):
    return [abs(z) for z in cm.polyroots([float(v) for v in c])]


def random_poly(rng, max_degree=6, lo=-4, hi=4):
    n = rng.randint(1, max_degree)
    c = [rng.randint(lo, hi) for _ in range(n + 1)]
    while c[0] == 0:
        c[0] = rng.randint(lo, hi)
    return c


def poly_from_roots(roots):
    c = [F(1)]
    for r in roots:
        c = cm.polymul(c, [F(1), -r])
    return c


def test_check_value_trace():
    # z^2 - z + 0.5 has both roots of modulus 1/sqrt(2).
    r = jury_table([1, -1, F(1, 2)])
    assert r.rows == [[1, -1, F(1, 2)], [F(3, 4), F(-1, 2)], [F(5, 12)]]
    assert r.first == [1, F(3, 4), F(5, 12)]
    assert r.alphas == [F(1, 2), F(-2, 3)]
    assert r.regular and r.schur and r.outside == 0
    assert all(abs(m - 1 / math.sqrt(2)) < 1e-12 for m in moduli([1, -1, 0.5]))


def test_cubic_with_one_root_outside():
    # 4z^3 + 4z^2 - 7z + 2 = 4 (z - 1/2)^2 (z + 2)
    r = jury_table([4, 4, -7, 2])
    assert r.rows == [[4, 4, -7, 2], [3, F(15, 2), -9], [-24, 30], [F(27, 2)]]
    assert r.first == [4, 3, -24, F(27, 2)]
    assert r.outside == 1 and not r.schur
    assert not jury_classic([4, 4, -7, 2])


def test_degree_two_triangle():
    # z^2 + a1 z + a2 is Schur iff |a2| < 1 and |a1| < 1 + a2.
    vals = [F(i, 4) for i in range(-12, 13)]
    for a1 in vals:
        for a2 in vals:
            boundary = abs(a2) == 1 or abs(a1) == 1 + a2
            want = abs(a2) < 1 and abs(a1) < 1 + a2
            r = jury_table([1, a1, a2])
            assert r.schur == want
            assert jury_classic([1, a1, a2]) == want
            if boundary and abs(a2) <= 1:
                assert not r.regular


def test_random_against_roots():
    rng = random.Random(20261115)
    checked = 0
    for _ in range(1500):
        c = random_poly(rng)
        ms = moduli(c)
        if any(abs(m - 1) < EDGE for m in ms):
            continue
        r = jury_table(c)
        out = sum(1 for m in ms if m > 1)
        assert r.schur == (out == 0)
        assert jury_classic(c) == (out == 0)
        if r.regular:
            assert r.outside == out
        checked += 1
    assert checked > 1000


def test_schur_polynomials_are_regular():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 6)
        roots = []
        while len(roots) < n:
            rad = F(rng.randint(0, 99), 100)
            if len(roots) <= n - 2 and rng.random() < 0.5:
                # a conjugate pair, the roots of z^2 - 2 rad x z + rad^2
                # with |x| < 1, both of modulus rad
                x = F(rng.randint(-99, 99), 100)
                roots.append(("pair", rad, x))
                roots.append(None)
            else:
                roots.append(rad if rng.random() < 0.5 else -rad)
        c = [F(1)]
        for r in roots:
            if r is None:
                continue
            if isinstance(r, tuple):
                _, rad, x = r
                c = cm.polymul(c, [F(1), -2 * rad * x, rad * rad])
            else:
                c = cm.polymul(c, [F(1), -r])
        res = jury_table(c)
        assert res.regular and res.schur and res.outside == 0
        assert jury_classic(c)


def test_regular_count_outside_with_random_roots():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 6)
        roots = []
        for _ in range(n):
            if rng.random() < 0.5:
                roots.append(F(rng.randint(-95, 95), 100))
            else:
                v = F(rng.randint(105, 400), 100)
                roots.append(v if rng.random() < 0.5 else -v)
        # avoid reciprocal pairs, which make the table singular
        if any(a * b == 1 for i, a in enumerate(roots) for b in roots[i + 1:]):
            continue
        c = poly_from_roots(roots)
        r = jury_table(c)
        if r.regular:
            assert r.outside == sum(1 for v in roots if abs(v) > 1)
        else:
            assert sum(1 for v in roots if abs(v) > 1) > 0


def test_singular_cases():
    # a root on the circle
    r = jury_table([1, F(-3, 2), F(1, 2)])  # (z - 1)(z - 1/2)
    assert not r.regular and not r.schur and r.outside is None
    assert r.first == [1, F(3, 4), 0]
    # a reciprocal pair, no root on the circle
    r = jury_table([1, F(-5, 2), 1])  # (z - 2)(z - 1/2)
    assert not r.regular and r.first == [1, 0]
    r = jury_table([8, -18, 3, 2])  # (z - 2)(2z - 1)(4z + 1)
    assert not r.regular and r.first == [8, F(15, 2), 0]
    # roots at -1 and on the circle at +-i
    assert not jury_table([1, 0, 1]).regular
    assert not is_schur([1, 1])


def test_relation_to_schur_cohn_transform():
    # p_(k-1) is the Schur transform of p_k, reversed and scaled by -1/c_0.
    rng = random.Random(3)
    for _ in range(200):
        c = [F(v) for v in random_poly(rng)]
        if c[0] < 0:
            c = [-v for v in c]
        r = jury_table(c)
        for pk, pk1 in zip(r.rows, r.rows[1:]):
            k = len(pk) - 1
            star = pk[::-1]
            t = [pk[k] * pk[i] - pk[0] * star[i] for i in range(k + 1)]
            assert t[0] == 0
            tail = t[1:]  # degree k - 1, highest power first
            assert [-v / pk[0] for v in tail[::-1]] == pk1


def test_input_handling():
    assert jury_table([0, 0, 1, F(-1, 2)]).schur  # leading zeros removed
    assert jury_table([-1, 1, F(-1, 2)]).schur  # negative leading coefficient
    assert jury_table([-2, 1, 3]).outside == outside_count([2, -1, -3])
    assert jury_table([5]).schur and jury_table([5]).outside == 0
    assert jury_table([1.0, -1.0, 0.5]).first == [1, F(3, 4), F(5, 12)]
    with pytest.raises(ValueError):
        jury_table([0, 0])
    with pytest.raises(TypeError):
        jury_table([1, "a"])


def test_gain_range_of_a_sampled_loop():
    # z^2 - e^-1 z + K (1 - e^-1): Schur for 0 < K < 1 / (1 - e^-1) = 1.58198.
    a = math.exp(-1)
    b = 1 - a
    kmax = 1 / b
    assert abs(kmax - 1.58198) < 1e-5
    for k in [0.01, 0.5, 1.0, 1.5, kmax * (1 - 1e-9)]:
        assert is_schur([1.0, -a, k * b])
    for k in [kmax * (1 + 1e-9), 1.6, 3.0]:
        assert not is_schur([1.0, -a, k * b])
        assert outside_count([1.0, -a, k * b]) == 2


def test_degree_drops_by_one():
    rng = random.Random(5)
    for _ in range(100):
        c = random_poly(rng)
        r = jury_table(c)
        n = len(c) - 1  # random_poly gives a nonzero leading coefficient
        assert [len(row) - 1 for row in r.rows] == list(range(n, n - len(r.rows), -1))
