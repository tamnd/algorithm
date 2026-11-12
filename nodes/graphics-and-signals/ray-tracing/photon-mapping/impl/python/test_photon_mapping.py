# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/photon-mapping/. The authors are listed in prov/EFE9E0.jsonl.

import math
import random

import pytest

from photon_mapping import (
    build_photon_map,
    fibonacci_sphere,
    furnace_exact,
    furnace_radiance,
    point_light_disc_average,
    point_light_irradiance,
    trace_photons_furnace,
    trace_photons_point_light,
)

RHO, BE = 0.5, 1.0


@pytest.fixture(scope="module")
def furnace_map():
    pts, pw = trace_photons_furnace(5000, RHO, BE, random.Random(1996))
    return pts, pw, build_photon_map(pts, pw)


def mean_se(xs):
    m = sum(xs) / len(xs)
    return m, math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1) / len(xs))


def test_photon_power_is_conserved(furnace_map) -> None:
    pts, pw, _ = furnace_map
    # Each path has a geometric number of hits with mean 1 / (1 - rho), so the stored power
    # per emitted unit is 4 pi B_e / (1 - rho) on average.
    total = sum(pw)
    want = 4 * math.pi * BE / (1 - RHO)
    n_paths = 5000
    sd_hits = math.sqrt(RHO) / (1 - RHO)  # standard deviation of a geometric count
    assert abs(total - want) < 4 * want * (1 - RHO) * sd_hits / math.sqrt(n_paths)
    assert all(abs(math.sqrt(sum(c * c for c in p)) - 1) < 1e-12 for p in pts)


def test_fixed_radius_is_unbiased_in_the_furnace(furnace_map) -> None:
    # Within the sphere, the cap of chord radius r has area exactly pi r^2 (Archimedes),
    # and the irradiance is constant, so the fixed-radius estimate is unbiased here.
    _, _, tree = furnace_map
    est = [furnace_radiance(tree, x, RHO, BE, r=0.15) for x in fibonacci_sphere(100)]
    m, se = mean_se(est)
    assert abs(m - furnace_exact(RHO, BE)) < 4 * se
    assert se < 0.01 * furnace_exact(RHO, BE)


def test_k_nearest_estimate_is_biased_by_k_over_k_minus_1(furnace_map) -> None:
    _, _, tree = furnace_map
    k = 10
    le = BE / math.pi
    reflected = [furnace_radiance(tree, x, RHO, BE, k=k) - le for x in fibonacci_sphere(400)]
    m, se = mean_se(reflected)
    exact = furnace_exact(RHO, BE) - le
    assert abs(m - exact * k / (k - 1)) < 4 * se
    assert m - exact > 3 * se


def test_fixed_radius_is_biased_and_not_consistent() -> None:
    # A point light over a plane. With a fixed radius R the estimate converges to the mean
    # irradiance over the disc, not to the irradiance at the center.
    phi, h, radius = 1.0, 1.0, 0.5
    center = point_light_irradiance(phi, h, 0.0)
    disc = point_light_disc_average(phi, h, radius)
    p = (1 - h / math.sqrt(h * h + radius * radius)) / 2  # the chance that a photon lands in the disc
    for n in (10000, 40000):
        pts, pw = trace_photons_point_light(n, phi, h, random.Random(n))
        tree = build_photon_map(pts, pw)
        est = tree.power_in_radius((0.0, 0.0, 0.0), radius) / (math.pi * radius * radius)
        se = math.sqrt(n * p * (1 - p)) * (phi / n) / (math.pi * radius * radius)
        assert abs(est - disc) < 4 * se
    assert center - disc > 8 * se  # the bias stays as n grows


def test_disc_average_closed_form() -> None:
    phi, h, radius = 1.0, 1.0, 0.5
    m = 4000
    # Midpoint rule over rings.
    num = sum(point_light_irradiance(phi, h, (i + 0.5) * radius / m) * 2 * math.pi * (i + 0.5) * radius / m for i in range(m)) * radius / m
    assert abs(num / (math.pi * radius * radius) - point_light_disc_average(phi, h, radius)) < 1e-8
    # For a small radius the relative bias is about -3 R^2 / (4 h^2).
    for radius in (0.05, 0.1):
        rel = point_light_disc_average(phi, h, radius) / point_light_irradiance(phi, h, 0.0) - 1
        assert abs(rel + 0.75 * radius * radius) < 2 * radius**4
