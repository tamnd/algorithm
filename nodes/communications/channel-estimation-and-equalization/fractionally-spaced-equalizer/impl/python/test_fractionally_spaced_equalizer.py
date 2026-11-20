# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fractionally-spaced-equalizer/. The authors are listed in prov/SDKX4V.jsonl.

import math
import random

import pytest

import cbb
from fractionally_spaced_equalizer import (
    best_delay,
    equalize,
    fse_matrix,
    fse_mmse,
    mmse_by_delay,
    mse,
    received,
)

ROOT = math.sqrt(2.5)
PULSE = [1 / ROOT, 0.5 / ROOT, 0.5 / ROOT, 1 / ROOT]  # even phase (1, 0.5), odd phase (0.5, 1), sum |p|^2 = 1
BETA = 0.35


def qpsk(rng):
    return complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / math.sqrt(2)


def slice_qpsk(z):
    return complex(1 if z.real >= 0 else -1, 1 if z.imag >= 0 else -1) / math.sqrt(2)


def rrc(t):
    # the root raised cosine pulse with T = 1 and roll-off BETA, of unit energy
    if abs(t) < 1e-12:
        return 1 - BETA + 4 * BETA / math.pi
    if abs(abs(t) - 1 / (4 * BETA)) < 1e-9:
        a = math.pi / (4 * BETA)
        return BETA / math.sqrt(2) * ((1 + 2 / math.pi) * math.sin(a) + (1 - 2 / math.pi) * math.cos(a))
    return (math.sin(math.pi * t * (1 - BETA)) + 4 * BETA * t * math.cos(math.pi * t * (1 + BETA))) / (math.pi * t * (1 - (4 * BETA * t) ** 2))


def rc(t):
    # the raised cosine pulse, rrc convolved with itself, with rc(0) = 1
    if abs(abs(t) - 1 / (2 * BETA)) < 1e-9:
        return math.pi / 4 * math.sin(math.pi / (2 * BETA)) / (math.pi / (2 * BETA))
    s = 1.0 if abs(t) < 1e-12 else math.sin(math.pi * t) / (math.pi * t)
    return s * math.cos(math.pi * BETA * t) / (1 - (2 * BETA * t) ** 2)


def test_example_on_the_page() -> None:
    c, j = fse_mmse(PULSE, 2, 4, 1, 0.0)
    assert abs(j) < 1e-12
    want = [0, -2 / 3 * ROOT, 4 / 3 * ROOT, 0]
    assert max(abs(p - q) for p, q in zip(c, want)) < 1e-12
    js = [fse_mmse(PULSE, 2, 4, d, 0.1)[1] for d in range(4)]
    assert max(abs(p - q) for p, q in zip(js, [0.244207, 0.276292, 0.276292, 0.244207])) < 1e-6
    # a T-spaced equalizer of the same span on either phase alone cannot reach J = 0
    jt = min(fse_mmse([1 / ROOT, 0.5 / ROOT], 1, 2, d, 1e-12)[1] for d in range(3))
    assert abs(jt - 1 / 21) < 1e-9  # the least-squares residual of 2 taps against 1 / (1 + 0.5 z^-1)


def test_ls_one_is_the_symbol_spaced_mmse_equalizer() -> None:
    # for h = (1, 0.5), N = 5, N0 = 0.1 the MMSE linear equalizer has J = 0.11197 at the delay 1
    c, j = fse_mmse([1, 0.5], 1, 5, 1, 0.1)
    assert abs(j - 0.1119702) < 1e-7
    assert abs(mse(c, [1, 0.5], 1, 1, 0.1) - j) < 1e-12


def test_closed_form_and_minimum_on_random_pulses() -> None:
    rng = random.Random(8101)
    for _ in range(40):
        ls, lp, nf = rng.randint(1, 3), rng.randint(1, 7), rng.randint(1, 7)
        p = [cbb.cn(rng, 1.0) for _ in range(lp)]
        s = math.sqrt(cbb.norm2(p))
        p = [v / s for v in p]
        n0, es = rng.uniform(0.01, 0.5), rng.uniform(0.5, 2.0)
        js = mmse_by_delay(p, ls, nf, n0, es)
        d = rng.randrange(len(js))
        c, j = fse_mmse(p, ls, nf, d, n0, es)
        assert abs(j - js[d]) < 1e-9 and abs(mse(c, p, ls, d, n0, es) - j) < 1e-9
        for scale in (1.0, 1e-3):
            other = [v + scale * cbb.cn(rng, 1.0) for v in c]
            assert mse(other, p, ls, d, n0, es) >= j - 1e-12


