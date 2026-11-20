# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metadynamics/. The authors are listed in prov/EGQBSZ.jsonl.
import math
import random

import pytest

from metadynamics import GridBias, double_well, free_energy_estimate, metadynamics

U, DU = double_well(8.0)  # barrier of 8 kT at kT = 1
GRID = [-2.5 + 0.01 * i for i in range(501)]


def transitions(xs):
    """Well-to-well moves, counted only when x passes from below -0.5 to above 0.5 or back."""
    side, count = None, 0
    for x in xs:
        new = -1 if x < -0.5 else (1 if x > 0.5 else side)
        if side is not None and new != side:
            count += 1
        side = new
    return count


def test_grid_bias_matches_direct_sum_and_force_is_its_derivative():
    b = GridBias(-2.5, 2.5, 501)
    b.deposit(0.3, 1.0, 0.2)
    b.deposit(-0.4, 0.5, 0.3)

    def direct(x):
        return math.exp(-0.5 * ((x - 0.3) / 0.2) ** 2) + 0.5 * math.exp(-0.5 * ((x + 0.4) / 0.3) ** 2)

    xs = [-2.0 + 0.0137 * i for i in range(290)]
    assert max(abs(b.value(x) - direct(x)) for x in xs) < 1e-6
    fd = [(b.value(x + 1e-6) - b.value(x - 1e-6)) / 2e-6 for x in xs]
    assert max(abs(f - b.deriv(x)) for f, x in zip(fd, xs)) < 1e-7
    assert b.value(3.0) == 0.0 and b.deriv(-3.0) == 0.0


def test_plain_dynamics_rarely_crosses_but_metadynamics_does():
    _, plain = metadynamics(DU, -1.0, 1.0, 0.005, 10000, 0.0, 0.2, 10, random.Random(1))
    _, meta = metadynamics(DU, -1.0, 1.0, 0.005, 10000, 0.1, 0.2, 10, random.Random(1))
    assert transitions(plain) <= 2
    assert transitions(meta) >= 20


def test_standard_bias_volume_grows_without_bound():
    # Each Gaussian adds w sigma sqrt(2 pi) to the integral of V; nothing slows the growth.
    steps, w, sigma, tau = 10000, 0.1, 0.2, 10
    bias, xs = metadynamics(DU, -1.0, 1.0, 0.005, steps, w, sigma, tau, random.Random(2))
    assert max(abs(x) for x in xs) < 2.2
    volume = sum(bias.v) * bias.dx
    assert volume == pytest.approx(steps // tau * w * sigma * math.sqrt(2 * math.pi), rel=1e-3)


def test_well_tempered_estimate_scale_factor():
    b = GridBias(-1.0, 1.0, 3)
    b.v = [1.0, 2.0, 0.5]
    assert free_energy_estimate(b, 1.0) == [-1.0, -2.0, -0.5]
    assert free_energy_estimate(b, 1.0, 7.0) == pytest.approx([-8 / 7, -16 / 7, -4 / 7])


def test_well_tempered_profile_against_exact():
    bt = 7.0
    bias, _ = metadynamics(DU, -1.0, 1.0, 0.005, 80000, 0.1, 0.2, 10, random.Random(1), bias_temp=bt)
    f = free_energy_estimate(bias, 1.0, bt)
    idx = [i for i, s in enumerate(GRID) if U(s) < 5.0]
    off = sum(U(GRID[i]) - f[i] for i in idx) / len(idx)
    assert max(abs(f[i] + off - U(GRID[i])) for i in idx) < 0.8
    # grid points 150, 250 and 350 are x = -1, 0 and 1
    assert f[250] - f[350] == pytest.approx(8.0, abs=0.7)
    assert abs(f[150] - f[350]) < 0.5
    # The bias stays bounded: well below the standard bias after the same number of hills.
    std, _ = metadynamics(DU, -1.0, 1.0, 0.005, 80000, 0.1, 0.2, 10, random.Random(1))
    assert max(bias.v) < 0.8 * max(std.v)
