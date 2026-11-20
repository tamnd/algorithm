# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/v-blast/. The authors are listed in prov/Z0RT80.jsonl.

import itertools
import math
import random

import pytest

import cbb
import constel
from v_blast import nearest, post_detection_snr, vblast_detect


def rayleigh(rng, m, n):
    return [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]


def sic_fixed_order(y, h, points, order):
    """ZF nulling and cancelling in a given order, without the V-BLAST choice."""
    r = list(y)
    left = list(range(len(h[0])))
    out = [-1] * len(left)
    for k in order:
        hk = [[row[c] for c in left] for row in h]
        w = cbb.solve(cbb.matmul(cbb.herm(hk), hk), cbb.herm(hk))
        i = left.index(k)
        out[k] = nearest(sum(c * v for c, v in zip(w[i], r)), points)
        r = [rv - row[k] * points[out[k]] for rv, row in zip(r, h)]
        left.pop(i)
    return out


def test_example_on_the_page() -> None:
    h = [[2, 1], [1, 1]]
    y = [0.7, 0.4]  # x = (+1, -1) and w = (-0.3, 0.4)
    bpsk = constel.pam(2)
    w = cbb.inv(h)
    z = cbb.matvec(w, y)
    assert abs(z[0] - 0.3) < 1e-12 and abs(z[1] - 0.1) < 1e-12  # ZF decides (+1, +1)
    assert vblast_detect(y, h, bpsk) == ([0, 1], [0, 1])
    assert constel.ml_vector(y, h, bpsk) == [0, 1]
    assert sic_fixed_order(y, h, bpsk, [1, 0]) == [1, 0]  # the other order: two errors
    a, b = post_detection_snr(h, [0, 1], 1.0, 1.0), post_detection_snr(h, [1, 0], 1.0, 1.0)
    assert max(abs(a[0] - 0.5), abs(a[1] - 2.0), abs(b[0] - 0.2), abs(b[1] - 5.0)) < 1e-12


def test_noiseless_recovery_is_exact() -> None:
    rng = random.Random(1401)
    pts = constel.qam(16)
    for _ in range(60):
        n = rng.randint(1, 4)
        m = rng.randint(n, 5)
        h = rayleigh(rng, m, n)
        idx = [rng.randrange(16) for _ in range(n)]
        y = cbb.matvec(h, [pts[i] for i in idx])
        d, order = vblast_detect(y, h, pts)
        assert d == idx and sorted(order) == list(range(n))
        d, _ = vblast_detect(y, h, pts, n0=1e-9, mmse=True)
        assert d == idx


def test_greedy_order_maximizes_the_smallest_snr() -> None:
    # theorem: the V-BLAST order maximizes the minimum post-detection SNR (ZF) or SINR (MMSE)
    rng = random.Random(1402)
    pts = constel.qam(4)
    for _ in range(40):
        n = rng.randint(2, 4)
        m = rng.randint(n, 5)
        h = rayleigh(rng, m, n)
        for mmse in (False, True):
            _, order = vblast_detect([0j] * m, h, pts, n0=0.1, mmse=mmse)
            best = min(post_detection_snr(h, order, 1.0, 0.1, mmse))
            for perm in itertools.permutations(range(n)):
                assert min(post_detection_snr(h, list(perm), 1.0, 0.1, mmse)) <= best * (1 + 1e-9)


def test_mmse_sic_sinrs_add_up_to_the_capacity_in_any_order() -> None:
    # theorem: with MMSE nulling and correct cancellation, sum log2(1 + SINR_k) = log2 det(I + (Es/N0) H^H H)
    rng = random.Random(1403)
    for _ in range(30):
        n = rng.randint(1, 4)
        m = rng.randint(1, 5)
        h = rayleigh(rng, m, n)
        snr = rng.uniform(0.5, 30.0)
        g = cbb.matmul(cbb.herm(h), h)
        cap = math.log2(abs(cbb.det(cbb.add(cbb.eye(n), cbb.scale(snr, g)))))
        order = list(range(n))
        rng.shuffle(order)
        s = post_detection_snr(h, order, 1.0, 1.0 / snr, mmse=True)
        assert abs(sum(math.log2(1 + v) for v in s) - cap) < 1e-9 * (1 + cap)


def test_one_stream_is_maximal_ratio_combining() -> None:
    rng = random.Random(1404)
    h = rayleigh(rng, 4, 1)
    assert abs(post_detection_snr(h, [0], 1.0, 0.5)[0] - cbb.norm2([r[0] for r in h]) / 0.5) < 1e-12


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        vblast_detect([0j], [[1, 1]], constel.pam(2))
    with pytest.raises(ValueError):
        vblast_detect([0j, 0j], [[1, 2], [2, 4]], constel.pam(2))
    with pytest.raises(ValueError):
        vblast_detect([0j], [[1]], constel.pam(2), n0=0.0, mmse=True)


def test_most_decisions_match_ml_and_beat_zf() -> None:
    # measured: 4-QAM, m = n = 4, Es/N0 = 15 dB, seed 1405, 150 vectors
    rng = random.Random(1405)
    pts = constel.qam(4)
    n0 = 1 / cbb.undb(15.0)
    agree_zf = agree_mmse = err_vb = err_zf = 0
    for _ in range(150):
        h = rayleigh(rng, 4, 4)
        idx = [rng.randrange(4) for _ in range(4)]
        y = cbb.awgn(rng, cbb.matvec(h, [pts[i] for i in idx]), n0)
        ml = constel.ml_vector(y, h, pts)
        d, _ = vblast_detect(y, h, pts)
        agree_zf += d == ml
        agree_mmse += vblast_detect(y, h, pts, n0=n0, mmse=True)[0] == ml
        err_vb += sum(a != b for a, b in zip(d, idx))
        w = cbb.solve(cbb.matmul(cbb.herm(h), h), cbb.herm(h))
        err_zf += sum(nearest(z, pts) != b for z, b in zip(cbb.matvec(w, y), idx))
    print(agree_zf, agree_mmse, err_vb, err_zf)
    assert agree_zf >= 140 and agree_mmse >= 145
    assert err_vb < err_zf
