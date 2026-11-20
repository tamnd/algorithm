# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-forcing-equalizer/. The authors are listed in prov/2260NZ.jsonl.

import math
import random

import pytest

import cbb
from zero_forcing_equalizer import (
    combined_response,
    equalize,
    forcing_window,
    noise_gain,
    peak_distortion,
    zf_equalizer,
)

PROAKIS_B = [0.407, 0.815, 0.407]


def close(a, b, tol=1e-12):
    return len(a) == len(b) and all(abs(p - q) <= tol for p, q in zip(a, b))


def qpsk(rng):
    return complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / math.sqrt(2)


def slice_qpsk(z):
    return complex(1 if z.real >= 0 else -1, 1 if z.imag >= 0 else -1) / math.sqrt(2)


def test_example_on_the_page() -> None:
    c = zf_equalizer([1, 0.5], 5, 0)
    assert close(c, [1, -0.5, 0.25, -0.125, 0.0625])
    g = combined_response(c, [1, 0.5])
    assert close(g, [1, 0, 0, 0, 0, 0.03125])
    assert abs(peak_distortion(g, 0) - 0.03125) < 1e-12
    assert abs(noise_gain(c) - 1.33203125) < 1e-12
    # the delay 2 centers the window: g = (0, 0, 1, 0, 0, 0.125)
    assert close(combined_response(zf_equalizer([1, 0.5], 5, 2), [1, 0.5]), [0, 0, 1, 0, 0, 0.125])


def test_noise_gain_closed_form_for_two_taps() -> None:
    # for h = (1, a) and delay 0, c[k] = (-a)^k, so ||c||^2 = (1 - |a|^(2N)) / (1 - |a|^2)
    for a in (0.5, 0.9, -0.3 + 0.4j):
        for n in (1, 4, 9, 30):
            want = (1 - abs(a) ** (2 * n)) / (1 - abs(a) ** 2)
            assert abs(noise_gain(zf_equalizer([1, a], n, 0)) - want) < 1e-9 * want


def test_forcing_conditions_hold_on_random_channels() -> None:
    rng = random.Random(6101)
    done = 0
    while done < 200:
        taps, n = rng.randint(1, 5), rng.randint(1, 9)
        h = [cbb.cn(rng, 1.0) for _ in range(taps)]
        delay = rng.randint(0, n + taps - 2)
        c = zf_equalizer(h, n, delay)
        g = combined_response(c, h)
        s = forcing_window(taps, n, delay)
        if noise_gain(c) > 1e6:
            continue  # nearly singular: the forcing still holds, but not to 1e-9
        want = [1 if k == delay else 0 for k in range(s, s + n)]
        assert close(g[s : s + n], want, 1e-9)
        done += 1


def test_noiseless_data_are_recovered_exactly() -> None:
    rng = random.Random(6102)
    for h, n, delay in (([1, 0.5], 5, 0), ([0.5, 1], 7, 6), (PROAKIS_B, 31, 16), ([0.8, -0.4j, 0.2], 11, 1)):
        x = [qpsk(rng) for _ in range(400)]
        y = cbb.conv(x, h)
        c = zf_equalizer(h, n, delay)
        assert peak_distortion(combined_response(c, h), delay) < 1  # the eye is open
        z = equalize(c, y, delay, len(x))
        assert [slice_qpsk(v) for v in z] == x


def test_output_noise_variance_is_n0_times_noise_gain() -> None:
    rng = random.Random(6103)
    c = zf_equalizer([1, 0.9], 9, 0)
    n0, runs = 0.2, 6000
    acc = 0.0
    for _ in range(runs):
        w = [cbb.cn(rng, n0) for _ in range(len(c))]
        acc += abs(sum(ci * wi for ci, wi in zip(c, reversed(w)))) ** 2 / runs
    want = n0 * noise_gain(c)
    assert abs(acc - want) < 0.06 * want  # 6000 runs, seed 6103


def test_bpsk_error_rate_after_zf_matches_the_formula() -> None:
    # h = (1, 0.5) with N = 15: the residual ISI is 0.5^15, so the output is x + Gaussian noise
    rng = random.Random(6104)
    h, n, n0, count = [1, 0.5], 15, 0.277, 20000
    c = zf_equalizer(h, n, 0)
    x = [rng.choice((-1.0, 1.0)) for _ in range(count)]
    y = cbb.awgn(rng, cbb.conv(x, h), n0)
    z = equalize(c, y, 0, count)
    errors = sum((v.real >= 0) != (s > 0) for v, s in zip(z, x))
    p = cbb.qfunc(math.sqrt(2 / (n0 * noise_gain(c))))  # real noise variance N0 ||c||^2 / 2, Es = 1
    lo, hi = cbb.wilson(errors, count)  # z = 3.29, about 200 errors expected
    assert lo <= p <= hi


def test_lucky_peak_distortion_is_minimal_when_the_eye_is_open() -> None:
    rng = random.Random(6105)
    done = 0
    while done < 60:
        taps, k = rng.randint(2, 4), rng.randint(1, 3)
        n = 2 * k + 1
        h = [rng.uniform(-1, 1) for _ in range(taps)]
        p = max(range(taps), key=lambda i: abs(h[i]))
        if sum(abs(v) for v in h) / abs(h[p]) - 1 >= 1:
            continue  # Lucky's theorem needs an initial distortion D0 < 1
        delay = p + k  # the cursor of h under the center tap of c
        c = zf_equalizer(h, n, delay)
        best = peak_distortion(combined_response(c, h), delay)
        for scale in (1e-1, 1e-2, 1e-4):
            for _ in range(20):
                d = [rng.uniform(-1, 1) for _ in range(n)]
                gd = combined_response(d, h)[delay]
                d = [a - gd * b for a, b in zip(d, c)]  # keep g[delay] = 1
                other = [a + scale * b for a, b in zip(c, d)]
                assert peak_distortion(combined_response(other, h), delay) >= best - 1e-12
        done += 1


def test_delay_matters_for_a_maximum_phase_channel() -> None:
    gains = [noise_gain(zf_equalizer([0.5, 1], 5, d)) for d in range(6)]
    assert abs(gains[0] - 1364) < 1e-9 and abs(gains[5] - 1.33203125) < 1e-9
    assert min(range(6), key=lambda d: gains[d]) == 3


def test_proakis_channel_b_has_a_huge_noise_gain() -> None:
    assert abs(PROAKIS_B[0] - PROAKIS_B[1] + PROAKIS_B[2] + 0.001) < 1e-12  # H at half the symbol rate
    best = min(noise_gain(zf_equalizer(PROAKIS_B, 31, d)) for d in range(32))
    assert 2000 < best < 3000
    a, b = 0.815, 0.814  # |H(w)| = |0.815 + 0.814 cos w|; the infinite-length gain is a / (a^2 - b^2)^(3/2)
    assert 12390 < a / (a * a - b * b) ** 1.5 < 12400


def test_errors() -> None:
    with pytest.raises(ValueError):
        zf_equalizer([0, 1], 3, 0)  # h[0] = 0 makes the triangular system singular
    with pytest.raises(ValueError):
        zf_equalizer([1, 0.5], 3, 4)  # the delay must be at most N + L - 2 = 3
    with pytest.raises(ValueError):
        zf_equalizer([], 3, 0)
