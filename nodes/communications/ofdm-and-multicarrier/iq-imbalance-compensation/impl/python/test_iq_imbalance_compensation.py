# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iq-imbalance-compensation/. The authors are listed in prov/GSXKAS.jsonl.

import math
import random

import cbb
from iq_imbalance_compensation import compensate, estimate, image_coefficient, impair, mu_nu

S = 1 / math.sqrt(2)
N = 64
TAPS = [0.9, 0.3j, -0.2]
G, PHI = 1.1, math.radians(5.0)
USED = [k for k in range(1, N) if 2 * k != N]


def qpsk(rng: random.Random, n: int) -> list[complex]:
    return [complex(rng.choice((S, -S)), rng.choice((S, -S))) for _ in range(n)]


def received(rng: random.Random, x: list[complex], n0: float, g: float = G, phi: float = PHI) -> list[complex]:
    """Subcarrier values after the channel (prefix long enough), AWGN, IQ imbalance and the unitary DFT."""
    y = cbb.cconv(cbb.uidft(x), TAPS, N)
    if n0 > 0:
        y = cbb.awgn(rng, y, n0)
    return cbb.udft(impair(y, g, phi))


def training(rng: random.Random) -> tuple[list[complex], list[complex]]:
    """T2 equals T1 on k < N/2 and -T1 on k >= N/2, so each 2x2 training matrix is invertible."""
    t1 = qpsk(rng, N)
    return t1, [t1[k] if k < N // 2 else -t1[k] for k in range(N)]


def test_impairment_matches_the_two_branch_model() -> None:
    rng = random.Random(1)
    for _ in range(20):
        y = cbb.cn(rng, 1.0)
        r = impair([y], G, PHI)[0]
        want = complex(y.real, G * (y.imag * math.cos(PHI) - y.real * math.sin(PHI)))
        assert abs(r - want) < 1e-12


def test_subcarrier_k_sees_its_mirror() -> None:
    rng = random.Random(2)
    mu, nu = mu_nu(G, PHI)
    h = cbb.dft(TAPS + [0j] * (N - len(TAPS)))
    x = qpsk(rng, N)
    r = received(rng, x, 0.0)
    for k in range(N):
        m = (N - k) % N
        assert abs(r[k] - (mu * h[k] * x[k] + nu * h[m].conjugate() * x[m].conjugate())) < 1e-9


def test_exact_without_noise() -> None:
    rng = random.Random(3)
    mu, nu = mu_nu(G, PHI)
    h = cbb.dft(TAPS + [0j] * (N - len(TAPS)))
    t1, t2 = training(rng)
    a, b = estimate(received(rng, t1, 0.0), received(rng, t2, 0.0), t1, t2)
    for k in USED:
        assert abs(a[k] - mu * h[k]) < 1e-9
        assert abs(b[k] - nu * h[N - k].conjugate()) < 1e-9
    assert abs(image_coefficient(a, b) - nu / mu.conjugate()) < 1e-9
    for _ in range(3):
        x = qpsk(rng, N)
        xh = compensate(received(rng, x, 0.0), a, b)
        assert max(abs(xh[k] - x[k]) for k in USED) < 1e-9


def test_without_imbalance_the_image_term_is_zero() -> None:
    rng = random.Random(4)
    t1, t2 = training(rng)
    a, b = estimate(received(rng, t1, 0.0, 1.0, 0.0), received(rng, t2, 0.0, 1.0, 0.0), t1, t2)
    assert max(abs(b[k]) for k in USED) < 1e-12


def test_time_domain_fix_removes_the_image() -> None:
    rng = random.Random(5)
    mu, nu = mu_nu(G, PHI)
    c = nu / mu.conjugate()
    y = [cbb.cn(rng, 1.0) for _ in range(32)]
    z = [v - c * v.conjugate() for v in impair(y, G, PHI)]
    scale = mu - abs(nu) ** 2 / mu.conjugate()
    assert max(abs(a - scale * b) for a, b in zip(z, y)) < 1e-12


def test_error_power_with_and_without_compensation() -> None:
    # Closed form without noise: a one-tap equalizer R[k] / A[k] leaves the image B[k] conj(X[-k]) / A[k],
    # of power |B[k]|^2 / |A[k]|^2 with |X| = 1. Image rejection |mu|^2 / |nu|^2 = 23.79 dB for g = 1.1, 5 degrees.
    # With N0 = 0.001 (30 dB), 25 symbols, seed 6, compensation brings the error down to the noise level.
    rng = random.Random(6)
    mu, nu = mu_nu(G, PHI)
    assert abs(cbb.db(abs(mu) ** 2 / abs(nu) ** 2) - 23.7946) < 1e-4
    t1, t2 = training(rng)
    a, b = estimate(received(rng, t1, 0.0), received(rng, t2, 0.0), t1, t2)
    x = qpsk(rng, N)
    r = received(rng, x, 0.0)
    plain = sum(abs(r[k] / a[k] - x[k]) ** 2 for k in USED)
    assert abs(plain - sum(abs(b[k] / a[k]) ** 2 for k in USED)) < 1e-9
    n0 = 0.001
    e_plain = e_comp = 0.0
    for _ in range(25):
        t1, t2 = training(rng)
        a, b = estimate(received(rng, t1, n0), received(rng, t2, n0), t1, t2)
        x = qpsk(rng, N)
        r = received(rng, x, n0)
        xh = compensate(r, a, b)
        e_plain += sum(abs(r[k] / a[k] - x[k]) ** 2 for k in USED)
        e_comp += sum(abs(xh[k] - x[k]) ** 2 for k in USED)
    assert e_comp < e_plain / 2
