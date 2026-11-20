# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-flight-sampling/. The authors are listed in prov/21RHN1.jsonl.
import math
import random

import pytest

from free_flight_sampling import free_flight, optical_depth, region_of, sample_free_flight


def test_hand_values():
    # xi = 0.5 and sigma_t = 2 cm^-1 give s = ln 2 / 2.
    x, i, ev = free_flight(0.0, 1.0, 0, [0.0, 10.0], [2.0], 0.5)
    assert ev == "collide" and i == 0
    assert x == pytest.approx(0.346574, abs=1e-6)
    # Two regions: [0, 1) with 0.5 cm^-1 and [1, 3) with 2 cm^-1, xi = 0.1.
    # tau = 2.302585; region 0 uses 0.5, so 1.802585 is left for region 1.
    x, i, ev = free_flight(0.0, 1.0, 0, [0.0, 1.0, 3.0], [0.5, 2.0], 0.1)
    assert ev == "collide" and i == 1
    assert x == pytest.approx(1.901293, abs=1e-6)
    # A slanted path with mu = 0.5 doubles the path per unit of depth.
    x, i, ev = free_flight(0.0, 0.5, 0, [0.0, 1.0, 3.0], [0.5, 2.0], 0.1)
    assert ev == "collide" and i == 1
    assert x == pytest.approx(1.0 + 0.5 * (2.302585093 - 1.0) / 2.0, abs=1e-6)


def test_escape_and_void():
    # xi = 0.01 gives tau = 4.6, more than the 3 units of the slab.
    x, i, ev = free_flight(0.0, 1.0, 0, [0.0, 1.0, 2.0, 3.0], [1.0, 0.0, 2.0], 0.01)
    assert ev == "escape" and i == 3 and x == 3.0
    # A void region never holds a collision.
    rng = random.Random(5)
    for _ in range(2000):
        x, i, ev = free_flight(0.0, 1.0, 0, [0.0, 1.0, 2.0, 3.0], [1.0, 0.0, 2.0], 1.0 - rng.random())
        assert not (ev == "collide" and i == 1)
    # Moving to the left from the middle region.
    x, i, ev = free_flight(1.5, -1.0, 1, [0.0, 1.0, 2.0], [1.0, 1.0], math.exp(-0.25))
    assert ev == "collide" and i == 1 and x == pytest.approx(1.25)
    x, i, ev = free_flight(1.5, -1.0, 1, [0.0, 1.0, 2.0], [1.0, 1.0], math.exp(-2.0))
    assert ev == "escape" and i == -1 and x == 0.0


def test_uniform_mean_and_tail():
    rng = random.Random(11)
    sig, n = 2.0, 40000
    s = [sample_free_flight(sig, rng) for _ in range(n)]
    mean = sum(s) / n
    # The exponential law has mean 1/sigma and standard deviation 1/sigma.
    assert abs(mean - 1.0 / sig) < 4.0 * (1.0 / sig) / math.sqrt(n)
    for length in (0.5, 1.0, 2.0):
        p = math.exp(-sig * length)
        frac = sum(1 for v in s if v > length) / n
        assert abs(frac - p) < 4.0 * math.sqrt(p * (1 - p) / n)
    assert sample_free_flight(0.0, rng) == math.inf


def test_region_collision_probabilities_exact_law():
    # P(collision in region k) = exp(-tau before k) - exp(-tau up to the end of k).
    bounds, sigmas = [0.0, 0.5, 1.5, 2.0, 3.0], [1.0, 0.2, 3.0, 0.0]
    rng = random.Random(3)
    n = 40000
    counts = [0] * (len(sigmas) + 1)  # the last entry counts escapes
    for _ in range(n):
        x, i, ev = free_flight(0.0, 1.0, 0, bounds, sigmas, 1.0 - rng.random())
        counts[i if ev == "collide" else len(sigmas)] += 1
    cum = [0.0]
    for k, sig in enumerate(sigmas):
        cum.append(cum[-1] + sig * (bounds[k + 1] - bounds[k]))
    for k in range(len(sigmas)):
        p = math.exp(-cum[k]) - math.exp(-cum[k + 1])
        assert abs(counts[k] / n - p) <= 4.0 * math.sqrt(p * (1 - p) / n) + 1e-12
    p_esc = math.exp(-cum[-1])
    assert abs(counts[-1] / n - p_esc) < 4.0 * math.sqrt(p_esc * (1 - p_esc) / n)


def delta_tracking(x, mu, bounds, sigmas, sig_max, rng):
    """An independent method: tentative flights at a majorant, accepted with sigma / sig_max."""
    while True:
        x += mu * sample_free_flight(sig_max, rng)
        if x < bounds[0] or x >= bounds[-1]:
            return x, "escape"
        if rng.random() < sigmas[region_of(x, bounds)] / sig_max:
            return x, "collide"


def test_agrees_with_delta_tracking():
    bounds, sigmas = [0.0, 1.0, 1.7, 3.0], [0.4, 2.5, 1.0]
    rng = random.Random(21)
    n = 30000
    a = [free_flight(0.1, 0.6, 0, bounds, sigmas, 1.0 - rng.random()) for _ in range(n)]
    b = [delta_tracking(0.1, 0.6, bounds, sigmas, 2.5, rng) for _ in range(n)]
    xa = [x for x, _, ev in a if ev == "collide"]
    xb = [x for x, ev in b if ev == "collide"]
    pa, pb = len(xa) / n, len(xb) / n
    assert abs(pa - pb) < 4.0 * math.sqrt(2 * pa * (1 - pa) / n)
    ma, mb = sum(xa) / len(xa), sum(xb) / len(xb)
    va = sum((v - ma) ** 2 for v in xa) / (len(xa) - 1)
    assert abs(ma - mb) < 4.0 * math.sqrt(2 * va / min(len(xa), len(xb)))


def test_optical_depth():
    assert optical_depth(0.0, 3.0, 1.0, [0.0, 1.0, 3.0], [0.5, 2.0]) == pytest.approx(4.5)
    assert optical_depth(3.0, 0.5, -0.5, [0.0, 1.0, 3.0], [0.5, 2.0]) == pytest.approx(2 * 4.25)
