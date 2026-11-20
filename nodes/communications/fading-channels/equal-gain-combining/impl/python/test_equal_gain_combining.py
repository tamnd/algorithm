# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equal-gain-combining/. The authors are listed in prov/FAG3FG.jsonl.

import math
import random

import cbb
from equal_gain_combining import (
    ber_bpsk_rayleigh_dual,
    ber_bpsk_rayleigh_dual_integral,
    egc,
    egc_snr,
    mean_snr_gain,
)


def snr_of_weights(c, h, n0):
    """Brute-force SNR of z = sum conj(c_l) y_l with the same noise N0 on every branch."""
    return abs(sum(a.conjugate() * b for a, b in zip(c, h))) ** 2 / (n0 * sum(abs(a) ** 2 for a in c))


def test_noiseless_recovery() -> None:
    rng = random.Random(6001)
    for _ in range(200):
        branches = rng.randint(1, 8)
        h = [cbb.cn(rng, 1.0) for _ in range(branches)]
        x = complex(rng.choice((-1, 1)), rng.choice((-1, 1)))
        est, a = egc(h, [v * x for v in h])
        assert abs(est - x) < 1e-12
        assert abs(a - sum(abs(v) for v in h)) < 1e-12


def test_snr_between_selection_and_mrc_bounds() -> None:
    rng = random.Random(6002)
    for _ in range(300):
        branches = rng.randint(1, 8)
        h = [cbb.cn(rng, 1.0) for _ in range(branches)]
        n0 = rng.uniform(0.1, 2.0)
        s = egc_snr(h, n0)
        c = [v / abs(v) for v in h]
        assert abs(s - snr_of_weights(c, h, n0)) < 1e-9 * s
        mrc = sum(abs(v) ** 2 for v in h) / n0
        assert s <= mrc * (1 + 1e-12)  # Cauchy-Schwarz
        assert s >= mrc / branches * (1 - 1e-12)


def test_egc_can_lose_to_selection() -> None:
    h = [1 + 0j, 0j]
    assert abs(egc_snr(h, 1.0) - 0.5) < 1e-15
    assert max(abs(v) ** 2 for v in h) == 1.0


def test_dual_branch_closed_form() -> None:
    assert abs(ber_bpsk_rayleigh_dual(1.0) - 0.5 * (1 - math.sqrt(3) / 2)) < 1e-15
    for gdb in (0, 5, 10):
        g = cbb.undb(gdb)
        a = ber_bpsk_rayleigh_dual(g)
        assert abs(a - ber_bpsk_rayleigh_dual_integral(g)) < 1e-5 * a
    assert abs(ber_bpsk_rayleigh_dual(10.0) - 2.0704e-3) < 1e-7


def test_ber_by_simulation() -> None:
    # L = 2, gamma_bar = 5 dB, BPSK: Pb = 0.014645, so n = 20000 bits give about 293 errors.
    rng = random.Random(6003)
    n, g = 20000, cbb.undb(5.0)
    n0 = 1.0 / g
    errors = 0
    for _ in range(n):
        x = rng.choice((-1.0, 1.0))
        h = [cbb.cn(rng, 1.0) for _ in range(2)]
        y = [v * x + cbb.cn(rng, n0) for v in h]
        est, _ = egc(h, y)
        errors += (est.real >= 0) != (x > 0)
    lo, hi = cbb.wilson(errors, n, 3.29)
    assert lo <= ber_bpsk_rayleigh_dual(g) <= hi


def test_mean_snr_gain() -> None:
    rng = random.Random(6004)
    n = 20000
    for branches in (2, 4):
        total = sum(egc_snr([cbb.cn(rng, 1.0) for _ in range(branches)], 1.0) for _ in range(n))
        assert abs(total / n - mean_snr_gain(branches)) < 0.03 * mean_snr_gain(branches)
    assert abs(mean_snr_gain(2) - 1.7854) < 1e-4 and abs(mean_snr_gain(4) - 3.3562) < 1e-4
