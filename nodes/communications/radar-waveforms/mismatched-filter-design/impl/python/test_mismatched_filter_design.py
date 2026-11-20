# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mismatched-filter-design/. The authors are listed in prov/T4GZMK.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from mismatched_filter_design import (
    autocorrelation,
    center,
    conj,
    convolve,
    matched_filter,
    metrics,
    min_isl,
    mismatched_filter,
)

B3 = [1, 1, -1]
B7 = [1, 1, 1, -1, -1, 1, -1]
B11 = [1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1]
B13 = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
FRANK16 = [cmath.exp(2j * math.pi * m * n / 4) for m in range(4) for n in range(4)]


def db(x):
    return 10 * math.log10(x)


def correlate_back(s, y, length):
    """(C^H y)[i] = sum over m of conj(s[m - i]) y[m], i = 0 .. length - 1."""
    return [sum((conj(s[m - i]) * y[m] for m in range(len(y)) if 0 <= m - i < len(s)), 0) for i in range(length)]


def isl_of(s, h, c):
    return metrics(s, h, c)["isl"]


def test_page_example_barker3() -> None:
    h = mismatched_filter(B3, 3)
    assert h == [Fraction(-3, 10), Fraction(2, 5), Fraction(3, 10)]
    m = metrics(B3, h)
    assert m["output"] == [Fraction(-3, 10), Fraction(1, 10), 1, Fraction(-1, 10), Fraction(-3, 10)]
    assert m["isl"] == Fraction(1, 5)
    assert m["loss"] == Fraction(50, 51)
    assert m["psl2"] == Fraction(9, 100)
    h5 = mismatched_filter(B3, 5)
    assert h5 == [Fraction(2, 13), Fraction(-7, 26), Fraction(6, 13), Fraction(7, 26), Fraction(2, 13)]
    assert metrics(B3, h5)["isl"] == Fraction(1, 13)


def test_matched_filter_reference() -> None:
    for code in (B3, B7, B11, B13):
        m = metrics(code, matched_filter(code))
        n = len(code)
        assert m["peak"] == 1
        assert m["loss"] == 1
        assert m["psl2"] == Fraction(1, n * n)  # Barker sidelobes have magnitude 1
    assert autocorrelation(B13) == [13, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]


def test_normal_equations_hold_exactly() -> None:
    for code in (B7, B11, B13):
        for length in (len(code), len(code) + 8, 2 * len(code) + 1):
            c = center(len(code), length)
            h = mismatched_filter(code, length)
            y = convolve(h, code)
            assert y[c] == 1
            back = correlate_back(code, y, length)
            e = [conj(code[c - i]) if 0 <= c - i < len(code) else 0 for i in range(length)]
            lam = next(back[i] / e[i] for i in range(length) if e[i] != 0)
            assert all(back[i] == lam * e[i] for i in range(length)), (code, length)
            assert lam == 1 + metrics(code, h)["isl"]  # C^H C h = (h^H R h) e


def test_closed_form_matches_output() -> None:
    for code in (B3, B7, B11, B13):
        for length in range(len(code), 2 * len(code) + 2, 2):
            assert min_isl(code, length) == metrics(code, mismatched_filter(code, length))["isl"]


def test_no_perturbation_does_better() -> None:
    rng = random.Random(7301)
    code, length = B7, 11
    c = center(len(code), length)
    h = mismatched_filter(code, length)
    e = [conj(code[c - i]) if 0 <= c - i < len(code) else 0 for i in range(length)]
    best = isl_of(code, h, c)
    ee = sum(x * x for x in e)
    for _ in range(200):
        d = [Fraction(rng.randint(-20, 20), rng.randint(1, 50)) for _ in range(length)]
        t = sum(d[i] * e[i] for i in range(length)) / ee
        d = [d[i] - t * e[i] for i in range(length)]  # keep the peak at 1
        if not any(d):
            continue
        g = [h[i] + d[i] for i in range(length)]
        assert convolve(g, code)[c] == 1
        assert isl_of(code, g, c) > best


def test_coordinate_descent_agrees() -> None:
    """A second method: Gauss-Seidel on the normal equations, in floats, from zero."""
    code, length = B7, 15
    n = len(code)
    c = center(n, length)
    r = autocorrelation(code)
    rr = [[float(r[abs(i - j)]) if abs(i - j) < n else 0.0 for j in range(length)] for i in range(length)]
    e = [float(code[c - i]) if 0 <= c - i < n else 0.0 for i in range(length)]
    g = [0.0] * length
    for _ in range(3000):
        for i in range(length):
            g[i] = (e[i] - sum(rr[i][j] * g[j] for j in range(length) if j != i)) / rr[i][i]
    peak = sum(e[i] * g[i] for i in range(length))
    h = mismatched_filter(code, length)
    assert max(abs(g[i] / peak - float(h[i])) for i in range(length)) < 1e-9


def test_longer_filter_never_worse() -> None:
    prev = None
    for length in range(13, 41, 2):
        v = min_isl(B13, length)
        if prev is not None:
            assert v <= prev
        prev = v


def test_barker13_page_values() -> None:
    m = metrics(B13, mismatched_filter(B13, 13))
    assert m["isl"] == Fraction(1, 37)
    assert db(m["psl2"]) == pytest.approx(-24.00, abs=0.01)
    assert db(m["loss"]) == pytest.approx(-0.143, abs=0.001)
    m = metrics(B13, mismatched_filter(B13, 39))
    assert db(m["psl2"]) == pytest.approx(-38.47, abs=0.01)
    assert db(m["isl"]) == pytest.approx(-30.03, abs=0.01)
    assert db(m["loss"]) == pytest.approx(-0.204, abs=0.001)
    assert 0 < m["loss"] < 1


def test_barker11_psl_can_rise() -> None:
    """Least squares lowers the ISL but not always the PSL (pitfall on the page)."""
    mf = metrics(B11, matched_filter(B11))
    ls = metrics(B11, mismatched_filter(B11, 11))
    assert ls["isl"] < mf["isl"]
    assert ls["psl2"] > mf["psl2"]


def test_complex_frank_code() -> None:
    for length in (16, 31, 47):
        h = mismatched_filter(FRANK16, length)
        c = center(16, length)
        m = metrics(FRANK16, h)
        assert abs(m["peak"] - 1) < 1e-9
        assert m["loss"] <= 1 + 1e-12
        assert abs(m["isl"] - min_isl(FRANK16, length)) < 1e-9
        y = m["output"]
        back = correlate_back(FRANK16, y, length)
        e = [conj(FRANK16[c - i]) if 0 <= c - i < 16 else 0 for i in range(length)]
        i0 = next(i for i in range(length) if abs(e[i]) > 0.5)
        lam = back[i0] / e[i0]
        assert max(abs(back[i] - lam * e[i]) for i in range(length)) < 1e-9


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        mismatched_filter([0, 0, 0], 5)
    with pytest.raises(ValueError):
        mismatched_filter(B3, 0)
    with pytest.raises(ValueError):
        mismatched_filter(B3, 3, c=9)
