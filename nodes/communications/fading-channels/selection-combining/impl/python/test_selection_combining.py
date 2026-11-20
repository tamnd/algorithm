# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selection-combining/. The authors are listed in prov/611EDQ.jsonl.

import math
import random

import cbb
from selection_combining import (
    ber_bpsk_rayleigh,
    ber_bpsk_rayleigh_integral,
    mean_snr_gain,
    outage_rayleigh,
    select,
)


def test_noiseless_recovery_and_choice() -> None:
    rng = random.Random(6101)
    for _ in range(300):
        branches = rng.randint(1, 8)
        h = [cbb.cn(rng, 1.0) for _ in range(branches)]
        n0 = [rng.uniform(0.1, 3.0) for _ in range(branches)]
        x = complex(rng.choice((-1, 1)), rng.choice((-1, 1)))
        est, k = select(h, [v * x for v in h], n0)
        assert abs(est - x) < 1e-12
        snr = [abs(v) ** 2 / s for v, s in zip(h, n0)]
        assert snr[k] == max(snr)


def test_noise_level_matters() -> None:
    # the larger gain is not the better branch when its noise is stronger
    _, k = select([2 + 0j, 1 + 0j], [0j, 0j], [8.0, 1.0])
    assert k == 1


def test_check_values() -> None:
    assert abs(outage_rayleigh(2, 1.0, 10.0) - 9.0559e-3) < 1e-7
    assert abs(ber_bpsk_rayleigh(1, 10.0) - 0.5 * (1 - math.sqrt(10 / 11))) < 1e-15
    assert abs(ber_bpsk_rayleigh(2, 10.0) - 2.9729e-3) < 1e-7
    assert abs(ber_bpsk_rayleigh(4, 10.0) - 1.4870e-4) < 1e-8
    assert abs(mean_snr_gain(2) - 1.5) < 1e-15
    assert abs(mean_snr_gain(4) - 25 / 12) < 1e-15


def test_closed_form_against_integral() -> None:
    for branches in (1, 2, 3, 4):
        for gdb in (0, 5, 10, 20):
            g = cbb.undb(gdb)
            a = ber_bpsk_rayleigh(branches, g)
            assert abs(a - ber_bpsk_rayleigh_integral(branches, g)) < 1e-6 * a


def test_outage_by_simulation() -> None:
    # L = 2, gamma_bar = 10 dB, threshold x = 1: 9.06e-3, so n = 20000 channels give about 181 outages.
    rng = random.Random(6102)
    n, g = 20000, 10.0
    below = 0
    total = 0.0
    for _ in range(n):
        best = max(g * abs(cbb.cn(rng, 1.0)) ** 2 for _ in range(2))
        below += best < 1.0
        total += best
    lo, hi = cbb.wilson(below, n, 3.29)
    assert lo <= outage_rayleigh(2, 1.0, g) <= hi
    assert abs(total / n - 1.5 * g) < 0.04 * 1.5 * g


def test_ber_by_simulation() -> None:
    # L = 2, gamma_bar = 5 dB, BPSK: Pb = 0.019701, so n = 20000 bits give about 394 errors.
    rng = random.Random(6103)
    n, g = 20000, cbb.undb(5.0)
    n0 = [1.0 / g] * 2
    errors = 0
    for _ in range(n):
        x = rng.choice((-1.0, 1.0))
        h = [cbb.cn(rng, 1.0) for _ in range(2)]
        y = [v * x + cbb.cn(rng, n0[0]) for v in h]
        est, _ = select(h, y, n0)
        errors += (est.real >= 0) != (x > 0)
    lo, hi = cbb.wilson(errors, n, 3.29)
    assert lo <= ber_bpsk_rayleigh(2, g) <= hi
