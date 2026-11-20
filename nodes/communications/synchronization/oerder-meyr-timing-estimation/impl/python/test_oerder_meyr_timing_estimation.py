# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oerder-meyr-timing-estimation/. The authors are listed in prov/WF9W5Z.jsonl.

import cmath
import math
import random

import pytest

from oerder_meyr_timing_estimation import oerder_meyr, oerder_meyr_blocks, spectral_line

BETA = 0.5
TAU = 0.3
LS = 4
QPSK = [cmath.exp(1j * (math.pi / 4 + m * math.pi / 2)) for m in range(4)]


def rc(t, b):
    """The raised cosine pulse with roll-off b and T = 1."""
    if abs(t) < 1e-12:
        return 1.0
    if abs(abs(t) - 1 / (2 * b)) < 1e-9:
        return math.pi / 4 * math.sin(math.pi / (2 * b)) / (math.pi / (2 * b))
    return math.sin(math.pi * t) / (math.pi * t) * math.cos(math.pi * b * t) / (1 - (2 * b * t) ** 2)


def rrc(t, b):
    """The root raised cosine pulse with roll-off b and T = 1."""
    if abs(t) < 1e-12:
        return 1 - b + 4 * b / math.pi
    if abs(abs(t) - 1 / (4 * b)) < 1e-9:
        return b / math.sqrt(2) * ((1 + 2 / math.pi) * math.sin(math.pi / (4 * b)) + (1 - 2 / math.pi) * math.cos(math.pi / (4 * b)))
    return (math.sin(math.pi * (1 - b) * t) + 4 * b * t * math.cos(math.pi * (1 + b) * t)) / (math.pi * t * (1 - (4 * b * t) ** 2))


def samples(a, tau, n_sym, ls=LS, n0=0.0, seed=0, theta=0.0, drift=0.0, start=0, span=4, reach=8):
    """x[n] = y(start + n / ls) for n < n_sym ls, where
    y(t) = e^(j theta) sum a_k g(t - k - tau - drift k) + v(t), g raised cosine.

    The noise is v(t) = sum_m w_m rrc(t - m h) with h = 1/2 and w_m i.i.d.
    CN(0, h n0): a stationary process with autocorrelation n0 g(t - s).
    """
    rot = cmath.exp(1j * theta)
    h = 0.5
    m_lo = int(-6 / h)
    w = None
    if n0 > 0:
        rng = random.Random(seed)
        sd = math.sqrt(h * n0 / 2)
        w = [complex(rng.gauss(0, sd), rng.gauss(0, sd)) for _ in range(int((len(a) + 12) / h))]
    reach_w = int(span / h)
    out = []
    for n in range(n_sym * ls):
        t = start + n / ls
        k0 = int(round((t - tau) / (1 + drift)))
        acc = 0j
        for k in range(max(0, k0 - reach), min(len(a), k0 + reach + 1)):
            acc += a[k] * rc(t - k - tau - drift * k, BETA)
        acc *= rot
        if w is not None:
            c = int(round(t / h))
            for m in range(c - reach_w, c + reach_w + 1):
                acc += w[m - m_lo] * rrc(t - m * h, BETA)
        out.append(acc)
    return out


def qpsk(n, seed):
    rng = random.Random(seed)
    return [rng.choice(QPSK) for _ in range(n)]


def brute_force(x, ls):
    """argmax over tau_c of J(tau_c) = sum_n |x[n]|^2 cos(2 pi (n / ls - tau_c)), by a grid then ternary search."""
    p = [abs(v) ** 2 for v in x]

    def j(tc):
        return sum(pn * math.cos(2 * math.pi * (n / ls - tc)) for n, pn in enumerate(p))

    grid = [-0.5 + i / 400 for i in range(400)]
    best = max(grid, key=j)
    lo, hi = best - 1 / 400, best + 1 / 400
    for _ in range(80):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if j(m1) < j(m2):
            lo = m1
        else:
            hi = m2
    tc = 0.5 * (lo + hi)
    return (tc + 0.5) % 1.0 - 0.5


def wrap(d):
    return (d + 0.5) % 1.0 - 0.5


def test_alternating_data_gives_exact_delay():
    # a_k = (-1)^k gives |y|^2 = (1 + cos(2 pi (t - tau))) / 2: a pure symbol-rate line.
    a = [(-1) ** k + 0j for k in range(140)]
    for tau in (0.3, -0.45, 0.0, 0.12):
        for ls in (3, 4, 5, 8):
            x = samples(a, tau, 100, ls=ls, start=20, reach=24)
            assert abs(wrap(oerder_meyr(x, ls) - tau)) < 1e-5


def test_matches_brute_force_search():
    for seed in range(4):
        a = qpsk(100, seed)
        x = samples(a, TAU, 100, n0=0.1, seed=seed + 50)
        assert abs(wrap(oerder_meyr(x, LS) - brute_force(x, LS))) < 1e-7


def test_carrier_phase_does_not_change_the_estimate():
    a = qpsk(100, 9)
    x0 = samples(a, TAU, 100)
    x1 = samples(a, TAU, 100, theta=2.0)
    assert abs(oerder_meyr(x0) - oerder_meyr(x1)) < 1e-12


def test_needs_three_samples_per_symbol():
    # At L_s = 2 the rotations are +1 and -1, so X would be real and its phase could not show tau.
    with pytest.raises(ValueError):
        spectral_line([1 + 0j] * 8, 2)


def test_range_of_estimate():
    rng = random.Random(3)
    for _ in range(100):
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(40)]
        t = oerder_meyr(x)
        assert -0.5 <= t < 0.5


def test_noiseless_random_data_is_close():
    # The data run on for 10 symbols on each side of the 100-symbol window, as in a
    # stream. What is left is self-noise: the data pattern moves the line a little.
    errs = []
    for seed in range(20):
        x = samples(qpsk(120, seed), TAU, 100, start=10)
        errs.append(wrap(oerder_meyr(x) - TAU))
    rms = math.sqrt(sum(e * e for e in errs) / len(errs))
    assert rms < 0.01


def test_noise_variance_against_mcrb():
    snr = 10.0
    l0 = 100
    xi = 1.0 / 12.0 + BETA ** 2 * (0.25 - 2.0 / math.pi ** 2)
    mcrb = 1.0 / (8 * math.pi ** 2 * xi * l0 * snr)
    errs = []
    for seed in range(30):
        x = samples(qpsk(l0 + 20, 100 + seed), TAU, l0, start=10, n0=1.0 / snr, seed=200 + seed)
        errs.append(wrap(oerder_meyr(x) - TAU))
    mse = sum(e * e for e in errs) / len(errs)
    assert 1.0 <= mse / mcrb <= 4.0


def test_blocks_follow_a_drifting_delay():
    # The delay grows by 0.004 T per symbol, from 0.3 to 1.5 over 300 symbols.
    a = [(-1) ** k + 0j for k in range(330)]
    x = samples(a, TAU, 300, start=0, drift=0.004, reach=24)
    est = oerder_meyr_blocks(x, LS, 20)
    assert len(est) == 15
    for i, e in enumerate(est):
        mid = 20 * i + 10
        assert abs(e - (TAU + 0.004 * mid)) < 0.01
    assert est[-1] > 1.0
