# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cardano-formula/. The authors are listed in prov/XGZ50G.jsonl.

import cmath
import random

import pytest

from cardano_formula import cardano, polish


def match(got, want, tol):
    """Match two multisets of complex numbers greedily within tol."""
    rest = list(want)
    for z in got:
        j = min(range(len(rest)), key=lambda i: abs(rest[i] - z))
        if abs(rest[j] - z) > tol:
            return False
        rest.pop(j)
    return True


def test_cardano_example():
    roots = cardano(1, 0, 6, -20)
    assert abs(roots[0] - 2) < 1e-14
    assert match(roots, [2, -1 + 3j, -1 - 3j], 1e-13)


def test_three_real_roots_need_complex_intermediates():
    roots = cardano(1, -6, 11, -6)
    assert match(roots, [1, 2, 3], 1e-13)
    assert [round(z.real) for z in roots] == [3, 1, 2]
    assert all(abs(z.imag) < 1e-15 for z in roots)


def test_double_and_triple_roots():
    assert match(cardano(1, 0, -3, 2), [1, 1, -2], 1e-7)
    assert cardano(1, 0, 0, 0) == (0, 0, 0)
    assert match(cardano(1, -3, 3, -1), [1, 1, 1], 1e-5)  # (x - 1)^3: about u^(1/3)


def test_sign_choice_avoids_false_triple_root():
    roots = cardano(1, 0, 1e-8, 1)
    want = [-1, cmath.exp(1j * cmath.pi / 3), cmath.exp(-1j * cmath.pi / 3)]
    assert match(roots, want, 1e-8)


def test_independent_cube_roots_pitfall():
    r = cmath.sqrt(100 + 8)
    u, v = (10 + r) ** (1 / 3), complex(10 - r) ** (1 / 3)
    t = u + v
    assert abs(t ** 3 + 6 * t - 20) > 1  # not a root
    assert abs(cardano(1, 0, 6, -20)[0] - 2) < 1e-14


def test_zero_coefficients_and_complex_input():
    assert match(cardano(2, 0, 0, -16), [2, 2 * cmath.exp(2j * cmath.pi / 3),
                                         2 * cmath.exp(-2j * cmath.pi / 3)], 1e-13)
    want = [1j, 2, -1 - 1j]
    a = 3
    b = -a * sum(want)
    c = a * (want[0] * want[1] + want[0] * want[2] + want[1] * want[2])
    d = -a * want[0] * want[1] * want[2]
    assert match(cardano(a, b, c, d), want, 1e-12)


def test_a_zero_is_rejected():
    with pytest.raises(ValueError):
        cardano(0, 1, 2, 3)


def test_roots_of_different_sizes_and_polishing():
    r = [1e-6, 1.0, 1000.0]
    b, c, d = -sum(r), r[0] * r[1] + r[0] * r[2] + r[1] * r[2], -r[0] * r[1] * r[2]
    small = min(cardano(1, b, c, d), key=abs)
    assert 1e-6 < abs(small - 1e-6) / 1e-6 < 1e-4  # the shift loses digits
    assert abs(polish(1, b, c, d, small) - 1e-6) / 1e-6 < 1e-12


def test_random_cubics_with_known_roots():
    rng = random.Random(31)
    for _ in range(600):
        if rng.random() < 0.5:
            want = [complex(rng.uniform(-10, 10), 0) for _ in range(3)]
        else:
            x = rng.uniform(-10, 10)
            z = complex(rng.uniform(-10, 10), rng.uniform(0.5, 10))
            want = [complex(x, 0), z, z.conjugate()]
        gap = min(abs(want[i] - want[j]) for i in range(3) for j in range(i))
        if gap < 0.1:
            continue
        a = rng.choice([1, -2.5, 7])
        b = -a * sum(want)
        c = a * (want[0] * want[1] + want[0] * want[2] + want[1] * want[2])
        d = -a * want[0] * want[1] * want[2]
        got = cardano(a, b.real, c.real, d.real)
        assert match(got, want, 1e-9 * 10 / gap)
        for z in got:
            assert abs(((a * z + b) * z + c) * z + d) < 1e-9 * abs(a) * 1e3
