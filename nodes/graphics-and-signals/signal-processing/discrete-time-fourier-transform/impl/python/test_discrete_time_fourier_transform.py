# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-time-fourier-transform/. The authors are listed in prov/0QHXWM.jsonl.

import cmath
import math
import random

from discrete_time_fourier_transform import dirichlet, dtft, dtft_at_bins, fold, inverse_from_bins

TOL = 1e-9


def fft(a: list[complex]) -> list[complex]:
    """Recursive radix-2 Cooley-Tukey FFT, an independent reference."""
    n = len(a)
    if n == 1:
        return [complex(a[0])]
    even = fft(a[0::2])
    odd = fft(a[1::2])
    out = [0j] * n
    for k in range(n // 2):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + t
        out[k + n // 2] = even[k] - t
    return out


def close(a: complex, b: complex, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * (1 + abs(b))


def test_exact_example() -> None:
    # e^(-i pi k / 2) is 1, -i, -1, i, so the N = 4 DFT of integers is a Gaussian integer.
    x = [1, 2, 0, -1]
    want = [2, 1 - 3j, 0, 1 + 3j]
    got = dtft_at_bins(x, 4)
    assert all(close(g, w) for g, w in zip(got, want))


def test_dft_frequencies_against_fft() -> None:
    rng = random.Random(7)
    for n in (1, 2, 4, 8, 16, 32):
        for _ in range(20):
            x = [complex(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)]
            assert all(close(g, w) for g, w in zip(dtft_at_bins(x, n), fft(x)))


def test_zero_padding_samples_the_dtft_densely() -> None:
    rng = random.Random(8)
    for _ in range(20):
        x = [float(rng.randint(-5, 5)) for _ in range(rng.randint(1, 8))]
        padded = x + [0.0] * (32 - len(x))
        assert all(close(g, w) for g, w in zip(dtft_at_bins(x, 32), fft(padded)))


def test_inverse_at_bins_for_any_length() -> None:
    rng = random.Random(9)
    for n in range(1, 13):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        values = dtft_at_bins(x, n)
        assert all(close(inverse_from_bins(values, j), x[j]) for j in range(n))


def test_periodic_and_conjugate_symmetric() -> None:
    rng = random.Random(10)
    x = [rng.uniform(-1, 1) for _ in range(9)]
    for _ in range(50):
        w = rng.uniform(-math.pi, math.pi)
        assert close(dtft(x, w), dtft(x, w + 2 * math.pi))
        assert close(dtft(x, -w), dtft(x, w).conjugate())


def test_shift_multiplies_by_a_phase() -> None:
    x = [3.0, -1.0, 2.0]
    for w in (0.3, 1.1, 2.9):
        assert close(dtft(x, w, start=5), cmath.exp(-5j * w) * dtft(x, w))


def test_dirichlet_closed_form() -> None:
    for length in range(1, 12):
        box = [1.0] * length
        for j in range(-200, 201):
            w = j * math.pi / 100
            assert close(dirichlet(length, w), dtft(box, w))


def test_folding_explains_the_dft_of_a_long_sequence() -> None:
    # x[n] = (1/2)^n for n >= 0 has the DTFT 1 / (1 - e^(-i w) / 2).
    x = [0.5**n for n in range(80)]
    for n in (1, 3, 4, 7):
        got = dtft_at_bins(fold(x, n), n)
        for k in range(n):
            w = 2 * math.pi * k / n
            assert close(got[k], 1 / (1 - 0.5 * cmath.exp(-1j * w)))


def test_convolution_becomes_a_product() -> None:
    rng = random.Random(11)
    a = [rng.uniform(-1, 1) for _ in range(6)]
    b = [rng.uniform(-1, 1) for _ in range(4)]
    c = [sum(a[i] * b[k - i] for i in range(len(a)) if 0 <= k - i < len(b)) for k in range(len(a) + len(b) - 1)]
    for w in (0.0, 0.7, 2.0, math.pi):
        assert close(dtft(c, w), dtft(a, w) * dtft(b, w))
