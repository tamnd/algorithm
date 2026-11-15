# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-infinity-norm-computation/. The authors are listed in prov/KBHPWA.jsonl.

import math
import random
from fractions import Fraction

import pytest

from ctlmat import charpoly, mul, polyder, polyroots, transpose
from h_infinity_norm_computation import (even_polynomial, freq_response, hamiltonian,
                                         hankel_singular_values, hinf_norm_bisection,
                                         hinf_norm_level_set, imaginary_frequencies,
                                         sigma_max)

# Tolerances: both methods run with eps = 1e-8, so the returned interval has
# relative width at most 2e-8; values are compared with a relative
# tolerance of 1e-7. The frequency sweep is a lower bound of the norm; it
# must not exceed the upper end of the interval by more than 1e-9
# (relative), and on these systems it comes within 1e-6 of the lower end.

EPS = 1e-8
F = Fraction

FIRST_ORDER = ([[-1]], [[1]], [[1]], [[0]])                       # 1 / (s + 1)
LIGHT = ([[0, 1], [-1, F(-1, 5)]], [[0], [1]], [[1, 0]], [[0]])   # 1 / (s^2 + 0.2 s + 1)
NON_MINIMAL = ([[-4, -8, 12], [0, -8, 0], [0, 0, -16]], [[1], [0], [0]], [[1, 1, 1]], [[0]])
PEAK_AT_ZERO = ([[-1]], [[1]], [[1]], [[1]])                      # (s + 2) / (s + 1)
PEAK_AT_INFINITY = ([[-2]], [[1]], [[-1]], [[1]])                 # (s + 1) / (s + 2)

LIGHT_NORM = 1 / (0.2 * math.sqrt(1 - 0.01))                     # 1 / (2 zeta sqrt(1 - zeta^2))


def close(x, y, tol=1e-7):
    return abs(x - y) <= tol * max(1.0, abs(y))


