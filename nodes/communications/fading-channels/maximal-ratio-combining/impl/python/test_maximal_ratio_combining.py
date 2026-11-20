# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-ratio-combining/. The authors are listed in prov/5E6BSS.jsonl.

import math
import random

import cbb
from maximal_ratio_combining import (
    ber_bpsk_rayleigh,
    ber_bpsk_rayleigh_craig,
    mrc,
    outage_rayleigh,
    output_snr,
)


def test_noiseless_recovery() -> None:
    rng = random.Random(5001)
    for _ in range(200):
        branches = rng.randint(1, 8)
        h = [cbb.cn(rng, 1.0) for _ in range(branches)]
        n0 = [rng.uniform(0.1, 3.0) for _ in range(branches)]
        x = complex(rng.choice((-1, 1)), rng.choice((-1, 1)))
        est, g = mrc(h, [v * x for v in h], n0)
        assert abs(est - x) < 1e-12
        assert abs(g - sum(abs(v) ** 2 / s for v, s in zip(h, n0))) < 1e-12


def test_output_snr_is_the_sum_and_is_maximal() -> None:
    rng = random.Random(5002)
    for _ in range(200):
        branches = rng.randint(1, 6)
        h = [cbb.cn(rng, 1.0) for _ in range(branches)]
        n0 = [rng.uniform(0.1, 3.0) for _ in range(branches)]
        best = output_snr([v / s for v, s in zip(h, n0)], h, n0)
        assert abs(best - sum(abs(v) ** 2 / s for v, s in zip(h, n0))) < 1e-9
        for _ in range(20):
            c = [cbb.cn(rng, 1.0) for _ in range(branches)]
            assert output_snr(c, h, n0) <= best * (1 + 1e-12)
        # scaling all weights by one complex number changes nothing
        a = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        assert abs(output_snr([a * v / s for v, s in zip(h, n0)], h, n0) - best) < 1e-9 * best


def test_check_values() -> None:
    assert abs(ber_bpsk_rayleigh(1, 10.0) - 0.5 * (1 - math.sqrt(10 / 11))) < 1e-15
    assert abs(ber_bpsk_rayleigh(2, 10.0) - 1.5991e-3) < 1e-7
    assert abs(ber_bpsk_rayleigh(4, 10.0) - 9.698e-6) < 1e-9
    # the high-SNR form C(2L - 1, L) / (4 gamma_bar)^L for L = 2 at 10 dB
    assert abs(math.comb(3, 2) / 40.0 ** 2 - 1.875e-3) < 1e-15


def test_closed_form_against_mgf_integral() -> None:
    for branches in (1, 2, 3, 4, 6):
        for gdb in (0, 5, 10, 20, 30):
            g = cbb.undb(gdb)
            a = ber_bpsk_rayleigh(branches, g)
            b = ber_bpsk_rayleigh_craig(branches, g)
            assert abs(a - b) <= 1e-9 * a


def test_ber_by_simulation() -> None:
    # L = 2, gamma_bar = 5 dB, BPSK: Pb = 0.011829, so n = 20000 bits give about 237 errors.
    rng = random.Random(5003)
    n, branches, g = 20000, 2, cbb.undb(5.0)
    n0 = [1.0 / g] * branches
    errors = 0
    for _ in range(n):
        x = rng.choice((-1.0, 1.0))
        h = [cbb.cn(rng, 1.0) for _ in range(branches)]
        y = [v * x + cbb.cn(rng, n0[0]) for v in h]
        est, _ = mrc(h, y, n0)
        errors += (est.real >= 0) != (x > 0)
    lo, hi = cbb.wilson(errors, n, 3.29)
    assert lo <= ber_bpsk_rayleigh(branches, g) <= hi


def test_mean_output_snr_and_outage() -> None:
    # mean output SNR L gamma_bar, and the outage at x = 1 for L = 2 at 10 dB: 4.68e-3,
    # so n = 25000 channels give about 117 outages
    rng = random.Random(5004)
    n, branches, g = 25000, 2, 10.0
    total, below = 0.0, 0
    for _ in range(n):
        h = [cbb.cn(rng, 1.0) for _ in range(branches)]
        snr = g * sum(abs(v) ** 2 for v in h)
        total += snr
        below += snr < 1.0
    assert abs(total / n - branches * g) < 0.05 * branches * g
    p = outage_rayleigh(branches, 1.0, g)
    assert abs(p - 4.6788e-3) < 1e-6
    lo, hi = cbb.wilson(below, n, 3.29)
    assert lo <= p <= hi
