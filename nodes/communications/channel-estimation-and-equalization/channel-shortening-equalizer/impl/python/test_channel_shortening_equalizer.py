# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-shortening-equalizer/. The authors are listed in prov/B8R7HN.jsonl.

import math
import random

import pytest

from channel_shortening_equalizer import best_delay, mssnr_teq, shortening_snr, window_wall


def mv(m, v):
    return [sum(a * b for a, b in zip(row, v)) for row in m]


def cholesky(a):
    n = len(a)
    r = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(r[i][k] * r[j][k] for k in range(j))
            r[i][j] = math.sqrt(s) if i == j else s / r[j][j]
    return r


def jacobi_eigenvalues(s):
    n = len(s)
    a = [row[:] for row in s]
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                sn = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - sn * akq, sn * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - sn * aqk, sn * apk + c * aqk
    return [a[i][i] for i in range(n)]


def largest_ssnr(a, b):
    # B w = lambda A w with A = R R^T is the symmetric problem (R^-1 B R^-T) u = lambda u
    n = len(a)
    r = cholesky(a)
    rinv = [[0.0] * n for _ in range(n)]
    for col in range(n):
        for i in range(n):
            s = (1.0 if i == col else 0.0) - sum(r[i][k] * rinv[k][col] for k in range(i))
            rinv[i][col] = s / r[i][i]
    c = [[sum(rinv[i][k] * b[k][l] * rinv[j][l] for k in range(n) for l in range(n)) for j in range(n)] for i in range(n)]
    return max(jacobi_eigenvalues(c))


def test_example_on_the_page() -> None:
    w, s = mssnr_teq([1, 0.5], 2, 0, 0)
    assert abs(w[1] / w[0] + 0.4) < 1e-12
    assert abs(s - 20) < 1e-9
    a, b = window_wall([1, 0.5], 2, 0, 0)
    assert a == [[0.25, 0.5], [0.5, 1.25]] and b == [[1, 0], [0, 0]]
    h = [0.8**k for k in range(8)]
    d, w, s = best_delay(h, 4, 2)
    assert d == 0 and abs(10 * math.log10(s) - 15.87) < 0.005
    base = max(shortening_snr(h, [1.0], 2, k) for k in range(6))
    assert abs(10 * math.log10(base) - 4.99) < 0.005


def test_eigen_residual_and_snr() -> None:
    rng = random.Random(7901)
    for _ in range(30):
        h = [rng.gauss(0, 1) for _ in range(rng.randint(3, 9))]
        lw, nu = rng.randint(2, 6), rng.randint(0, 3)
        d = rng.randint(0, len(h) + lw - 2 - nu)
        a, b = window_wall(h, lw, nu, d)
        try:
            w, s = mssnr_teq(h, lw, nu, d)
        except ValueError:
            continue
        mu = 1 / s
        aw, bw = mv(a, w), mv(b, w)
        assert abs(sum(x * y for x, y in zip(w, bw)) - 1) < 1e-9
        scale = max(1.0, max(abs(x) for x in aw))
        assert max(abs(x - mu * y) for x, y in zip(aw, bw)) < 1e-9 * scale
        assert abs(shortening_snr(h, w, nu, d) - s) < 1e-7 * s


def test_it_is_the_largest_generalized_eigenvalue() -> None:
    rng = random.Random(7902)
    checked = 0
    for _ in range(25):
        h = [rng.gauss(0, 1) for _ in range(rng.randint(4, 8))]
        lw, nu = rng.randint(2, 5), rng.randint(1, 2)
        d = rng.randint(0, len(h) + lw - 2 - nu)
        a, b = window_wall(h, lw, nu, d)
        w, s = mssnr_teq(h, lw, nu, d)
        assert abs(s - largest_ssnr(a, b)) < 1e-8 * s
        checked += 1
    assert checked == 25


def test_beats_random_search() -> None:
    rng = random.Random(7903)
    for _ in range(5):
        h = [rng.gauss(0, 1) for _ in range(7)]
        lw, nu, d = 4, 2, 2
        _, s = mssnr_teq(h, lw, nu, d)
        best = 0.0
        for _ in range(2000):
            w = [rng.gauss(0, 1) for _ in range(lw)]
            best = max(best, shortening_snr(h, w, nu, d))
        assert best <= s * (1 + 1e-12)
        assert best > 0.5 * s  # the search gets close, so the bound is not trivial


def test_best_delay_is_best() -> None:
    h = [0.3, 1, 0.8, 0.5, 0.3, 0.2, 0.1]
    d, _, s = best_delay(h, 3, 2)
    for k in range(len(h) + 3 - 1 - 2):
        assert mssnr_teq(h, 3, 2, k)[1] <= s * (1 + 1e-12)


def test_input_checks() -> None:
    with pytest.raises(ValueError):
        window_wall([1, 0.5], 2, 0, 3)
