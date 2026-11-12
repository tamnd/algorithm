# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instant-radiosity/. The authors are listed in prov/H80DBM.jsonl.

import math
import random

import pytest

from instant_radiosity import (
    cosine_direction,
    floor_scene,
    floor_sensor_exact,
    furnace_exact,
    furnace_scene,
    gather,
    generate_vpls,
)


def _mean_sd(values):
    m = sum(values) / len(values)
    return m, math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def test_cosine_direction_has_the_right_mean_cosine():
    rng = random.Random(5)
    n = (0.0, 0.6, -0.8)
    cs = [sum(a * b for a, b in zip(cosine_direction(n, rng), n)) for _ in range(20000)]
    assert min(cs) >= -1e-12
    # E[cos] = 2/3 for the density cos / pi; the standard deviation of cos is sqrt(1/2 - 4/9).
    assert abs(sum(cs) / len(cs) - 2 / 3) < 4 * math.sqrt(0.5 - 4 / 9) / math.sqrt(len(cs))


def test_furnace_is_unbiased_without_clamping():
    rho, b_e, n = 0.5, 1.0, 500
    vals = []
    for seed in range(40):
        sl, nv = furnace_scene(b_e, rho, n)
        vpls = generate_vpls(n, sl, nv, random.Random(seed))
        vals.append(gather((0.0, 0.0, -1.0), (0.0, 0.0, 1.0), rho, vpls))
    m, _ = _mean_sd(vals)
    # In the sphere every VPL adds the same amount, so the estimate is rho / pi (1 + rho S / n) with S the
    # number of surface vertices, a sum of n geometric counts with mean 1/(1-rho) and variance rho/(1-rho)^2.
    sd_one = rho * rho / math.pi * math.sqrt(rho / (1 - rho) ** 2 / n)
    assert abs(m - furnace_exact(b_e, rho)) < 4 * sd_one / math.sqrt(len(vals))


def test_furnace_estimate_is_the_same_everywhere():
    rho = 0.7
    sl, nv = furnace_scene(1.0, rho, 200)
    vpls = generate_vpls(200, sl, nv, random.Random(9))
    values = []
    for p in [(0.0, 0.0, -1.0), (1.0, 0.0, 0.0), (0.0, -0.6, 0.8)]:
        values.append(gather(p, (-p[0], -p[1], -p[2]), rho, vpls))
    assert max(values) - min(values) < 1e-12 * max(values)


def test_vpl_count_follows_russian_roulette():
    rho, n = 0.6, 4000
    sl, nv = furnace_scene(1.0, rho, n)
    vpls = generate_vpls(n, sl, nv, random.Random(1))
    surface = len(vpls) - n
    # n light vertices, and about n / (1 - rho) surface vertices.
    assert abs(surface - n / (1 - rho)) < 4 * math.sqrt(n * rho) / (1 - rho)


def test_floor_exact_matches_the_closed_form():
    # With the sensor at the height of the light, the one-bounce radiance is rho_x rho phi / (10 pi^2 a^2).
    for a in (0.5, 1.0, 2.0):
        exact = floor_sensor_exact(1.0, a, 0.5, a, 1.0)
        assert math.isclose(exact, 0.5 / (10 * math.pi**2 * a * a), rel_tol=1e-8)


def test_clamp_changes_nothing_when_the_bound_is_never_reached():
    # The largest geometry term on the axis is 1 / a^2.
    assert floor_sensor_exact(1.0, 1.0, 0.5, 0.5, 1.0, 4.0) == floor_sensor_exact(1.0, 1.0, 0.5, 0.5, 1.0)
    assert floor_sensor_exact(1.0, 1.0, 0.5, 0.2, 1.0, 4.0) < floor_sensor_exact(1.0, 1.0, 0.5, 0.2, 1.0)


@pytest.mark.parametrize("a", [0.5, 0.2, 0.1])
def test_floor_unclamped_and_clamped_match_their_integrals(a):
    phi, h, rho, n = 1.0, 1.0, 0.5, 2000
    plain, clamped = [], []
    for seed in range(30):
        sl, nv = floor_scene(phi, h, rho, n)
        vpls = generate_vpls(n, sl, nv, random.Random(1000 + seed))
        plain.append(gather((0.0, 0.0, a), (0.0, 0.0, -1.0), 1.0, vpls))
        clamped.append(gather((0.0, 0.0, a), (0.0, 0.0, -1.0), 1.0, vpls, 4.0))
    mp, sp = _mean_sd(plain)
    mc, sc = _mean_sd(clamped)
    exact = floor_sensor_exact(phi, h, rho, a, 1.0)
    exact_clamped = floor_sensor_exact(phi, h, rho, a, 1.0, 4.0)
    assert abs(mp - exact) < 4 * sp / math.sqrt(30)
    assert abs(mc - exact_clamped) < 4 * sc / math.sqrt(30) + 1e-15
    assert sc <= sp + 1e-15  # the clamp never adds variance here


def test_clamping_bias_grows_near_the_floor():
    biases = [floor_sensor_exact(1.0, 1.0, 0.5, a, 1.0, 4.0) / floor_sensor_exact(1.0, 1.0, 0.5, a, 1.0) - 1 for a in (0.4, 0.2, 0.1, 0.05)]
    assert all(b < 0 for b in biases)
    assert biases == sorted(biases, reverse=True)
    assert biases[-1] < -0.8
