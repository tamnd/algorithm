# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/analog-monte-carlo-transport/. The authors are listed in prov/W64KF5.jsonl.
import math
import random

import pytest

from analog_monte_carlo_transport import (
    ABSORBED,
    REFLECTED,
    TRANSMITTED,
    analog_history,
    analog_monte_carlo,
    isotropic_volume_source,
)


class FixedRng:
    """Returns the given numbers in order, so that a history can be checked by hand."""

    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def test_hand_trace():
    # L = 2 cm, sigma_t = 1, sigma_s = 0.5. The flights use xi = 1 - r.
    # r = 0.5: s = ln 2 = 0.693147, collision at x = 0.693147.
    # r = 0.7: not below 0.5, so the particle scatters; r = 0.1: mu = -0.8.
    # r = 0.4: s = -ln 0.6 = 0.510826, x = 0.693147 - 0.8 * 0.510826 = 0.284487.
    # r = 0.2: below 0.5, so the particle is absorbed after 2 collisions.
    rng = FixedRng([0.5, 0.7, 0.1, 0.4, 0.2])
    assert analog_history(0.0, 1.0, 2.0, 1.0, 0.5, rng) == (ABSORBED, 2)
    rng = FixedRng([0.5, 0.7, 0.1, 0.9])  # the second flight is 2.302585 long and leaves on the left
    assert analog_history(0.0, 1.0, 2.0, 1.0, 0.5, rng) == (REFLECTED, 1)


def test_pure_absorber_transmission():
    n = 20000
    out = analog_monte_carlo(n, 2.0, 1.0, 0.0, random.Random(7))
    p, se = out[TRANSMITTED]
    exact = math.exp(-2.0)  # 0.135335
    assert abs(p - exact) < 4.0 * math.sqrt(exact * (1 - exact) / n)
    assert out[REFLECTED][0] == 0.0
    assert se > 0.0


def test_balance_is_exact():
    n = 5000
    out = analog_monte_carlo(n, 3.0, 1.0, 0.7, random.Random(8))
    assert sum(out["counts"].values()) == n


def test_uncollided_part_with_scattering():
    # The uncollided transmission is exp(-sigma_t L) whatever the scattering is.
    n = 20000
    out = analog_monte_carlo(n, 1.5, 2.0, 1.6, random.Random(9))
    p0 = out["uncollided"][0]
    exact = math.exp(-3.0)
    assert abs(p0 - exact) < 4.0 * math.sqrt(exact * (1 - exact) / n)


@pytest.mark.parametrize("c", [0.5, 0.8])
def test_infinite_medium_collisions(c):
    # Each collision is the last one with probability 1 - c, so the number of
    # collisions is geometric with mean 1 / (1 - c) and variance c / (1 - c)^2.
    n = 20000
    out = analog_monte_carlo(n, math.inf, 1.0, c, random.Random(10), isotropic_volume_source)
    mean, se = out["collisions"]
    sd_exact = math.sqrt(c) / (1 - c)
    assert abs(mean - 1.0 / (1.0 - c)) < 4.0 * sd_exact / math.sqrt(n)
    assert se == pytest.approx(sd_exact / math.sqrt(n), rel=0.1)
    assert out["counts"][ABSORBED] == n


def test_pure_scatterer_slab_loses_nothing():
    n = 4000
    out = analog_monte_carlo(n, 2.0, 1.0, 1.0, random.Random(12))
    assert out["counts"][ABSORBED] == 0
    assert out["counts"][TRANSMITTED] + out["counts"][REFLECTED] == n
