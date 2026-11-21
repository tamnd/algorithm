# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambda-tomography/. The authors are listed in prov/8VWFH5.jsonl.

import math
import random

from lambda_tomography import lambda_at, lambda_filter, lambda_tomography, lin_interp

A, D, N = 32, 65, 16
TAU = 2.0 * math.sqrt(2.0) / D
XS = [-1.0 + (2 * j + 1) / N for j in range(N)]
YS = [1.0 - (2 * i + 1) / N for i in range(N)]


def sinogram(fun, a=A, d=D, tau=TAU):
    return [[fun(k * math.pi / a, (j - (d - 1) / 2.0) * tau) for j in range(d)] for k in range(a)]


def gauss(theta, s):
    """R f for f(x) = exp(-4 pi |x|^2)."""
    return 0.5 * math.exp(-4.0 * math.pi * s * s)


def disk(theta, s, radius=0.5):
    return 2.0 * math.sqrt(radius * radius - s * s) if abs(s) < radius else 0.0


def lambda_gauss(x, y, m=400):
    """(1 / (2 pi)) integral_0^pi -p''(x . omega) dtheta for p(s) = exp(-4 pi s^2) / 2, by the midpoint rule."""
    total = 0.0
    for k in range(m):
        th = (k + 0.5) * math.pi / m
        s = x * math.cos(th) + y * math.sin(th)
        total += 0.5 * (8.0 * math.pi - 64.0 * math.pi ** 2 * s * s) * math.exp(-4.0 * math.pi * s * s)
    return total / (2.0 * m)


def test_filter_values() -> None:
    q = lambda_filter([0.0, 1.0, 4.0, 1.0], 0.5, mu=2.0)
    assert q == [-4.0 + 0.0, -(4.0 - 2.0) * 4.0 + 2.0, -(1.0 - 8.0 + 1.0) * 4.0 + 8.0, -(0.0 - 2.0 + 4.0) * 4.0 + 2.0]
    assert lin_interp([1.0, 3.0], 0.25) == 1.5 and lin_interp([1.0, 3.0], -1.0) == 0.0


def test_gaussian_matches_sqrt_minus_laplacian() -> None:
    sino = sinogram(gauss)
    # Lambda f(0) = integral 2 pi |xi| (1/4) exp(-pi |xi|^2 / 4) d xi = 2 pi
    assert abs(lambda_at(sino, TAU, 0.0, 0.0) - 2.0 * math.pi) < 0.15
    img = lambda_tomography(sino, TAU, N)
    for i in range(N):
        for j in range(N):
            assert abs(img[i][j] - lambda_gauss(XS[j], YS[i])) < 0.2


def test_disk_values() -> None:
    sino = sinogram(disk)
    # For the disk of radius R: Lambda f(0) = 1 / R, and it grows toward the edge and is negative outside.
    assert abs(lambda_at(sino, TAU, 0.0, 0.0) - 2.0) < 0.05
    want = 2.0 * sum((1.0 - 0.25 * math.cos((k + 0.5) * math.pi / 2000) ** 2) ** -1.5 for k in range(2000)) / 2000
    assert abs(lambda_at(sino, TAU, 0.25, 0.0) - want) < 0.1
    assert lambda_at(sino, TAU, 0.45, 0.0) > 4.0
    assert lambda_at(sino, TAU, 0.6, 0.0) < 0.0


def test_local_data_suffices() -> None:
    # Change the data far from the point: the value at the point does not change.
    rng = random.Random(7)
    sino = sinogram(gauss)
    x, y = 0.2, -0.1
    radius = math.hypot(x, y) + 2.0 * TAU
    changed = [
        [v if abs((j - (D - 1) / 2.0) * TAU) <= radius else v + rng.uniform(-5, 5) for j, v in enumerate(row)]
        for row in sino
    ]
    assert lambda_at(changed, TAU, x, y) == lambda_at(sino, TAU, x, y)
    # truncated data: zero outside |s| < 0.4
    cut = [[v if abs((j - (D - 1) / 2.0) * TAU) < 0.4 else 0.0 for j, v in enumerate(row)] for row in sino]
    assert abs(lambda_at(cut, TAU, 0.05, 0.05) - lambda_at(sino, TAU, 0.05, 0.05)) < 1e-12


def test_mu_term_adds_the_smooth_part() -> None:
    sino = sinogram(gauss)
    mu = 3.0
    with_mu = lambda_at(sino, TAU, 0.0, 0.0, mu)
    without = lambda_at(sino, TAU, 0.0, 0.0)
    # Lambda^(-1) f(0) = (1 / (2 pi)) integral_0^pi R f(theta, 0) dtheta = 1/4 for this Gaussian
    assert abs((with_mu - without) / mu - 0.25) < 1e-12
    # in general the mu term is mu / (2 a) times the plain back-projection of the data
    x, y = 0.3, 0.1
    plain = 0.0
    for k, row in enumerate(sino):
        th = k * math.pi / A
        plain += lin_interp(row, (x * math.cos(th) + y * math.sin(th)) / TAU + (D - 1) / 2.0)
    diff = lambda_at(sino, TAU, x, y, mu) - lambda_at(sino, TAU, x, y)
    assert abs(diff - mu * plain / (2.0 * A)) < 1e-12


def test_point_and_grid_agree() -> None:
    sino = sinogram(disk, a=8, d=33, tau=0.05)
    img = lambda_tomography(sino, 0.05, 4)
    xs = [-1.0 + (2 * j + 1) / 4 for j in range(4)]
    ys = [1.0 - (2 * i + 1) / 4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            assert abs(img[i][j] - lambda_at(sino, 0.05, xs[j], ys[i])) < 1e-12
