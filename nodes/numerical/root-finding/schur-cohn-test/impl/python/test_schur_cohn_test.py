# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schur-cohn-test/. The authors are listed in prov/AXFQZ4.jsonl.

import random
from fractions import Fraction

import pytest

from schur_cohn_test import is_schur_stable, poly_from_roots, schur_cohn


def test_page_example_trace():
    # 6z^3 - 19z^2 + 2z + 3 = (2z - 1)(3z + 1)(z - 3)
    r = schur_cohn([3, 2, -19, 6])
    assert r.converged and r.count == 2
    assert r.steps == 3 == r.degree
    assert r.deltas == [-27, -448, -9]


def test_constant_and_linear():
    assert schur_cohn([5]).count == 0 and schur_cohn([5]).steps == 0
    assert schur_cohn([Fraction(-1, 2), 1]).count == 1  # z - 1/2
    assert schur_cohn([-2, 1]).count == 0  # z - 2


def test_zero_polynomial_and_bad_radius():
    with pytest.raises(ValueError):
        schur_cohn([0, 0])
    with pytest.raises(ValueError):
        schur_cohn([1, 1], radius=0)


def test_leading_zeros_trimmed():
    assert schur_cohn([Fraction(-1, 2), 1, 0, 0]).count == 1


def test_zeros_at_origin():
    r = schur_cohn([0, 0, 0, 1])  # z^3
    assert r.count == 3 and r.steps == 1
    assert schur_cohn(poly_from_roots([0, 0, 3])).count == 2


def test_zero_on_circle_is_singular():
    for roots in ([1], [-1, Fraction(1, 2)], [1j, 3], [(Fraction(3, 5), Fraction(4, 5))]):
        r = schur_cohn(poly_from_roots(roots))
        assert r.reason == "singular" and r.count is None and not r.converged


def test_symmetric_pair_and_accidental_singular():
    assert schur_cohn(poly_from_roots([Fraction(1, 2), 2])).reason == "singular"
    # z^2 + z + i: no zero on the circle, but |a0| = |a2|
    assert schur_cohn([1j, 1, 1]).reason == "singular"


def test_other_discs():
    p = [3, 2, -19, 6]  # zeros 1/2, -1/3, 3
    assert schur_cohn(p, center=3, radius=Fraction(1, 10)).count == 1
    assert schur_cohn(p, center=0, radius=4).count == 3
    assert schur_cohn(p, center=Fraction(1, 2), radius=Fraction(1, 2)).count == 1
    assert schur_cohn(p, center=10, radius=1).count == 0


def test_complex_and_float_coefficients():
    roots = [0.25 + 0.5j, -0.75j, 1.5 - 0.5j]
    assert schur_cohn(poly_from_roots(roots)).count == 2
    # z^2 - z + 0.5 has zeros (1 +- i)/2, inside: discrete-time stable
    assert is_schur_stable([0.5, -1, 1])
    assert not is_schur_stable([1, -1, 0.5])  # zeros 1 +- i


def test_reciprocal_count():
    # p and its reversal: zeros z and 1/z, so counts add up to n
    p = [3, 2, -19, 6]
    assert schur_cohn(p).count + schur_cohn(p[::-1]).count == 3


def _random_root(rng):
    while True:
        re = Fraction(rng.randint(-40, 40), 16)
        im = Fraction(rng.randint(-40, 40), 16) if rng.random() < 0.6 else Fraction(0)
        m2 = re * re + im * im
        if abs(m2 - 1) > Fraction(1, 20):
            return (re, im), m2 < 1


def test_random_known_roots():
    rng = random.Random(20261108)
    regular = 0
    for _ in range(600):
        n = rng.randint(1, 8)
        roots, flags = [], []
        for _ in range(n):
            if roots and rng.random() < 0.15:
                z, ins = roots[-1], flags[-1]  # a repeated root
            else:
                z, ins = _random_root(rng)
            roots.append(z)
            flags.append(ins)
        lead = Fraction(rng.randint(1, 9), rng.randint(1, 4))
        p = [(c[0] * lead, c[1] * lead) for c in poly_from_roots(roots)]
        r = schur_cohn(p)
        assert r.steps <= n
        if r.converged:
            regular += 1
            assert r.count == sum(flags)
        else:
            assert r.reason == "singular"
    assert regular >= 450
