# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-cittert-deconvolution/. The authors are listed in prov/3D8AWP.jsonl.

import math
import random
from fractions import Fraction as F

from imgkit import dft, disk_phantom, gauss_noise, img_norm
from van_cittert_deconvolution import (
    blur,
    blur_adjoint,
    converges,
    filter_factors,
    otf,
    van_cittert,
    van_cittert_landweber,
)


def norm(v):
    return math.sqrt(sum(abs(t) ** 2 for t in v))


def sub(a, b):
    return [p - q for p, q in zip(a, b)]


def psf_1d(n, taps):
    """A PSF of length n with taps[d] at offset d (d may be negative), centered at index 0."""
    h = [0] * n
    for d, v in taps.items():
        h[d % n] += v
    return h


def test_delta_psf_is_the_identity():
    rng = random.Random(1)
    x = [rng.uniform(-1, 1) for _ in range(12)]
    delta = [1] + [0] * 11
    assert blur(x, delta) == x
    assert van_cittert(x, delta, beta=1, iters=1) == x
    img = [[rng.random() for _ in range(5)] for _ in range(4)]
    delta2 = [[1 if (i, j) == (0, 0) else 0 for j in range(5)] for i in range(4)]
    assert blur(img, delta2) == img


def test_adjoint_of_the_blur():
    rng = random.Random(2)
    for n in (8, 13, 16):
        h = [rng.random() for _ in range(n)]
        x = [rng.gauss(0, 1) for _ in range(n)]
        y = [rng.gauss(0, 1) for _ in range(n)]
        ax = blur(x, h)
        gap = abs(sum(a * b for a, b in zip(ax, y)) - sum(a * b for a, b in zip(x, blur_adjoint(y, h))))
        assert gap <= 1e-10 * norm(ax) * norm(y)
    h2 = [[rng.random() for _ in range(6)] for _ in range(5)]
    x2 = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(5)]
    y2 = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(5)]
    ax2 = blur(x2, h2)
    lhs = sum(a * b for ra, rb in zip(ax2, y2) for a, b in zip(ra, rb))
    rhs = sum(a * b for ra, rb in zip(x2, blur_adjoint(y2, h2)) for a, b in zip(ra, rb))
    assert abs(lhs - rhs) <= 1e-10 * img_norm(ax2) * img_norm(y2)


def test_exact_iterates_match_the_matrix_series():
    # x_K = beta sum_{j < K} (I - beta A)^j y with the dense circulant matrix A.
    rng = random.Random(3)
    for _ in range(5):
        n = rng.choice([5, 6, 8])
        raw = [rng.randint(0, 3) for _ in range(n)]
        raw[0] += 1
        h = [F(v, sum(raw)) for v in raw]
        a = [[h[(i - j) % n] for j in range(n)] for i in range(n)]
        beta = F(rng.randint(1, 3), 2)
        y = [F(rng.randint(-5, 5)) for _ in range(n)]
        iters = rng.randint(1, 6)
        term = list(y)
        total = [F(0)] * n
        for _ in range(iters):
            total = [t + beta * s for t, s in zip(total, term)]
            aterm = [sum(a[i][j] * term[j] for j in range(n)) for i in range(n)]
            term = [s - beta * q for s, q in zip(term, aterm)]
        assert van_cittert(y, h, beta=beta, iters=iters) == total


def test_filter_factors_in_the_fourier_domain():
    rng = random.Random(4)
    for _ in range(6):
        n = rng.choice([8, 12, 16])
        h = [rng.random() for _ in range(n)]
        s = sum(h)
        h = [v / s for v in h]
        y = [rng.gauss(0, 1) for _ in range(n)]
        beta = rng.uniform(0.2, 1.5)
        iters = rng.randint(1, 8)
        xk = dft(van_cittert(y, h, beta=beta, iters=iters))
        yk, hk = dft(y), otf(h)
        f = filter_factors(h, beta, iters)
        for k in range(n):
            expect = f[k] / hk[k] * yk[k]
            assert abs(xk[k] - expect) <= 1e-9 * (1 + abs(expect))


def test_check_values_of_the_filter_factor():
    # 1 - 0.99^100 is the Landweber check value of the area.
    h = [F(1)] + [F(0)] * 3
    f = filter_factors([1.0, 0.0, 0.0, 0.0], 0.01, 100)
    assert abs(f[0] - 0.63397) < 1e-5
    assert van_cittert([F(1), F(0), F(0), F(0)], h, beta=F(1, 2), iters=3) == [F(7, 8), 0, 0, 0]


def test_positive_otf_converges_and_the_error_never_grows():
    n = 32
    h = psf_1d(n, {0: F(2, 3), 1: F(1, 6), -1: F(1, 6)})
    hf = [float(v) for v in h]
    assert converges(hf, 1.0)
    rng = random.Random(5)
    xt = [rng.choice([0.0, 0.0, 1.0, 3.0]) for _ in range(n)]
    y = blur(xt, hf)
    errs = []
    van_cittert(y, hf, beta=1.0, iters=70, callback=lambda k, x: errs.append(norm(sub(x, xt))))
    for a, b in zip(errs, errs[1:]):
        assert b <= a * (1 + 1e-12)
    assert errs[-1] < 1e-9 * norm(xt)


def test_negative_otf_diverges():
    # Box of width 5 on 16 points: H_4 = -1/5, so |1 - beta H_4| > 1 for every beta > 0.
    n = 16
    h = psf_1d(n, {d: 0.2 for d in range(-2, 3)})
    assert abs(otf(h)[4] - (-0.2)) < 1e-12
    assert not converges(h, 1.0)
    xt = [math.cos(2 * math.pi * 4 * j / n) for j in range(n)]
    y = blur(xt, h)
    e10 = norm(sub(van_cittert(y, h, iters=10), xt))
    e20 = norm(sub(van_cittert(y, h, iters=20), xt))
    assert abs(e20 / e10 - 1.2 ** 10) < 1e-6 * 1.2 ** 10
    # The Landweber form uses |H|^2 > 0 and its error never grows.
    errs = [norm(sub(van_cittert_landweber(y, h, beta=1.0, iters=k), xt)) for k in (0, 5, 10, 40)]
    for a, b in zip(errs, errs[1:]):
        assert b <= a * (1 + 1e-12)
    assert errs[-1] < 0.5 * errs[0]


def test_noise_gives_semi_convergence():
    n = 32
    h = psf_1d(n, {0: 0.36, 1: 0.24, -1: 0.24, 2: 0.08, -2: 0.08})
    assert converges(h, 1.0)
    rng = random.Random(6)
    xt = [0.0] * n
    for j in range(10, 16):
        xt[j] = 1.0
    y = [a + b for a, b in zip(blur(xt, h), gauss_noise(rng, n, 0.02))]
    errs = []
    van_cittert(y, h, beta=1.0, iters=3000, callback=lambda k, x: errs.append(norm(sub(x, xt))))
    best = min(errs)
    assert errs.index(best) < len(errs) - 1
    assert errs[-1] > 2 * best


def test_image_deblurring_with_a_separable_psf():
    n = 16
    w = {0: 2 / 3, 1: 1 / 6, n - 1: 1 / 6}
    h = [[w.get(i, 0.0) * w.get(j, 0.0) for j in range(n)] for i in range(n)]
    xt = disk_phantom(n, 0.6)
    y = blur(xt, h)
    assert converges(h, 1.0)
    x = van_cittert(y, h, beta=1.0, iters=120)
    err = img_norm([[a - b for a, b in zip(ra, rb)] for ra, rb in zip(x, xt)])
    assert err < 1e-4 * img_norm(xt)
