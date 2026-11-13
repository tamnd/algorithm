# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiener-filter/. The authors are listed in prov/F5ZCZM.jsonl.

import cmath
import math
import random
from fractions import Fraction as F

import pytest

from wiener_filter import apply_fir, dft, solve_linear, wiener_dft, wiener_fir, wiener_gain


def gauss_jordan(a, b):
    """Independent solver: Gauss-Jordan elimination, first nonzero pivot."""
    n = len(a)
    m = [list(row) + [bb] for row, bb in zip(a, b)]
    for c in range(n):
        piv = next(i for i in range(c, n) if m[i][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [u - f * v for u, v in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def test_ar1_in_white_noise() -> None:
    # x[n] = x[n-1]/2 + e[n], var e = 1, observed in unit white noise; d = x.
    rs = lambda k: F(4, 3) * F(1, 2) ** k
    want = {1: ([F(4, 7)], F(4, 7)), 2: ([F(8, 15), F(2, 15)], F(8, 15)),
            3: ([F(17, 32), F(1, 8), F(1, 32)], F(17, 32))}
    for m, (w_want, j_want) in want.items():
        rx = [rs(k) + (1 if k == 0 else 0) for k in range(m)]
        rdx = [rs(k) for k in range(m)]
        w, j = wiener_fir(rx, rdx, F(4, 3), m)
        assert w == w_want and j == j_want
    # the error decreases toward the causal limit (sqrt(65) - 7) / 2
    rx = [float(rs(k)) + (1 if k == 0 else 0) for k in range(30)]
    w, j = wiener_fir(rx, [float(rs(k)) for k in range(30)], 4 / 3, 30)
    assert abs(j - (math.sqrt(65) - 7) / 2) < 1e-12


def periodic_case(rng, m):
    p = rng.randint(m + 1, m + 6)
    z = [F(rng.randint(-4, 4)) for _ in range(p)]
    q = [F(rng.randint(-4, 4)) for _ in range(p)]
    mean = lambda f: sum(f(n) for n in range(p)) / p
    rx = [mean(lambda n: z[n] * z[(n - k) % p]) for k in range(m)]
    rdx = [mean(lambda n: q[n] * z[(n - k) % p]) for k in range(m)]
    var_d = mean(lambda n: q[n] * q[n])
    return p, z, q, rx, rdx, var_d


def test_against_brute_force_mmse() -> None:
    """The joint law: n uniform on one period; u = (x[n], .., x[n-M+1])."""
    rng = random.Random(5201)
    done = 0
    while done < 500:
        m = rng.randint(1, 4)
        p, z, q, rx, rdx, var_d = periodic_case(rng, m)
        mat = [[rx[abs(i - j)] for j in range(m)] for i in range(m)]
        try:
            want = gauss_jordan(mat, rdx)
        except StopIteration:
            continue  # singular second-moment matrix
        w, jmin = wiener_fir(rx, rdx, var_d, m)
        assert w == want
        err = lambda v: [q[n] - sum(v[k] * z[(n - k) % p] for k in range(m)) for n in range(p)]
        e = err(w)
        assert sum(x * x for x in e) / p == jmin  # E[(d - w.u)^2] by enumeration
        for k in range(m):  # orthogonality principle
            assert sum(e[n] * z[(n - k) % p] for n in range(p)) == 0
        v = [wk + F(rng.randint(-2, 2), 5) for wk in w]
        ev = err(v)
        assert sum(x * x for x in ev) / p >= jmin
        done += 1


def test_dft_matches_definition() -> None:
    rng = random.Random(5202)
    for n in (1, 2, 3, 6, 8, 16):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        want = [sum(a[t] * cmath.exp(-2j * cmath.pi * k * t / n) for t in range(n)) for k in range(n)]
        assert max(abs(u - v) for u, v in zip(dft(a), want)) < 1e-12
        back = dft(dft(a), inverse=True)
        assert max(abs(u - v) for u, v in zip(back, a)) < 1e-12


def even_spectrum(rng, n):
    s = [rng.uniform(0.1, 3.0) for _ in range(n)]
    return [(s[m] + s[-m % n]) / 2 for m in range(n)]


def test_dft_gain_equals_matrix_mmse() -> None:
    """x_hat = C_x (C_x + C_n)^-1 y for circulant covariances, against the DFT gain."""
    rng = random.Random(5203)
    for _ in range(120):
        n = rng.choice([4, 6, 8, 16])
        sx, sn = even_spectrum(rng, n), even_spectrum(rng, n)
        corr = lambda s, k: sum(s[m] * cmath.exp(2j * cmath.pi * m * k / n) for m in range(n)).real / n
        cx = [[corr(sx, (i - j) % n) for j in range(n)] for i in range(n)]
        cn = [[corr(sn, (i - j) % n) for j in range(n)] for i in range(n)]
        y = [rng.uniform(-2, 2) for _ in range(n)]
        zvec = gauss_jordan([[cx[i][j] + cn[i][j] for j in range(n)] for i in range(n)], y)
        want = [sum(cx[i][j] * zvec[j] for j in range(n)) for i in range(n)]
        got = wiener_dft(y, sx, sn)
        assert max(abs(u - v) for u, v in zip(got, want)) < 1e-9


def test_gain_values() -> None:
    assert wiener_gain([1.0, 3.0, 0.0, 0.0], [1.0, 1.0, 2.0, 0.0]) == [0.5, 0.75, 0.0, 0.0]
    # the example on the page: impulse response of the gain (3/4, 1/2, 0, 1/2)
    got = wiener_dft([1.0, 0.0, 0.0, 0.0], [3.0, 1.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0])
    assert max(abs(u - v) for u, v in zip(got, [7 / 16, 3 / 16, -1 / 16, 3 / 16])) < 1e-15


def test_monte_carlo_error_of_two_tap_filter() -> None:
    rng = random.Random(5204)
    x, w = 0.0, [8 / 15, 2 / 15]
    prev_y, total, count = 0.0, 0.0, 0
    for n in range(200000):
        x = 0.5 * x + rng.gauss(0, 1)
        y = x + rng.gauss(0, 1)
        if n > 100:
            est = w[0] * y + w[1] * prev_y
            total += (x - est) ** 2
            count += 1
        prev_y = y
    assert abs(total / count - 8 / 15) < 0.01


def test_apply_fir_and_errors() -> None:
    assert apply_fir([1, 2], [1, 0, 0, 3]) == [1, 2, 0, 3]
    with pytest.raises(ValueError):
        solve_linear([[1, 2], [2, 4]], [1, 2])
