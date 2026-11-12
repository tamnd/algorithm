# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volumetric-path-tracing/. The authors are listed in prov/C7K88C.jsonl.

import math
import random

import pytest

from volumetric_path_tracing import (
    chandrasekhar_h,
    gauss_legendre,
    render,
    semi_infinite_reflection,
    single_scattering,
)

# A heterogeneous slab: sigma_t(z) = A + B sin^2(C z), with a closed-form optical depth.
A, B, C = 1.0, 0.5, 3.0
MAJORANT = A + B
MU0, MU, E = 0.6, 0.8, math.pi


def sigma(z: float) -> float:
    return A + B * math.sin(C * z) ** 2


def optical_depth(z: float) -> float:
    return A * z + B * (z / 2 - math.sin(2 * C * z) / (4 * C))


def test_gauss_legendre_is_exact_for_polynomials() -> None:
    xs, ws = gauss_legendre(8)
    assert abs(sum(ws) - 1) < 1e-14
    for k in range(16):
        assert abs(sum(w * x**k for x, w in zip(xs, ws)) - 1 / (k + 1)) < 1e-14


@pytest.mark.parametrize("omega", [0.5, 0.9])
def test_h_function(omega: float) -> None:
    H = chandrasekhar_h(omega)
    assert abs(H(0.0) - 1.0) < 1e-12
    # The first form of the equation holds at test points.
    xs, ws = gauss_legendre(64)
    for m in [0.1, 0.5, 1.0]:
        integral = sum(w * H(x) / (m + x) for x, w in zip(xs, ws))
        assert abs(H(m) - (1 + 0.5 * omega * m * H(m) * integral)) < 1e-8
    # The zeroth moment: (omega / 2) integral_0^1 H = 1 - sqrt(1 - omega).
    moment = sum(w * H(x) for x, w in zip(xs, ws))
    assert abs(0.5 * omega * moment - (1 - math.sqrt(1 - omega))) < 1e-10


@pytest.mark.parametrize("omega", [0.5, 0.9])
def test_single_scattering_on_a_heterogeneous_slab(omega: float) -> None:
    depth = 2.0
    exact = single_scattering(omega, E, MU0, MU, optical_depth(depth))
    mean, se = render(sigma, MAJORANT, depth, omega, E, MU0, MU, 20000, random.Random(1), max_bounces=1)
    assert se < 0.02 * exact
    assert abs(mean - exact) < 4 * se


def test_single_scattering_with_a_loose_majorant() -> None:
    depth = 2.0
    exact = single_scattering(0.9, E, MU0, MU, optical_depth(depth))
    mean, se = render(sigma, 3 * MAJORANT, depth, 0.9, E, MU0, MU, 20000, random.Random(4), max_bounces=1)
    assert abs(mean - exact) < 4 * se


def test_multiple_scattering_on_a_thick_slab() -> None:
    # Optical depth 25: the slab is semi-infinite to far below the noise.
    depth = 20.0
    exact = semi_infinite_reflection(0.9, E, MU0, MU)
    mean, se = render(sigma, MAJORANT, depth, 0.9, E, MU0, MU, 20000, random.Random(2))
    assert se < 0.02 * exact
    assert abs(mean - exact) < 4 * se
    # Multiple scattering adds much to the single-scattering part.
    assert exact > 2 * single_scattering(0.9, E, MU0, MU, math.inf)


def test_no_scattering_gives_zero() -> None:
    mean, se = render(sigma, MAJORANT, 2.0, 0.0, E, MU0, MU, 200, random.Random(3))
    assert mean == 0.0 and se == 0.0
