# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-code-phase-search/. The authors are listed in prov/NZHGJE.jsonl.

import cmath
import math
import random

from cbb import cn, dft
from parallel_code_phase_search import dirichlet, fft, ifft, mseq_code, pcps, received_block

C63 = mseq_code([6, 1, 0])


def brute_force(x: list[complex], c: list[complex], nu: float) -> list[complex]:
    n = len(x)
    y = [x[k] * cmath.exp(-2j * math.pi * nu * k / n) for k in range(n)]
    return [sum(y[k] * c[(k - t) % n].conjugate() for k in range(n)) for t in range(n)]


def test_fft_matches_the_direct_dft() -> None:
    rng = random.Random(0)
    for n in (1, 2, 3, 7, 8, 12, 30, 63, 64, 105):
        x = [cn(rng, 1.0) for _ in range(n)]
        xf = fft(x)
        ref = dft(x)
        assert max(abs(a - b) for a, b in zip(xf, ref)) < 1e-9 * n
        back = ifft(xf)
        assert max(abs(a - b) for a, b in zip(back, x)) < 1e-12 * n


def test_code_is_an_m_sequence() -> None:
    assert len(C63) == 63
    for s in range(1, 63):
        r = sum(C63[k].conjugate() * C63[(k - s) % 63] for k in range(63))
        assert abs(r + 1 / 63) < 1e-12


def test_matches_brute_force_at_every_cell() -> None:
    rng = random.Random(1)
    nus = [-1.0, -0.5, 0.0, 0.5, 1.0]
    x = received_block(rng, C63, 17, 0.4, 2.0, 1.0)
    _, _, _, rows = pcps(x, C63, nus)
    for nu, row in zip(nus, rows):
        ref = brute_force(x, C63, nu)
        assert max(abs(a - b) for a, b in zip(row, ref)) < 1e-9


def test_doppler_loss_is_the_dirichlet_kernel() -> None:
    rng = random.Random(2)
    for dnu in (0.0, 0.1, 0.25, 0.5, 0.9):
        x = received_block(rng, C63, 30, dnu, 1.0, 0.0)
        _, _, _, rows = pcps(x, C63, [0.0])
        assert abs(abs(rows[0][30]) - dirichlet(dnu, 63)) < 1e-12
    # Near the sinc limit for a long block.
    assert abs(dirichlet(0.25, 10**6) - math.sin(math.pi / 4) / (math.pi / 4)) < 1e-9


def test_finds_the_phase_and_the_offset_in_noise() -> None:
    rng = random.Random(3)
    nus = [k / 2 for k in range(-4, 5)]
    for _ in range(20):
        tau = rng.randrange(63)
        i_true = rng.randrange(len(nus))
        x = received_block(rng, C63, tau, nus[i_true] + rng.uniform(-0.1, 0.1), math.sqrt(30.0), 1.0)
        i, t, peak, _ = pcps(x, C63, nus)
        assert (i, t) == (i_true, tau)
        assert peak > 10.0


def test_noiseless_peak_values() -> None:
    x = received_block(random.Random(4), C63, 5, 0.0, 1.0, 0.0)
    i, t, peak, rows = pcps(x, C63, [0.0])
    assert (i, t) == (0, 5)
    assert abs(peak - 1.0) < 1e-12
    for s in range(63):
        if s != 5:
            assert abs(rows[0][s] + 1 / 63) < 1e-12
