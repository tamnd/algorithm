# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irradiance-environment-map/. The authors are listed in prov/H7PF86.jsonl.

"""Tests of the irradiance environment map against closed forms and brute force.

The constants are checked against the values printed in the paper, the basis
for orthonormality, the matrix form against the spherical harmonic sum, and
the nine term irradiance against brute force quadrature: exactly for lighting
that is band limited, and within the proved bound 3/32 of the total light for
any lighting that is not negative.
"""

import math
import random

from irradiance_environment_map import (
    A_HAT,
    C1,
    C2,
    C3,
    C4,
    C5,
    build,
    gauss_legendre,
    irradiance,
    irradiance_brute_force,
    irradiance_matrix,
    irradiance_sh,
    point_light_coeffs,
    project,
    sh9,
    sphere_texels,
)


def unit(rng: random.Random) -> tuple[float, float, float]:
    while True:
        v = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))
        r = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
        if 0.1 < r <= 1.0:
            return (v[0] / r, v[1] / r, v[2] / r)


def test_constants_of_the_paper() -> None:
    for got, want in ((C1, 0.429043), (C2, 0.511664), (C3, 0.743125), (C4, 0.886227), (C5, 0.247708)):
        # The exact c2 and c3 are 0.5116634 and 0.7431239. The printed values
        # 0.511664 and 0.743125 come from the rounded basis constants.
        assert abs(got - want) < 2e-6
    for got, want in zip(A_HAT, (3.141593, 2.094395, 0.785398)):
        assert abs(got - want) < 5e-7


def test_kernel_is_the_clamped_cosine() -> None:
    # A_hat_l = 2 pi times the integral of t P_l(t) over [0, 1].
    legendre = (lambda t: 1.0, lambda t: t, lambda t: 0.5 * (3 * t * t - 1))
    rule = gauss_legendre(6)
    for l in range(3):
        val = 2 * math.pi * sum(0.5 * w * ((x + 1) / 2) * legendre[l]((x + 1) / 2) for x, w in rule)
        assert abs(val - A_HAT[l]) < 1e-12


def test_basis_is_orthonormal() -> None:
    texels = sphere_texels(lambda d: 1.0, 3, 8)
    assert abs(sum(t[2] for t in texels) - 4 * math.pi) < 1e-12
    for i in range(9):
        for j in range(9):
            s = sum(sh9(d)[i] * sh9(d)[j] * dw for d, _, dw in texels)
            assert abs(s - (1.0 if i == j else 0.0)) < 1e-12


def test_matrix_equals_the_harmonic_sum() -> None:
    rng = random.Random(7)
    for _ in range(50):
        coeffs = [rng.uniform(-2, 2) for _ in range(9)]
        m = irradiance_matrix(coeffs)
        assert all(m[i][j] == m[j][i] for i in range(4) for j in range(4))
        for _ in range(5):
            n = unit(rng)
            assert abs(irradiance(m, n) - irradiance_sh(coeffs, n)) < 1e-12


def test_point_light_check_values() -> None:
    d = (0.0, 0.0, 1.0)
    m = irradiance_matrix(point_light_coeffs(d, 1.0))
    assert abs(irradiance(m, d) - 17 / 16) < 1e-12
    assert abs(irradiance(m, (0.0, 0.0, -1.0)) - 1 / 16) < 1e-12
    assert abs(irradiance(m, (1.0, 0.0, 0.0)) - 3 / 32) < 1e-12


def test_kernel_of_nine_terms() -> None:
    # The addition theorem: sum of A_hat Y(w) Y(n) = 3/32 + t/2 + 15 t^2 / 32 with t = n . w.
    rng = random.Random(3)
    for _ in range(100):
        n, w = unit(rng), unit(rng)
        t = sum(a * b for a, b in zip(n, w))
        val = irradiance_sh(point_light_coeffs(w, 1.0), n)
        assert abs(val - (3 / 32 + t / 2 + 15 * t * t / 32)) < 1e-12


def test_sky_is_exact() -> None:
    texels = sphere_texels(lambda d: 1.0 if d[2] > 0 else 0.0, 4, 8)
    coeffs = project(texels)
    assert abs(coeffs[0] - math.sqrt(math.pi)) < 1e-12
    assert abs(coeffs[2] - 0.5 * math.sqrt(3 * math.pi)) < 1e-12
    assert all(abs(coeffs[k]) < 1e-12 for k in (1, 3, 4, 5, 6, 7, 8))
    m = build(texels)
    rng = random.Random(11)
    for _ in range(30):
        n = unit(rng)
        assert abs(irradiance(m, n) - math.pi * (1 + n[2]) / 2) < 1e-12


def test_band_limited_lighting_matches_brute_force() -> None:
    rng = random.Random(5)
    coeffs = [rng.uniform(-1, 1) for _ in range(9)]
    coeffs[0] = 4.0

    def radiance(d):
        return sum(c * y for c, y in zip(coeffs, sh9(d)))

    m = build(sphere_texels(radiance, 3, 8))
    fine = sphere_texels(radiance, 24, 96)
    for _ in range(8):
        n = unit(rng)
        assert abs(irradiance(m, n) - irradiance_sh(coeffs, n)) < 1e-12
        assert abs(irradiance(m, n) - irradiance_brute_force(fine, n)) < 2e-3


def test_error_bound_for_any_lighting() -> None:
    rng = random.Random(13)
    texels = sphere_texels(lambda d: 0.0, 6, 12)
    for trial in range(10):
        lit = [(d, rng.random() ** 6 * 10.0, dw) for d, _, dw in texels]
        total = sum(r * dw for _, r, dw in lit)
        m = build(lit)
        worst = 0.0
        for _ in range(20):
            n = unit(rng)
            err = abs(irradiance(m, n) - irradiance_brute_force(lit, n))
            worst = max(worst, err)
            assert err <= 3 / 32 * total + 1e-9
        assert worst > 0.0


def test_linear_in_the_lighting() -> None:
    rng = random.Random(17)
    texels = sphere_texels(lambda d: 0.0, 3, 8)
    a = [(d, rng.random(), dw) for d, _, dw in texels]
    b = [(d, rng.random(), dw) for d, _, dw in texels]
    ab = [(d, 2.0 * x[1] + 3.0 * y[1], d2) for (d, _, d2), x, y in zip(texels, a, b)]
    ma, mb, mab = build(a), build(b), build(ab)
    for i in range(4):
        for j in range(4):
            assert abs(mab[i][j] - 2.0 * ma[i][j] - 3.0 * mb[i][j]) < 1e-12
