# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pade-approximation/. The authors are listed in prov/Q79FRC.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from pade_approximation import pade, pade_eval, poly_eval, series_divide


def exp_pade_closed_form(m, n):
    """Known [m/n] Padé approximant of exp: P_mn(x) / P_nm(-x)."""
    def num(m, n):
        return [F(math.factorial(m + n - j) * math.factorial(m),
                  math.factorial(m + n) * math.factorial(j) * math.factorial(m - j))
                for j in range(m + 1)]
    p = num(m, n)
    q = [v * (-1) ** j for j, v in enumerate(num(n, m))]
    return p, q


def order_condition(c, p, q, m, n):
    """Coefficients of f q - p up to x^(m+n) are all zero."""
    for k in range(m + n + 1):
        s = sum(q[j] * c[k - j] for j in range(len(q)) if k - j >= 0)
        if k < len(p):
            s -= p[k]
        if s != 0:
            return False
    return True


EXP = [F(1, math.factorial(k)) for k in range(30)]


def test_exp_two_two():
    p, q = pade(EXP, 2, 2)
    assert p == [1, F(1, 2), F(1, 12)]
    assert q == [1, F(-1, 2), F(1, 12)]


def test_exp_table_matches_closed_form():
    for m in range(0, 8):
        for n in range(0, 8):
            assert pade(EXP, m, n) == exp_pade_closed_form(m, n)


def test_n_zero_is_taylor_polynomial():
    p, q = pade(EXP, 5, 0)
    assert q == [1] and p == EXP[:6]


def test_single_coefficient():
    p, q = pade([F(7)], 0, 0)
    assert p == [7] and q == [1]


def test_order_condition_random_series():
    rng = random.Random(11)
    for _ in range(200):
        m, n = rng.randint(0, 6), rng.randint(0, 6)
        c = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(m + n + 1)]
        try:
            p, q = pade(c, m, n)
        except ValueError:
            continue
        assert q[0] == 1 and len(p) == m + 1 and len(q) == n + 1
        assert order_condition(c, p, q, m, n)


def test_rational_functions_reproduced():
    rng = random.Random(12)
    done = 0
    while done < 60:
        m, n = rng.randint(0, 5), rng.randint(1, 5)
        a = [F(rng.randint(-5, 5)) for _ in range(m + 1)]
        b = [F(1)] + [F(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(n)]
        if a[-1] == 0 or b[-1] == 0:
            continue
        c = series_divide(a, b, m + n + 1)
        try:
            p, q = pade(c, m, n)
        except ValueError:
            continue  # a and b share a factor: not normal
        for x in (F(1, 3), F(-2, 7), F(5, 2)):
            if poly_eval(b, x) != 0 and poly_eval(q, x) != 0:
                assert pade_eval(p, q, x) == poly_eval(a, x) / poly_eval(b, x)
        done += 1


def test_pole_near_interval_exact():
    # f = 1/(1.05 - x) has one pole at 1.05; [0/1] is exact
    c = [F(20, 21) ** (k + 1) for k in range(5)]
    p, q = pade(c, 0, 1)
    assert pade_eval(p, q, F(1)) == 20
    assert pade_eval(p, q, F(-1, 2)) == 1 / (F(105, 100) + F(1, 2))


def test_log_converges_beyond_radius():
    c = [F(0)] + [F((-1) ** (k + 1), k) for k in range(1, 25)]
    errs = []
    for n in (2, 4, 8, 12):
        p, q = pade(c, n, n)
        errs.append(abs(float(pade_eval(p, q, F(3))) - math.log(4)))
    assert errs[-1] < 1e-10 and all(errs[i + 1] < errs[i] for i in range(3))


def test_float_agrees_with_exact():
    rng = random.Random(13)
    for _ in range(40):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        c = [F(1, math.factorial(k)) for k in range(m + n + 1)]
        pe, qe = pade(c, m, n)
        pf, qf = pade([float(v) for v in c], m, n)
        x = rng.uniform(-2, 2)
        assert abs(pade_eval(pf, qf, x) - float(pade_eval(pe, qe, F(x)))) < 1e-12


def test_blocks_raise():
    cos = [F(1), F(0), F(-1, 2), F(0), F(1, 24)]
    with pytest.raises(ValueError):
        pade(cos, 1, 1)  # [1/1] of cos does not exist with q(0) = 1
    geo = [F(1, 2 ** k) for k in range(9)]
    with pytest.raises(ValueError):
        pade(geo, 2, 2)  # f is of type (0, 1): [2/2] lies in a block


def test_errors():
    with pytest.raises(ValueError):
        pade([F(1), F(2)], 1, 1)
    with pytest.raises(ValueError):
        pade([F(1)], -1, 0)
