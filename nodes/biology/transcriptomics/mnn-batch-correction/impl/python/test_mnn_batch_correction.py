# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mnn-batch-correction/. The authors are listed in prov/MTE8PT.jsonl.

import math
import random

import pytest

from mnn_batch_correction import correct_pair, correction_vectors, cosine_normalize, mnn_correct, mnn_pairs
from rq3lin import knn, sqdist

PAGE_R = [(0, 0), (1, 0), (6, 0), (7, 0), (8, 0)]
PAGE_B = [(0, 3), (1, 3), (2, 3), (7, 3), (3, 9)]


def close(a, b, tol=1e-9):
    return all(math.isclose(x, y, abs_tol=tol) for x, y in zip(a, b))


def test_page_example():
    pairs = mnn_pairs(PAGE_R, PAGE_B, 1)
    assert pairs == [(0, 0), (1, 1), (3, 3)]
    out = mnn_correct([PAGE_R, PAGE_B], k=1, sigma=1.0, cos_norm=False)[1]
    want = [(0, 0), (1, 0), (2, 0), (7, 0), (3, 6)]
    assert all(close(a, b) for a, b in zip(out, want))
    # A global shift by the difference of the batch means would be wrong here.
    mr = [sum(c) / 5 for c in zip(*PAGE_R)]
    mb = [sum(c) / 5 for c in zip(*PAGE_B)]
    assert close([a - b for a, b in zip(mr, mb)], [1.8, -4.2])
    # With k = 2 the pairs include wrong matches, and the correction is no longer exact.
    p2 = mnn_pairs(PAGE_R, PAGE_B, 2)
    assert (2, 3) in p2


def brute_pairs(R, B, k):
    def near(points, q):
        return sorted(range(len(points)), key=lambda j: (sqdist(q, points[j]), j))[:k]
    return sorted((r, b) for r in range(len(R)) for b in range(len(B))
                  if r in near(R, B[b]) and b in near(B, R[r]))


def test_pairs_match_the_definition_and_are_bounded():
    rng = random.Random(1)
    for _ in range(20):
        R = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(rng.randint(3, 15))]
        B = [[rng.gauss(0.5, 1) for _ in range(3)] for _ in range(rng.randint(3, 15))]
        k = rng.randint(1, 3)
        p = mnn_pairs(R, B, k)
        assert p == brute_pairs(R, B, k)
        assert len(p) <= k * min(len(R), len(B))
        assert sorted((r, b) for b, r in mnn_pairs(B, R, k)) == p


def test_cosine_normalization():
    x = [3.0, 4.0, 0.0]
    assert close(cosine_normalize([x])[0], [0.6, 0.8, 0.0])
    assert close(cosine_normalize([[2.5 * v for v in x]])[0], [0.6, 0.8, 0.0])
    rng = random.Random(2)
    for _ in range(20):
        a = [rng.uniform(0, 5) for _ in range(4)]
        b = [rng.uniform(0, 5) for _ in range(4)]
        na, nb = cosine_normalize([a, b])
        cos = sum(p * q for p, q in zip(a, b)) / math.sqrt(sum(p * p for p in a) * sum(q * q for q in b))
        assert math.isclose(sqdist(na, nb), 2 - 2 * cos, abs_tol=1e-12)
    with pytest.raises(ValueError):
        cosine_normalize([[0.0, 0.0]])


def test_correction_is_a_convex_combination_of_the_pair_vectors():
    rng = random.Random(3)
    R = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(20)]
    B = [[rng.gauss(1, 1) for _ in range(2)] for _ in range(20)]
    pairs = mnn_pairs(R, B, 3)
    vecs = [[x - y for x, y in zip(R[r], B[b])] for r, b in pairs]
    for c in correction_vectors(R, B, pairs, 0.7):
        for a in range(2):
            assert min(v[a] for v in vecs) - 1e-12 <= c[a] <= max(v[a] for v in vecs) + 1e-12


def test_exact_translation_is_removed():
    """k = 1 and a shift shorter than half the closest distance in R: every pair is true, so B maps onto R."""
    rng = random.Random(4)
    for _ in range(10):
        R = [[rng.uniform(0, 10) for _ in range(3)] for _ in range(25)]
        dmin = min(math.sqrt(sqdist(p, q)) for i, p in enumerate(R) for q in R[i + 1:])
        c = [rng.gauss(0, 1) for _ in range(3)]
        n = math.sqrt(sum(v * v for v in c))
        c = [v * 0.45 * dmin / n for v in c]
        B = [[x + y for x, y in zip(p, c)] for p in R]
        assert mnn_pairs(R, B, 1) == [(i, i) for i in range(25)]
        out = correct_pair(R, B, 1, sigma=0.5)
        assert all(close(a, b) for a, b in zip(out, R))


