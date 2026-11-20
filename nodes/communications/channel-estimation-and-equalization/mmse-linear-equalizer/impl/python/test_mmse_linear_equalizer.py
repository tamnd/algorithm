# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmse-linear-equalizer/. The authors are listed in prov/4T3X0R.jsonl.

import itertools
import math
import random

import pytest

import cbb
from mmse_linear_equalizer import (
    best_delay,
    bias,
    channel_matrix,
    equalize,
    mmse_equalizer,
    mse,
    unbiased_sinr,
)

PROAKIS_B = [0.407, 0.815, 0.407]


def qpsk(rng):
    return complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / math.sqrt(2)


def zf_taps(h, n):
    # the delay 0 ZF taps: the first N terms of the power series of 1 / H(z)
    c = []
    for k in range(n):
        acc = (1 if k == 0 else 0) - sum(h[l] * c[k - l] for l in range(1, min(k, len(h) - 1) + 1))
        c.append(acc / h[0])
    return c


def test_example_on_the_page() -> None:
    want = [0.114043, 0.11197, 0.11547, 0.136058, 0.24147, 0.778511]
    for d, w in enumerate(want):
        assert abs(mmse_equalizer([1, 0.5], 5, d, 0.1)[1] - w) < 1e-6
    d, c, j = best_delay([1, 0.5], 5, 0.1)
    assert d == 1 and abs(j - 0.1119702) < 1e-7
    assert abs(bias(j) - 0.8880298) < 1e-7 and abs(cbb.db(unbiased_sinr(j)) - 8.993) < 1e-3
    assert abs(mse(zf_taps([1, 0.5], 5), [1, 0.5], 0, 0.1) - 0.1341796875) < 1e-12


def test_j_matches_the_closed_forms_on_random_channels() -> None:
    rng = random.Random(7101)
    for _ in range(60):
        taps, n = rng.randint(1, 4), rng.randint(1, 7)
        h = [cbb.cn(rng, 1.0) for _ in range(taps)]
        n0, es = rng.uniform(0.01, 1.0), rng.uniform(0.5, 2.0)
        d = rng.randint(0, n + taps - 2)
        c, j = mmse_equalizer(h, n, d, n0, es)
        assert abs(mse(c, h, d, n0, es) - j) < 1e-9
        # J = N0 Es [(Es H^H H + N0 I)^(-1)] at (d, d)
        hm = channel_matrix(h, n)
        m = len(hm[0])
        a = [[es * sum(hm[t][i].conjugate() * hm[t][k] for t in range(n)) + (n0 if i == k else 0) for k in range(m)] for i in range(m)]
        e = [1 if i == d else 0 for i in range(m)]
        assert abs(n0 * es * cbb.solve(a, e)[d].real - j) < 1e-9


def test_taps_are_the_minimum_against_perturbations() -> None:
    rng = random.Random(7102)
    for _ in range(40):
        taps, n = rng.randint(2, 4), rng.randint(2, 6)
        h = [cbb.cn(rng, 1.0) for _ in range(taps)]
        n0, d = rng.uniform(0.01, 0.5), rng.randint(0, n + taps - 2)
        c, j = mmse_equalizer(h, n, d, n0)
        for scale in (1.0, 1e-2, 1e-4):
            for _ in range(10):
                other = [v + scale * cbb.cn(rng, 1.0) for v in c]
                assert mse(other, h, d, n0) >= j - 1e-12


def test_monte_carlo_mse_and_bias() -> None:
    rng = random.Random(7103)
    h, n, n0, count = [1, 0.5], 5, 0.1, 20000
    d, c, j = best_delay(h, n, n0)
    x = [qpsk(rng) for _ in range(count)]
    y = cbb.awgn(rng, cbb.conv(x, h), n0)
    z = equalize(c, y, d, count)
    inner = range(n, count - n)  # skip the edges of the block
    got = sum(abs(z[k] - x[k]) ** 2 for k in inner) / len(inner)
    assert abs(got - j) < 0.05 * j  # 20000 symbols, seed 7103
    gain = sum(z[k] * x[k].conjugate() for k in inner) / len(inner)
    assert abs(gain - bias(j)) < 0.02


