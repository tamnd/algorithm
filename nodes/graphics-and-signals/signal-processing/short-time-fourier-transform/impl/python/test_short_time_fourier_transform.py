# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/short-time-fourier-transform/. The authors are listed in prov/YJH16Z.jsonl.

import random
from fractions import Fraction

import pytest

from short_time_fourier_transform import (
    dft,
    fft,
    frame_starts,
    hann_periodic,
    hann_symmetric,
    is_cola,
    istft_ola,
    istft_wola,
    overlap_sums,
    stft,
    stft_direct,
    triangle_periodic,
)


def max_err(a, b):
    return max(abs(u - v) for u, v in zip(a, b))


def test_fft_against_dft() -> None:
    rng = random.Random(11)
    for n in (1, 2, 4, 8, 16, 32):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        assert max_err(fft(a), dft(a)) < 1e-12


def test_frames_cover_every_sample_equally() -> None:
    for length, n, hop in ((10, 4, 2), (37, 16, 4), (5, 8, 8), (20, 6, 3)):
        starts = frame_starts(length, n, hop)
        brute = [s for s in range(-10 * n, length + 10 * n) if s % hop == 0 and s < length and s + n > 0]
        assert starts == brute
        counts = [sum(1 for s in starts if s <= i < s + n) for i in range(length)]
        if n % hop == 0:
            assert counts == [n // hop] * length


def test_stft_against_direct_sum() -> None:
    rng = random.Random(3)
    x = [rng.uniform(-1, 1) for _ in range(30)]
    for w, hop in ((hann_periodic(8), 2), (hann_symmetric(6), 3), ([1.0] * 5, 2)):
        _, frames = stft(x, w, hop)
        ref = stft_direct(x, w, hop)
        assert len(frames) == len(ref)
        for f, r in zip(frames, ref):
            assert max_err(f, r) < 1e-12


def test_worked_example() -> None:
    starts, frames = stft([1, 2, 3, 4], hann_periodic(4), 2)
    assert starts == [-2, 0, 2]
    want = [[2, -1 + 1j, 0, -1 - 1j], [6, -3 + 1j, 0, -3 - 1j], [2, -2j, -2, 2j]]
    for f, g in zip(frames, want):
        assert max_err(f, g) < 1e-12
    assert max_err(istft_ola(starts, frames, 4, 1.0), [1, 2, 3, 4]) < 1e-12


def test_cola_exact_with_fractions() -> None:
    for n in (4, 8, 16):
        w = triangle_periodic(n)
        assert overlap_sums(w, n // 2) == [Fraction(1)] * (n // 2)
    assert overlap_sums([1] * 16, 4) == [4, 4, 4, 4]
    assert overlap_sums([1] * 16, 6) == [3, 3, 3, 3, 2, 2]


@pytest.mark.parametrize("n,hop,gain", [(16, 8, 1.0), (16, 4, 2.0), (32, 8, 2.0), (32, 16, 1.0)])
def test_ola_reconstructs_for_cola_window(n, hop, gain) -> None:
    w = hann_periodic(n)
    assert is_cola(w, hop, 1e-12)
    assert abs(overlap_sums(w, hop)[0] - gain) < 1e-12
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        x = [rng.uniform(-1, 1) for _ in range(100)]
        starts, frames = stft(x, w, hop)
        assert max_err(istft_ola(starts, frames, len(x), gain), x) < 1e-12


def test_ola_fails_for_non_cola_window() -> None:
    rng = random.Random(1)
    x = [rng.uniform(-1, 1) for _ in range(100)]
    for w, hop in ((hann_symmetric(16), 8), ([1.0] * 16, 6), (hann_periodic(16), 6)):
        sums = overlap_sums(w, hop)
        assert max(sums) - min(sums) > 0.05
        gain = sum(sums) / len(sums)
        starts, frames = stft(x, w, hop)
        err = max_err(istft_ola(starts, frames, len(x), gain), x)
        assert err > 0.01
        # The error is the ripple of the overlap sum times the signal.
        bound = max(abs(s / gain - 1) for s in sums) * max(abs(v) for v in x)
        assert err <= bound + 1e-12
    starts, frames = stft(x, hann_symmetric(16), 8)
    err = max_err(istft_ola(starts, frames, len(x), 0.9375), x)
    assert 0.054 < err < 0.0542


def test_wola_inverts_any_covering_window() -> None:
    rng = random.Random(5)
    x = [rng.uniform(-1, 1) for _ in range(90)]
    for w, hop in ((hann_symmetric(16), 8), ([1.0] * 16, 6), (hann_periodic(16), 6), (hann_periodic(32), 8)):
        starts, frames = stft(x, w, hop)
        assert max_err(istft_wola(starts, frames, w, len(x)), x) < 1e-12


def test_wola_rejects_a_gap() -> None:
    w = [0.0, 1.0, 1.0, 0.0]
    starts, frames = stft([1.0] * 12, w, 4)
    with pytest.raises(ValueError):
        istft_wola(starts, frames, w, 12)
