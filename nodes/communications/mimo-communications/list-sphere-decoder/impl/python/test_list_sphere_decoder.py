# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-sphere-decoder/. The authors are listed in prov/C5A1BF.jsonl.

import itertools
import math
import random

import pytest

import cbb
import constel
from list_sphere_decoder import list_llrs, list_sphere, triangularize


def all_metrics(y, h, points):
    """Every (metric, indices) pair, sorted by metric, by brute force."""
    out = []
    for idx in itertools.product(range(len(points)), repeat=len(h[0])):
        x = [points[i] for i in idx]
        out.append((cbb.norm2(cbb.sub(y, cbb.matvec(h, x))), list(idx)))
    out.sort(key=lambda e: e[0])
    return out


def exact_llrs(y, h, points, m_bits, n0):
    """The exact bit LLRs by log-sum-exp over all M^n vectors."""
    cands = all_metrics(y, h, points)
    out = []
    for k in range(len(h[0])):
        for b in range(m_bits):
            zero, one = [], []
            for d, idx in cands:
                (one if constel.bits(idx[k], m_bits)[b] else zero).append(-d / n0)
            lz = max(zero) + math.log(sum(math.exp(v - max(zero)) for v in zero))
            lo = max(one) + math.log(sum(math.exp(v - max(one)) for v in one))
            out.append(lz - lo)
    return out


def rand_case(rng, m, n, points, n0):
    h = [[cbb.cn(rng, 1.0) for _ in range(n)] for _ in range(m)]
    idx = [rng.randrange(len(points)) for _ in range(n)]
    y = cbb.awgn(rng, cbb.matvec(h, [points[i] for i in idx]), n0)
    return y, h, idx


def test_example():
    h = [[2, 1], [1, 1]]
    y = [0.5, 0.6]
    pts = constel.pam(2)
    r, yb, c = triangularize(y, h)
    s5 = math.sqrt(5)
    assert abs(r[0][0] - s5) < 1e-12 and abs(r[0][1] - 3 / s5) < 1e-12 and abs(r[1][1] - 1 / s5) < 1e-12
    assert abs(yb[0] - 1.6 / s5) < 1e-12 and abs(yb[1] - 0.7 / s5) < 1e-12 and abs(c) < 1e-12
    full = list_sphere(y, h, pts, 4)
    assert [v for _, v in full] == [[0, 1], [1, 0], [0, 0], [1, 1]]
    for (d, _), want in zip(full, [0.61, 2.61, 8.21, 19.01]):
        assert abs(d - want) < 1e-12
    st = {}
    two = list_sphere(y, h, pts, 2, st)
    assert [v for _, v in two] == [[0, 1], [1, 0]] and st["nodes"] == 6
    ml = list_llrs(two, 1, 1.0)
    assert abs(ml[0] - 2.0) < 1e-12 and abs(ml[1] + 2.0) < 1e-12
    ex = list_llrs(full, 1, 1.0, maxlog=False)
    want0 = math.log(math.exp(-0.61) + math.exp(-8.21)) - math.log(math.exp(-2.61) + math.exp(-19.01))
    assert abs(ex[0] - want0) < 1e-12 and abs(ex[0] - 2.0005) < 1e-4


def test_triangular_metric():
    rng = random.Random(1701)
    pts = constel.qam(4)
    for _ in range(20):
        y, h, _ = rand_case(rng, 4, 3, pts, 0.3)
        r, yb, c = triangularize(y, h)
        for _ in range(5):
            x = [rng.choice(pts) for _ in range(3)]
            lhs = cbb.norm2(cbb.sub(y, cbb.matvec(h, x)))
            rhs = cbb.norm2(cbb.sub(yb, cbb.matvec(r, x))) + c
            assert abs(lhs - rhs) < 1e-9


def test_list_is_the_best_vectors():
    rng = random.Random(1702)
    for pts, m, n in ((constel.qam(4), 3, 3), (constel.pam(4), 4, 3), (constel.qam(16), 2, 2), (constel.psk(8), 3, 2)):
        for _ in range(8):
            y, h, _ = rand_case(rng, m, n, pts, 0.5)
            ref = all_metrics(y, h, pts)
            for size in (1, 2, 5, 11):
                got = list_sphere(y, h, pts, size)
                assert len(got) == size
                for (d, v), (dr, _) in zip(got, ref):
                    assert abs(d - dr) < 1e-9
                    xv = [pts[i] for i in v]
                    assert abs(d - cbb.norm2(cbb.sub(y, cbb.matvec(h, xv)))) < 1e-9
            one = list_sphere(y, h, pts, 1)[0]
            mlv = constel.ml_vector(y, h, pts)
            dml = cbb.norm2(cbb.sub(y, cbb.matvec(h, [pts[i] for i in mlv])))
            assert abs(one[0] - dml) < 1e-9


