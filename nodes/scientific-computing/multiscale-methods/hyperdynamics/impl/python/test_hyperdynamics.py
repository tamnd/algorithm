# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperdynamics/. The authors are listed in prov/W145MS.jsonl.
import math
import random

import pytest

from hyperdynamics import flat_bias, hyperdynamics

KT = 0.25
V_C = 0.6


def double_well(x):
    return (x[0] ** 2 - 1.0) ** 2, [4.0 * x[0] * (x[0] ** 2 - 1.0)]


def in_left(x):
    return x[0] < 0.0


def past_barrier(x):
    return x[0] >= 0.5


class ZeroNoise:
    def gauss(self, mu, sigma):
        return 0.0


def exact_times(kT, v_c, x_b=0.5, lo=-2.5, n=4000):
    """Mean escape times from x = -1 to x_b for the dynamics of the module.

    Returns (T, T_boost, T_wall): the unbiased mean first passage time, the
    mean of the boosted clock, and the mean simulated time of the biased run,
    from the formula T(y) = (1/kT) int_y^x_b e^(beta U(z)) int_-inf^z w(u) du dz
    with U = V or V + dV and w = e^(-beta V) or e^(-beta (V + dV)).
    """
    beta = 1.0 / kT

    def v(u):
        return (u * u - 1.0) ** 2

    def vb(u):
        return v(u) + (max(0.0, v_c - v(u)) if u < 0.0 else 0.0)

    dz = (x_b - lo) / n
    t = tb = tw = cum = cumb = 0.0
    for i in range(n):
        m = lo + (i + 0.5) * dz
        cum += 0.5 * math.exp(-beta * v(m)) * dz
        cumb += 0.5 * math.exp(-beta * vb(m)) * dz
        if m > -1.0:
            t += math.exp(beta * v(m)) * cum * dz
            tb += math.exp(beta * vb(m)) * cum * dz
            tw += math.exp(beta * vb(m)) * cumb * dz
        cum += 0.5 * math.exp(-beta * v(m)) * dz
        cumb += 0.5 * math.exp(-beta * vb(m)) * dz
    return t / kT, tb / kT, tw / kT


def test_flat_bias_values():
    bias = flat_bias(double_well, V_C, in_left)
    assert bias([-1.0]) == (pytest.approx(0.6), [pytest.approx(0.0)])
    # Near the barrier top V > V_C, so the bias is zero.
    assert bias([-0.2])[0] == 0.0
    # Outside the basin the bias is zero even where V < V_C.
    assert bias([1.0])[0] == 0.0
    # On the floor, V + dV is flat: the two gradients cancel.
    x = [-1.2]
    assert double_well(x)[1][0] + bias(x)[1][0] == pytest.approx(0.0, abs=1e-12)


def test_clock_by_hand():
    bias = flat_bias(double_well, V_C, in_left)
    x, t, steps, done = hyperdynamics([-1.0], double_well, bias, KT, 0.02, past_barrier, ZeroNoise(), max_steps=2)
    assert not done and steps == 2
    assert x == [-1.0]
    assert t == pytest.approx(2 * 0.02 * math.exp(0.6 / 0.25))
    assert t == pytest.approx(0.440927, abs=1e-6)


def test_zero_bias_is_plain_dynamics():
    zero = flat_bias(double_well, -1.0, in_left)
    x, t, steps, done = hyperdynamics([-1.0], double_well, zero, KT, 0.02, past_barrier, random.Random(3), max_steps=500)
    assert t == pytest.approx(steps * 0.02)


def test_exact_times_of_the_page():
    t, tb, tw = exact_times(KT, V_C)
    assert t == pytest.approx(65.925, abs=1e-2)
    assert tb == pytest.approx(71.527, abs=1e-2)
    assert tw == pytest.approx(14.591, abs=1e-2)
    # Without a bias the three agree.
    t0, tb0, tw0 = exact_times(KT, 0.0)
    assert t0 == pytest.approx(tb0) and t0 == pytest.approx(tw0)


def test_boosted_escape_times_are_statistically_right():
    # At most 10000 steps in total: the check is loose, about 3 standard errors.
    h = 0.02
    rng = random.Random(1)
    bias = flat_bias(double_well, V_C, in_left)
    hyper, wall = [], []
    used = 0
    while used < 10000:
        x, t, steps, done = hyperdynamics([-1.0], double_well, bias, KT, h, past_barrier, rng,
                                          max_steps=10000 - used)
        used += steps
        if done:
            hyper.append(t)
            wall.append(steps * h)
    n = len(hyper)
    assert n >= 10
    mean = sum(hyper) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in hyper) / (n - 1))
    _, tb, tw = exact_times(KT, V_C)
    assert abs(mean - tb) < 3.0 * sd / math.sqrt(n)
    # The measured boost of the runs: hyper time over simulated time.
    boost = sum(hyper) / sum(wall)
    assert 3.0 < boost < 7.0
