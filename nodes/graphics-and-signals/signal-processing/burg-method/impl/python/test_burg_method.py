# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burg-method/. The authors are listed in prov/CXSG6S.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from burg_method import burg, burg_psd, burg_with_errors, step_down


def stage_energy(f, b, m, k):
    """Sum over t = m .. N-1 of |f[t] + k b[t-1]|^2 + |b[t-1] + conj(k) f[t]|^2 (real signals)."""
    return sum((f[t] + k * b[t - 1]) ** 2 + (b[t - 1] + k * f[t]) ** 2 for t in range(m, len(f)))


def roots(coeffs):
    """Roots of z^p + c[1] z^(p-1) + ... + c[p] by Durand-Kerner iteration."""
    p = len(coeffs) - 1
    z = [(0.4 + 0.9j) ** i for i in range(p)]
    for _ in range(500):
        new = []
        for i in range(p):
            val = sum(c * z[i] ** (p - j) for j, c in enumerate(coeffs))
            den = 1
            for j in range(p):
                if j != i:
                    den *= z[i] - z[j]
            new.append(z[i] - val / den)
        z = new
    return z


def test_page_example() -> None:
    x = [Fraction(v) for v in (2, 1, -1, -2, -1, 1, 2, 1)]
    a, k, e = burg(x, 1)
    assert a == [1, Fraction(-16, 29)] and k == [Fraction(-16, 29)] and e == Fraction(9945, 6728)
    a, k, e = burg(x, 2)
    assert a == [1, Fraction(-232, 211), Fraction(419, 422)]
    assert k == [Fraction(-16, 29), Fraction(419, 422)]
    assert e == Fraction(29835, 1424672)
    assert burg(x, 0) == ([1], [], Fraction(17, 8))


def test_edges() -> None:
    with pytest.raises(ValueError):
        burg([1.0, 2.0], 2)
    with pytest.raises(ValueError):
        burg([1.0], -1)
    a, k, e = burg([0.0, 0.0, 0.0], 2)
    assert a == [1, 0, 0] and k == [0, 0] and e == 0
    with pytest.raises(ValueError):
        step_down([1, 0, 1])


def test_reflection_coefficients_inside_unit_disk() -> None:
    rng = random.Random(4601)
    for trial in range(500):
        n = rng.randint(3, 40)
        p = rng.randint(1, n - 1)
        if trial % 2:
            x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        else:
            x = [rng.gauss(0, 1) for _ in range(n)]
        a, ks, e = burg(x, p)
        assert all(abs(k) < 1 for k in ks)
        assert e >= 0


def test_lattice_errors_equal_direct_filtering_exact() -> None:
    rng = random.Random(4602)
    for _ in range(300):
        n = rng.randint(2, 9)
        p = rng.randint(1, n - 1)
        x = [Fraction(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(n)]
        if all(v == 0 for v in x):
            continue
        a, ks, e, f, b = burg_with_errors(x, p)
        for t in range(p, n):
            assert f[t] == sum(a[i] * x[t - i] for i in range(p + 1))
            assert b[t] == sum(a[i] * x[t - p + i] for i in range(p + 1))
        assert all(abs(k) <= 1 for k in ks)
        if all(abs(k) < 1 for k in ks):
            assert step_down(a) == ks
        else:
            # |k| = 1 exactly: the overlapping errors were proportional, e.g. x = (1, 1) with p = 1
            assert any(abs(k) == 1 for k in ks)
    assert burg([Fraction(1), Fraction(1)], 1)[1] == [-1]


def test_each_k_minimizes_the_stage_energy() -> None:
    rng = random.Random(4603)
    grid = [i / 200 - 1 for i in range(401)]
    for _ in range(200):
        n = rng.randint(4, 20)
        p = rng.randint(1, n - 1)
        x = [rng.gauss(0, 1) for _ in range(n)]
        for m in range(1, p + 1):
            _, _, _, f, b = burg_with_errors(x, m - 1)
            k = burg(x, m)[1][-1]
            best = stage_energy(f, b, m, k)
            assert all(best <= stage_energy(f, b, m, g) + 1e-9 for g in grid)


def test_model_is_minimum_phase() -> None:
    rng = random.Random(4604)
    for _ in range(200):
        n = rng.randint(6, 30)
        p = rng.randint(1, 4)
        x = [rng.gauss(0, 1) for _ in range(n)]
        a, _, _ = burg(x, p)
        assert all(abs(z) < 1 for z in roots(a))


def ar2(rng, n, a1, a2, burn=200):
    y1 = y2 = 0.0
    out = []
    for t in range(n + burn):
        y = -a1 * y1 - a2 * y2 + rng.gauss(0, 1)
        y2, y1 = y1, y
        if t >= burn:
            out.append(y)
    return out


def test_recovers_known_ar2() -> None:
    # A(z) = 1 - 0.75 z^-1 + 0.5 z^-2, unit noise, N = 2000, seeds 7000 to 7049.
    # The asymptotic standard deviation of each coefficient is sqrt((1 - 0.5^2) / 2000) = 0.0194.
    errors = []
    for seed in range(7000, 7050):
        a, ks, e = burg(ar2(random.Random(seed), 2000, -0.75, 0.5), 2)
        errors.append(max(abs(a[1] + 0.75), abs(a[2] - 0.5)))
        assert abs(e - 1) < 0.15
    assert sum(errors) / len(errors) < 0.03
    assert max(errors) < 0.08


def test_psd_of_known_model() -> None:
    a = [1, -0.75, 0.5]
    assert abs(burg_psd(a, 1.0, 0.0) - 1 / 0.75 ** 2) < 1e-12
    assert abs(burg_psd(a, 2.0, math.pi) - 2 / 2.25 ** 2) < 1e-12
    w = 1.0
    assert abs(burg_psd(a, 1.0, w) - 1 / abs(1 - 0.75 * cmath.exp(-1j * w) + 0.5 * cmath.exp(-2j * w)) ** 2) < 1e-12
