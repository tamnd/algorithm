# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/griffin-lim-algorithm/. The authors are listed in prov/KC8JAJ.jsonl.

import cmath
import math
import random

from griffin_lim_algorithm import (
    fft,
    frame_starts,
    griffin_lim,
    hann_periodic,
    ifft,
    istft_ls,
    spectral_distance,
    stft,
    with_magnitude,
)


def dft(a):
    n = len(a)
    return [sum(a[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def magnitudes(spec):
    return [[abs(v) for v in row] for row in spec]


def test_fft_against_dft() -> None:
    rng = random.Random(4)
    for n in (2, 4, 8, 16):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        assert max(abs(u - v) for u, v in zip(fft(a), dft(a))) < 1e-12
        assert max(abs(u - v) for u, v in zip(ifft(fft(a)), a)) < 1e-12


def test_least_squares_inverse_is_exact_on_consistent_stft() -> None:
    rng = random.Random(9)
    x = [rng.uniform(-1, 1) for _ in range(40)]
    for n, hop in ((8, 2), (16, 4), (16, 8)):
        w = hann_periodic(n)
        y = istft_ls(stft(x, w, hop), w, hop, len(x))
        assert max(abs(a - b) for a, b in zip(x, y)) < 1e-12


def test_least_squares_inverse_beats_perturbed_signals() -> None:
    """istft_ls is the orthogonal projection: no other real signal is closer to the given array."""
    rng = random.Random(21)
    n, hop, length = 8, 2, 24
    w = hann_periodic(n)
    frames = len(frame_starts(length, n, hop))
    spec = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(frames)]
    x = istft_ls(spec, w, hop, length)

    def dist(sig):
        return sum(abs(u - v) ** 2 for r1, r2 in zip(stft(sig, w, hop), spec) for u, v in zip(r1, r2))

    best = dist(x)
    for _ in range(200):
        y = [v + rng.gauss(0, 0.05) for v in x]
        assert dist(y) >= best - 1e-9


def test_magnitude_step_is_nearest_point() -> None:
    rng = random.Random(2)
    spec = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(4)] for _ in range(3)]
    mag = [[rng.uniform(0, 2) for _ in range(4)] for _ in range(3)]
    proj = with_magnitude(spec, mag)
    base = sum(abs(u - v) ** 2 for r1, r2 in zip(spec, proj) for u, v in zip(r1, r2))
    assert abs(base - spectral_distance(spec, mag)) < 1e-12
    for _ in range(300):
        other = [[a * cmath.exp(2j * math.pi * rng.random()) for a in row] for row in mag]
        d = sum(abs(u - v) ** 2 for r1, r2 in zip(spec, other) for u, v in zip(r1, r2))
        assert d >= base - 1e-12


def test_distance_never_increases_on_several_seeds() -> None:
    n, hop, length = 16, 4, 64
    w = hann_periodic(n)
    finals = []
    for seed in (1, 2, 3, 4, 5):
        rng = random.Random(seed)
        x0 = [rng.uniform(-1, 1) for _ in range(length)]
        mag = magnitudes(stft(x0, w, hop))
        total = sum(a * a for row in mag for a in row)
        _, hist = griffin_lim(mag, w, hop, length, 200, random.Random(100 + seed))
        for a, b in zip(hist, hist[1:]):
            assert b <= a + 1e-12 * total
        finals.append(math.sqrt(hist[-1] / total))
        assert hist[-1] < 0.1 * hist[0]
    # Measured final relative errors (sqrt of D over the energy of the target) after 200 iterations.
    want = [0.1310, 0.2184, 0.2223, 0.1625, 0.2254]
    assert all(abs(f - g) < 5e-4 for f, g in zip(finals, want))


def test_worked_example() -> None:
    w = hann_periodic(4)
    x0 = [1.0, 2.0, 3.0, 4.0]
    mag = magnitudes(stft(x0, w, 2))
    first = istft_ls([[complex(a) for a in row] for row in mag], w, 2, 4)
    want_first = [(1 - math.sqrt(2)) / 2, 2.0, (3 - math.sqrt(10)) / 2, 1.5]
    assert max(abs(a - b) for a, b in zip(first, want_first)) < 1e-12
    x, hist = griffin_lim(mag, w, 2, 4, 50, None)
    want = [48.3984, 21.7603, 6.3933, 1.9362, 0.6388, 0.2265]
    assert all(abs(a - b) < 1e-4 for a, b in zip(hist, want))
    assert hist[50] < 1e-18
    assert max(abs(a - b) for a, b in zip(x, x0)) < 1e-9


def test_zero_phase_start_also_monotone() -> None:
    n, hop, length = 16, 4, 64
    w = hann_periodic(n)
    x0 = [math.sin(2 * math.pi * 3 * i / length) + 0.5 * math.sin(2 * math.pi * 11 * i / length + 1) for i in range(length)]
    mag = magnitudes(stft(x0, w, hop))
    _, hist = griffin_lim(mag, w, hop, length, 100, None)
    assert all(b <= a + 1e-12 for a, b in zip(hist, hist[1:]))


def test_true_signal_and_its_negative_are_fixed_points() -> None:
    rng = random.Random(8)
    n, hop, length = 16, 4, 48
    w = hann_periodic(n)
    x0 = [rng.uniform(-1, 1) for _ in range(length)]
    mag = magnitudes(stft(x0, w, hop))
    for sig in (x0, [-v for v in x0]):
        assert spectral_distance(stft(sig, w, hop), mag) < 1e-20
        y = istft_ls(with_magnitude(stft(sig, w, hop), mag), w, hop, length)
        assert max(abs(a - b) for a, b in zip(y, sig)) < 1e-12
