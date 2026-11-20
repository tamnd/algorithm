# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/outer-loop-link-adaptation/. The authors are listed in prov/ZM1GV1.jsonl.

import math
import random
from fractions import Fraction

import pytest

from outer_loop_link_adaptation import OuterLoop, olla, select_scheme, step_down_for

RATES = [0.5, 1.0, 2.0, 3.0, 4.5]
MIDPOINTS = [-2.0, 1.0, 6.0, 10.0, 15.0]
SLOPE = 1.5
THRESHOLDS = [t + math.log(9) / SLOPE for t in MIDPOINTS]  # 10% BLER points


def bler(j, snr_db):
    return 1 / (1 + math.exp(SLOPE * (snr_db - MIDPOINTS[j])))


def simulate(step_up, bias, n=20000, seed=1, target=0.1):
    """Uniform true SINR in [0, 20] dB, reports with a bias and 1 dB noise."""
    rng = random.Random(seed)
    true = [rng.uniform(0, 20) for _ in range(n)]
    reports = [g + bias + rng.gauss(0, 1) for g in true]
    coin = random.Random(seed + 1)
    bits = [0.0]

    def feedback(i, j):
        ok = coin.random() >= bler(j, true[i])
        bits[0] += RATES[j] * ok
        return ok

    schemes, offsets, nacks = olla(THRESHOLDS, reports, feedback, step_up, target)
    return nacks / n, bits[0] / n, offsets


def test_step_rule() -> None:
    assert step_down_for(9, 0.1) == pytest.approx(1)
    assert step_down_for(Fraction(9), Fraction(1, 10)) == 1
    assert step_down_for(0.5, 0.1) == pytest.approx(0.5 / 9)


def test_identity_with_integer_steps() -> None:
    """Offset = offset0 + 9 * NACKs - 1 * ACKs, exactly, for any sequence."""
    rng = random.Random(7)
    for _ in range(200):
        acks = [rng.random() < 0.85 for _ in range(rng.randint(1, 60))]
        loop = OuterLoop(Fraction(9), Fraction(1, 10), offset=Fraction(3))
        for a in acks:
            loop.update(a)
        nacks = acks.count(False)
        n = len(acks)
        assert loop.offset == 3 + 9 * nacks - (n - nacks)
        # the NACK fraction identity of the proof
        assert Fraction(nacks, n) == (loop.offset - 3) / (n * 10) + Fraction(1, 10)


def test_nine_acks_and_one_nack_return_to_start() -> None:
    loop = OuterLoop(Fraction(9), Fraction(1, 10))
    for a in [True] * 9 + [False]:
        loop.update(a)
    assert loop.offset == 0


def test_select_scheme_matches_linear_scan() -> None:
    rng = random.Random(3)
    for _ in range(500):
        x = rng.uniform(-5, 25)
        linear = 0
        for j, th in enumerate(THRESHOLDS):
            if th <= x:
                linear = j
        assert select_scheme(THRESHOLDS, x) == linear
    assert select_scheme(THRESHOLDS, THRESHOLDS[2]) == 2
    assert select_scheme(THRESHOLDS, -100) == 0


@pytest.mark.parametrize("bias", [3.0, 0.0, -3.0])
def test_nack_rate_converges_to_target(bias) -> None:
    rate, throughput, offsets = simulate(0.5, bias)
    assert abs(rate - 0.1) < 0.005
    assert throughput > 2.2


def test_fixed_table_misses_target_with_bias() -> None:
    # a step of almost zero is the inner loop alone
    rate_up, tp_up, _ = simulate(1e-12, 3.0)
    rate_down, tp_down, _ = simulate(1e-12, -3.0)
    assert rate_up > 0.25 and rate_down < 0.01
    assert tp_up < 2.1 and tp_down < 1.8


def test_offset_tracks_the_bias() -> None:
    means = []
    for bias in (3.0, 0.0, -3.0):
        _, _, offsets = simulate(0.5, bias)
        tail = offsets[len(offsets) // 2:]
        means.append(sum(tail) / len(tail))
    # the learned offsets differ by about the difference of the biases
    assert abs((means[0] - means[1]) - 3) < 0.5
    assert abs((means[1] - means[2]) - 3) < 0.5


def test_bounds_clamp_the_offset() -> None:
    loop = OuterLoop(1.0, 0.1, lower=-2.0, upper=2.0)
    for _ in range(10):
        loop.update(False)
    assert loop.offset == 2.0
    for _ in range(1000):
        loop.update(True)
    assert loop.offset == -2.0


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        step_down_for(0, 0.1)
    with pytest.raises(ValueError):
        step_down_for(1, 0)
    with pytest.raises(ValueError):
        OuterLoop(1, 1.0)