def test_limits_in_n0() -> None:
    h, n, d = [1, 0.5], 5, 0
    # N0 -> 0: the MMSE taps tend to the least-squares fit of c * h to the unit pulse
    c_small = mmse_equalizer(h, n, d, 1e-9)[0]
    hm = channel_matrix(h, n)  # g = H^T c, so minimize ||H^T c - e||^2
    m = len(hm[0])
    gram = [[sum(hm[i][t] * hm[k][t].conjugate() for t in range(m)) for k in range(n)] for i in range(n)]
    ls = [v.conjugate() for v in cbb.solve(gram, [hm[i][d] for i in range(n)])]
    assert max(abs(p - q) for p, q in zip(c_small, ls)) < 1e-6
    # N0 large: the taps tend to the matched filter conj(H e_d) / N0
    n0 = 1e6
    c_big = mmse_equalizer(h, n, 1, n0)[0]
    assert max(abs(c_big[i] * n0 - hm[i][1].conjugate()) for i in range(n)) < 1e-4
    # with no ISI the MMSE equalizer is a scalar Es / (Es + N0)
    c1, j1 = mmse_equalizer([1], 1, 0, 0.25)
    assert abs(c1[0] - 0.8) < 1e-12 and abs(j1 - 0.2) < 1e-12


def test_long_equalizer_reaches_the_infinite_length_mse() -> None:
    # for h = (1, a), |H|^2 = 1 + a^2 + 2 a cos w, and J_inf = N0 / sqrt((1 + a^2 + N0)^2 - 4 a^2)
    for a, n0 in ((0.5, 0.1), (0.9, 0.05)):
        j_inf = n0 / math.sqrt((1 + a * a + n0) ** 2 - 4 * a * a)
        j5, j15 = best_delay([1, a], 5, n0)[2], best_delay([1, a], 15, n0)[2]
        j30 = mmse_equalizer([1, a], 30, 15, n0)[1]  # one delay in the middle is enough here
        assert j5 >= j15 >= j_inf - 1e-12 and j30 >= j_inf - 1e-12
        assert j30 - j_inf < 1e-3  # 1.7e-11 for a = 0.5 and 1.0e-4 for a = 0.9, whose zero is near the circle


def zf_window(h, n, d):
    # the ZF taps for delay d: force c * h = e_d on a window of N indices around d
    s = min(max(d - (n - 1) // 2, 0), len(h) - 1)
    a = [[complex(h[s + k - i]) if 0 <= s + k - i < len(h) else 0j for i in range(n)] for k in range(n)]
    return cbb.solve(a, [1 if s + k == d else 0 for k in range(n)])


def test_proakis_b_mmse_beats_zf_by_far() -> None:
    n0 = 0.01
    d, c, j = best_delay(PROAKIS_B, 31, n0)
    assert abs(j - 0.179469) < 1e-5
    zf = min(mse(zf_window(PROAKIS_B, 31, dd), PROAKIS_B, dd, n0) for dd in range(32))
    assert zf > 100 * j  # the best ZF equalizer has an MSE of about 26.7


def test_bpsk_error_rate_matches_exact_enumeration() -> None:
    rng = random.Random(7104)
    h, n, n0, count = PROAKIS_B, 11, 0.1, 5000
    d, c, j = best_delay(h, n, n0)
    g = [v.real for v in cbb.conv(c, h)]
    sigma = math.sqrt(n0 * cbb.norm2(c) / 2)  # real part of the filtered CN(0, N0) noise
    others = [g[k] for k in range(len(g)) if k != d]
    p = sum(cbb.qfunc((g[d] + sum(s * v for s, v in zip(signs, others))) / sigma) for signs in itertools.product((-1, 1), repeat=len(others)))
    p /= 2 ** len(others)  # about 0.059, so about 290 errors expected
    x = [rng.choice((-1.0, 1.0)) for _ in range(count)]
    y = cbb.awgn(rng, cbb.conv(x, h), n0)
    z = equalize(c, y, d, count)
    inner = range(n, count - n)
    errors = sum((z[k].real >= 0) != (x[k] > 0) for k in inner)
    lo, hi = cbb.wilson(errors, len(inner))  # z = 3.29
    assert lo <= p <= hi


def test_errors() -> None:
    with pytest.raises(ValueError):
        mmse_equalizer([1, 0.5], 3, 4, 0.1)  # the delay must be at most N + L - 2
    with pytest.raises(ValueError):
        mmse_equalizer([1, 0.5], 3, 0, -1.0)
    with pytest.raises(ValueError):
        mmse_equalizer([0, 0], 3, 0, 0.0)  # R = 0
    with pytest.raises(ValueError):
        channel_matrix([], 3)
