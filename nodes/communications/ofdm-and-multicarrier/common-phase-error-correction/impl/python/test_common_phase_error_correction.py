# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-phase-error-correction/. The authors are listed in prov/3R84JE.jsonl.

import cmath
import math
import random

import cbb
from common_phase_error_correction import correct, estimate_phase

S = 1 / math.sqrt(2)
N = 64
TAPS = [0.9, 0.3j, -0.2]
PILOTS = list(range(4, N, 8))


def qpsk(rng: random.Random, n: int) -> list[complex]:
    return [complex(rng.choice((S, -S)), rng.choice((S, -S))) for _ in range(n)]


def slice_qpsk(z: complex) -> complex:
    return complex(S if z.real >= 0 else -S, S if z.imag >= 0 else -S)


def wiener_phase(rng: random.Random, n: int, var: float, start: float) -> list[float]:
    """phi[0] = start, then independent steps of variance var (var = 2 pi beta T_s for linewidth beta)."""
    out = [start]
    for _ in range(n - 1):
        out.append(out[-1] + rng.gauss(0.0, math.sqrt(var)))
    return out


def receive(rng: random.Random, x: list[complex], phi: list[float], n0: float) -> list[complex]:
    """Subcarrier values through the channel (prefix assumed long enough), phase noise and AWGN."""
    t = cbb.cconv(cbb.uidft(x), TAPS, len(x))
    r = [v * cmath.exp(1j * p) for v, p in zip(t, phi)]
    return cbb.udft(cbb.awgn(rng, r, n0) if n0 > 0 else r)


def test_a_constant_phase_is_removed_exactly() -> None:
    rng = random.Random(1)
    h = cbb.dft(TAPS + [0j] * (N - len(TAPS)))
    for theta in (0.3, -2.0, 3.1):
        x = qpsk(rng, N)
        y = receive(rng, x, [theta] * N, 0.0)
        assert abs(estimate_phase(y, h, PILOTS, [x[p] for p in PILOTS]) - theta) < 1e-9
        z = correct(y, h, PILOTS, [x[p] for p in PILOTS])
        assert max(abs(a - b) for a, b in zip(z, x)) < 1e-9


def test_the_pilot_sum_is_unbiased_for_i0() -> None:
    # Fixed phase noise, random data: E[C] = I_0 sum |H[p] X_p|^2, because the ICI terms have zero mean.
    rng = random.Random(2)
    h = cbb.dft(TAPS + [0j] * (N - len(TAPS)))
    phi = wiener_phase(rng, N, 0.01, 0.7)
    i0 = sum(cmath.exp(1j * p) for p in phi) / N
    acc = 0j
    trials = 200
    for _ in range(trials):
        x = qpsk(rng, N)
        y = receive(rng, x, phi, 0.0)
        c = sum(y[p] * (h[p] * x[p]).conjugate() for p in PILOTS)
        acc += c / sum(abs(h[p] * x[p]) ** 2 for p in PILOTS)
    assert abs(acc / trials - i0) < 0.01


def test_symbol_errors_with_and_without_correction() -> None:
    # Measurement: N = 64, 8 pilots, per-sample phase step variance 0.002, a random start phase,
    # N0 = 0.02, 100 symbols, seed 3. Without correction about 3 in 4 data symbols are wrong;
    # with CPE correction about as few errors as with the true angle of I_0.
    rng = random.Random(3)
    h = cbb.dft(TAPS + [0j] * (N - len(TAPS)))
    data = [k for k in range(N) if k not in PILOTS]
    e_none = e_cpe = e_true = 0
    trials = 100
    for _ in range(trials):
        phi = wiener_phase(rng, N, 0.002, rng.uniform(-math.pi, math.pi))
        x = qpsk(rng, N)
        y = receive(rng, x, phi, 0.02)
        i0 = sum(cmath.exp(1j * p) for p in phi) / N
        z = correct(y, h, PILOTS, [x[p] for p in PILOTS])
        rot = cmath.exp(-1j * cmath.phase(i0))
        e_cpe += sum(slice_qpsk(z[k]) != x[k] for k in data)
        e_true += sum(slice_qpsk(y[k] * rot / h[k]) != x[k] for k in data)
        e_none += sum(slice_qpsk(y[k] / h[k]) != x[k] for k in data)
    total = trials * len(data)
    assert e_none > 0.5 * total
    assert e_cpe < 0.01 * total
    assert e_cpe <= e_true + 10


def test_power_left_in_i0() -> None:
    # Closed form for Wiener phase noise: E|I_0|^2 = (1/N^2) sum over n, m of e^(-var |n - m| / 2),
    # about 1 - var N / 6 for small var N. The rest, 1 - |I_0|^2, is ICI that CPE correction cannot remove.
    rng = random.Random(4)
    var = 0.002
    exact = sum(math.exp(-var * abs(a - b) / 2) for a in range(N) for b in range(N)) / N ** 2
    assert abs(exact - (1 - var * N / 6)) < 2e-3
    acc = 0.0
    trials = 1000
    for _ in range(trials):
        phi = wiener_phase(rng, N, var, 0.0)
        acc += abs(sum(cmath.exp(1j * p) for p in phi) / N) ** 2
    assert abs(acc / trials - exact) < 2e-3
