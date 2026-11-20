# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ayers-dainty-blind-deconvolution/. The authors are listed in prov/MB6VNZ.jsonl.

import math
import random

from ayers_dainty_blind_deconvolution import (
    ayers_dainty,
    conv2,
    dft2,
    idft2,
    misfit,
    project_psf,
    shift,
    wiener_update,
)

N = 12


def problem(seed, n=N, lo=2, hi=9):
    """A sparse positive object in rows and columns lo..hi and a random positive 3 x 3 PSF."""
    rng = random.Random(seed)
    f = [[0.0] * n for _ in range(n)]
    for i in range(lo, hi + 1):
        for j in range(lo, hi + 1):
            f[i][j] = rng.random() if rng.random() < 0.5 else 0.0
    h = [[0.0] * n for _ in range(n)]
    for a in range(-1, 2):
        for b in range(-1, 2):
            h[a % n][b % n] = rng.uniform(0.1, 1.0)
    s = sum(map(sum, h))
    h = [[v / s for v in r] for r in h]
    sup = [[min(i, n - i) <= 1 and min(j, n - j) <= 1 for j in range(n)] for i in range(n)]
    return f, h, sup


def rel_err(a, b):
    num = sum((p - q) ** 2 for ra, rb in zip(a, b) for p, q in zip(ra, rb))
    return math.sqrt(num / sum(q * q for rb in b for q in rb))


def start(y, sup, seed):
    """A random positive start image near the mean of the data and a flat PSF on its support.

    A flat start image has a spectrum that is zero except at frequency 0, up to
    rounding, and the first division would then divide by rounding errors.
    """
    mean = sum(map(sum, y)) / (len(y) * len(y[0]))
    rng = random.Random(100 + seed)
    f0 = [[mean * rng.uniform(0.5, 1.5) for _ in row] for row in y]
    h0 = [[1.0 if s else 0.0 for s in row] for row in sup]
    return f0, h0


def test_convolution_theorem_and_round_trip():
    rng = random.Random(1)
    x = [[rng.random() for _ in range(5)] for _ in range(4)]
    h = [[rng.random() for _ in range(5)] for _ in range(4)]
    lhs = dft2(conv2(x, h))
    xf, hf = dft2(x), dft2(h)
    assert max(abs(lhs[i][j] - xf[i][j] * hf[i][j]) for i in range(4) for j in range(5)) < 1e-12
    back = idft2(xf)
    assert max(abs(back[i][j] - x[i][j]) for i in range(4) for j in range(5)) < 1e-13


def test_wiener_update_is_the_regularized_least_squares_minimizer():
    # In the image domain B = dft2(b) minimizes ||y - a * b||^2 + alpha ||b||^2 (Parseval).
    rng = random.Random(2)
    n1, n2, alpha = 4, 5, 0.3
    a = [[rng.random() for _ in range(n2)] for _ in range(n1)]
    y = [[rng.random() for _ in range(n2)] for _ in range(n1)]
    b = [[v.real for v in row] for row in idft2(wiener_update(dft2(y), dft2(a), alpha))]

    def cost(bb):
        r = conv2(a, bb)
        fit = sum((p - q) ** 2 for rp, rq in zip(y, r) for p, q in zip(rp, rq))
        return fit + alpha * sum(v * v for row in bb for v in row)

    c0 = cost(b)
    for _ in range(200):
        eps = 10 ** rng.uniform(-4, -1)
        bb = [[v + eps * rng.gauss(0, 1) for v in row] for row in b]
        assert cost(bb) >= c0 - 1e-12


def test_shift_and_scale_give_the_same_data():
    f, h, _ = problem(3)
    y = conv2(f, h)
    y2 = conv2(shift(f, 1, -2), shift(h, -1, 2))
    y3 = conv2([[2.5 * v for v in r] for r in f], [[v / 2.5 for v in r] for r in h])
    assert rel_err(y2, y) < 1e-13 and rel_err(y3, y) < 1e-13


def test_true_pair_is_a_fixed_point_without_regularization():
    f, h, sup = problem(2)
    y = conv2(f, h)
    assert min(abs(v) for row in dft2(f) for v in row) > 1e-6
    f1, h1 = ayers_dainty(y, f, h, support=sup, alpha=0.0, iters=3)
    assert rel_err(f1, f) < 1e-9 and rel_err(h1, h) < 1e-9


def test_trivial_pair_is_a_fixed_point_and_attracts_the_start_f0_equal_y():
    f, h, sup = problem(1)
    y = conv2(f, h)
    rng = random.Random(4)
    h0 = [[rng.random() if s else 0.0 for s in row] for row in sup]
    f1, h1 = ayers_dainty(y, y, h0, support=sup, alpha=0.0, iters=5)
    assert abs(h1[0][0] - 1.0) < 1e-12
    assert sum(abs(v) for row in h1 for v in row) - h1[0][0] < 1e-12
    assert rel_err(f1, y) < 1e-12 and misfit(y, f1, h1) < 1e-12


def test_constraints_hold_after_every_pass():
    f, h, sup = problem(5)
    y = conv2(f, h)
    rng = random.Random(6)
    y = [[v + rng.gauss(0, 0.01) for v in row] for row in y]
    osup = [[1 <= i <= 10 and 1 <= j <= 10 for j in range(N)] for i in range(N)]
    f0, h0 = start(y, sup, 5)
    seen = []

    def check(k, fk, hk):
        seen.append(k)
        assert min(min(r) for r in fk) >= 0 and min(min(r) for r in hk) >= 0
        assert abs(sum(map(sum, hk)) - 1.0) < 1e-12
        for i in range(N):
            for j in range(N):
                if not sup[i][j]:
                    assert hk[i][j] == 0.0
                if not osup[i][j]:
                    assert fk[i][j] == 0.0

    ayers_dainty(y, f0, h0, support=sup, obj_support=osup, alpha=1e-3, beta=0.5, iters=8, callback=check)
    assert seen == list(range(1, 9))


def test_psf_projection_keeps_the_old_psf_when_nothing_positive_is_left():
    sup = [[True, False], [False, False]]
    old = [[1.0, 0.0], [0.0, 0.0]]
    assert project_psf([[-1 + 0j, 2 + 0j], [3 + 0j, 4 + 0j]], sup, old) == old


def test_measured_recovery_on_seed_2():
    # A measurement, not a theorem: on this problem 110 passes recover f and h.
    f, h, sup = problem(2)
    y = conv2(f, h)
    f0, h0 = start(y, sup, 2)
    f1, h1 = ayers_dainty(y, f0, h0, support=sup, alpha=0.0, iters=110)
    assert rel_err(f1, f) < 1e-3 and rel_err(h1, h) < 1e-3


def test_misfit_is_not_monotone_on_seed_1():
    # A measurement: the alternation has no descent property.
    f, h, sup = problem(1)
    y = conv2(f, h)
    f0, h0 = start(y, sup, 1)
    vals = []
    ayers_dainty(y, f0, h0, support=sup, alpha=0.0, iters=30, callback=lambda k, fk, hk: vals.append(misfit(y, fk, hk)))
    assert any(vals[k + 1] > vals[k] * 1.01 for k in range(len(vals) - 1))
