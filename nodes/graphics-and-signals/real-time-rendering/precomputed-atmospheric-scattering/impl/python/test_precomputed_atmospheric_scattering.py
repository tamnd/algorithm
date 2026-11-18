# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precomputed-atmospheric-scattering/. The authors are listed in prov/22XP7T.jsonl.

"""Tests of the toy: the transmittance table and single scattering against direct quadrature.

The table coordinates invert, the table matches a direct quadrature of the
optical depth, optical depth adds along a ray, the transmittance between two
points from two table lookups matches the direct value, the phase functions
integrate to 1 over the sphere, and single scattering from the table matches
the same integral with every transmittance computed directly. The color
checks at the end are measurements of the toy, not proved properties.
"""

import math
import random

import pytest

from precomputed_atmospheric_scattering import (
    BETA_R, RG, RT, TransmittanceTable, dist_to_ground, dist_to_top,
    mu_horizon, optical_depth, phase_mie, phase_rayleigh, point_on_ray, ray_of_coords,
    single_scattering, single_scattering_direct, table_coords, transmittance_to_top)

TABLE = TransmittanceTable(32, 64, 200)


def rand_ray(rng: random.Random, ground: bool = False) -> tuple[float, float]:
    r = RG + rng.uniform(0.0, RT - RG)
    mh = mu_horizon(r)
    mu = rng.uniform(-1.0, mh) if ground else rng.uniform(mh, 1.0)
    return r, mu


def test_table_coordinates_invert() -> None:
    rng = random.Random(1)
    for _ in range(500):
        x, y = rng.random(), rng.random()
        r, mu = ray_of_coords(x, y)
        assert RG - 1e-9 <= r <= RT + 1e-9 and mu >= mu_horizon(r) - 1e-9
        x2, y2 = table_coords(r, mu)
        assert abs(x - x2) < 1e-9 and abs(y - y2) < 1e-9
    # The corners: the ground looking up, the ground along the horizon, the top looking up.
    assert table_coords(RG, 1.0) == (0.0, 0.0)
    assert abs(table_coords(RG, 0.0)[1] - 1.0) < 1e-12
    assert abs(table_coords(RT, 1.0)[0] - 1.0) < 1e-12


def test_table_matches_direct_quadrature() -> None:
    rng = random.Random(2)
    for _ in range(300):
        r, mu = rand_ray(rng)
        a, b = TABLE.lookup(r, mu), transmittance_to_top(r, mu)
        assert all(abs(x - y) < 3e-3 for x, y in zip(a, b))
        assert all(0.0 < y <= 1.0 for y in b)


def test_transmittance_basics() -> None:
    assert transmittance_to_top(RT, 1.0) == (1.0, 1.0, 1.0)
    zen, hor = transmittance_to_top(RG, 1.0), transmittance_to_top(RG, 0.0)
    for c in range(3):
        assert hor[c] < zen[c] < 1.0
    # Blue light is scattered out more than red light.
    assert zen[2] < zen[1] < zen[0] and hor[2] < hor[1] < hor[0]


def test_optical_depth_adds_along_the_ray() -> None:
    rng = random.Random(3)
    for _ in range(20):
        r, mu = rand_ray(rng)
        d = dist_to_top(r, mu)
        s1 = rng.uniform(0.0, d)
        r1, mu1 = point_on_ray(r, mu, s1)
        whole = optical_depth(r, mu, d, 4000)
        parts = [a + b for a, b in zip(optical_depth(r, mu, s1, 4000), optical_depth(r1, mu1, d - s1, 4000))]
        assert all(abs(x - y) < 1e-5 * x for x, y in zip(whole, parts))


def test_transmittance_between_two_points() -> None:
    rng = random.Random(4)
    for ground in (False, True):
        for _ in range(100):
            r, mu = rand_ray(rng, ground)
            d = dist_to_ground(r, mu) if ground else dist_to_top(r, mu)
            s = rng.uniform(0.0, d)
            tau = optical_depth(r, mu, s, 400)
            want = [math.exp(-t) for t in tau]
            got = TABLE.between(r, mu, s, ground)
            assert all(abs(x - y) < 1e-2 for x, y in zip(got, want))


def test_phase_functions_are_normalized() -> None:
    def sphere_integral(f, m=20000):
        h = 2.0 / m
        acc = f(-1.0) + f(1.0)
        for k in range(1, m):
            acc += (4 if k % 2 else 2) * f(-1.0 + k * h)
        return 2.0 * math.pi * acc * h / 3.0

    assert abs(sphere_integral(phase_rayleigh) - 1.0) < 1e-9
    for g in (0.0, 0.5, 0.8):
        assert abs(sphere_integral(lambda nu: phase_mie(nu, g)) - 1.0) < 1e-6
    # With g = 0 the Cornette-Shanks function is the Rayleigh function.
    assert abs(phase_mie(0.3, 0.0) - phase_rayleigh(0.3)) < 1e-15
    assert phase_mie(1.0) > 50 * phase_mie(-1.0)


def test_single_scattering_matches_direct_transmittance() -> None:
    rays = [(RG + 0.001, 1.0, 1.0, 1.0), (RG + 0.001, 1.0, 0.5, 0.5),
            (RG + 0.001, 0.2, 0.05, 0.9), (RG + 10.0, -0.5, 0.7, 0.0),
            (RG + 30.0, 0.4, 0.3, -0.6)]
    for r, mu, mu_s, nu in rays:
        a = single_scattering(TABLE, r, mu, mu_s, nu)
        b = single_scattering_direct(r, mu, mu_s, nu)
        assert all(abs(x - y) < 1e-2 * y for x, y in zip(a, b))


def test_no_light_when_the_sun_is_far_below_the_horizon() -> None:
    assert single_scattering(TABLE, RG, 1.0, -0.5, -0.5) == (0.0, 0.0, 0.0)


def test_colors_of_the_toy_sky() -> None:
    # Measurements of the toy. Rayleigh data follow lambda^-4 within 1 percent.
    assert abs(BETA_R[2] / BETA_R[0] / (680.0 / 440.0) ** 4 - 1.0) < 1e-2
    # The zenith with the sun at 60 degrees from it is blue.
    s = single_scattering(TABLE, RG, 1.0, 0.5, 0.5)
    assert s[2] > s[1] > s[0] > 0.0
    # Looking near the sun as it sets, red and green win over blue.
    s = single_scattering(TABLE, RG, 0.2, 0.05, 0.9)
    assert s[0] > s[2] and s[1] > s[2]


def test_bad_table() -> None:
    with pytest.raises(ValueError):
        TransmittanceTable(1, 8)
