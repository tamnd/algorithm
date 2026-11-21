# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filtered-back-projection/. The authors are listed in prov/M3HFA2.jsonl.

import math
import random

import imgkit as ik
from filtered_back_projection import (
    back_project,
    filter_projection,
    filter_projection_direct,
    filtered_back_projection,
    kernel_spectrum,
    ram_lak_kernel,
    shepp_logan_kernel,
)

A, D, N = 32, 47, 32
TAU = 2.0 * math.sqrt(2.0) / D  # the bins cover [-sqrt(2), sqrt(2)], as in imgkit


def ellipse_projection(table, theta, s):
    """The exact Radon transform of an ellipse table (Kak and Slaney, chapter 3)."""
    total = 0.0
    for rho, a, b, x0, y0, phi in table:
        t = theta - math.radians(phi)
        u = s - (x0 * math.cos(theta) + y0 * math.sin(theta))
        a2 = a * a * math.cos(t) ** 2 + b * b * math.sin(t) ** 2
        if u * u < a2:
            total += 2.0 * rho * a * b / a2 * math.sqrt(a2 - u * u)
    return total


def sinogram(fun, a=A, d=D, tau=TAU):
    return [[fun(k * math.pi / a, (j - (d - 1) / 2.0) * tau) for j in range(d)] for k in range(a)]


def test_kernel_values() -> None:
    h = ram_lak_kernel(4, 0.5)
    assert len(h) == 7
    assert h[3] == 1.0
    assert h[1] == 0.0 and h[5] == 0.0
    assert abs(h[2] + 4.0 / math.pi ** 2) < 1e-15
    assert abs(h[0] + 4.0 / (9.0 * math.pi ** 2)) < 1e-15
    g = shepp_logan_kernel(4, 0.5)
    assert abs(g[3] - 8.0 / math.pi ** 2) < 1e-15
    assert abs(g[2] + 8.0 / (3.0 * math.pi ** 2)) < 1e-15


def test_kernel_frequency_response() -> None:
    # tau sum_m h(m tau) cos(2 pi m nu tau) -> |nu| (Ram-Lak) and sin(pi nu tau) / (pi tau) (Shepp-Logan)
    tau, d = 1.0, 4001
    h, g = ram_lak_kernel(d, tau), shepp_logan_kernel(d, tau)
    for nu in (0.05, 0.2, 0.35, 0.45):
        r = sum(tau * h[m + d - 1] * math.cos(2 * math.pi * m * nu * tau) for m in range(-(d - 1), d))
        s = sum(tau * g[m + d - 1] * math.cos(2 * math.pi * m * nu * tau) for m in range(-(d - 1), d))
        assert abs(r - nu) < 1e-3
        assert abs(s - math.sin(math.pi * nu * tau) / (math.pi * tau)) < 1e-3


def test_fft_filter_equals_direct_sum() -> None:
    rng = random.Random(11)
    for d in (1, 2, 7, 16, 47):
        p = [rng.uniform(-1.0, 1.0) for _ in range(d)]
        h = ram_lak_kernel(d, 0.1)
        length = 1
        while length < 2 * d - 1:
            length *= 2
        q1 = filter_projection(p, kernel_spectrum(h, d, length), 0.1)
        q2 = filter_projection_direct(p, h, 0.1)
        assert max(abs(u - v) for u, v in zip(q1, q2)) < 1e-10


