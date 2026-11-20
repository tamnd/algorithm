# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-doppler-processing/. The authors are listed in prov/YRN86W.jsonl.

import math
import random

import pytest

from cbb import cn, dft
from range_doppler_processing import (
    doppler_bin,
    fft,
    hamming,
    point_target,
    radial_velocity,
    range_doppler,
    range_doppler_direct,
)

C = 299792458.0
BARKER13 = [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]


def close(a, b, tol=1e-9):
    return all(abs(u - v) <= tol * (1 + abs(v)) for ra, rb in zip(a, b) for u, v in zip(ra, rb))


def test_fft_matches_direct_dft():
    rng = random.Random(7101)
    for _ in range(300):
        n = 2 ** rng.randint(0, 8)
        x = [cn(rng, 1.0) for _ in range(n)]
        got, want = fft(x), dft(x)
        assert all(abs(a - b) < 1e-9 * n for a, b in zip(got, want))


def test_fft_rejects_other_lengths():
    for n in (0, 3, 6, 12):
        with pytest.raises(ValueError):
            fft([1.0] * n)


def test_worked_example():
    # Pulse s = [1, 1], P = 4 pulses of N = 5 samples, a target at delay 1 with f_d = PRF / 4.
    x = point_target(4, 5, [1, 1], 1, 0.25)
    d = range_doppler(x, [1, 1])
    want = [[0, 0, 0, 0], [4, 8, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    assert close(d, want, 1e-12)


def test_map_matches_double_sum():
    rng = random.Random(7102)
    for _ in range(500):
        p_count = 2 ** rng.randint(0, 3)
        n = rng.randint(1, 9)
        length = rng.randint(1, min(n, 4))
        x = [[cn(rng, 1.0) for _ in range(n)] for _ in range(p_count)]
        s = [cn(rng, 1.0) for _ in range(length)]
        w = [rng.uniform(0.1, 1.0) for _ in range(p_count)] if rng.random() < 0.5 else None
        assert close(range_doppler(x, s, w), range_doppler_direct(x, s, w))


def test_point_target_peak_and_bins():
    p_count, n, delay = 16, 24, 5
    for k in (0, 3, 7, 12):
        a = 0.5 - 2j
        d = range_doppler(point_target(p_count, n, BARKER13, delay, k / p_count, a), BARKER13)
        mags = [[abs(v) for v in row] for row in d]
        best = max((mags[q][r], q, r) for q in range(p_count) for r in range(len(d[0])))
        assert (best[1], best[2]) == (k, delay)
        assert best[0] == pytest.approx(abs(a) * 13 * p_count)
        # An on-bin target leaves the other Doppler bins of its range bin empty.
        assert all(mags[q][delay] < 1e-9 for q in range(p_count) if q != k)


def test_negative_doppler_and_aliasing():
    p_count, n, delay = 16, 20, 3
    base = range_doppler(point_target(p_count, n, BARKER13, delay, 3 / p_count), BARKER13)
    neg = range_doppler(point_target(p_count, n, BARKER13, delay, -3 / p_count), BARKER13)
    assert abs(neg[p_count - 3][delay]) == pytest.approx(13 * p_count)
    alias = range_doppler(point_target(p_count, n, BARKER13, delay, 3 / p_count + 1), BARKER13)
    assert close(alias, base, 1e-9)


def test_hamming_window_gain_and_sidelobes():
    p_count, n, delay = 32, 16, 1
    w = hamming(p_count)
    x = point_target(p_count, n, BARKER13, delay, 5.5 / p_count)
    rect = [abs(row[delay]) for row in range_doppler(x, BARKER13)]
    ham = [abs(row[delay]) for row in range_doppler(x, BARKER13, w)]
    on = range_doppler(point_target(p_count, n, BARKER13, delay, 5 / p_count), BARKER13, w)
    assert abs(on[5][delay]) == pytest.approx(13 * sum(w))
    # Far from the target (8 or more bins away), the Hamming window keeps the leak
    # below -40 dB of the peak; the rectangular window does not.
    far = [q for q in range(p_count) if min((q - 5.5) % p_count, (5.5 - q) % p_count) >= 8]
    assert max(ham[q] for q in far) / max(ham) < 10 ** (-40 / 20)
    assert max(rect[q] for q in far) / max(rect) > 10 ** (-40 / 20)


def test_noise_gain_is_n0_times_pulse_energy_times_p():
    # Noise only, N0 = 2, P = 8, Barker 13: E |D|^2 = N0 * 13 * 8 = 208. 150 maps, seed 7103.
    rng = random.Random(7103)
    p_count, n, n0 = 8, 20, 2.0
    acc, count = 0.0, 0
    for _ in range(150):
        x = [[cn(rng, n0) for _ in range(n)] for _ in range(p_count)]
        for row in range_doppler(x, BARKER13):
            acc += sum(abs(v) ** 2 for v in row)
            count += len(row)
    assert acc / count == pytest.approx(n0 * 13 * p_count, rel=0.06)


def test_check_values():
    wavelength, prf, p_count = C / 10e9, 10e3, 16
    assert prf / p_count == 625.0
    assert radial_velocity(prf / p_count, wavelength) == pytest.approx(9.37, abs=0.01)
    assert radial_velocity(prf / 2, wavelength) == pytest.approx(74.95, abs=0.01)
    assert C / (2 * prf) == pytest.approx(14990, abs=1)
    assert doppler_bin(1875.0, prf, p_count) == 3
    assert doppler_bin(-1875.0, prf, p_count) == 13
    assert radial_velocity(1875.0, wavelength) == pytest.approx(28.11, abs=0.01)
    assert 10 * math.log10(13 * 16) == pytest.approx(23.18, abs=0.01)


def test_bad_input():
    assert range_doppler([], [1]) == []
    with pytest.raises(ValueError):
        range_doppler([[1, 2]], [1, 1, 1])
    with pytest.raises(ValueError):
        range_doppler([[1, 2], [1]], [1])
