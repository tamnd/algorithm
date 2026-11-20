# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-best-detector/. The authors are listed in prov/3ZQXDE.jsonl.

import itertools
import math
import random

import pytest

import cbb
import constel
from k_best_detector import k_best, k_best_detect, triangularize


def rayleigh(rng, m, n):
    return [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]


def metric(y, h, points, idx):
    return cbb.norm2(cbb.sub(y, cbb.matvec(h, [points[i] for i in idx])))


def zf_sic_fixed_order(y, h, points):
    """ZF nulling and cancelling in the order n - 1, n - 2, ..., 0."""
    r, out = list(y), [0] * len(h[0])
    for k in range(len(h[0]) - 1, -1, -1):
        hk = [row[: k + 1] for row in h]
        w = cbb.solve(cbb.matmul(cbb.herm(hk), hk), cbb.herm(hk))
        z = sum(c * v for c, v in zip(w[k], r))
        out[k] = min(range(len(points)), key=lambda j: abs(z - points[j]))
        r = [rv - row[k] * points[out[k]] for rv, row in zip(r, h)]
    return out


def test_example_on_the_page() -> None:
    h = [[2, 1], [1, 1]]
    y = [0.5, 0.6]
    bpsk = constel.pam(2)
    r, yb, c = triangularize(y, h)
    s5 = math.sqrt(5)
    assert abs(r[0][0] - s5) < 1e-12 and abs(r[0][1] - 3 / s5) < 1e-12 and abs(r[1][1] - 1 / s5) < 1e-12
    assert abs(yb[0] - 1.6 / s5) < 1e-12 and abs(yb[1] - 0.7 / s5) < 1e-12 and abs(c) < 1e-12
    one = k_best(y, h, bpsk, 1)
    assert one[0][1] == [1, 0] and abs(one[0][0] - 2.61) < 1e-12  # (-1, +1): both symbols wrong
    two = k_best(y, h, bpsk, 2)
    assert [e[1] for e in two] == [[0, 1], [1, 0]] and abs(two[0][0] - 0.61) < 1e-12  # the ML vector


def test_triangular_metric_equals_the_ml_metric() -> None:
    rng = random.Random(1601)
    pts = constel.qam(16)
    for _ in range(20):
        n = rng.randint(1, 4)
        m = rng.randint(n, 6)
        h = rayleigh(rng, m, n)
        y = [cbb.cn(rng, 2.0) for _ in range(m)]
        r, yb, c = triangularize(y, h)
        assert all(abs(r[i][j]) == 0 for i in range(n) for j in range(i))
        idx = [rng.randrange(16) for _ in range(n)]
        x = [pts[i] for i in idx]
        assert abs(cbb.norm2(cbb.sub(yb, cbb.matvec(r, x))) + c - metric(y, h, pts, idx)) < 1e-9


def test_large_k_is_exact_ml_and_returns_the_k_best_vectors() -> None:
    # theorem: with K >= M^(n-1) nothing is pruned before the last level
    rng = random.Random(1602)
    for M, n, m in [(2, 3, 3), (4, 2, 3), (4, 3, 3), (2, 4, 5)]:
        pts = constel.qam(M) if M == 4 else constel.pam(M)
        for _ in range(6):
            h = rayleigh(rng, m, n)
            y = cbb.awgn(rng, cbb.matvec(h, [pts[rng.randrange(M)] for _ in range(n)]), 0.5)
            k = M ** (n - 1)
            got = k_best(y, h, pts, k)
            allm = sorted(metric(y, h, pts, idx) for idx in itertools.product(range(M), repeat=n))
            assert all(abs(g[0] - b) < 1e-9 for g, b in zip(got, allm[:k]))
            assert all(abs(g[0] - metric(y, h, pts, g[1])) < 1e-9 for g in got)
            assert k_best_detect(y, h, pts, k) == constel.ml_vector(y, h, pts)


def test_k_equal_to_one_is_zf_successive_cancellation() -> None:
    rng = random.Random(1603)
    pts = constel.qam(16)
    for _ in range(40):
        n = rng.randint(1, 4)
        m = rng.randint(n, 5)
        h = rayleigh(rng, m, n)
        y = cbb.awgn(rng, cbb.matvec(h, [pts[rng.randrange(16)] for _ in range(n)]), 0.05)
        assert k_best_detect(y, h, pts, 1) == zf_sic_fixed_order(y, h, pts)


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        k_best([0j], [[1, 1]], constel.pam(2), 2)
    with pytest.raises(ValueError):
        k_best([0j, 0j], [[1, 2], [2, 4]], constel.pam(2), 2)
    with pytest.raises(ValueError):
        k_best([0j], [[1]], constel.pam(2), 0)


def test_small_k_is_close_to_ml_at_high_snr() -> None:
    # measured: 4-QAM, m = n = 4, Es/N0 = 15 dB, seed 1605, 150 vectors
    rng = random.Random(1605)
    pts = constel.qam(4)
    n0 = 1 / cbb.undb(15.0)
    agree = {1: 0, 4: 0}
    for _ in range(150):
        h = rayleigh(rng, 4, 4)
        y = cbb.awgn(rng, cbb.matvec(h, [pts[rng.randrange(4)] for _ in range(4)]), n0)
        ml = constel.ml_vector(y, h, pts)
        for k in agree:
            agree[k] += k_best_detect(y, h, pts, k) == ml
    print(agree)
    assert agree[1] >= 140 and agree[4] >= 148 and agree[1] <= agree[4]