def test_bandwidth_limits():
    rng = random.Random(5)
    R = [[rng.gauss(0, 1) for _ in range(2)] for _ in range(15)]
    B = [[rng.gauss(0.3, 1) for _ in range(2)] for _ in range(15)]
    pairs = mnn_pairs(R, B, 2)
    vecs = [[x - y for x, y in zip(R[r], B[b])] for r, b in pairs]
    mean = [sum(v[a] for v in vecs) / len(vecs) for a in range(2)]
    for c in correction_vectors(R, B, pairs, 1e4):
        assert close(c, mean, 1e-6)
    # A cell of B that is in exactly one pair gets that pair's vector when sigma is tiny.
    tiny = correction_vectors(R, B, pairs, 1e-3)
    for (r, b), v in zip(pairs, vecs):
        if sum(1 for _, bb in pairs if bb == b) == 1:
            assert close(tiny[b], v, 1e-9)


def two_batches(rng, frac1, frac2, n=60, dim=5):
    """Two cell types in two batches with different mixes; batch 2 is shifted by a constant vector."""
    types = [[0.0] * dim, [4.0] + [0.0] * (dim - 1)]
    shift = [0.0, 2.0, 1.0] + [0.0] * (dim - 3)

    def cells(frac):
        out, lab = [], []
        for i in range(n):
            t = 1 if i < frac * n else 0
            out.append([m + rng.gauss(0, 0.5) for m in types[t]])
            lab.append(t)
        return out, lab

    R, lr = cells(frac1)
    T, lb = cells(frac2)
    B = [[x + s for x, s in zip(p, shift)] for p in T]
    return R, lr, B, lb, T


def test_different_cell_type_mix_measured():
    """A measurement: MNN finds the shift when the mixes differ; centering the batch means does not."""
    rng = random.Random(2018)
    R, lr, B, lb, truth = two_batches(rng, 0.2, 0.8)
    out = mnn_correct([R, B], k=10, sigma=1.0, cos_norm=False)[1]
    mr = [sum(c) / len(R) for c in zip(*R)]
    mb = [sum(c) / len(B) for c in zip(*B)]
    centered = [[x + a - b for x, a, b in zip(p, mr, mb)] for p in B]

    def err(X):
        return sum(math.sqrt(sqdist(p, q)) for p, q in zip(X, truth)) / len(X)

    # Measured: 0.78 against 2.36. The error left is the noise of the paired cells.
    assert err(out) < 0.4 * err(centered)
    # After correction the nearest reference cell of each cell of B has its cell type.
    nn = knn(R, 1, queries=out)
    assert sum(lr[nn[i][0]] == lb[i] for i in range(len(B))) >= 0.95 * len(B)


def test_cell_type_missing_from_the_reference_measured():
    """A measurement: a type found only in batch 2 is moved, but not onto a type of batch 1."""
    rng = random.Random(7)
    R, lr, B, lb, truth = two_batches(rng, 0.5, 0.5)
    extra = [[0.0, 0.0, 0.0, 5.0, 0.0] for _ in range(15)]
    extra = [[m + rng.gauss(0, 0.5) for m in p] for p in extra]
    shift = [0.0, 2.0, 1.0, 0.0, 0.0]
    B2 = B + [[x + s for x, s in zip(p, shift)] for p in extra]
    out = mnn_correct([R, B2], k=10, sigma=1.0, cos_norm=False)[1]
    moved = out[len(B):]
    gap = min(math.sqrt(sqdist(p, q)) for p in moved for q in R)
    assert gap > 2.0
    assert sum(math.sqrt(sqdist(p, q)) for p, q in zip(moved, extra)) / 15 < 1.5


def test_three_batches_in_order():
    rng = random.Random(8)
    R = [[rng.uniform(0, 10) for _ in range(2)] for _ in range(20)]
    B = [[x + 0.01, y - 0.02] for x, y in R]
    C = [[x - 0.015, y + 0.01] for x, y in R]
    out = mnn_correct([R, B, C], k=1, sigma=0.5, cos_norm=False)
    assert all(close(a, b, 1e-9) for a, b in zip(out[1], R))
    assert all(close(a, b, 1e-9) for a, b in zip(out[2], R))


def test_no_pairs_is_an_error():
    with pytest.raises(ValueError):
        correction_vectors([[0.0]], [[1.0]], [], 1.0)
