# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-feedback-equalizer/. The authors are listed in prov/K3EMZX.jsonl.

import math
import random

import pytest

import cbb
from decision_feedback_equalizer import (
    channel_matrix,
    combined_response,
    dfe_design,
    dfe_run,
    mse,
    soft_outputs,
)

PROAKIS_B = [0.407, 0.815, 0.407]
QPSK = [complex(a, b) / math.sqrt(2) for a in (-1, 1) for b in (-1, 1)]


def infinite_dfe_j(h, n0, es=1.0, grid=4096):
    # N0 / (geometric mean of |H|^2 + N0 / Es), by the midpoint rule on the unit circle
    s = 0.0
    for k in range(grid):
        w = 2 * math.pi * (k + 0.5) / grid
        hw = sum(v * complex(math.cos(w * l), -math.sin(w * l)) for l, v in enumerate(h))
        s += math.log(abs(hw) ** 2 + n0 / es)
    return n0 / math.exp(s / grid)


def test_example_on_the_page() -> None:
    want = [0.090909, 0.089069, 0.088705, 0.088634, 0.08862, 0.778511]
    for d, w in enumerate(want):
        assert abs(dfe_design([1, 0.5], 5, 1, d, 0.1)[2] - w) < 1e-6
    c, b, j = dfe_design([1, 0.5], 1, 1, 0, 0.1)
    assert abs(c[0] - 1 / 1.1) < 1e-12 and abs(b[0] - 0.5 / 1.1) < 1e-12 and abs(j - 0.1 / 1.1) < 1e-12
    jinf = 0.1 / ((1.35 + math.sqrt(1.35**2 - 1)) / 2)
    assert abs(jinf - 0.0886164) < 1e-7
    assert abs(dfe_design([1, 0.5], 15, 1, 14, 0.1)[2] - jinf) < 1e-7
    assert abs(cbb.db(1 / jinf - 1) - 10.12) < 0.005
    j = min(dfe_design(PROAKIS_B, 11, 2, d, 0.01)[2] for d in range(12))
    assert abs(j - 0.0296778) < 1e-6 and abs(cbb.db(1 / j - 1) - 15.14) < 0.01


def test_long_filters_reach_the_infinite_length_error() -> None:
    for h, n0 in (([1, 0.5], 0.1), (PROAKIS_B, 0.01), ([0.5, 1], 0.1)):
        jinf = infinite_dfe_j(h, n0)
        j = min(dfe_design(h, 25, len(h) - 1, d, n0)[2] for d in range(26))
        assert j >= jinf - 1e-9 and j - jinf < 1e-4


def test_design_error_matches_the_error_of_the_taps_and_is_minimal() -> None:
    rng = random.Random(7201)
    for _ in range(40):
        taps, nf = rng.randint(1, 4), rng.randint(1, 6)
        nb = rng.randint(0, 3)
        h = [cbb.cn(rng, 1.0) for _ in range(taps)]
        n0, es = rng.uniform(0.01, 1.0), rng.uniform(0.5, 2.0)
        d = rng.randint(0, nf + taps - 2)
        c, b, j = dfe_design(h, nf, nb, d, n0, es)
        assert abs(mse(c, b, h, d, n0, es) - j) < 1e-9
        # the cursor is the bias factor 1 - J / Es
        g = combined_response(c, h)
        assert abs(g[d] - (1 - j / es)) < 1e-9
        # the feedback cancels the postcursors exactly
        for t, v in enumerate(b, start=1):
            assert abs(v - (g[d + t] if d + t < len(g) else 0)) < 1e-12
        for _ in range(5):
            c2 = [v + cbb.cn(rng, 0.01) for v in c]
            b2 = [v + cbb.cn(rng, 0.01) for v in b]
            assert mse(c2, b2, h, d, n0, es) > j
            assert mse(c2, b, h, d, n0, es) > j


