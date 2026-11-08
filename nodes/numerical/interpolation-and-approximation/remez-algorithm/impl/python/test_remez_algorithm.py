# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/remez-algorithm/. The authors are listed in prov/VZ77TJ.jsonl.

import math
import random

import pytest

from remez_algorithm import _levelled_fit, cheb_eval, evaluate, remez


def check_equioscillation(f, n, a, b, c, E, ref, rel=1e-7):
    """The error alternates in sign on ref with size E, and E is the max."""
    errs = [f(x) - evaluate(c, x, a, b) for x in ref]
    assert len(ref) == n + 2
    assert all(ref[i] < ref[i + 1] for i in range(n + 1))
    for i in range(n + 1):
        assert errs[i] * errs[i + 1] < 0
    for e in errs:
        assert abs(abs(e) - E) <= rel * E + 1e-14
    grid = [a + (b - a) * k / 5000 for k in range(5001)]
    assert max(abs(f(x) - evaluate(c, x, a, b)) for x in grid) <= E * (1 + rel) + 1e-14


def test_degree_zero_is_midrange():
    c, E, ref, _ = remez(math.exp, 0)
    assert abs(E - math.sinh(1)) < 1e-12
    assert abs(c[0] - math.cosh(1)) < 1e-12


def test_degree_one_exp_closed_form():
    s = math.sinh(1)
    xi = math.log(s)
    exact = (math.exp(-1) - math.exp(xi) + s * (1 + xi)) / 2
    c, E, ref, _ = remez(math.exp, 1)
    assert abs(E - exact) < 1e-12
    assert abs(ref[1] - xi) < 1e-6


def test_monomial_gives_scaled_chebyshev():
    for n in range(0, 9):
        f = lambda x, n=n: x ** (n + 1)
        c, E, ref, _ = remez(f, n)
        assert abs(E - 2.0 ** (-n)) < 1e-12
        for k in range(n + 2):
            assert abs(ref[k] + math.cos(math.pi * k / (n + 1))) < 1e-6


def test_random_degree_n_plus_one_polynomials():
    rng = random.Random(7)
    for _ in range(40):
        n = rng.randint(0, 7)
        a = rng.uniform(-3, 1)
        b = a + rng.uniform(0.5, 4)
        coef = [rng.uniform(-2, 2) for _ in range(n + 2)]
        f = lambda x, coef=coef: sum(ck * x ** k for k, ck in enumerate(coef))
        expected = abs(coef[-1]) * ((b - a) / 2) ** (n + 1) * 2.0 ** (-n)
        c, E, ref, _ = remez(f, n, a, b)
        assert abs(E - expected) <= 1e-9 * max(1.0, expected)


def test_polynomials_of_degree_n_are_reproduced():
    rng = random.Random(8)
    for _ in range(30):
        n = rng.randint(0, 8)
        coef = [rng.uniform(-3, 3) for _ in range(n + 1)]
        f = lambda x, coef=coef: sum(ck * x ** k for k, ck in enumerate(coef))
        c, E, ref, _ = remez(f, n)
        assert E < 1e-12
        for x in (-0.9, -0.1, 0.37, 1.0):
            assert abs(evaluate(c, x) - f(x)) < 1e-12


def test_abs_degree_two():
    c, E, ref, _ = remez(abs, 2)
    assert abs(E - 0.125) < 1e-12
    for x in (-1.0, -0.3, 0.0, 0.6, 1.0):
        assert abs(evaluate(c, x) - (x * x + 0.125)) < 1e-10


def test_equioscillation_on_assorted_functions():
    cases = [
        (math.exp, 6, -1.0, 1.0),
        (lambda x: 1 / (1 + 25 * x * x), 12, -1.0, 1.0),
        (abs, 8, -1.0, 1.0),
        (math.sqrt, 5, 0.25, 4.0),
        (lambda x: 1 / (x - 1.05), 10, -1.0, 1.0),  # pole near the interval
        (math.sin, 7, 0.0, 6.0),
    ]
    for f, n, a, b in cases:
        c, E, ref, it = remez(f, n, a, b)
        assert it < 60
        check_equioscillation(f, n, a, b, c, E, ref)


def test_de_la_vallee_poussin_lower_bound():
    rng = random.Random(9)
    for f, n in ((math.exp, 4), (lambda x: 1 / (1 + 25 * x * x), 8), (math.atan, 5)):
        _, E, _, _ = remez(f, n)
        for _ in range(100):
            ref = sorted(rng.uniform(-1, 1) for _ in range(n + 2))
            _, h = _levelled_fit(f, ref, n, -1.0, 1.0)
            assert abs(h) <= E * (1 + 1e-9)


def test_jump_does_not_crash_and_error_is_near_one():
    sign = lambda x: 1.0 if x >= 0 else -1.0
    c, E, ref, it = remez(sign, 5)
    assert 0.99 <= E <= 1.5


def test_clenshaw():
    c = [0.5, -1.0, 2.0, 0.25]
    for t in (-1.0, -0.3, 0.0, 0.8, 1.0):
        T = [1.0, t, 2 * t * t - 1, 4 * t ** 3 - 3 * t]
        assert abs(cheb_eval(c, t) - sum(a * b for a, b in zip(c, T))) < 1e-14


def test_errors():
    with pytest.raises(ValueError):
        remez(math.exp, -1)
    with pytest.raises(ValueError):
        remez(math.exp, 2, 1.0, 1.0)
