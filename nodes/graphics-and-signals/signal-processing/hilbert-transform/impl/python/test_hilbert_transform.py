# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hilbert-transform/. The authors are listed in prov/MW0VT7.jsonl.

import math
import random

from hilbert_transform import dft, hilbert, hilbert_by_convolution, ideal_fir, kernel


def max_err(a, b):
    return max(abs(u - v) for u, v in zip(a, b))


def test_cos_goes_to_sin_on_a_full_period() -> None:
    for n in (8, 15, 16, 33):
        for k in range(1, (n + 1) // 2):
            if 2 * k == n:
                continue
            for phase in (0.0, 0.7):
                cos = [math.cos(2 * math.pi * k * i / n + phase) for i in range(n)]
                sin = [math.sin(2 * math.pi * k * i / n + phase) for i in range(n)]
                assert max_err(hilbert(cos), sin) < 1e-12
                assert max_err(hilbert(sin), [-v for v in cos]) < 1e-12


def test_dc_and_nyquist_are_removed() -> None:
    n = 16
    assert max_err(hilbert([1.0] * n), [0.0] * n) < 1e-12
    assert max_err(hilbert([(-1.0) ** i for i in range(n)]), [0.0] * n) < 1e-12


def test_twice_is_minus_identity_on_the_rest() -> None:
    rng = random.Random(5)
    n = 16
    x = [rng.uniform(-1, 1) for _ in range(n)]
    spec = dft(x)
    mean = spec[0].real / n
    nyq = spec[n // 2].real / n
    rest = [v - mean - nyq * (-1) ** i for i, v in enumerate(x)]
    assert max_err(hilbert(hilbert(x)), [-v for v in rest]) < 1e-12


def test_energy_and_orthogonality() -> None:
    rng = random.Random(6)
    n = 20
    x = [rng.uniform(-1, 1) for _ in range(n)]
    y = hilbert(x)
    spec = dft(x)
    lost = (abs(spec[0]) ** 2 + abs(spec[n // 2]) ** 2) / n
    assert abs(sum(v * v for v in y) - (sum(v * v for v in x) - lost)) < 1e-12
    assert abs(sum(a * b for a, b in zip(x, y))) < 1e-12


def test_kernel_closed_form_against_its_sum() -> None:
    for n in (4, 8, 12, 16):
        h = kernel(n)
        for m in range(n):
            direct = 2 / n * sum(math.sin(2 * math.pi * k * m / n) for k in range(1, n // 2))
            assert abs(h[m] - direct) < 1e-12


def test_convolution_form_equals_multiplier_form() -> None:
    rng = random.Random(7)
    for n in (4, 10, 16, 24):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        assert max_err(hilbert(x), hilbert_by_convolution(x)) < 1e-12


def test_truncated_ideal_filter_converges_slowly() -> None:
    w0 = 2 * math.pi * 0.1
    errs = []
    for half in (5, 21, 85, 341):
        h = ideal_fir(half)
        n0 = 3
        y = sum(h[m + half] * math.cos(w0 * (n0 - m)) for m in range(-half, half + 1))
        errs.append(abs(y - math.sin(w0 * n0)))
    assert errs[0] > errs[1] > errs[2] > errs[3]
    assert 0.14 < errs[0] < 0.15 and errs[3] > 5e-4
