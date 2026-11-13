# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/analytic-signal/. The authors are listed in prov/F0XV5Y.jsonl.

import math
import random

from analytic_signal import analytic_signal, dft, envelope, instantaneous_frequency, instantaneous_phase, weights


def test_weights() -> None:
    assert weights(8) == [1, 2, 2, 2, 1, 0, 0, 0]
    assert weights(7) == [1, 2, 2, 2, 0, 0, 0]


def test_worked_example() -> None:
    z = analytic_signal([1.0, 2.0, 3.0, 4.0])
    want = [1 + 1j, 2 - 1j, 3 - 1j, 4 + 1j]
    assert max(abs(a - b) for a, b in zip(z, want)) < 1e-12
    spec = dft(z)
    assert max(abs(a - b) for a, b in zip(spec, [10, -4 + 4j, -2, 0])) < 1e-12


def test_no_negative_frequencies_and_real_part_is_input() -> None:
    for seed, n in ((1, 16), (2, 17), (3, 32), (4, 9)):
        rng = random.Random(seed)
        x = [rng.uniform(-1, 1) for _ in range(n)]
        z = analytic_signal(x)
        spec = dft(z)
        for k in range(n):
            if 2 * k > n:
                assert abs(spec[k]) < 1e-12
        assert max(abs(v.real - a) for v, a in zip(z, x)) < 1e-12


def test_imaginary_part_is_orthogonal_to_input() -> None:
    rng = random.Random(11)
    x = [rng.uniform(-1, 1) for _ in range(24)]
    z = analytic_signal(x)
    assert abs(sum(a * v.imag for a, v in zip(x, z))) < 1e-12


def test_cos_becomes_complex_exponential() -> None:
    n = 32
    for k in (1, 5, 15):
        x = [math.cos(2 * math.pi * k * i / n) for i in range(n)]
        z = analytic_signal(x)
        assert max(abs(v.imag - math.sin(2 * math.pi * k * i / n)) for i, v in enumerate(z)) < 1e-12
        assert max(abs(e - 1) for e in envelope(z)) < 1e-12
        assert max(abs(f - 2 * math.pi * k / n) for f in instantaneous_frequency(z)) < 1e-12


def test_envelope_of_am_signal_when_spectra_do_not_overlap() -> None:
    n = 64
    amp = [1 + 0.5 * math.cos(2 * math.pi * 2 * i / n) for i in range(n)]
    x = [a * math.cos(2 * math.pi * 20 * i / n + 0.3) for i, a in enumerate(amp)]
    z = analytic_signal(x)
    assert max(abs(e - a) for e, a in zip(envelope(z), amp)) < 1e-12
    phase = instantaneous_phase(z)
    assert max(abs(p - (2 * math.pi * 20 * i / n + 0.3)) for i, p in enumerate(phase)) < 1e-12


def test_envelope_is_wrong_when_spectra_overlap() -> None:
    n = 64
    amp = [1 + 0.5 * math.cos(2 * math.pi * 6 * i / n) for i in range(n)]
    x = [a * math.cos(2 * math.pi * 4 * i / n) for i, a in enumerate(amp)]
    err = max(abs(e - a) for e, a in zip(envelope(analytic_signal(x)), amp))
    assert 0.39 < err < 0.41