def test_feedback_never_hurts_with_ideal_decisions() -> None:
    rng = random.Random(7202)
    for _ in range(30):
        h = [cbb.cn(rng, 1.0) for _ in range(rng.randint(2, 4))]
        nf, n0 = rng.randint(2, 6), rng.uniform(0.01, 0.5)
        d = rng.randint(0, nf - 1)
        js = [dfe_design(h, nf, nb, d, n0)[2] for nb in range(4)]
        assert all(js[i + 1] <= js[i] + 1e-12 for i in range(3))


def test_noiseless_qpsk_is_recovered_with_decision_feedback() -> None:
    rng = random.Random(7203)
    for _ in range(10):
        h = [complex(1.0)] + [0.4 * cbb.cn(rng, 1.0) for _ in range(rng.randint(1, 3))]
        nf = 8
        best = min((dfe_design(h, nf, len(h) - 1, d, 1e-8)[2], d) for d in range(nf + len(h) - 1))
        d = best[1]
        c, b, j = dfe_design(h, nf, len(h) - 1, d, 1e-8)
        x = [rng.choice(QPSK) for _ in range(300)]
        y = cbb.conv(x, h)
        assert dfe_run(c, b, d, y, len(x), QPSK, 1 - j) == x


def test_mse_with_ideal_feedback_matches_j() -> None:
    rng = random.Random(7204)
    h, n0, nf, nb, d = [0.8 + 0.2j, -0.5, 0.3j], 0.05, 6, 2, 3
    c, b, j = dfe_design(h, nf, nb, d, n0)
    count = 20000
    x = [rng.choice(QPSK) for _ in range(count)]
    y = cbb.awgn(rng, cbb.conv(x, h), n0)
    q = soft_outputs(c, b, d, y, count, x)
    e = [abs(q[k] - x[k]) ** 2 for k in range(20, count)]
    m = sum(e) / len(e)
    sd = math.sqrt(sum((v - m) ** 2 for v in e) / (len(e) - 1))
    assert abs(m - j) < 3.29 * sd / math.sqrt(len(e))


def test_zf_dfe_bpsk_error_rate_with_ideal_feedback() -> None:
    # c = 1 and b = 0.5 cancel the ISI of (1, 0.5) with noise gain 1, so the BER is Q(sqrt(2 / N0))
    rng = random.Random(7205)
    n0, count = 0.3, 40000
    x = [rng.choice((-1, 1)) for _ in range(count)]
    y = [v + rng.gauss(0.0, math.sqrt(n0 / 2)) for v in cbb.conv(x, [1, 0.5])[:count]]
    dec = dfe_run([1], [0.5], 0, y, count, [-1, 1], known=x)
    err = sum(1 for p, q in zip(dec, x) if p != q)
    p = cbb.qfunc(math.sqrt(2 / n0))
    assert p * count >= 100
    lo, hi = cbb.wilson(err, count)
    assert lo <= p <= hi


def test_error_propagation_is_measured() -> None:
    # the same noise with decided feedback: more errors than with ideal feedback, but not many more
    rng = random.Random(7206)
    n0, count = 0.3, 40000
    x = [rng.choice((-1, 1)) for _ in range(count)]
    y = [v + rng.gauss(0.0, math.sqrt(n0 / 2)) for v in cbb.conv(x, [1, 0.5])[:count]]
    genie = sum(1 for p, q in zip(dfe_run([1], [0.5], 0, y, count, [-1, 1], known=x), x) if p != q)
    real = sum(1 for p, q in zip(dfe_run([1], [0.5], 0, y, count, [-1, 1]), x) if p != q)
    assert genie < real < 2 * genie


def test_channel_matrix_and_input_checks() -> None:
    assert channel_matrix([1, 2], 2) == [[1, 2, 0], [0, 1, 2]]
    with pytest.raises(ValueError):
        dfe_design([1, 0.5], 3, 1, 4, 0.1)
    with pytest.raises(ValueError):
        dfe_design([1, 0.5], 3, -1, 0, 0.1)
    with pytest.raises(ValueError):
        dfe_design([1, 0.5], 0, 1, 0, 0.1)
    with pytest.raises(ValueError):
        dfe_design([1, 0.5], 3, 1, 0, -0.1)
