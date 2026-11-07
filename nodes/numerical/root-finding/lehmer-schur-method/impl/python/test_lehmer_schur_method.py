# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lehmer-schur-method/. The authors are listed in prov/GXZ3FQ.jsonl.

import math
import random
from fractions import Fraction

import pytest

from lehmer_schur_method import (
    BETA,
    RHO,
    cauchy_radius,
    lehmer_schur,
    poly_from_roots,
    schur_cohn_count,
    shift_scale,
    to_gq,
)

SHRINK = Fraction(33, 64)  # the largest possible radius ratio per pass


def _inside(z, c, r):
    dx, dy = z[0] - c[0], z[1] - c[1]
    return dx * dx + dy * dy < r * r


def _check_shrink(res):
    for a, b in zip(res.radii, res.radii[1:]):
        assert b <= SHRINK * a


def test_quintic_page_example():
    res = lehmer_schur([-1, -1, 0, 0, 0, 1], tol=Fraction(1, 2 ** 40))
    assert res.converged and res.count == 1
    assert abs(res.center - 1.1673039782614187) < float(res.radius)
    assert res.iterations == 39 and res.tests == 80
    _check_shrink(res)


def test_iteration_bound():
    for coeffs in ([-2, -1, 0, 1], [1, 0, 1], [-1, -1, 0, 0, 0, 1]):
        tol = Fraction(1, 2 ** 30)
        res = lehmer_schur(coeffs, tol=tol)
        p = [to_gq(a) for a in coeffs]
        bound = math.ceil(math.log(cauchy_radius(p) / tol) / math.log(64 / 33))
        assert res.converged and res.iterations <= bound
        # at most 9 regular tests per pass, each with at most 5 tries
        assert res.tests <= 45 * res.iterations


def test_observed_linear_order():
    res = lehmer_schur([-2, -1, 0, 1], tol=Fraction(1, 2 ** 40))
    ratios = [float(b / a) for a, b in zip(res.radii, res.radii[1:])]
    assert all(0.43 <= q <= 0.516 for q in ratios)
    mean = math.exp(sum(math.log(q) for q in ratios) / len(ratios))
    assert 0.43 < mean < 0.52  # order 1, rate about 0.47 per pass


def test_complex_root_and_double_root_and_zero_root():
    res = lehmer_schur([1, 0, 1])
    assert res.converged and abs(abs(res.center) - 1) < 1e-11 and abs(res.center.real) < 1e-11
    res = lehmer_schur([1, -2, 1])  # (z - 1)^2
    assert res.converged and res.count == 2 and abs(res.center - 1) < 1e-11
    res = lehmer_schur([0, 0, 1])  # z^2: only inner halvings
    assert res.converged and res.count == 2 and res.center == 0
    assert res.tests == res.iterations


def test_edge_cases():
    assert lehmer_schur([7]).reason == "no roots"
    with pytest.raises(ValueError):
        lehmer_schur([0, 0])
    with pytest.raises(ValueError):
        lehmer_schur([1, 1], tol=0)
    res = lehmer_schur([-2, -1, 0, 1], max_iter=3)
    assert res.reason == "kmax reached" and not res.converged
    res = lehmer_schur([Fraction(-1, 2), 1, 0, 0])  # trailing zero coefficients ignored
    assert res.converged and abs(res.center - 0.5) < 1e-11


def test_float_and_complex_coefficients():
    res = lehmer_schur([0.25j, -1.5, 1.0])
    z = res.center
    assert res.converged and abs(z * z - 1.5 * z + 0.25j) < 1e-10


def test_schur_cohn_count_helper():
    p = [to_gq(a) for a in [3, 2, -19, 6]]  # zeros 1/2, -1/3, 3
    assert schur_cohn_count(p) == 2
    assert schur_cohn_count(shift_scale(p, to_gq(3), Fraction(1, 10))) == 1
    assert schur_cohn_count([to_gq(-1), to_gq(1)]) is None  # zero on the circle


def test_covering_constants():
    # every point with 0.484375 <= |z| <= 1 is within 0.4238 of a centre (see the proof)
    s_min = Fraction(1, 2) * Fraction(31, 32)
    for s in (float(s_min), 1.0):
        for rho in (float(RHO), float(RHO) * 181 / 256 * math.sqrt(2)):
            d = math.sqrt(s * s + rho * rho - 2 * s * rho * math.cos(math.pi / 8))
            assert d < float(BETA * Fraction(31, 32))


def test_random_known_roots():
    rng = random.Random(8112026)
    for _ in range(500):
        n = rng.randint(1, 4)
        roots = []
        for _ in range(n):
            if roots and rng.random() < 0.1:
                roots.append(roots[-1])
            else:
                im = Fraction(rng.randint(-24, 24), 8) if rng.random() < 0.5 else Fraction(0)
                roots.append((Fraction(rng.randint(-24, 24), 8), im))
        lead = Fraction(rng.randint(1, 5))
        p = [(a[0] * lead, a[1] * lead) for a in poly_from_roots(roots)]
        res = lehmer_schur(p, tol=Fraction(1, 2 ** 10))
        assert res.converged
        _check_shrink(res)
        c, r = res.center_exact, res.radius
        assert res.count == sum(_inside(z, c, r) for z in roots) >= 1