def test_full_list_gives_exact_llrs():
    rng = random.Random(1703)
    for pts, mb in ((constel.qam(4), 2), (constel.pam(4), 2), (constel.qam(16), 4)):
        n = 3 if len(pts) == 4 else 2
        for _ in range(6):
            n0 = 0.4
            y, h, _ = rand_case(rng, n + 1, n, pts, n0)
            full = list_sphere(y, h, pts, len(pts) ** n)
            got = list_llrs(full, mb, n0, maxlog=False)
            want = exact_llrs(y, h, pts, mb, n0)
            for a, b in zip(got, want):
                assert abs(a - b) < 1e-9
            ref = all_metrics(y, h, pts)
            got_ml = list_llrs(full, mb, n0)
            k = 0
            for s in range(n):
                for b in range(mb):
                    d0 = min(d for d, v in ref if constel.bits(v[s], mb)[b] == 0)
                    d1 = min(d for d, v in ref if constel.bits(v[s], mb)[b] == 1)
                    assert abs(got_ml[k] - (d1 - d0) / n0) < 1e-9
                    k += 1


def test_max_log_exact_when_both_values_in_list():
    """Max-log LLRs from a short list equal the full max-log value for each bit whose two values both occur."""
    rng = random.Random(1706)
    pts = constel.qam(4)
    for _ in range(10):
        y, h, _ = rand_case(rng, 3, 3, pts, 0.5)
        ref = all_metrics(y, h, pts)
        short = list_sphere(y, h, pts, 8)
        got = list_llrs(short, 2, 0.5, clip=99.0)
        k = 0
        for s in range(3):
            for b in range(2):
                vals = {constel.bits(v[s], 2)[b] for _, v in short}
                if len(vals) == 2:
                    d0 = min(d for d, v in ref if constel.bits(v[s], 2)[b] == 0)
                    d1 = min(d for d, v in ref if constel.bits(v[s], 2)[b] == 1)
                    assert abs(got[k] - (d1 - d0) / 0.5) < 1e-9
                else:
                    assert got[k] == (99.0 if vals == {0} else -99.0)
                k += 1


def test_clipping():
    cands = [(1.0, [0, 3]), (2.0, [0, 2])]
    llr = list_llrs(cands, 2, 1.0, clip=7.5)
    # stream 0 has label 00 in both: both bits clip to +7.5
    assert llr[0] == 7.5 and llr[1] == 7.5
    # stream 1: labels 11 and 10; bit 0 is always 1, bit 1 differs
    # bit 1 is 0 at metric 2.0 and 1 at metric 1.0: LLR = (1.0 - 2.0) / N0 = -1
    assert llr[2] == -7.5 and abs(llr[3] + 1.0) < 1e-12


def test_bad_arguments():
    pts = constel.pam(2)
    with pytest.raises(ValueError):
        list_sphere([1, 1], [[1, 2], [2, 4]], pts, 2)
    with pytest.raises(ValueError):
        list_sphere([1], [[1, 1]], pts, 2)
    with pytest.raises(ValueError):
        list_sphere([1, 1], [[1, 0], [0, 1]], pts, 0)
    with pytest.raises(ValueError):
        list_llrs([(0.0, [0])], 1, 0.0)


def test_measured_node_count():
    """Measurement, seed 1704: 4x4 4-QAM at 15 dB SNR, 100 vectors. The full tree has 340 nodes."""
    rng = random.Random(1704)
    pts = constel.qam(4)
    n0 = cbb.undb(-15)
    nodes1 = nodes16 = 0
    for _ in range(100):
        y, h, _ = rand_case(rng, 4, 4, pts, n0)
        st = {}
        list_sphere(y, h, pts, 1, st)
        nodes1 += st["nodes"]
        st = {}
        list_sphere(y, h, pts, 16, st)
        nodes16 += st["nodes"]
    assert nodes1 / 100 < 12
    assert nodes16 / 100 < 130
