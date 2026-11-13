# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-predictive-coding/. The authors are listed in prov/YG23QB.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from linear_predictive_coding import (
    autocorrelation,
    durbin,
    hann_window,
    lpc_analyze,
    lpc_gain,
    lpc_residual,
    lpc_synthesize,
)


def solve_exact(a, b):
    """Gaussian elimination with pivot search, in Fraction."""
    n = len(a)
    m = [[F(v) for v in row] + [F(bb)] for row, bb in zip(a, b)]
    for c in range(n):
        piv = next(i for i in range(c, n) if m[i][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def direct_autocorr(s, p):
    """r[k] = sum over all integers n of s[n] s[n - k], with zeros outside."""
    n = len(s)
    get = lambda i: s[i] if 0 <= i < n else 0
    return [sum(get(i) * get(i - k) for i in range(-p, n + p)) for k in range(p + 1)]


def poly_roots(coef):
    """Roots of z^p + coef[0] z^(p-1) + ... + coef[p-1] by Durand-Kerner."""
    p = len(coef)
    poly = lambda z: sum(c * z ** (p - 1 - i) for i, c in enumerate(coef)) + z ** p
    roots = [complex(0.4, 0.9) ** i for i in range(p)]
    for _ in range(2000):
        new = []
        for i, z in enumerate(roots):
            den = 1
            for j, w in enumerate(roots):
                if i != j:
                    den *= z - w
            new.append(z - poly(z) / den)
        done = max(abs(u - v) for u, v in zip(new, roots)) < 1e-14
        roots = new
        if done:
            break
    return roots, max(abs(poly(z)) for z in roots)


def test_example_frame() -> None:
    a, k, err = lpc_analyze([F(1), F(2), F(1)], 2)
    assert autocorrelation([1, 2, 1], 2) == [6, 4, 1]
    assert a == [1, F(-1, 2)] and k == [F(2, 3), F(-1, 2)] and err == F(5, 2)
    e = lpc_residual([1, 2, 1], a)
    assert e == [1, 1, F(-1, 2), 0, F(1, 2)]
    assert sum(v * v for v in e) == err
    assert lpc_synthesize(a, 1, e) == [1, 2, 1, 0, 0]
    assert abs(lpc_gain(err) - math.sqrt(2.5)) < 1e-15


def test_matches_direct_toeplitz_solve() -> None:
    rng = random.Random(5101)
    for _ in range(600):
        n = rng.randint(1, 12)
        x = [F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)]
        if all(v == 0 for v in x):
            continue
        p = rng.randint(1, 8)
        r = direct_autocorr(x, p)
        assert autocorrelation(x, p) == r
        a, k, err = lpc_analyze(x, p)
        mat = [[r[abs(i - j)] for j in range(p)] for i in range(p)]
        want = solve_exact(mat, r[1:p + 1])
        assert a == want
        assert err == r[0] - sum(ai * ri for ai, ri in zip(a, r[1:]))
        assert err > 0 and all(abs(ki) < 1 for ki in k)
        e = lpc_residual(x, a)
        assert sum(v * v for v in e) == err


def test_minimizes_residual_energy() -> None:
    rng = random.Random(5102)
    for _ in range(300):
        n, p = rng.randint(2, 10), rng.randint(1, 5)
        x = [F(rng.randint(-5, 5)) for _ in range(n)]
        if all(v == 0 for v in x):
            continue
        a, _, err = lpc_analyze(x, p)
        b = [ai + F(rng.randint(-3, 3), 7) for ai in a]
        energy = sum(v * v for v in lpc_residual(x, b))
        assert energy >= err
        assert (energy == err) == (b == a)


def ar_autocorr(poles, kmax):
    """Exact autocorrelation of x = h * e, unit white e, H = prod 1/(1 - q z^-1).

    The poles must be distinct. h[n] = sum_i c_i q_i^n by partial fractions,
    and sum_n q_i^n q_j^(n + k) = q_j^k / (1 - q_i q_j).
    """
    c = []
    for i, qi in enumerate(poles):
        prod = F(1)
        for j, qj in enumerate(poles):
            if i != j:
                prod *= 1 - qj / qi
        c.append(1 / prod)
    return [sum(ci * cj * qj ** k / (1 - qi * qj) for ci, qi in zip(c, poles) for cj, qj in zip(c, poles))
            for k in range(kmax + 1)]


def poly_from_poles(poles):
    """a with A(z) = 1 - sum a_k z^-k = prod (1 - q z^-1)."""
    coef = [F(1)]
    for q in poles:
        coef = [x - q * y for x, y in zip(coef + [F(0)], [F(0)] + coef)]
    return [-v for v in coef[1:]]


def test_recovers_ar2_from_exact_autocorrelation() -> None:
    r = ar_autocorr([F(1, 2), F(1, 4)], 6)
    assert r[:3] == [F(64, 35), F(128, 105), F(24, 35)]
    a, k, err = durbin(r, 2)
    assert a == [F(3, 4), F(-1, 8)] and err == 1
    a4, _, err4 = durbin(r, 6)
    assert a4 == [F(3, 4), F(-1, 8), 0, 0, 0, 0] and err4 == 1


def test_recovers_random_ar_models() -> None:
    rng = random.Random(5103)
    for _ in range(80):
        order = rng.randint(1, 4)
        poles = []
        while len(poles) < order:
            q = F(rng.randint(-9, 9), 10)
            if q != 0 and q not in poles:
                poles.append(q)
        r = ar_autocorr(poles, order + 2)
        a, _, err = durbin(r, order + 2)
        assert a == poly_from_poles(poles) + [0, 0]
        assert err == 1


def test_prediction_filter_is_minimum_phase() -> None:
    rng = random.Random(5104)
    for trial in range(500):
        n = rng.randint(3, 40)
        x = [rng.randint(-20, 20) for _ in range(n)]
        if all(v == 0 for v in x):
            continue
        p = rng.randint(1, 6)
        win = hann_window(n) if trial % 2 else None
        a, k, err = lpc_analyze(x, p, win)
        if err == 0:
            continue
        roots, resid = poly_roots([-float(v) for v in a])
        assert resid < 1e-8
        assert max(abs(z) for z in roots) < 1
        assert all(abs(ki) < 1 for ki in k)


def test_synthesis_inverts_analysis() -> None:
    rng = random.Random(5105)
    for _ in range(200):
        n, p = rng.randint(1, 15), rng.randint(1, 6)
        x = [F(rng.randint(-9, 9)) for _ in range(n)]
        if all(v == 0 for v in x):
            continue
        a, _, _ = lpc_analyze(x, p)
        assert lpc_synthesize(a, 1, lpc_residual(x, a)) == x + [0] * p


def test_silent_frame_and_errors() -> None:
    assert lpc_analyze([0, 0, 0], 2) == ([0, 0], [0, 0], 0)
    with pytest.raises(ValueError):
        lpc_analyze([], 2)
    with pytest.raises(ValueError):
        durbin([1, 1, 1], 2)  # the Toeplitz matrix of (1, 1, 1) is singular