def test_back_projection_is_scaled_adjoint_of_projector() -> None:
    # back_project with linear interpolation is (pi / a) / scale times the transpose of the
    # pixel-driven projector of imgkit, and that pair passes the adjoint test.
    a, d, n = 8, 23, 12
    tau = 2.0 * math.sqrt(2.0) / d
    angles = [k * math.pi / a for k in range(a)]
    rows = ik.parallel_beam_matrix(n, angles, d)
    scale = (2.0 / n) ** 2 / tau
    rng = random.Random(5)
    y = [rng.gauss(0.0, 1.0) for _ in range(a * d)]
    x = [rng.gauss(0.0, 1.0) for _ in range(n * n)]
    bp = ik.flatten(back_project([y[k * d:(k + 1) * d] for k in range(a)], tau, n))
    at_y = ik.sp_rmatvec(rows, y, n * n)
    c = (math.pi / a) / scale
    assert max(abs(u - c * v) for u, v in zip(bp, at_y)) < 1e-12
    ax = ik.sp_matvec(rows, x)
    lhs = sum(u * v for u, v in zip(ax, y))
    rhs = sum(u * v for u, v in zip(x, bp)) / c
    norm = math.sqrt(sum(v * v for v in ax)) * math.sqrt(sum(v * v for v in y))
    assert abs(lhs - rhs) <= 1e-10 * norm


def test_gaussian_known_answer() -> None:
    # f(x) = exp(-pi |x|^2 / w^2) has R f(theta, s) = w exp(-pi s^2 / w^2).
    w = 0.5
    sino = sinogram(lambda th, s: w * math.exp(-math.pi * s * s / (w * w)))
    img = filtered_back_projection(sino, TAU, N)
    xs, ys = ik.pixel_centers(N)
    err = max(abs(img[i][j] - math.exp(-math.pi * (xs[j] ** 2 + ys[i] ** 2) / (w * w))) for i in range(N) for j in range(N))
    assert err < 0.03  # measured 0.017 for a = 32, d = 47, n = 32


def test_disk_interior() -> None:
    sino = sinogram(lambda th, s: 2.0 * math.sqrt(0.25 - s * s) if s * s < 0.25 else 0.0)
    xs, ys = ik.pixel_centers(N)
    for kernel in ("ram-lak", "shepp-logan"):
        img = filtered_back_projection(sino, TAU, N, kernel)
        inner = [img[i][j] for i in range(N) for j in range(N) if xs[j] ** 2 + ys[i] ** 2 < 0.35 ** 2]
        outer = [img[i][j] for i in range(N) for j in range(N) if xs[j] ** 2 + ys[i] ** 2 > 0.65 ** 2]
        assert max(abs(v - 1.0) for v in inner) < 0.02  # measured 0.010
        assert max(abs(v) for v in outer) < 0.05


def test_shepp_logan_center() -> None:
    sino = sinogram(lambda th, s: ellipse_projection(ik.SHEPP_LOGAN, th, s))
    img = filtered_back_projection(sino, TAU, N)
    center = (img[15][15] + img[15][16] + img[16][15] + img[16][16]) / 4.0
    assert abs(center - 1.02) < 0.02  # measured 1.017


def test_linear_and_zero() -> None:
    rng = random.Random(3)
    s1 = [[rng.uniform(0, 1) for _ in range(9)] for _ in range(4)]
    s2 = [[rng.uniform(0, 1) for _ in range(9)] for _ in range(4)]
    s3 = [[u + 2.0 * v for u, v in zip(r1, r2)] for r1, r2 in zip(s1, s2)]
    f1, f2, f3 = (filtered_back_projection(s, 0.3, 6) for s in (s1, s2, s3))
    assert max(abs(f3[i][j] - f1[i][j] - 2.0 * f2[i][j]) for i in range(6) for j in range(6)) < 1e-12
    z = filtered_back_projection([[0.0] * 9 for _ in range(4)], 0.3, 6)
    assert all(v == 0.0 for row in z for v in row)


def test_hand_trace_center() -> None:
    # Disk of radius 1/2, d = 7, tau = 1/4: the filtered center bin is 0.29803,
    # and with 4 angles the value at the origin is pi times that.
    p = [2.0 * math.sqrt(max(0.0, 0.25 - ((j - 3) * 0.25) ** 2)) for j in range(7)]
    q = filter_projection_direct(p, ram_lak_kernel(7, 0.25), 0.25)
    assert abs(q[3] - 0.29803) < 1e-5
    assert abs(math.pi * q[3] - 0.93628) < 1e-5
