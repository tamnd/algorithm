# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/richardson-lucy-total-variation/. The authors are listed in prov/DC5KCE.jsonl.

import math
import random

import pytest

from imgkit import circ_conv2, img_norm, poisson_sample
from richardson_lucy_total_variation import (
    div,
    grad,
    neg_log_likelihood,
    objective,
    rl_correction,
    rltv,
    tv,
    tv_curvature,
)


def gaussian_psf(n, sigma):
    h = [[0.0] * n for _ in range(n)]
    for di in range(-2, 3):
        for dj in range(-2, 3):
            h[di % n][dj % n] = math.exp(-(di * di + dj * dj) / (2 * sigma * sigma))
    s = sum(map(sum, h))
    return [[v / s for v in row] for row in h]


def rand_img(rng, n1, n2, lo=0.5, hi=3.0):
    return [[rng.uniform(lo, hi) for _ in range(n2)] for _ in range(n1)]


def inner(a, b):
    return sum(p * q for ra, rb in zip(a, b) for p, q in zip(ra, rb))


def diff(a, b):
    return [[p - q for p, q in zip(ra, rb)] for ra, rb in zip(a, b)]


def numeric_grad(f, x, h=1e-6):
    out = []
    for i in range(len(x)):
        row = []
        for j in range(len(x[0])):
            xp = [list(r) for r in x]
            xm = [list(r) for r in x]
            xp[i][j] += h
            xm[i][j] -= h
            row.append((f(xp) - f(xm)) / (2 * h))
        out.append(row)
    return out


def matrix_em_step(x, y, h):
    """The EM update for Poisson data with an explicit blur matrix, as a reference."""
    n1, n2 = len(x), len(x[0])
    n = n1 * n2
    a = [[h[(i1 - j1) % n1][(i2 - j2) % n2] for j1 in range(n1) for j2 in range(n2)]
         for i1 in range(n1) for i2 in range(n2)]
    xv = [v for row in x for v in row]
    yv = [v for row in y for v in row]
    b = [sum(a[i][j] * xv[j] for j in range(n)) for i in range(n)]
    col = [sum(a[i][j] for i in range(n)) for j in range(n)]
    out = [xv[j] / col[j] * sum(a[i][j] * yv[i] / b[i] for i in range(n) if yv[i] > 0) for j in range(n)]
    return [out[i * n2:(i + 1) * n2] for i in range(n1)]


def test_div_is_the_negative_adjoint_of_grad():
    rng = random.Random(1)
    x = rand_img(rng, 5, 7, -1, 1)
    p1, p2 = rand_img(rng, 5, 7, -1, 1), rand_img(rng, 5, 7, -1, 1)
    g1, g2 = grad(x)
    lhs = inner(g1, p1) + inner(g2, p2)
    rhs = -inner(x, div(p1, p2))
    scale = math.sqrt(img_norm(g1) ** 2 + img_norm(g2) ** 2) * math.sqrt(img_norm(p1) ** 2 + img_norm(p2) ** 2)
    assert abs(lhs - rhs) <= 1e-10 * scale


def test_blur_adjoint():
    rng = random.Random(2)
    h = gaussian_psf(8, 1.0)
    x, y = rand_img(rng, 8, 8, -1, 1), rand_img(rng, 8, 8, -1, 1)
    hx = circ_conv2(x, h)
    ht = [[h[(-i) % 8][(-j) % 8] for j in range(8)] for i in range(8)]
    assert abs(inner(hx, y) - inner(x, circ_conv2(y, ht))) <= 1e-10 * img_norm(hx) * img_norm(y)


def test_tv_curvature_is_minus_the_tv_gradient_and_is_bounded():
    rng = random.Random(3)
    x = rand_img(rng, 6, 6)
    eps = 0.1
    num = numeric_grad(lambda z: tv(z, eps), x)
    kappa = tv_curvature(x, eps)
    for rn, rk in zip(num, kappa):
        for a, b in zip(rn, rk):
            assert abs(a + b) < 1e-6
    for _ in range(5):
        z = rand_img(rng, 6, 6, 0, 10)
        assert all(-4 <= v <= 4 for row in tv_curvature(z, 1e-6) for v in row)


