# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/root-raised-cosine-filter/. The authors are listed in prov/TCPRM3.jsonl.

import math

from root_raised_cosine_filter import convolve, pair_at_symbols, rrc_pulse, rrc_taps


def rc_pulse(t: float, beta: float) -> float:
    """The raised-cosine pulse for T = 1, written out here to compare with g * g."""
    if beta > 0 and abs(abs(2 * beta * t) - 1) < 1e-12:
        x = 1 / (2 * beta)
        return math.pi / 4 * math.sin(math.pi * x) / (math.pi * x)
    s = 1.0 if t == 0 else math.sin(math.pi * t) / (math.pi * t)
    return s * math.cos(math.pi * beta * t) / (1 - (2 * beta * t) ** 2)


def test_check_values() -> None:
    assert abs(rrc_pulse(0, 0.25) - 1.0683099) < 5e-8
    assert abs(rrc_pulse(0, 0.5) - 1.1366198) < 5e-8
    assert abs(rrc_pulse(0, 0.35) - 1.0956338) < 5e-8
    assert abs(rrc_pulse(0, 0.22) - 1.0601127) < 5e-8
    assert abs(rrc_pulse(1, 0.25) - (-0.0642372)) < 5e-8
    assert abs(rrc_pulse(0.5, 0.5) - 0.5786325) < 5e-8
    assert abs(rrc_pulse(1, 0.5) - (-1 / (3 * math.pi))) < 1e-15
    assert abs(rrc_pulse(2, 0.25) - 0.0530516) < 5e-8
    assert abs(rrc_pulse(2, 0.5) - 0.0424413) < 5e-8
    # With T = 4 the pulse is the T = 1 pulse stretched by 4 and scaled by 1/2.
    assert abs(rrc_pulse(2.0, 0.5, 4.0) - rrc_pulse(0.5, 0.5) / 2) < 1e-15


def test_limits_at_the_special_points() -> None:
    for beta in (0.1, 0.22, 0.25, 0.35, 0.5, 1.0):
        for t0 in (0.0, 1 / (4 * beta), -1 / (4 * beta)):
            at = rrc_pulse(t0, beta)
            for eps in (1e-6, -1e-6):
                assert abs(rrc_pulse(t0 + eps, beta) - at) < 1e-5


def test_unit_energy() -> None:
    # g is band-limited to below 1, so the sum with step 1/8 is the integral up to the tail.
    for beta in (0.25, 0.5, 1.0):
        e = sum(rrc_pulse(n / 8, beta) ** 2 for n in range(-3200, 3201)) / 8
        assert abs(e - 1) < 1e-6


def test_two_rrc_pulses_make_a_raised_cosine() -> None:
    for beta in (0.25, 0.5, 1.0):
        g = {n: rrc_pulse(n / 8, beta) for n in range(-3300, 3301)}
        for k in range(-16, 17):  # t = k/8, from -2 to 2
            pair = sum(g[n] * g[k - n] for n in range(-3200, 3201)) / 8
            assert abs(pair - rc_pulse(k / 8, beta)) < 1e-5


def test_truncated_pair_has_small_isi() -> None:
    for beta, want in ((0.25, 5.43e-4), (0.5, 1.81e-4)):
        s = pair_at_symbols(rrc_taps(beta, 8, 8), 8)
        c = len(s) // 2
        assert abs(s[c] - 1) < 1e-12
        isi = max(abs(v) for i, v in enumerate(s) if i != c)
        assert isi < 1e-3
        assert abs(isi - want) < 5e-6


def test_one_rrc_alone_has_isi() -> None:
    for beta, want in ((0.25, 0.06013), (0.5, 0.09335)):
        g = rrc_taps(beta, 8, 8)
        c = len(g) // 2
        rel = max(abs(g[c + 8 * k]) for k in range(-8, 9) if k != 0) / g[c]
        assert abs(rel - want) < 5e-5


def test_mismatched_roll_off_has_isi() -> None:
    a = rrc_taps(0.25, 8, 8)
    b = rrc_taps(0.35, 8, 8)
    r = convolve(a, b)
    c = len(r) // 2
    isi = max(abs(r[c + 8 * k]) for k in range(-16, 17) if k != 0) / r[c]
    assert isi > 2e-3
