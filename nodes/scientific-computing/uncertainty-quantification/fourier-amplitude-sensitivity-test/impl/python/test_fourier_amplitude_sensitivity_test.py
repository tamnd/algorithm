# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fourier-amplitude-sensitivity-test/. The authors are listed in prov/VVPHQA.jsonl.
import math
import random

import pytest

from fourier_amplitude_sensitivity_test import efast, frequencies, search_points, spectrum


def ishigami_unit(u):
    x = [-math.pi + 2 * math.pi * v for v in u]
    return math.sin(x[0]) + 7 * math.sin(x[1]) ** 2 + 0.1 * x[2] ** 4 * math.sin(x[0])


ISHIGAMI_S = [0.3139, 0.4424, 0.0]
ISHIGAMI_ST = [0.5576, 0.4424, 0.2437]


def test_frequencies_put_the_high_one_at_input_i():
    assert frequencies(3, 1, 64, 4) == [1, 64, 8]
    assert frequencies(5, 0, 64, 4) == [64, 1, 3, 5, 8]
    with pytest.raises(ValueError):
        frequencies(3, 0, 7, 4)


def test_search_curve_has_uniform_marginals():
    pts = search_points([1, 11, 4], [0.3, 1.1, 2.0], 2001)
    for j in range(3):
        col = sorted(p[j] for p in pts)
        assert all(0.0 <= v <= 1.0 for v in col)
        assert abs(sum(col) / len(col) - 0.5) < 0.01
        assert abs(col[len(col) // 4] - 0.25) < 0.01


def test_spectrum_power_sums_to_the_variance():
    rng = random.Random(3)
    n_s = 257
    y = [rng.random() for _ in range(n_s)]
    m = sum(y) / n_s
    assert abs(sum(spectrum(y, n_s)[1:]) - sum((v - m) ** 2 for v in y) / n_s) < 1e-12


def test_cosine_model_is_exact():
    # cos(2 pi x_j) along the curve is a pure harmonic at 2 omega_j, so no power leaks
    c = [1.0, 2.0, 0.0, 3.0]
    f = lambda x: sum(cj * math.cos(2 * math.pi * xj) for cj, xj in zip(c, x))  # noqa: E731
    res = efast(f, 4, 32, 4, 2, random.Random(11))
    assert res["runs"] == 4 * 2 * res["n_s"]
    total = sum(cj * cj for cj in c)
    for i in range(4):
        assert abs(res["S"][i] - c[i] ** 2 / total) < 1e-9
        assert abs(res["ST"][i] - c[i] ** 2 / total) < 1e-9


def test_ishigami_first_order_and_total_indices():
    res = efast(ishigami_unit, 3, 64, 4, 1, random.Random(1))
    assert res["runs"] == 3 * 513
    for i in range(3):
        assert abs(res["S"][i] - ISHIGAMI_S[i]) < 0.03
        assert abs(res["ST"][i] - ISHIGAMI_ST[i]) < 0.06
    # x3 acts only through its interaction with x1
    assert res["ST"][2] - res["S"][2] > 0.15


def test_even_or_short_curves_are_rejected():
    with pytest.raises(ValueError):
        efast(ishigami_unit, 3, 16, 4, 1, random.Random(0), n_s=128)
    with pytest.raises(ValueError):
        efast(ishigami_unit, 3, 16, 4, 1, random.Random(0), n_s=101)
