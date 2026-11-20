# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hogbom-clean/. The authors are listed in prov/0ZFP8H.jsonl.

import random

from hogbom_clean import (
    data_misfit,
    dirty_beam,
    dirty_image,
    fit_clean_beam,
    hogbom_clean,
    restore,
)
from imgkit import circ_conv2, new_image


def mask_1d(n, freqs):
    w = [0.0] * n
    for k in freqs:
        w[k % n] = 1.0
        w[-k % n] = 1.0
    return [w]


def mask_2d(n, fraction, rng):
    """Random gridded uv weights, symmetric under (k, l) -> (-k, -l), with the zero spacing measured."""
    w = new_image(n, n)
    w[0][0] = 1.0
    for k in range(n):
        for l in range(n):
            if rng.random() < fraction:
                w[k][l] = 1.0
                w[-k % n][-l % n] = 1.0
    return w


def max_abs(img):
    return max(abs(v) for row in img for v in row)


def test_page_example_1d():
    w = mask_1d(16, (0, 1, 2, 3, 5))
    sky = [[0.0] * 16]
    sky[0][4], sky[0][7] = 1.0, 0.6
    beam = dirty_beam(w)
    dirty = dirty_image(sky, w)
    assert abs(beam[0][0] - 1.0) < 1e-12
    assert abs(beam[0][8] + 1.0 / 3.0) < 1e-12
    assert abs(dirty[0][4] - 1.0234) < 1e-4
    model, res, comps = hogbom_clean(dirty, beam, gain=0.5, max_iter=4)
    assert [(j, round(c, 4)) for _, j, c in comps] == [(4, 0.5117), (7, 0.3095), (4, 0.2498), (7, 0.1499)]
    model, res, comps = hogbom_clean(dirty, beam, gain=0.5, max_iter=80)
    assert max(abs(a - b) for a, b in zip(model[0], sky[0])) < 1e-9
    assert max_abs(res) < 1e-9


def test_dirty_image_is_beam_convolution():
    rng = random.Random(11)
    w = mask_2d(16, 0.25, rng)
    sky = [[rng.random() if rng.random() < 0.1 else 0.0 for _ in range(16)] for _ in range(16)]
    a = dirty_image(sky, w)
    b = circ_conv2(sky, dirty_beam(w))
    assert max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb)) < 1e-12


def test_residual_invariant_2d():
    rng = random.Random(5)
    w = mask_2d(16, 0.2, rng)
    sky = new_image(16, 16)
    for _ in range(4):
        sky[rng.randrange(16)][rng.randrange(16)] += rng.uniform(0.5, 2.0)
    beam = dirty_beam(w)
    dirty = dirty_image(sky, w)
    model, res, comps = hogbom_clean(dirty, beam, gain=0.2, max_iter=60)
    pred = circ_conv2(model, beam)
    gap = max(abs(d - p - r) for rd, rp, rr in zip(dirty, pred, res) for d, p, r in zip(rd, rp, rr))
    assert gap < 1e-10
    assert abs(sum(c for _, _, c in comps) - sum(sum(r) for r in model)) < 1e-10


def test_misfit_drops_by_the_proved_amount():
    rng = random.Random(7)
    w = mask_2d(16, 0.2, rng)
    sky = new_image(16, 16)
    for _ in range(5):
        sky[rng.randrange(16)][rng.randrange(16)] += rng.uniform(0.2, 1.0)
    beam = dirty_beam(w)
    dirty = dirty_image(sky, w)
    for gain in (0.1, 1.0, 1.9):
        model, res = new_image(16, 16), dirty
        q = data_misfit(model, sky, w)
        for _ in range(8):
            m2, r2, comps = hogbom_clean(res, beam, gain=gain, max_iter=1)
            i, j, c = comps[0]
            peak = res[i][j]
            model[i][j] += c
            q2 = data_misfit(model, sky, w)
            assert abs((q - q2) - (2 * gain - gain * gain) * peak * peak) < 1e-9
            assert q2 <= q + 1e-12
            q, res = q2, r2


def test_gain_range():
    rng = random.Random(3)
    w = mask_2d(16, 0.3, rng)
    sky = new_image(16, 16)
    for _ in range(3):
        sky[rng.randrange(16)][rng.randrange(16)] += 1.0
    beam = dirty_beam(w)
    dirty = dirty_image(sky, w)
    start = max_abs(dirty)
    _, res, _ = hogbom_clean(dirty, beam, gain=0.5, max_iter=300)
    assert max_abs(res) < 1e-3 * start
    _, res, _ = hogbom_clean(dirty, beam, gain=2.2, max_iter=60)
    assert max_abs(res) > 10 * start


def test_full_coverage_gives_the_sky():
    n = 8
    w = new_image(n, n, 1.0)
    beam = dirty_beam(w)
    assert abs(beam[0][0] - 1.0) < 1e-12 and abs(beam[3][5]) < 1e-12
    sky = new_image(n, n)
    sky[1][2], sky[5][6], sky[7][0] = 3.0, -1.0, 2.0
    model, res, comps = hogbom_clean(dirty_image(sky, w), beam, gain=1.0, threshold=1e-9, max_iter=10)
    assert len(comps) == 3
    assert max(abs(a - b) for ra, rb in zip(model, sky) for a, b in zip(ra, rb)) < 1e-12


def test_threshold_positive_and_window():
    rng = random.Random(9)
    w = mask_2d(16, 0.3, rng)
    sky = new_image(16, 16)
    sky[4][4], sky[10][12] = 1.0, 0.5
    beam = dirty_beam(w)
    dirty = dirty_image(sky, w)
    _, res, comps = hogbom_clean(dirty, beam, gain=0.1, threshold=0.05, max_iter=5000)
    assert max_abs(res) <= 0.05 + 1e-12
    _, _, comps = hogbom_clean(dirty, beam, gain=0.1, positive_only=True, max_iter=200)
    assert all(c > 0 for _, _, c in comps)
    win = [[abs(i - 4) <= 1 and abs(j - 4) <= 1 for j in range(16)] for i in range(16)]
    _, _, comps = hogbom_clean(dirty, beam, gain=0.1, window=win, max_iter=50)
    assert all(abs(i - 4) <= 1 and abs(j - 4) <= 1 for i, j, _ in comps)


def test_restore_point_source():
    rng = random.Random(4)
    w = mask_2d(16, 0.35, rng)
    for k in range(-2, 3):
        for l in range(-2, 3):
            w[k % 16][l % 16] = 1.0
    sky = new_image(16, 16)
    sky[8][8] = 2.0
    beam = dirty_beam(w)
    model, res, _ = hogbom_clean(dirty_image(sky, w), beam, gain=0.2, max_iter=200)
    cb = fit_clean_beam(beam)
    assert cb[0][0] == 1.0 and 0.0 < cb[0][1] < 1.0
    img = restore(model, res, cb)
    assert abs(img[8][8] - 2.0) < 1e-6
    assert abs(sum(sum(r) for r in model) - 2.0) < 1e-6
