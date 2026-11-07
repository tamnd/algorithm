# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laguerre-method/. The authors are listed in prov/K13QF2.jsonl.

import math
import random
from decimal import Decimal, getcontext

import pytest

from laguerre_method import U, deflate, horner2, laguerre, laguerre_all_roots

Q4 = [1, -10, 35, -50, 24]  # (x - 1)(x - 2)(x - 3)(x - 4)


def poly_from_roots(zs):
    c = [1 + 0j]
    for z in zs:
        c = [a - z * b for a, b in zip(c + [0], [0] + c)]
    return c


def test_example_real_roots_from_zero():
    r = laguerre(Q4, 0)
    assert r.reason == "root" and r.iterations == 4 and r.evaluations == 4
    assert r.root == 0.9999999999999998 and r.root.imag == 0


def test_observed_cubic_order_in_high_precision():
    getcontext().prec = 200
    c = [Decimal(a) for a in Q4]
    n = 4
    x = Decimal(0)
    errs = []
    for _ in range(5):
        errs.append(abs(x - 1))
        p = d = dd = Decimal(0)
        p = c[0]
        for a in c[1:]:
            dd = dd * x + d
            d = d * x + p
            p = p * x + a
        g = d / p
        h = g * g - 2 * dd / p
        r = ((n - 1) * (n * h - g * g)).sqrt()
        den = g + r if abs(g + r) >= abs(g - r) else g - r
        x = x - n / den
    ratios = [errs[k + 1] / errs[k] ** 3 for k in range(2, 4)]
    assert all(abs(q - Decimal("0.12037")) < Decimal("1e-5") for q in ratios)
    assert errs[1] < errs[0] and x < 1  # monotone from the left


def test_real_rooted_moves_to_neighbouring_root():
    # start between 2 and 3: the iterates stay in [2, 3]
    for x0, want in [(2.4, 2), (2.6, 3), (10.0, 4), (-7.0, 1), (3.5, None)]:
        r = laguerre(Q4, x0)
        assert r.converged
        z = r.root.real
        assert abs(r.root.imag) == 0
        if want is not None:
            assert abs(z - want) < 1e-12
        else:
            assert abs(z - 3) < 1e-12 or abs(z - 4) < 1e-12


def test_complex_root_from_real_start():
    r = laguerre([1, 0, 1], 0)
    assert r.root == 1j and r.reason == "root" and r.evaluations == 2


def test_zero_denominator_fallback():
    # at 0, p' = p'' = 0 for x^3 - 1
    r = laguerre([1, 0, 0, -1], 0)
    assert r.converged
    assert abs(r.root ** 3 - 1) < 1e-14


def test_root_of_power_is_exact_in_one_step():
    for n in range(1, 8):
        c = [math.comb(n, j) * (-1) ** j for j in range(n + 1)]  # (x - 1)^n
        r = laguerre(c, -3.0)
        assert r.root == 1 and r.reason == "root" and r.iterations == 2


def test_multiple_root_converges_linearly():
    # (x - 1)^2 (x + 2): double root at 1, linear convergence
    c = [1, 0, -3, 2]
    r = laguerre(c, 3.0, max_iter=200)
    assert r.converged and abs(r.root - 1) < 1e-7


def test_root_at_start_and_kmax_and_bad_input():
    r = laguerre(Q4, 3)
    assert r.reason == "root" and r.evaluations == 1
    r = laguerre(Q4, 100.0, max_iter=1)
    assert r.reason == "kmax reached" and r.evaluations == 1
    with pytest.raises(ValueError):
        laguerre([0, 1, 2], 0)
    with pytest.raises(ValueError):
        laguerre([5], 0)


def test_nan_and_overflow():
    r = laguerre([1, float("nan"), 1], 0.5)
    assert r.reason == "failure"
    r = laguerre([1, 0, 1], 1e200)
    assert r.reason in ("failure", "converged", "residual", "root")
    assert r.evaluations <= 100


def test_horner2_and_deflate():
    p, d1, d2, s = horner2(Q4, 5)
    assert (p, d1, d2, s) == (24, 50, 70, 1 * 625 + 10 * 125 + 35 * 25 + 50 * 5 + 24)
    assert deflate(Q4, 1) == [1, -9, 26, -24]


def test_all_roots_wilkinson_small_and_cubic():
    rs = laguerre_all_roots([1, 0, 0, -1])
    want = [1, complex(-0.5, math.sqrt(3) / 2), complex(-0.5, -math.sqrt(3) / 2)]
    for w in want:
        assert min(abs(z - w) for z in rs) < 1e-15
    rs = laguerre_all_roots(poly_from_roots(range(1, 11)))
    assert sorted(round(z.real) for z in rs) == list(range(1, 11))
    assert max(min(abs(z - j) for z in rs) for j in range(1, 11)) < 1e-7


def test_random_polynomials():
    rng = random.Random(20261108)
    for _ in range(500):
        n = rng.randint(1, 10)
        zs = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        c = poly_from_roots(zs)
        rs = laguerre_all_roots(c)
        assert len(rs) == n
        rem = list(rs)
        for z in zs:
            j = min(range(len(rem)), key=lambda i: abs(rem[i] - z))
            assert abs(rem[j] - z) < 1e-8
            rem.pop(j)
        for z in rs:
            p, _, _, s = horner2(c, z)
            assert abs(p) <= 1e-12 * s
