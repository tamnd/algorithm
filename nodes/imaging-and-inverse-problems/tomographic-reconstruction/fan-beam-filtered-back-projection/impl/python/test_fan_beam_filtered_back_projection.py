# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fan-beam-filtered-back-projection/. The authors are listed in prov/2Y6GKS.jsonl.

import math
import random

from fan_beam_filtered_back_projection import (
    convolve,
    fan_beam_fbp,
    fan_beam_fbp_flat,
    fan_kernel,
    flat_kernel,
    parker_weight,
    ram_lak,
    source_coordinates,
)

DIST = 3.0
GAMMA_MAX = math.asin(math.sqrt(2.0) / DIST)  # the fan covers the disk of radius sqrt(2)
D = 49
ALPHA = 2.0 * GAMMA_MAX / (D - 1)
TAU_FLAT = 2.0 * DIST * math.tan(GAMMA_MAX) / (D - 1)
A = 64
N = 32
XS = [-1.0 + (2 * j + 1) / N for j in range(N)]
YS = [1.0 - (2 * i + 1) / N for i in range(N)]

# The modified Shepp-Logan phantom: rho, A, B, x0, y0, phi in degrees (Toft 1996, first five ellipses).
PHANTOM = [
    (1.0, 0.69, 0.92, 0.0, 0.0, 0.0),
    (-0.8, 0.6624, 0.874, 0.0, -0.0184, 0.0),
    (-0.2, 0.11, 0.31, 0.22, 0.0, -18.0),
    (-0.2, 0.16, 0.41, -0.22, 0.0, 18.0),
    (0.1, 0.21, 0.25, 0.0, 0.35, 0.0),
]


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


def gauss_projection(theta, s):
    """R f for f(x) = exp(-4 pi |x|^2): (1/2) exp(-4 pi s^2) at every angle."""
    return 0.5 * math.exp(-4.0 * math.pi * s * s)


def fan_data(radon, betas, gammas):
    """g(beta, gamma) = R f(beta + gamma, D sin gamma)."""
    return [[radon(b + g, DIST * math.sin(g)) for g in gammas] for b in betas]


def gauss_error(img):
    return max(abs(img[i][j] - math.exp(-4.0 * math.pi * (XS[j] ** 2 + YS[i] ** 2))) for i in range(N) for j in range(N))


EQUI = [(j - (D - 1) / 2.0) * ALPHA for j in range(D)]
FULL = [2.0 * math.pi * k / A for k in range(A)]


def test_kernel_values() -> None:
    kern = fan_kernel(D, ALPHA)
    assert abs(kern[D - 1] - 1.0 / (8.0 * ALPHA * ALPHA)) < 1e-9
    for m in range(1, D):
        want = 0.5 * (m * ALPHA / math.sin(m * ALPHA)) ** 2 * ram_lak(m, ALPHA)
        assert abs(kern[D - 1 + m] - want) <= 1e-12 * abs(kern[D - 1])
        assert kern[D - 1 + m] == kern[D - 1 - m]
    assert flat_kernel(3, 0.5) == [0.5 * ram_lak(m, 0.5) for m in range(-2, 3)]
    assert convolve([1.0, 2.0], [3.0, 4.0, 5.0], 2.0) == [2.0 * (4.0 + 6.0), 2.0 * (5.0 + 8.0)]


def test_geometry_identity() -> None:
    # x . omega(beta + gamma) - D sin gamma = L sin(gamma' - gamma)
    rng = random.Random(1)
    for _ in range(200):
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        beta, gamma = rng.uniform(0, 2 * math.pi), rng.uniform(-0.5, 0.5)
        lc, ls = source_coordinates(x, y, beta, DIST)
        big_l, gp = math.hypot(lc, ls), math.atan2(ls, lc)
        lhs = x * math.cos(beta + gamma) + y * math.sin(beta + gamma) - DIST * math.sin(gamma)
        assert abs(lhs - big_l * math.sin(gp - gamma)) < 1e-12


def test_conjugate_ray_is_the_same_line() -> None:
    rng = random.Random(2)
    for _ in range(100):
        beta, gamma = rng.uniform(0, 2 * math.pi), rng.uniform(-0.5, 0.5)
        b2, g2 = beta + math.pi + 2 * gamma, -gamma
        # same line: (theta, s) and (theta + pi, -s) describe one line
        assert abs(math.sin(b2 + g2 - (beta + gamma) - math.pi)) < 1e-12
        assert abs(DIST * math.sin(g2) + DIST * math.sin(gamma)) < 1e-12


def test_parker_weights_add_to_one() -> None:
    delta = GAMMA_MAX
    span = math.pi + 2 * delta
    rng = random.Random(3)
    for _ in range(2000):
        beta, gamma = rng.uniform(0, span), rng.uniform(-delta, delta)
        b2 = beta + math.pi + 2 * gamma
        if b2 > span:
            b2 -= 2 * math.pi
        w = parker_weight(beta, gamma, delta) + parker_weight(b2, -gamma, delta)
        assert abs(w - 1.0) < 1e-12
        assert 0.0 <= parker_weight(beta, gamma, delta) <= 1.0


def test_gaussian_full_scan() -> None:
    img = fan_beam_fbp(fan_data(gauss_projection, FULL, EQUI), DIST, ALPHA, N)
    assert gauss_error(img) < 0.03


def test_gaussian_short_scan() -> None:
    a = 40
    span = math.pi + 2 * GAMMA_MAX
    betas = [span * k / a for k in range(a)]
    img = fan_beam_fbp(fan_data(gauss_projection, betas, EQUI), DIST, ALPHA, N, scan="short", delta=GAMMA_MAX)
    assert gauss_error(img) < 0.03


def test_gaussian_flat_detector() -> None:
    gammas = [math.atan((j - (D - 1) / 2.0) * TAU_FLAT / DIST) for j in range(D)]
    img = fan_beam_fbp_flat(fan_data(gauss_projection, FULL, gammas), DIST, TAU_FLAT, N)
    assert gauss_error(img) < 0.03


def test_phantom_values() -> None:
    img = fan_beam_fbp(fan_data(lambda t, s: ellipse_projection(PHANTOM, t, s), FULL, EQUI), DIST, ALPHA, N)
    assert abs(img[16][16] - 0.2) < 0.03  # pixel (1/32, -1/32), true value 0.2
    assert abs(img[8][16] - 0.3) < 0.04  # pixel (1/32, 15/32), inside the top ellipse, true value 0.3


def test_linear_in_the_data() -> None:
    rng = random.Random(4)
    a, d, n = 8, 9, 8
    alpha = 0.05
    g1 = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(a)]
    g2 = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(a)]
    mix = [[2.0 * u - 3.0 * v for u, v in zip(r1, r2)] for r1, r2 in zip(g1, g2)]
    f1, f2, fm = (fan_beam_fbp(g, DIST, alpha, n) for g in (g1, g2, mix))
    for i in range(n):
        for j in range(n):
            assert abs(fm[i][j] - (2.0 * f1[i][j] - 3.0 * f2[i][j])) < 1e-9