def test_matrix_matches_the_sampled_signal() -> None:
    rng = random.Random(8102)
    p = [cbb.cn(rng, 1.0) for _ in range(5)]
    x = [qpsk(rng) for _ in range(12)]
    y = received(x, p, 2)
    hm = fse_matrix(p, 2, 6)
    k = 8  # u = (y[2k], ..., y[2k - 5]) = H (x[k], ..., x[k - Q + 1])
    u = [y[2 * k - i] for i in range(6)]
    s = [x[k - j] for j in range(len(hm[0]))]
    assert max(abs(a - b) for a, b in zip(u, cbb.matvec(hm, s))) < 1e-12


def test_zf_fse_recovers_noiseless_data_exactly() -> None:
    rng = random.Random(8103)
    for p, nf in ((PULSE, 4), (PULSE, 3), ([0.3, 0.8j, -0.4, 0.2, 0.1j, 0.5], 6)):
        d = (len(p) + nf - 2) // 4  # a delay near the middle
        c, j = fse_mmse(p, 2, nf, d, 0.0)
        assert abs(j) < 1e-9
        x = [qpsk(rng) for _ in range(300)]
        z = equalize(c, received(x, p, 2), 2, d, len(x))
        assert max(abs(a - b) for a, b in zip(z, x)) < 1e-9
        assert [slice_qpsk(v) for v in z] == x


def test_insensitive_to_the_sampling_phase() -> None:
    # T-spaced: matched filter, then samples rc(kT + tau). FSE: T/2 samples of rrc(t - tau). Both have Es / N0 = 20 dB.
    n0, span = 0.01, 8
    bound = n0 / (1 + n0)  # J of the matched filter bound with no ISI
    jt, jf = [], []
    for tau in (0.0, 0.25, 0.5):
        pt = [rc(k + tau) for k in range(-span, span + 1)]
        jt.append(best_delay(pt, 1, 15, n0)[2])
        pf = [rrc(m / 2 - tau) for m in range(-2 * span, 2 * span + 1)]
        s = math.sqrt(sum(v * v for v in pf))
        jf.append(best_delay([v / s for v in pf], 2, 30, n0)[2])
    assert all(abs(j - bound) < 0.01 * bound for j in jf)  # the FSE is within 1 percent at every phase
    assert abs(jt[0] - bound) < 0.01 * bound
    assert jt[2] > 5 * bound  # a symbol-spaced equalizer at tau = T/2 loses more than 7 dB
    assert jt[0] < jt[1] < jt[2]


def test_monte_carlo_mse_and_bias() -> None:
    rng = random.Random(8104)
    nf, n0, count = 8, 0.1, 20000
    d, c, j = best_delay(PULSE, 2, nf, n0)
    x = [qpsk(rng) for _ in range(count)]
    y = cbb.awgn(rng, received(x, PULSE, 2), n0)
    z = equalize(c, y, 2, d, count)
    inner = range(nf, count - nf)
    got = sum(abs(z[k] - x[k]) ** 2 for k in inner) / len(inner)
    assert abs(got - j) < 0.05 * j  # 20000 symbols, seed 8104
    gain = sum(z[k] * x[k].conjugate() for k in inner) / len(inner)
    assert abs(gain - (1 - j)) < 0.02  # the MMSE output is biased by 1 - J / Es


def test_errors() -> None:
    with pytest.raises(ValueError):
        fse_mmse([1, 1, 0.5, 0.5], 2, 4, 0, 0.0)  # both phases are (1, 0.5): a common zero, so R is singular
    with pytest.raises(ValueError):
        fse_mmse(PULSE, 2, 4, 4, 0.1)  # Q = 4, so the delay must be at most 3
    with pytest.raises(ValueError):
        fse_mmse(PULSE, 0, 4, 0, 0.1)
    with pytest.raises(ValueError):
        mmse_by_delay(PULSE, 2, 4, 0.0)
