# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latency-hiding/.

from fractions import Fraction

from latency_hiding import bytes_in_flight, needed_parallelism, predicted_rate, simulate


def test_littles_law_examples():
    assert needed_parallelism(18, 32) == 576  # Volkov slide 11, GF100
    assert needed_parallelism(24, 8) == 192  # Volkov slide 11, G80 to GT200
    assert needed_parallelism(18, 48) == 864  # Volkov slide 11, GF104
    per_sm = bytes_in_flight(1555 * 10**9, Fraction(500, 10**9)) / 108  # page example, assumed latency
    assert 7199 < per_sm < 7200
    assert per_sm / 128 > 56


def test_simulated_rate_matches_min_of_one_and_parallelism_over_latency():
    for latency in (1, 4, 8, 20):
        for warps in (1, 2, 3, 4, 8, 16):
            for ilp in (1, 2, 4):
                per_warp = 40 * latency
                cycles = simulate(warps, ilp, latency, per_warp)
                rate = Fraction(warps * per_warp, cycles)
                pred = predicted_rate(warps, ilp, latency)
                # The last chain of each warp needs no wait, so a finite run is a little faster.
                assert abs(rate - pred) <= pred / 10
                # The scheduler can never be busier than one issue per cycle.
                assert rate <= 1


def test_ilp_replaces_warps():
    latency = 16
    assert predicted_rate(16, 1, latency) == 1
    assert predicted_rate(4, 4, latency) == 1
    assert predicted_rate(4, 1, latency) == Fraction(1, 4)
    c1 = simulate(4, 1, latency, 200)
    c4 = simulate(4, 4, latency, 200)
    assert c1 > 3 * c4
