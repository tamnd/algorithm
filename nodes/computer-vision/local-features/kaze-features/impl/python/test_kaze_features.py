# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kaze-features/. The authors are listed in prov/VCC3TB.jsonl.

import math
import random

from kaze_features import (aos_step, conductivity, contrast_factor, convolve, derivatives, describe, detect,
                           implicit_1d, kaze, level_sigmas, nonlinear_scale_space, orientation, scharr, thomas)


def random_image(seed, w, h):
    rng = random.Random(seed)
    return [[rng.randint(0, 255) for _ in range(w)] for _ in range(h)]


def dense_solve(m, d):
    """Gaussian elimination with partial pivoting, the reference for the Thomas algorithm."""
    n = len(d)
    a = [row[:] + [d[i]] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for j in range(c, n + 1):
                a[r][j] -= f * a[c][j]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (a[r][n] - sum(a[r][j] * x[j] for j in range(r + 1, n))) / a[r][r]
    return x


def test_thomas_matches_dense_elimination():
    rng = random.Random(1)
    for n in (1, 2, 5, 17):
        a = [0.0] + [rng.uniform(-1, 1) for _ in range(n - 1)]
        c = [rng.uniform(-1, 1) for _ in range(n - 1)] + [0.0]
        b = [abs(a[j]) + abs(c[j]) + rng.uniform(0.5, 2) for j in range(n)]
        d = [rng.uniform(-5, 5) for _ in range(n)]
        m = [[b[i] if i == j else a[i] if j == i - 1 else c[i] if j == i + 1 else 0.0 for j in range(n)]
             for i in range(n)]
        x, y = thomas(a, b, c, d), dense_solve(m, d)
        assert all(abs(p - q) < 1e-9 for p, q in zip(x, y))


def test_aos_keeps_the_mean_and_the_range():
    rng = random.Random(2)
    L = [[rng.random() for _ in range(12)] for _ in range(10)]
    g = [[rng.uniform(0.05, 1) for _ in range(12)] for _ in range(10)]
    for tau in (0.1, 3.0, 50.0):
        out = aos_step(L, g, tau)
        assert abs(sum(map(sum, out)) - sum(map(sum, L))) < 1e-9
        lo, hi = min(map(min, L)), max(map(max, L))
        assert all(lo - 1e-12 <= x <= hi + 1e-12 for row in out for x in row)
    flat = [[0.3] * 7 for _ in range(6)]
    assert all(abs(x - 0.3) < 1e-12 for row in aos_step(flat, g, 5.0) for x in row)


def test_small_steps_agree_with_the_explicit_scheme():
    rng = random.Random(3)
    f = [rng.random() for _ in range(9)]
    g = [rng.uniform(0.2, 1) for _ in range(9)]
    tau = 1e-4
    w = [(g[j] + g[j + 1]) / 2 for j in range(8)]
    af = [(w[j - 1] * (f[j - 1] - f[j]) if j > 0 else 0) + (w[j] * (f[j + 1] - f[j]) if j < 8 else 0)
          for j in range(9)]
    x = implicit_1d(f, g, tau)
    assert all(abs(x[j] - (f[j] + tau * af[j])) < 10 * tau * tau for j in range(9))


def test_contrast_and_conductivity():
    img = random_image(4, 16, 16)
    L = convolve([[x / 255 for x in row] for row in img], 1.6)
    k = contrast_factor(L)
    gu, gv = scharr(L, 1, 0), scharr(L, 1, 1)
    mags = [math.hypot(a, b) for ru, rv in zip(gu, gv) for a, b in zip(ru, rv)]
    below = sum(1 for m in mags if m < k) / len(mags)
    assert 0.65 <= below <= 0.75
    g = conductivity(L, k)
    assert all(0 < x <= 1 for row in g for x in row)
    assert all(x == 1.0 for row in conductivity([[0.5] * 6 for _ in range(6)], k) for x in row)


def test_the_nonlinear_space_keeps_an_edge():
    img = [[200 if u >= 12 else 40 for u in range(24)] for _ in range(8)]
    levels, sig, _ = nonlinear_scale_space(img, O=2, S=2)
    assert len(levels) == 4 and abs(sig[-1] - 1.6 * 2 ** 1.5) < 1e-12
    gauss = convolve([[x / 255 for x in row] for row in img], sig[-1])
    step = lambda L: L[4][12] - L[4][11]
    assert step(levels[-1]) > step(gauss)
    assert abs(sum(map(sum, levels[-1])) - sum(map(sum, levels[0]))) < 1e-9


def test_a_blob_is_detected_at_its_center():
    img = [[230 if (u - 15) ** 2 + (v - 16) ** 2 <= 9 else 20 for u in range(32)] for v in range(32)]
    feats = kaze(img, O=2, S=3)
    assert any((u, v) == (15, 16) for (u, v, s, t), _ in feats)
    for _, d in feats:
        assert len(d) == 64 and abs(math.sqrt(sum(x * x for x in d)) - 1) < 1e-12


def test_detect_returns_strict_maxima_above_the_threshold():
    rng = random.Random(5)
    dets = [[[rng.random() for _ in range(8)] for _ in range(7)] for _ in range(4)]
    found = detect(dets, [1, 2, 3, 4], threshold=0.2)
    brute = [(u, v, i, i + 1) for i in (1, 2) for v in range(1, 6) for u in range(1, 7)
             if dets[i][v][u] > 0.2 and dets[i][v][u] == max(dets[j][v + b][u + a] for j in (i - 1, i, i + 1)
                                                             for b in (-1, 0, 1) for a in (-1, 0, 1))]
    assert found == brute


def test_orientation_on_a_ramp():
    ramp = [[3.0 * u + 2.0 * v for u in range(40)] for v in range(40)]
    lu, lv, _ = derivatives(ramp, 1.0)
    assert abs(orientation(lu, lv, 20, 20, 1.5) - math.atan2(2, 3)) < 1e-12


def test_a_quarter_turn():
    n = 24
    img = random_image(6, n, n)
    rot = [[img[n - 1 - u][v] for u in range(n)] for v in range(n)]
    la, sa, ka = nonlinear_scale_space(img, O=1, S=3)
    lb, _, kb = nonlinear_scale_space(rot, O=1, S=3)
    assert abs(ka - kb) < 1e-12
    for A, B in zip(la, lb):
        assert all(abs(A[v][u] - B[u][n - 1 - v]) < 1e-9 for v in range(n) for u in range(n))
    s = sa[2]
    ua, va, _ = derivatives(la[2], s)
    ub, vb, _ = derivatives(lb[2], s)
    for u, v in [(12, 9), (8, 14)]:
        ta, tb = orientation(ua, va, u, v, s), orientation(ub, vb, n - 1 - v, u, s)
        assert abs(math.remainder(tb - ta - math.pi / 2, 2 * math.pi)) < 1e-9
        da, db = describe(ua, va, u, v, s, ta), describe(ub, vb, n - 1 - v, u, s, ta + math.pi / 2)
        assert all(abs(x - y) < 1e-9 for x, y in zip(da, db))


def test_gain_does_not_change_the_descriptor():
    img = random_image(7, 20, 20)
    a, _, _ = nonlinear_scale_space(img, O=1, S=2)
    b, _, _ = nonlinear_scale_space([[0.5 * x for x in row] for row in img], O=1, S=2)
    s = level_sigmas(O=1, S=2)[1]
    da = describe(*derivatives(a[1], s)[:2], 10, 9, s, 0.4)
    db = describe(*derivatives(b[1], s)[:2], 10, 9, s, 0.4)
    assert all(abs(x - y) < 1e-12 for x, y in zip(da, db))
