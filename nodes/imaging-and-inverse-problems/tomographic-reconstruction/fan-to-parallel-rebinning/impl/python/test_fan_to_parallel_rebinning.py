# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fan-to-parallel-rebinning/. The authors are listed in prov/D52MD2.jsonl.

import math
import random

from fan_to_parallel_rebinning import (
    bilinear,
    fan_coordinates,
    parallel_fbp,
    ram_lak_kernel,
    rebin,
    rebin_and_reconstruct,
)

DIST = 3.0
GAMMA_MAX = math.asin(math.sqrt(2.0) / DIST)  # the fan covers the disk of radius sqrt(2)
D = 49
ALPHA = 2.0 * GAMMA_MAX / (D - 1)
TAU_FLAT = 2.0 * DIST * math.tan(GAMMA_MAX) / (D - 1)
A = 64
AP, DP = 32, 47
TAU = 2.0 * math.sqrt(2.0) / DP
N = 32
XS = [-1.0 + (2 * j + 1) / N for j in range(N)]
YS = [1.0 - (2 * i + 1) / N for i in range(N)]
EQUI = [(j - (D - 1) / 2.0) * ALPHA for j in range(D)]
FLAT = [math.atan((j - (D - 1) / 2.0) * TAU_FLAT / DIST) for j in range(D)]
BETAS = [2.0 * math.pi * k / A for k in range(A)]

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


def blob_projection(theta, s):
    """R f for f(x) = exp(-4 pi |x - c|^2) with c = (0.3, -0.2)."""
    u = s - (0.3 * math.cos(theta) - 0.2 * math.sin(theta))
    return 0.5 * math.exp(-4.0 * math.pi * u * u)


def fan_data(radon, gammas):
    return [[radon(b + g, DIST * math.sin(g)) for g in gammas] for b in BETAS]


def parallel_data(radon):
    return [[radon(k * math.pi / AP, (j - (DP - 1) / 2.0) * TAU) for j in range(DP)] for k in range(AP)]


def blob_error(img):
    return max(
        abs(img[i][j] - math.exp(-4.0 * math.pi * ((XS[j] - 0.3) ** 2 + (YS[i] + 0.2) ** 2)))
        for i in range(N)
        for j in range(N)
    )


def test_fan_coordinates() -> None:
    beta, gamma = fan_coordinates(0.3, 0.5, 2.0)
    assert abs(gamma - 0.25268) < 1e-5 and abs(beta - 0.04732) < 1e-5
    rng = random.Random(1)
    for _ in range(200):
        theta, s = rng.uniform(0, math.pi), rng.uniform(-1.4, 1.4)
        beta, gamma = fan_coordinates(theta, s, DIST)
        assert 0.0 <= beta < 2.0 * math.pi
        assert abs(math.sin(beta + gamma - theta)) < 1e-12 and math.cos(beta + gamma - theta) > 0
        assert abs(DIST * math.sin(gamma) - s) < 1e-12


def test_bilinear_is_periodic_in_the_angle() -> None:
    g = [[1.0, 2.0], [3.0, 4.0]]
    assert bilinear(g, 0.5, 0.5) == 2.5
    assert bilinear(g, 1.5, 0.0) == 2.0  # half way between row 1 and row 0
    assert bilinear(g, 0.0, 1.5) == 1.0  # half way between column 1 and nothing


def test_exact_on_data_linear_in_the_fan_angle() -> None:
    # g = c + e gamma is reproduced by the interpolation, so the result is c + e asin(s / D)
    g = [[0.7 + 2.0 * gm for gm in EQUI] for _ in BETAS]
    p = rebin(g, DIST, ALPHA, AP, DP, TAU)
    for k in range(AP):
        for j in range(DP):
            s = (j - (DP - 1) / 2.0) * TAU
            if abs(s) <= DIST * math.sin(GAMMA_MAX) - 1e-9:
                assert abs(p[k][j] - (0.7 + 2.0 * math.asin(s / DIST))) < 1e-12


def test_rebinned_sinogram_is_close() -> None:
    want = parallel_data(blob_projection)
    for det, gammas, step in (("equiangular", EQUI, ALPHA), ("flat", FLAT, TAU_FLAT)):
        for avg in (False, True):
            p = rebin(fan_data(blob_projection, gammas), DIST, step, AP, DP, TAU, detector=det, average=avg)
            assert max(abs(p[k][j] - want[k][j]) for k in range(AP) for j in range(DP)) < 0.02


def test_reconstruction_of_a_blob() -> None:
    img = rebin_and_reconstruct(fan_data(blob_projection, EQUI), DIST, ALPHA, AP, DP, TAU, N)
    assert blob_error(img) < 0.03
    direct = parallel_fbp(parallel_data(blob_projection), TAU, N)
    assert blob_error(direct) < 0.03


def test_phantom_values() -> None:
    radon = lambda t, s: ellipse_projection(PHANTOM, t, s)
    img = rebin_and_reconstruct(fan_data(radon, EQUI), DIST, ALPHA, AP, DP, TAU, N, average=True)
    assert abs(img[16][16] - 0.2) < 0.04
    assert abs(img[8][16] - 0.3) < 0.05


def test_ram_lak_kernel() -> None:
    h = ram_lak_kernel(3, 0.5)
    assert h[2] == 1.0 and h[1] == h[3] == -4.0 / math.pi ** 2 and h[0] == h[4] == 0.0