def random_system(rng):
    """A random rational system with n <= 3, m, p <= 2 and A Hurwitz (max Re < -0.1)."""
    while True:
        n, m, p = rng.randint(1, 3), rng.randint(1, 2), rng.randint(1, 2)
        a = [[F(rng.randint(-6, 6), 4) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            a[i][i] = F(-rng.randint(2, 12), 4)
        if max(r.real for r in polyroots(charpoly(a))) >= -0.1:
            continue
        b = [[F(rng.randint(-4, 4), 4) for _ in range(m)] for _ in range(n)]
        c = [[F(rng.randint(-4, 4), 4) for _ in range(n)] for _ in range(p)]
        d = [[F(rng.randint(-2, 2), 4) for _ in range(m)] for _ in range(p)]
        if all(v == 0 for row in b for v in row) or all(v == 0 for row in c for v in row):
            continue
        return a, b, c, d


def sweep(sys, points=1201):
    """A lower bound of the norm: a log grid from 1e-3 to 1e3, the value at 0
    and at infinity (sigma_max(D)), and a golden section refinement around the
    best grid point."""
    a, b, c, d = sys
    grid = [10 ** (-3 + 6 * k / (points - 1)) for k in range(points)]
    vals = [sigma_max(a, b, c, d, w) for w in grid]
    k = max(range(points), key=lambda i: vals[i])
    best = max(vals[k], sigma_max(a, b, c, d, 0.0), sigma_max(a, b, c, d, 1e9))
    lo, hi = grid[max(k - 1, 0)], grid[min(k + 1, points - 1)]
    g = (math.sqrt(5) - 1) / 2
    x1, x2 = hi - g * (hi - lo), lo + g * (hi - lo)
    f1, f2 = sigma_max(a, b, c, d, x1), sigma_max(a, b, c, d, x2)
    for _ in range(80):
        if f1 > f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - g * (hi - lo)
            f1 = sigma_max(a, b, c, d, x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + g * (hi - lo)
            f2 = sigma_max(a, b, c, d, x2)
    return max(best, f1, f2)


def singular_values(g):
    """Singular values of a complex matrix with at most 2 columns, from G^H G."""
    gh = [[v.conjugate() for v in row] for row in transpose(g)]
    q = mul(gh, g)
    if len(q) == 1:
        return [math.sqrt(max(q[0][0].real, 0.0))]
    a, d, b = q[0][0].real, q[1][1].real, q[0][1]
    mid, rad = (a + d) / 2, math.sqrt(((a - d) / 2) ** 2 + abs(b) ** 2)
    return [math.sqrt(max(mid + rad, 0.0)), math.sqrt(max(mid - rad, 0.0))]


def sturm_count_nonpositive(r):
    """Number of distinct real roots of the Fraction polynomial r in (-inf, 0]."""
    seq = [r, polyder(r)]
    while len(seq[-1]) > 1 or seq[-1][0] != 0:
        num, den = list(seq[-2]), seq[-1]
        if len(den) == 1 and den[0] == 0:
            break
        while len(num) >= len(den) and any(v != 0 for v in num):
            f = num[0] / den[0]
            for i in range(len(den)):
                num[i] -= f * den[i]
            num.pop(0)
        while len(num) > 1 and num[0] == 0:
            num.pop(0)
        if not num or all(v == 0 for v in num):
            break
        seq.append([-v for v in num])

    def changes(signs):
        s = [v for v in signs if v != 0]
        return sum(1 for x, y in zip(s, s[1:]) if (x > 0) != (y > 0))

    at_minus_inf = [p[0] * (-1) ** (len(p) - 1) for p in seq]
    at_zero = [p[-1] for p in seq]
    return changes(at_minus_inf) - changes(at_zero)


def test_check_value_first_order():
    lo, hi, _ = hinf_norm_bisection(*FIRST_ORDER, eps=EPS)
    assert lo <= 1.0 <= hi and hi - lo <= 2 * EPS * lo
    lo, hi, w, _ = hinf_norm_level_set(*FIRST_ORDER, eps=EPS)
    assert close(lo, 1.0) and w == 0.0


def test_check_value_light_damping():
    lo, hi, _ = hinf_norm_bisection(*LIGHT, eps=EPS)
    assert close(lo, LIGHT_NORM) and close(hi, LIGHT_NORM)
    assert close(LIGHT_NORM, 5.02519, 1e-6)
    lo, hi, w, _ = hinf_norm_level_set(*LIGHT, eps=EPS)
    assert close(lo, LIGHT_NORM) and close(w, math.sqrt(0.98), 1e-6)


def test_even_polynomial_exact():
    # r(t) = t^2 + 1.96 t + 1 - 1/gamma^2, in exact arithmetic.
    for gamma in (F(1), F(5), F(11, 2)):
        r = even_polynomial(hamiltonian(*LIGHT, gamma))
        assert r == [1, F(49, 25), 1 - 1 / gamma ** 2]


def test_level_crossings_light_damping():
    a, b, c, d = LIGHT
    assert close(imaginary_frequencies(a, b, c, d, 1.0)[-1], 1.4, 1e-9)
    w = imaginary_frequencies(a, b, c, d, 5.0)
    assert len(w) == 2 and close(w[0], math.sqrt(0.96), 1e-9) and close(w[1], 1.0, 1e-9)
    assert imaginary_frequencies(a, b, c, d, 5.03) == []


def test_non_minimal_realization():
    # G = 1/(s + 4): the modes at -8 and -16 cancel.
    for lo, hi in (hinf_norm_bisection(*NON_MINIMAL, eps=EPS)[:2],
                   hinf_norm_level_set(*NON_MINIMAL, eps=EPS)[:2]):
        assert close(lo, 0.25) and close(hi, 0.25)


def test_feedthrough():
    lo, hi, _ = hinf_norm_bisection(*PEAK_AT_ZERO, eps=EPS)
    assert close(lo, 2.0) and close(hi, 2.0)
    lo, hi, w, _ = hinf_norm_level_set(*PEAK_AT_ZERO, eps=EPS)
    assert close(lo, 2.0) and w == 0.0
    lo, hi, _ = hinf_norm_bisection(*PEAK_AT_INFINITY, eps=EPS)
    assert close(lo, 1.0) and close(hi, 1.0)
    lo, hi, w, _ = hinf_norm_level_set(*PEAK_AT_INFINITY, eps=EPS)
    assert close(lo, 1.0) and w == math.inf


def test_not_hurwitz():
    with pytest.raises(ValueError):
        hinf_norm_bisection([[1]], [[1]], [[1]], [[0]])
    with pytest.raises(ValueError):
        hinf_norm_level_set([[0, 1], [-1, 0]], [[0], [1]], [[1, 0]], [[0]])


def test_random_systems():
    rng = random.Random(20240611)
    for _ in range(12):
        sys = random_system(rng)
        a, b, c, d = sys
        n = len(a)
        lo1, hi1, it = hinf_norm_bisection(*sys, eps=EPS)
        lo2, hi2, w2, _ = hinf_norm_level_set(*sys, eps=EPS)
        # The difference of two close floats carries a relative error near 1e-8.
        assert hi1 - lo1 <= 2 * EPS * lo1 * (1 + 1e-6)
        assert hi2 - lo2 <= 2 * EPS * lo2 * (1 + 1e-6)
        # The two intervals hold the same number.
        assert max(lo1, lo2) <= min(hi1, hi2) * (1 + 1e-9)
        # The proved bound on the number of bisection steps.
        assert it <= math.ceil(math.log2(n / EPS))
        # The start interval of the bisection holds the norm.
        hsv = hankel_singular_values(a, b, c)
        sd = sigma_max(a, b, c, d, 1e12)
        assert max(sd, hsv[0]) <= hi1 * (1 + 1e-9)
        assert lo1 <= (sd + 2 * sum(hsv)) * (1 + 1e-9)
        # The level set lower bound is a value of sigma_max.
        if w2 != math.inf:
            assert close(sigma_max(a, b, c, d, w2), lo2, 1e-12)
        # A dense sweep never beats the upper bound, and it finds the peak.
        s = sweep(sys)
        assert s <= hi1 * (1 + 1e-9)
        assert s >= lo1 * (1 - 1e-6)


def test_decision_against_exact_sturm_count():
    rng = random.Random(7)
    checked = 0
    for _ in range(10):
        sys = random_system(rng)
        a, b, c, d = sys
        lo, hi, _ = hinf_norm_bisection(*sys, eps=EPS)
        sd = max(singular_values([[complex(v) for v in row] for row in d]))
        for factor in (F(1, 2), F(4, 5), F(19, 20), F(21, 20), F(5, 4), F(2)):
            gamma = F(lo).limit_denominator(10 ** 6) * factor
            if gamma <= sd * 1.001:
                continue
            exact = even_polynomial(hamiltonian(a, b, c, d, gamma))
            has_exact = sturm_count_nonpositive(exact) > 0
            assert has_exact == (factor < 1)
            assert bool(imaginary_frequencies(a, b, c, d, float(gamma))) == has_exact
            checked += 1
    assert checked >= 20


def test_frequencies_are_singular_values():
    rng = random.Random(11)
    for _ in range(10):
        sys = random_system(rng)
        a, b, c, d = sys
        lo, _, _ = hinf_norm_bisection(*sys, eps=EPS)
        sd = max(singular_values([[complex(v) for v in row] for row in d]))
        gamma = 0.8 * lo
        if gamma <= sd * 1.001:
            continue
        ws = imaginary_frequencies(a, b, c, d, gamma)
        assert ws
        for w in ws:
            g = freq_response(a, b, c, d, w)
            sv = singular_values(g) if len(g[0]) <= 2 else None
            assert min(abs(s - gamma) for s in sv) <= 1e-6 * gamma
