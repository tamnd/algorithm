# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-reduction-aided-detection/. The authors are listed in prov/YKT7T0.jsonl.

import math
import random

import pytest

import cbb
import constel
from lattice_reduction_aided_detection import gram_schmidt, lll, lr_detect, real_model


def rand_channel(rng, m, n):
    return [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]


def det_int(a):
    """The determinant of a small integer matrix by cofactor expansion."""
    if len(a) == 1:
        return a[0][0]
    return sum((-1) ** j * a[0][j] * det_int([row[:j] + row[j + 1 :] for row in a[1:]]) for j in range(len(a)))


def test_example():
    h = [[2, 1], [1, 1]]
    y = [0.5, 0.6]
    pts = constel.pam(2)
    b, t, swaps = lll([[2.0, 1.0], [1.0, 1.0]])
    assert b == [[-1.0, 0.0], [0.0, 1.0]] and t == [[-1, 1], [-1, 2]] and swaps == 1
    # without reduction, ZF and SIC both decide x = (-1, +1); with LLL both decide (+1, -1), the ML vector
    assert lr_detect(y, h, pts, "zf", reduce=False) == [1, 0]
    assert lr_detect(y, h, pts, "sic", reduce=False) == [1, 0]
    assert lr_detect(y, h, pts, "zf") == [0, 1]
    assert lr_detect(y, h, pts, "sic") == [0, 1]
    assert constel.ml_vector(y, h, pts) == [0, 1]


def test_real_model_preserves_metric():
    rng = random.Random(1801)
    for kind, pts in (("qam", constel.qam(16)), ("pam", constel.pam(4))):
        for _ in range(10):
            h = rand_channel(rng, 3, 2)
            y = [cbb.cn(rng, 1.0) for _ in range(3)]
            x = [rng.choice(pts) for _ in range(2)]
            yr, hr = real_model(y, h, kind)
            xr = [v.real for v in x] + ([v.imag for v in x] if kind == "qam" else [])
            lhs = cbb.norm2(cbb.sub(y, cbb.matvec(h, x)))
            rhs = sum((a - sum(c * d for c, d in zip(row, xr))) ** 2 for a, row in zip(yr, hr))
            assert abs(lhs - rhs) < 1e-9


def test_lll_output_is_reduced_and_unimodular():
    rng = random.Random(1802)
    for n in (2, 3, 4, 6):
        for _ in range(10):
            cols = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
            if rng.random() < 0.5:  # a badly conditioned basis
                cols[1] = [a + 0.01 * rng.gauss(0, 1) for a in cols[0]]
            b, t, _ = lll(cols, 0.75)
            for k in range(n):
                want = [sum(t[k][j] * cols[j][i] for j in range(n)) for i in range(n)]
                assert all(abs(u - v) < 1e-9 for u, v in zip(b[k], want))
            assert all(isinstance(v, int) for row in t for v in row)
            assert abs(det_int(t)) == 1
            _, mu, norms = gram_schmidt(b)
            for k in range(n):
                for j in range(k):
                    assert abs(mu[k][j]) <= 0.5 + 1e-9
            for k in range(1, n):
                assert norms[k] >= (0.75 - mu[k][k - 1] ** 2) * norms[k - 1] - 1e-9


def test_noiseless_exact():
    rng = random.Random(1803)
    for pts, m, n in ((constel.qam(16), 3, 3), (constel.qam(4), 4, 4), (constel.pam(8), 2, 3)):
        for _ in range(10):
            h = rand_channel(rng, m, n)
            x = [rng.randrange(len(pts)) for _ in range(n)]
            y = cbb.matvec(h, [pts[i] for i in x])
            for method in ("zf", "sic"):
                for red in (False, True):
                    assert lr_detect(y, h, pts, method, reduce=red) == x


def test_babai_radius_guarantee():
    """LR-SIC is correct whenever the scaled noise is shorter than half the smallest Gram-Schmidt length."""
    rng = random.Random(1804)
    pts = constel.qam(4)
    s = math.sqrt(2.0)
    for _ in range(40):
        h = rand_channel(rng, 3, 3)
        x = [rng.randrange(4) for _ in range(3)]
        _, hr = real_model([0j] * 3, h, "qam")
        b, _, _ = lll([[row[k] for row in hr] for k in range(6)])
        _, _, norms = gram_schmidt(b)
        rad = 0.5 * math.sqrt(min(norms))
        # noise w with ||s w_r / 2|| just below rad
        w = [cbb.cn(rng, 1.0) for _ in range(3)]
        wn = math.sqrt(cbb.norm2(w)) * s / 2
        w = [v * 0.99 * rad / wn for v in w]
        y = cbb.add(cbb.matvec(h, [pts[i] for i in x]), w)
        assert lr_detect(y, h, pts, "sic") == x


def test_bad_arguments():
    with pytest.raises(ValueError):
        lr_detect([0j], [[1]], constel.psk(8))
    with pytest.raises(ValueError):
        lr_detect([0j], [[1]], constel.pam(2), "ml")
    with pytest.raises(ValueError):
        lll([[1.0, 0.0], [0.0, 1.0]], 0.2)
    with pytest.raises(ValueError):
        lll([[1.0, 2.0], [2.0, 4.0]])


def test_measured_errors():
    """Measurement, seed 1805: 2x2 4-QAM, i.i.d. Rayleigh, 20 dB, 1000 vectors."""
    rng = random.Random(1805)
    pts = constel.qam(4)
    n0 = cbb.undb(-20)
    err_zf = err_lr = swaps = most = 0
    for _ in range(1000):
        h = rand_channel(rng, 2, 2)
        x = [rng.randrange(4) for _ in range(2)]
        y = cbb.awgn(rng, cbb.matvec(h, [pts[i] for i in x]), n0)
        err_zf += lr_detect(y, h, pts, "zf", reduce=False) != x
        st = {}
        err_lr += lr_detect(y, h, pts, "sic", stats=st) != x
        swaps += st["swaps"]
        most = max(most, st["swaps"])
    # measured on CPython 3: ZF 11 vector errors, LR-SIC 1; 2.34 swaps on average, at most 10
    assert err_zf >= 8
    assert err_lr <= 3
    assert swaps / 1000 < 3 and most <= 12
