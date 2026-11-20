# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-deconvolution/. The authors are listed in prov/03GAAZ.jsonl.

import math
import random
from fractions import Fraction

from imgkit import circ_conv2, img_norm
from nearest_neighbor_deconvolution import blur_stack, nearest_neighbor, wiener_2d


def gpsf(n, sigma):
    h = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            di = i if i <= n // 2 else i - n
            dj = j if j <= n // 2 else j - n
            h[i][j] = math.exp(-(di * di + dj * dj) / (2 * sigma * sigma))
    s = sum(map(sum, h))
    return [[v / s for v in r] for r in h]


def delta(n):
    return [[1 if (i, j) == (0, 0) else 0 for j in range(n)] for i in range(n)]


def rand_stack(rng, nz, n, lo=-1.0, hi=1.0):
    return [[[rng.uniform(lo, hi) for _ in range(n)] for _ in range(n)] for _ in range(nz)]


def stack_inner(a, b):
    return sum(p * q for pa, pb in zip(a, b) for ra, rb in zip(pa, pb) for p, q in zip(ra, rb))


def stack_norm(a):
    return math.sqrt(stack_inner(a, a))


def stack_lin(alpha, a, beta, b):
    return [[[alpha * p + beta * q for p, q in zip(ra, rb)] for ra, rb in zip(pa, pb)] for pa, pb in zip(a, b)]


def mirror(h):
    n1, n2 = len(h), len(h[0])
    return [[h[(-i) % n1][(-j) % n2] for j in range(n2)] for i in range(n1)]


def test_blur_stack_adjoint():
    # The adjoint of y_j = sum_k h_{j-k} * x_k is x_k = sum_j h~_{j-k} * y_j, the blur with mirrored PSFs and offsets.
    rng = random.Random(1)
    n, nz = 6, 4
    psfs = {d: gpsf(n, 0.6 + abs(d)) for d in (-1, 0, 1)}
    psfs[1] = [[v * (1 + 0.1 * i) for v in row] for i, row in enumerate(psfs[1])]
    adj = {-d: mirror(h) for d, h in psfs.items()}
    x, y = rand_stack(rng, nz, n), rand_stack(rng, nz, n)
    ax = blur_stack(x, psfs)
    gap = abs(stack_inner(ax, y) - stack_inner(x, blur_stack(y, adj)))
    assert gap <= 1e-10 * stack_norm(ax) * stack_norm(y)


def test_formula_on_each_plane():
    rng = random.Random(2)
    n, nz = 5, 4
    hp, hn = gpsf(n, 1.0), gpsf(n, 1.3)
    y = rand_stack(rng, nz, n, 0, 5)
    c = 0.45
    x = nearest_neighbor(y, hp, hn, c)
    for j in range(nz):
        for i in range(n):
            for q in range(n):
                b = 0.0
                if j > 0:
                    b += circ_conv2(y[j - 1], hp)[i][q]
                if j < nz - 1:
                    b += circ_conv2(y[j + 1], hn)[i][q]
                assert abs(x[j][i][q] - (y[j][i][q] - c * b)) < 1e-12


def test_exact_second_order_identity():
    # With h_0 = delta and h_d = 0 for |d| >= 2, y = (I + E) x and the method is I - cE, so
    # x_hat = x + (1 - c) E x - c E^2 x exactly.
    n, nz = 3, 4
    rng = random.Random(3)
    hp = [[Fraction(rng.randint(0, 4), 20) for _ in range(n)] for _ in range(n)]
    hn = [[Fraction(rng.randint(0, 4), 20) for _ in range(n)] for _ in range(n)]
    x = [[[Fraction(rng.randint(0, 9)) for _ in range(n)] for _ in range(n)] for _ in range(nz)]
    e = {1: hp, -1: hn}
    y = blur_stack(x, {0: delta(n), 1: hp, -1: hn})
    ex = blur_stack(x, e)
    eex = blur_stack(ex, e)
    for c in (Fraction(1), Fraction(1, 2), Fraction(9, 20)):
        got = nearest_neighbor(y, hp, hn, c)
        want = [[[xv + (1 - c) * a - c * b for xv, a, b in zip(rx, ra, rb)]
                  for rx, ra, rb in zip(px, pa, pb)] for px, pa, pb in zip(x, ex, eex)]
        assert got == want


