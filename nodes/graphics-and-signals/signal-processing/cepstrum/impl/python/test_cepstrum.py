# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cepstrum/. The authors are listed in prov/YRJ2PT.jsonl.

import math
import random

from cepstrum import circular_echo, dft, echo_cepstrum, fft, peak_quefrency, real_cepstrum


def test_fft_against_dft() -> None:
    rng = random.Random(1)
    for n in (1, 2, 8, 32):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        assert max(abs(u - v) for u, v in zip(fft(a), dft(a))) < 1e-12


def test_echo_alone_matches_closed_form() -> None:
    for n, d, a in ((64, 10, 0.5), (64, 7, -0.8), (128, 30, 0.3)):
        e = [0.0] * n
        e[0] = 1.0
        e[d] = a
        c = real_cepstrum(e)
        assert max(abs(u - v) for u, v in zip(c, echo_cepstrum(n, d, a))) < 1e-12


def test_cepstrum_of_impulse_is_zero_and_scale_only_moves_c0() -> None:
    n = 16
    imp = [1.0] + [0.0] * (n - 1)
    assert max(abs(v) for v in real_cepstrum(imp)) < 1e-15
    rng = random.Random(3)
    x = [rng.uniform(-1, 1) for _ in range(n)]
    c1 = real_cepstrum(x)
    c2 = real_cepstrum([3 * v for v in x])
    assert abs(c2[0] - c1[0] - math.log(3)) < 1e-12
    assert max(abs(u - v) for u, v in zip(c1[1:], c2[1:])) < 1e-12


def test_convolution_becomes_addition() -> None:
    rng = random.Random(4)
    n = 32
    s = [rng.uniform(-1, 1) for _ in range(n)]
    h = [rng.uniform(-1, 1) for _ in range(n)]
    conv = [sum(s[j] * h[(i - j) % n] for j in range(n)) for i in range(n)]
    lhs = real_cepstrum(conv)
    rhs = [u + v for u, v in zip(real_cepstrum(s), real_cepstrum(h))]
    assert max(abs(u - v) for u, v in zip(lhs, rhs)) < 1e-10


def test_peak_at_echo_delay_for_smooth_source() -> None:
    n, d = 64, 10
    s = [0.6**i for i in range(n)]
    c = real_cepstrum(circular_echo(s, d, 0.5))
    assert peak_quefrency(c, 2, n // 2) == d


def test_peak_at_echo_delay_for_noise_sources() -> None:
    n, d = 512, 37
    for seed in (1, 2, 3, 4, 5):
        rng = random.Random(seed)
        s = [rng.gauss(0, 1) for _ in range(n)]
        c = real_cepstrum(circular_echo(s, d, 0.5))
        assert peak_quefrency(c, 5, n // 2) == d
