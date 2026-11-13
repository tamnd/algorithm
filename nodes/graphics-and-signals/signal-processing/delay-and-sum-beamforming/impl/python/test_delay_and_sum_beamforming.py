# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-and-sum-beamforming/. The authors are listed in prov/HE5XFQ.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from delay_and_sum_beamforming import (arrival_delays, beam_pattern, das_weights, delay_and_sum,
                                       dirichlet_pattern, grating_lobes)


def test_page_example_values() -> None:
    w = das_weights(4, 0.5, 0.5)
    root2 = math.sqrt(2)
    want_sq = {0.5: 1.0, 0.75: (2 + root2) / 8, 0.25: (2 + root2) / 8, 0.0: 0.0, 1.0: 0.0,
               -0.25: (2 - root2) / 8, -0.75: (2 - root2) / 8}
    for u, b2 in want_sq.items():
        assert abs(beam_pattern(w, 0.5, u) ** 2 - b2) < 1e-12
    w = das_weights(4, 1.0, 0.5)
    assert abs(beam_pattern(w, 1.0, -0.5) - 1) < 1e-12  # the grating lobe at d = lambda


def test_closed_form_matches_the_defining_sum() -> None:
    rng = random.Random(5701)
    for _ in range(500):
        m = rng.randint(1, 16)
        spacing = rng.uniform(0.05, 2.5)
        u0, u = rng.uniform(-1, 1), rng.uniform(-1, 1)
        assert abs(beam_pattern(das_weights(m, spacing, u0), spacing, u)
                   - dirichlet_pattern(m, spacing, u0, u)) < 1e-9


def test_peak_is_at_the_steered_angle() -> None:
    """Brute force over a grid: for d <= lambda / 2 the only point with the full gain is u0."""
    rng = random.Random(5702)
    grid = [Fraction(k, 400) for k in range(-400, 401)]
    for _ in range(500):
        m = rng.randint(2, 12)
        spacing = Fraction(rng.randint(1, 50), 100)  # up to one half
        u0 = grid[rng.randrange(1, len(grid) - 1)]  # not endfire, where d = lambda / 2 has a lobe
        w = das_weights(m, spacing, u0)
        values = [beam_pattern(w, spacing, u) for u in grid]
        best = max(range(len(grid)), key=lambda i: values[i])
        assert grid[best] == u0
        assert abs(values[best] - 1) < 1e-12
        assert all(v < 1 - 1e-9 for u, v in zip(grid, values) if u != u0)


def lobe_exists(spacing: Fraction, u0: Fraction) -> bool:
    """The condition on the page: a grating lobe exists exactly when d >= lambda / (1 + |u0|)."""
    return spacing * (1 + abs(u0)) >= 1


def test_grating_lobes_match_the_exact_condition() -> None:
    rng = random.Random(5703)
    for _ in range(2000):
        spacing = Fraction(rng.randint(1, 300), rng.randint(1, 150))
        u0 = Fraction(rng.randint(-60, 60), 60)
        lobes = grating_lobes(spacing, u0)
        assert bool(lobes) == lobe_exists(spacing, u0)
        for u in lobes:
            assert (spacing * (u - u0)).denominator == 1 and -1 <= u <= 1 and u != u0
            assert dirichlet_pattern(7, spacing, u0, u) == 1.0
            assert abs(beam_pattern(das_weights(7, spacing, u0), spacing, u) - 1) < 1e-9


def test_some_steering_has_a_grating_lobe_iff_spacing_exceeds_half_a_wavelength() -> None:
    rng = random.Random(5704)
    for _ in range(500):
        spacing = Fraction(rng.randint(1, 400), 200)  # from 1/200 to 2
        if spacing > Fraction(1, 2):
            # steer close enough to endfire: |u0| >= 1/spacing - 1 < 1
            u0 = 1 / spacing - 1
            assert -1 < u0 < 1 and grating_lobes(spacing, u0)
        else:
            for _ in range(20):
                u0 = Fraction(rng.randint(-999, 999), 1000)  # inside (-1, 1)
                assert grating_lobes(spacing, u0) == []
    # at exactly half a wavelength only endfire steering gives a lobe, at the other endfire
    assert grating_lobes(Fraction(1, 2), Fraction(1)) == [Fraction(-1)]
    # broadside steering needs d >= lambda
    assert grating_lobes(Fraction(99, 100), Fraction(0)) == []
    assert grating_lobes(Fraction(1), Fraction(0)) == [Fraction(-1), Fraction(1)]