def test_zero_neighbor_psfs_give_the_data():
    rng = random.Random(4)
    n = 4
    zero = [[0.0] * n for _ in range(n)]
    y = rand_stack(rng, 3, n, 0, 1)
    assert nearest_neighbor(y, zero, zero, 0.5) == y


def test_linear_without_clipping():
    rng = random.Random(5)
    n, nz = 5, 3
    hp, hn = gpsf(n, 1.0), gpsf(n, 1.0)
    a, b = rand_stack(rng, nz, n), rand_stack(rng, nz, n)
    lhs = nearest_neighbor(stack_lin(2.0, a, -3.0, b), hp, hn, 0.45)
    rhs = stack_lin(2.0, nearest_neighbor(a, hp, hn, 0.45), -3.0, nearest_neighbor(b, hp, hn, 0.45))
    assert stack_norm(stack_lin(1.0, lhs, -1.0, rhs)) < 1e-12 * stack_norm(rhs)


def test_uniform_stack_keeps_one_minus_two_c():
    # Each defocused PSF sums to 1, so an interior plane of a uniform stack becomes (1 - 2c) times its value.
    n, nz = 4, 5
    hp, hn = gpsf(n, 1.5), gpsf(n, 1.5)
    y = [[[7.0] * n for _ in range(n)] for _ in range(nz)]
    for c in (0.3, 0.45, 0.5):
        x = nearest_neighbor(y, hp, hn, c)
        for j in range(1, nz - 1):
            assert all(abs(v - 7.0 * (1 - 2 * c)) < 1e-12 for row in x[j] for v in row)
        assert all(abs(v - 7.0 * (1 - c)) < 1e-12 for row in x[0] for v in row)


def test_wiener_step_inverts_an_invertible_in_focus_psf():
    rng = random.Random(6)
    n = 8
    h0 = [[0.0] * n for _ in range(n)]
    h0[0][0], h0[1][0], h0[n - 1][0], h0[0][1], h0[0][n - 1] = 0.6, 0.1, 0.1, 0.1, 0.1
    x = [[rng.uniform(0, 1) for _ in range(n)] for _ in range(n)]
    back = wiener_2d(circ_conv2(x, h0), h0, 0.0)
    assert img_norm([[p - q for p, q in zip(ra, rb)] for ra, rb in zip(back, x)]) < 1e-10 * img_norm(x)
    y = [[[rng.uniform(0, 1) for _ in range(n)] for _ in range(n)] for _ in range(2)]
    zero = [[0.0] * n for _ in range(n)]
    out = nearest_neighbor(y, zero, zero, 0.5, h0=h0, alpha=0.0, clip=True)
    for j in range(2):
        want = [[max(v, 0) for v in row] for row in wiener_2d(y[j], h0, 0.0)]
        assert img_norm([[p - q for p, q in zip(ra, rb)] for ra, rb in zip(out[j], want)]) < 1e-12


def test_out_of_focus_haze_is_reduced():
    # A measurement: three point sources in a 5-plane stack of 8 x 8 planes, PSF widths 0.7 + 1.5 |d| pixels.
    n, nz = 8, 5
    psfs = {d: gpsf(n, 0.7 + 1.5 * abs(d)) for d in range(-4, 5)}
    x = [[[0.0] * n for _ in range(n)] for _ in range(nz)]
    x[2][2][2] = 100.0
    x[3][5][6] = 100.0
    x[1][4][1] = 50.0
    y = blur_stack(x, psfs)
    target = [circ_conv2(p, psfs[0]) for p in x]
    est = nearest_neighbor(y, psfs[1], psfs[-1], 0.45, clip=True)
    err_raw = stack_norm(stack_lin(1.0, y, -1.0, target))
    err_nn = stack_norm(stack_lin(1.0, est, -1.0, target))
    assert err_nn < 0.6 * err_raw