def test_poisson_gradient_is_one_minus_the_rl_correction():
    rng = random.Random(4)
    h = gaussian_psf(6, 0.8)
    x = rand_img(rng, 6, 6)
    y = [[float(rng.randint(0, 5)) for _ in range(6)] for _ in range(6)]
    num = numeric_grad(lambda z: neg_log_likelihood(z, y, h), x)
    c = rl_correction(x, y, h)
    for rn, rc in zip(num, c):
        for a, b in zip(rn, rc):
            assert abs(a - (1 - b)) < 1e-6


def test_the_step_is_a_scaled_gradient_step():
    # x+ - x = -(x / (1 - lam kappa)) * grad J, so x is a fixed point exactly where grad J = 0.
    rng = random.Random(5)
    h = gaussian_psf(6, 0.8)
    x = rand_img(rng, 6, 6)
    y = [[float(rng.randint(0, 6)) for _ in range(6)] for _ in range(6)]
    lam, eps = 0.05, 0.2
    num = numeric_grad(lambda z: objective(z, y, h, lam, eps), x)
    kappa = tv_curvature(x, eps)
    xp = rltv(y, h, lam, 1, x0=x, eps=eps)
    for i in range(6):
        for j in range(6):
            expect = x[i][j] - x[i][j] / (1 - lam * kappa[i][j]) * num[i][j]
            assert abs(xp[i][j] - expect) < 1e-5


def test_lam_zero_is_richardson_lucy():
    rng = random.Random(6)
    h = gaussian_psf(6, 1.0)
    y = [[float(rng.randint(0, 9)) for _ in range(6)] for _ in range(6)]
    mean =sum(map(sum, y)) / 36
    ref = [[mean] * 6 for _ in range(6)]
    for _ in range(3):
        ref = matrix_em_step(ref, y, h)
    x = rltv(y, h, 0.0, 3)
    assert img_norm(diff(x, ref)) < 1e-10 * img_norm(ref)


def test_delta_psf_gives_the_data_in_one_step():
    rng = random.Random(7)
    delta = [[1.0 if (i, j) == (0, 0) else 0.0 for j in range(5)] for i in range(5)]
    y = rand_img(rng, 5, 5)
    x = rltv(y, delta, 0.0, 1, x0=rand_img(rng, 5, 5))
    assert img_norm(diff(x, y)) < 1e-12 * img_norm(y)


def test_positivity_for_small_lam_and_failure_for_large_lam():
    rng = random.Random(8)
    h = gaussian_psf(8, 1.0)
    y = [[float(rng.randint(0, 20)) for _ in range(8)] for _ in range(8)]
    x = rltv(y, h, 0.24, 20, eps=1e-6)
    assert all(v >= 0 for row in x for v in row)
    pit = [[1.0] * 8 for _ in range(8)]
    pit[3][3] = 0.01
    with pytest.raises(ValueError):
        rltv(y, h, 0.5, 1, x0=pit, eps=1e-6)


def test_tv_term_lowers_the_error_on_noisy_counts():
    # A measurement on one seed: a piecewise constant phantom, Poisson counts, 80 iterations.
    n = 16
    rng = random.Random(9)
    xt = [[20.0 + (60.0 if 4 <= i < 11 and 5 <= j < 12 else 0.0) for j in range(n)] for i in range(n)]
    h = gaussian_psf(n, 1.0)
    b = circ_conv2(xt, h)
    y = [[float(poisson_sample(rng, v)) for v in row] for row in b]
    rl = rltv(y, h, 0.0, 80)
    tvx = rltv(y, h, 0.02, 80, eps=1e-2)
    e_rl = img_norm(diff(rl, xt))
    e_tv = img_norm(diff(tvx, xt))
    assert e_tv < 0.9 * e_rl
