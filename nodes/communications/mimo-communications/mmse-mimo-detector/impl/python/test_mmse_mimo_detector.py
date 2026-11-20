# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmse-mimo-detector/. The authors are listed in prov/ZA2PHJ.jsonl.

import random

import pytest

import cbb
import constel
from mmse_mimo_detector import (
    bias,
    error_covariance,
    mmse_detect,
    mmse_matrix,
    mmse_outputs,
    mmse_parts,
    nearest,
    sinr,
)


def rayleigh(rng, m, n):
    return [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]


def close(a, b, tol=1e-9):
    return all(abs(p - q) <= tol for p, q in zip(a, b))


def test_example_on_the_page() -> None:
    h = [[2, 1], [1, 1]]
    y = [0.5, 0.6]
    bpsk = constel.pam(2)
    p, w = mmse_parts(h, 0.5)
    assert close([p[0][0], p[0][1], p[1][1]], [2.5 / 4.75, -3 / 4.75, 5.5 / 4.75])
    assert close([w[0][0], w[0][1], w[1][0], w[1][1]], [2 / 4.75, -0.5 / 4.75, -0.5 / 4.75, 2.5 / 4.75])
    assert close(mmse_outputs(y, h, 0.5, unbiased=False), [0.7 / 4.75, 1.25 / 4.75])
    assert close(bias(h, 0.5), [3.5 / 4.75, 2 / 4.75])
    assert close(mmse_outputs(y, h, 0.5), [0.2, 0.625])
    assert mmse_detect(y, h, bpsk, 0.5) == [0, 0]  # (+1, +1): the first stream is now right
    assert close(sinr(h, 0.5), [2.8, 8 / 11])


def test_push_through_form_and_zf_limit() -> None:
    rng = random.Random(1301)
    for _ in range(40):
        n = rng.randint(1, 4)
        m = rng.randint(1, 5)
        h = rayleigh(rng, m, n)
        n0 = rng.uniform(0.05, 2.0)
        w = mmse_matrix(h, n0)
        # W = H^H (H H^H + N0 I)^-1, which also holds when n > m
        hh = cbb.herm(h)
        g = cbb.matmul(h, hh)
        for i in range(m):
            g[i][i] += n0
        w2 = cbb.matmul(hh, cbb.inv(g))
        assert all(close(r, s) for r, s in zip(w, w2))
        if m >= n:
            wz = cbb.solve(cbb.matmul(hh, h), hh)
            assert all(close(r, s, 1e-6) for r, s in zip(mmse_matrix(h, 1e-12), wz))


def test_bias_is_the_diagonal_of_wh_and_sinr_matches_the_direct_formula() -> None:
    rng = random.Random(1302)
    for _ in range(40):
        n = rng.randint(1, 4)
        m = rng.randint(1, 5)
        h = rayleigh(rng, m, n)
        n0, es = rng.uniform(0.05, 2.0), rng.uniform(0.5, 2.0)
        w = mmse_matrix(h, n0, es)
        wh = cbb.matmul(w, h)
        assert close(bias(h, n0, es), [wh[k][k].real for k in range(n)])
        for k, s in enumerate(sinr(h, n0, es)):
            sig = abs(wh[k][k]) ** 2 * es
            intf = sum(abs(wh[k][j]) ** 2 for j in range(n) if j != k) * es
            noise = n0 * cbb.norm2(w[k])
            assert abs(s - sig / (intf + noise)) < 1e-9 * (1 + s)


def test_mse_matches_the_closed_form() -> None:
    # closed form: E|(W y)_k - x_k|^2 = N0 P_kk for x with i.i.d. entries of energy Es
    rng = random.Random(1303)
    h = [[0.9 + 0.2j, 0.4 - 0.3j, 0.1j], [0.3, -0.7 + 0.5j, 0.6], [0.2 - 0.6j, 0.5, 1.1 - 0.1j], [0.4j, 0.3 + 0.3j, -0.5]]
    pts = constel.qam(16)
    n0 = 0.3
    e = error_covariance(h, n0)
    w = mmse_matrix(h, n0)
    trials = 4000
    acc = [0.0] * 3
    for _ in range(trials):
        x = [pts[rng.randrange(16)] for _ in range(3)]
        z = cbb.matvec(w, cbb.awgn(rng, cbb.matvec(h, x), n0))
        for k in range(3):
            acc[k] += abs(z[k] - x[k]) ** 2
    for k in range(3):
        assert abs(acc[k] / trials - e[k][k].real) < 0.08 * e[k][k].real


def test_wide_channels_work_and_n0_zero_needs_full_rank() -> None:
    rng = random.Random(1304)
    h = rayleigh(rng, 2, 3)
    assert len(mmse_detect(cbb.awgn(rng, [0j, 0j], 0.1), h, constel.qam(4), 0.1)) == 3
    with pytest.raises(ValueError):
        mmse_matrix([[1, 2], [2, 4]], 0.0)
    with pytest.raises(ValueError):
        sinr(h, 0.0)
    assert nearest(0j, constel.pam(2)) == 0


def run(rng, m, n, snr_db, pts, trials, with_ml):
    n0 = 1 / cbb.undb(snr_db)
    out = {"agree": 0, "mmse": 0, "zf": 0, "biased": 0}
    for _ in range(trials):
        h = rayleigh(rng, m, n)
        idx = [rng.randrange(len(pts)) for _ in range(n)]
        y = cbb.awgn(rng, cbb.matvec(h, [pts[i] for i in idx]), n0)
        d = mmse_detect(y, h, pts, n0)
        if with_ml:
            out["agree"] += d == constel.ml_vector(y, h, pts)
        out["mmse"] += sum(a != b for a, b in zip(d, idx))
        out["zf"] += sum(a != b for a, b in zip(mmse_detect(y, h, pts, 0.0), idx))
        out["biased"] += sum(a != b for a, b in zip(mmse_detect(y, h, pts, n0, unbiased=False), idx))
    return out


def test_most_decisions_match_ml_and_mmse_beats_zf() -> None:
    # measured: 4-QAM, m = n = 4, Es/N0 = 15 dB, seed 1305, 200 vectors:
    # 192 agree with ML; 9 symbol errors for MMSE against 29 for ZF
    out = run(random.Random(1305), 4, 4, 15.0, constel.qam(4), 200, True)
    assert out["agree"] >= 185
    assert out["mmse"] < out["zf"]


def test_bias_removal_helps_16qam() -> None:
    # measured: 16-QAM, m = n = 2, Es/N0 = 15 dB, seed 1306, 1500 vectors:
    # the unbiased slicer makes fewer symbol errors than the biased one
    out = run(random.Random(1306), 2, 2, 15.0, constel.qam(16), 1500, False)
    assert out["mmse"] < out["biased"]
