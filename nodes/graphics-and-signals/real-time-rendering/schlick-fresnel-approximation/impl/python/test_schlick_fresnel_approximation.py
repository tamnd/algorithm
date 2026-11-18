# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schlick-fresnel-approximation/. The authors are listed in prov/W0ZH9M.jsonl.

"""Tests of Schlick's approximation against the exact Fresnel equations."""

import math
import random

from schlick_fresnel_approximation import (
    f0_conductor,
    f0_from_ior,
    fresnel_conductor,
    fresnel_dielectric,
    schlick,
    schlick_dielectric,
)


def cosd(deg: float) -> float:
    return math.cos(math.radians(deg))


def worst(f, g, steps: int = 20000) -> tuple[float, float]:
    """The largest |f - g| over theta in [0, 90] degrees, and where it is."""
    best = (0.0, 0.0)
    for i in range(steps + 1):
        t = i * (math.pi / 2.0) / steps
        e = abs(f(math.cos(t)) - g(math.cos(t)))
        if e > best[0]:
            best = (e, math.degrees(t))
    return best


def test_end_points() -> None:
    rng = random.Random(1)
    for _ in range(200):
        eta = rng.uniform(1.01, 3.0)
        f0 = f0_from_ior(eta)
        assert abs(schlick(1.0, f0) - f0) < 1e-15
        assert abs(fresnel_dielectric(1.0, eta) - f0) < 1e-12
        assert schlick(0.0, f0) == 1.0
        assert abs(fresnel_dielectric(0.0, eta) - 1.0) < 1e-12
        f90 = rng.uniform(0.0, 1.0)
        assert abs(schlick(0.0, f0, f90) - f90) < 1e-15


def test_monotone_and_range() -> None:
    rng = random.Random(2)
    for _ in range(100):
        f0 = rng.uniform(0.0, 1.0)
        prev = schlick(1.0, f0)
        for i in range(999, -1, -1):
            cur = schlick(i / 1000.0, f0)
            assert f0 - 1e-15 <= cur <= 1.0
            assert cur >= prev - 1e-15
            prev = cur


def test_page_values_glass() -> None:
    f0 = f0_from_ior(1.5)
    assert abs(f0 - 0.04) < 1e-15
    table = {30.0: -0.00148, 45.0: -0.00817, 60.0: -0.01919, 80.0: 0.02221, 85.0: 0.03569}
    for deg, err in table.items():
        assert abs((schlick(cosd(deg), f0) - fresnel_dielectric(cosd(deg), 1.5)) - err) < 1e-5
    assert abs(fresnel_dielectric(cosd(85.0), 1.5) - 0.6128) < 5e-5


def test_worst_error_by_ior() -> None:
    expected = {1.33: (0.0599, 83.8), 1.5: (0.0357, 85.0), 2.0: (0.0444, 85.2), 2.4: (0.0740, 84.5)}
    for eta, (err, deg) in expected.items():
        f0 = f0_from_ior(eta)
        e, at = worst(lambda c: schlick(c, f0), lambda c: fresnel_dielectric(c, eta))
        assert abs(e - err) < 5e-4
        assert abs(at - deg) < 0.2


def test_inside_the_denser_medium() -> None:
    eta = 1.0 / 1.5
    crit = math.degrees(math.asin(eta))
    assert abs(crit - 41.81) < 0.01
    # Plain Schlick with cos_i misses total internal reflection.
    assert abs(fresnel_dielectric(cosd(40.0), eta) - 0.2453) < 5e-5
    assert abs(schlick(cosd(40.0), 0.04) - 0.0407) < 5e-5
    assert fresnel_dielectric(cosd(42.0), eta) == 1.0
    assert schlick_dielectric(cosd(42.0), eta) == 1.0
    # With cos_t the error is the same as outside, because R(theta_i, eta) = R(theta_t, 1 / eta).
    e_in, _ = worst(lambda c: schlick_dielectric(c, eta), lambda c: fresnel_dielectric(c, eta))
    e_out, _ = worst(lambda c: schlick(c, 0.04), lambda c: fresnel_dielectric(c, 1.5))
    assert abs(e_in - e_out) < 1e-4


def test_reciprocity_of_exact_fresnel() -> None:
    rng = random.Random(3)
    for _ in range(500):
        eta = rng.uniform(1.05, 2.5)
        ti = rng.uniform(0.0, math.pi / 2.0)
        st = math.sin(ti) / eta
        tt = math.asin(st)
        assert abs(fresnel_dielectric(math.cos(ti), eta) - fresnel_dielectric(math.cos(tt), 1.0 / eta)) < 1e-12


def test_conductor() -> None:
    n, k = 1.0, 6.7
    f0 = f0_conductor(n, k)
    assert abs(f0 - 0.9182) < 5e-5
    assert abs(fresnel_conductor(1.0, n, k) - f0) < 1e-12
    # The exact curve dips below f0 near 81 degrees; Schlick only rises.
    low, at = min((fresnel_conductor(math.cos(math.radians(d / 100.0)), n, k), d / 100.0) for d in range(9001))
    assert abs(low - 0.8627) < 5e-5 and abs(at - 80.92) < 0.05
    e, at = worst(lambda c: schlick(c, f0), lambda c: fresnel_conductor(c, n, k))
    assert abs(e - 0.0947) < 5e-4 and abs(at - 83.1) < 0.2
    # A dielectric index with k = 0 gives the dielectric formula.
    for deg in (0.0, 30.0, 60.0, 85.0):
        assert abs(fresnel_conductor(cosd(deg), 1.5, 0.0) - fresnel_dielectric(cosd(deg), 1.5)) < 1e-12
