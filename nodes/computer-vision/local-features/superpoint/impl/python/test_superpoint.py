# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superpoint/. The authors are listed in prov/P2KH05.jsonl.

import math
import random

import pytest

from superpoint import decode_heatmap, nms, sample_descriptor, softmax, superpoint_decode


def random_logits(rng, hc, wc, spread=3.0):
    return [[[rng.gauss(0.0, spread) for _ in range(65)] for _ in range(wc)] for _ in range(hc)]


def brute_nms(heat, tau, r, border):
    """Greedy NMS by its definition, in O(n^2): keep a pixel if no kept pixel is within r."""
    h, w = len(heat), len(heat[0])
    cand = [(heat[v][u], u, v) for v in range(h) for u in range(w)
            if heat[v][u] >= tau and border <= u < w - border and border <= v < h - border]
    cand.sort(key=lambda t: (-t[0], t[2], t[1]))
    kept = []
    for s, u, v in cand:
        if all(max(abs(u - a), abs(v - b)) > r for a, b, _ in kept):
            kept.append((u, v, s))
    return kept


def test_cell_probabilities_with_dustbin_sum_to_one():
    rng = random.Random(1)
    X = random_logits(rng, 3, 4)
    heat = decode_heatmap(X)
    assert len(heat) == 24 and len(heat[0]) == 32
    for cy in range(3):
        for cx in range(4):
            cell = sum(heat[8 * cy + i][8 * cx + j] for i in range(8) for j in range(8))
            dust = softmax(X[cy][cx])[64]
            assert abs(cell + dust - 1.0) < 1e-12
            assert all(0.0 < heat[8 * cy + i][8 * cx + j] < 1.0 for i in range(8) for j in range(8))


def test_channel_goes_to_its_pixel():
    for cy, cx, c in ((0, 0, 0), (1, 2, 27), (2, 1, 63), (0, 3, 8)):
        X = [[[0.0] * 65 for _ in range(4)] for _ in range(3)]
        X[cy][cx][c] = 20.0
        heat = decode_heatmap(X)
        best = max((heat[v][u], u, v) for v in range(24) for u in range(32))
        assert (best[1], best[2]) == (8 * cx + c % 8, 8 * cy + c // 8)


def test_shift_of_logits_and_large_values():
    rng = random.Random(2)
    X = random_logits(rng, 2, 2)
    Y = [[[x + 1000.0 for x in cell] for cell in row] for row in X]
    a, b = decode_heatmap(X), decode_heatmap(Y)
    assert all(abs(p - q) < 1e-12 for ra, rb in zip(a, b) for p, q in zip(ra, rb))
    with pytest.raises(ValueError):
        decode_heatmap([[[0.0] * 64]])


def test_nms_equals_brute_force_definition():
    rng = random.Random(3)
    for trial in range(12):
        X = random_logits(rng, 3, 3, spread=rng.choice((1.0, 3.0, 6.0)))
        heat = decode_heatmap(X)
        if trial % 3 == 0:  # create exact ties
            heat = [[round(x, 2) for x in row] for row in heat]
        for r in (0, 1, 2, 4):
            for border in (0, 2):
                tau = rng.choice((0.0, 0.01, 0.05))
                assert nms(heat, tau, r, border) == brute_nms(heat, tau, r, border)


def test_many_small_heat_maps_against_brute_force():
    rng = random.Random(6)
    for _ in range(600):
        h, w = rng.randint(1, 9), rng.randint(1, 9)
        heat = [[rng.choice((0.0, 0.1, 0.2, 0.3, rng.random())) for _ in range(w)] for _ in range(h)]
        r, border = rng.randint(0, 3), rng.randint(0, 2)
        tau = rng.choice((0.0, 0.1, 0.25))
        assert nms(heat, tau, r, border) == brute_nms(heat, tau, r, border)


def test_nms_output_properties():
    rng = random.Random(4)
    heat = decode_heatmap(random_logits(rng, 4, 4, 4.0))
    r, tau = 3, 0.02
    kept = nms(heat, tau, r, 0)
    for i, (u, v, s) in enumerate(kept):
        for a, b, t in kept[i + 1:]:
            assert max(abs(u - a), abs(v - b)) > r and t <= s
    keep_set = {(u, v) for u, v, _ in kept}
    for v in range(32):
        for u in range(32):
            if heat[v][u] >= tau and (u, v) not in keep_set:
                assert any(max(abs(u - a), abs(v - b)) <= r and s >= heat[v][u] for a, b, s in kept)


def test_bilinear_sampling_reproduces_an_affine_map():
    hc, wc = 3, 4
    F = [[[2.0 * cx - cy + 1.0, 0.5 * cy, 3.0] for cx in range(wc)] for cy in range(hc)]
    for u, v in ((3.5, 3.5), (10.0, 7.0), (20.25, 12.5), (27.5, 19.5)):
        fx, fy = (u - 3.5) / 8, (v - 3.5) / 8
        got = sample_descriptor(F, u, v, normalize=False)
        want = [2.0 * fx - fy + 1.0, 0.5 * fy, 3.0]
        assert all(abs(g - w) < 1e-12 for g, w in zip(got, want))
    # outside the centers the sample is clamped to the border cells
    assert sample_descriptor(F, 0.0, 0.0, normalize=False) == F[0][0]


def test_full_decode_gives_unit_descriptors():
    rng = random.Random(5)
    X = random_logits(rng, 4, 5, 3.0)
    F = [[[rng.gauss(0, 1) for _ in range(16)] for _ in range(5)] for _ in range(4)]
    kps, desc = superpoint_decode(X, F, tau=0.01, r=2, border=4)
    assert len(kps) == len(desc) > 0
    for (u, v, s), f in zip(kps, desc):
        assert 4 <= u < 36 and 4 <= v < 28 and s >= 0.01
        assert abs(math.sqrt(sum(t * t for t in f)) - 1.0) < 1e-12