def test_grid_scan_finds_the_predicted_lobes() -> None:
    """Brute force: the full-gain maxima on a fine grid are u0 and the predicted lobes."""
    for spacing, u0 in ((Fraction(5, 8), Fraction(7, 10)), (Fraction(1), Fraction(1, 2)), (Fraction(2), Fraction(1, 5)),
                        (Fraction(5, 4), Fraction(-3, 10)), (Fraction(1, 2), Fraction(9, 10))):
        grid = [Fraction(k, 1000) for k in range(-1000, 1001)]
        w = das_weights(8, spacing, u0)
        peaks = [u for u in grid if beam_pattern(w, spacing, u) > 1 - 1e-9]
        assert peaks == sorted(grating_lobes(spacing, u0) + [u0])


def test_integer_delays_recover_the_source_exactly() -> None:
    rng = random.Random(5705)
    for _ in range(500):
        m = rng.randint(1, 8)
        s = [rng.randint(-100, 100) for _ in range(60)]
        delays = [rng.randint(0, 9) for _ in range(m)]
        signals = [[0] * delays[i] + s for i in range(m)]  # sensor i hears s delayed by delays[i]
        out = delay_and_sum(signals, delays)
        base, span = min(delays), max(delays) - min(delays)
        assert len(out) == base + len(s) - span
        assert out == ([0] * base + s)[:len(out)]  # every sensor gives s[t - base], or 0 before it
        assert all(isinstance(v, Fraction) for v in out)


def test_arrival_delays_of_a_uniform_array() -> None:
    # d = 0.05 m, c = 343 m/s, fs = 48 kHz, u0 = 1/2: m * 0.05 * 0.5 * 48000 / 343 samples
    got = arrival_delays([0.05 * m for m in range(5)], 0.5, 343.0, 48000.0)
    assert got == [round(m * 0.05 * 0.5 * 48000 / 343) for m in range(5)] == [0, 3, 7, 10, 14]
    assert arrival_delays([Fraction(k) for k in range(4)], Fraction(1, 2), 1, 2) == [0, 1, 2, 3]


def test_white_noise_power_drops_by_m_exactly() -> None:
    """Enumerate every pattern of independent +-1 noise: the output power is exactly 1/M."""
    for m in range(1, 9):
        total = Fraction(0)
        for signs in itertools.product((-1, 1), repeat=m):
            y = delay_and_sum([[v] for v in signs], [0] * m)[0]
            total += y * y
        assert total / 2 ** m == Fraction(1, m)


def test_off_axis_tone_comes_out_scaled_by_the_beam_pattern() -> None:
    """A tone from u reaches sensor m with m * D samples of delay; steering to D0 gives the gain B."""
    for m, d_true, d_look, period in ((4, 1, 0, 16), (6, 2, 1, 24), (5, 3, -1, 40), (8, 0, 0, 10)):
        omega = 2 * math.pi / period
        n = 400
        offset = m * 4
        signals = [[math.cos(omega * (t - i * d_true - offset)) for t in range(n)] for i in range(m)]
        look = [i * d_look + offset for i in range(m)]
        y = delay_and_sum(signals, look)  # advance sensor i by its look delay
        amp = math.sqrt(2 * sum(v * v for v in y[:period * 5]) / (period * 5))
        psi = omega * (d_true - d_look)  # the phase step between sensors
        want = 1.0 if abs(math.sin(psi / 2)) < 1e-12 else abs(math.sin(m * psi / 2) / (m * math.sin(psi / 2)))
        assert abs(amp - want) < 1e-9


def test_errors() -> None:
    with pytest.raises(ValueError):
        delay_and_sum([], [])
    with pytest.raises(ValueError):
        delay_and_sum([[1, 2]], [0, 1])
    with pytest.raises(ValueError):
        grating_lobes(Fraction(0), Fraction(0))
