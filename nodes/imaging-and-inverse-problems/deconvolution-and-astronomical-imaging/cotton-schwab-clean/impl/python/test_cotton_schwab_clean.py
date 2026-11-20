# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cotton-schwab-clean/. The authors are listed in prov/R1NZQT.jsonl.

import random

from cotton_schwab_clean import (
    cotton_schwab_clean,
    dirty_beam,
    dirty_from,
    minor_cycle,
    misfit,
    outside_sidelobe,
    predict,
)


def make_vis(seed, n, pairs, sources, umax=6.0):
    """Random uv points in conjugate pairs, and the exact visibilities of a sky of point sources."""
    rng = random.Random(seed)
    dl = 1.0 / 16
    sky = [[0.0] * n for _ in range(n)]
    for i, j, f in sources:
        sky[i][j] = f
    uv = []
    for _ in range(pairs):
        u, v = rng.uniform(-umax, umax), rng.uniform(-umax, umax)
        uv += [(u, v, 1.0, 0), (-u, -v, 1.0, 0)]
    vals = predict(sky, uv, dl)
    return sky, [(u, v, w, val) for (u, v, w, _), val in zip(uv, vals)], dl


PAGE_SOURCES = ((4, 5, 1.0), (10, 11, 0.7), (6, 12, 0.5), (12, 3, 0.4))


def max_abs(img):
    return max(abs(x) for row in img for x in row)


def diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_dirty_image_is_the_beam_convolution():
    n = 10
    sky, vis, dl = make_vis(3, n, 40, ((2, 3, 1.0), (7, 6, -0.5), (5, 5, 0.8)))
    beam = dirty_beam(vis, n, dl)
    assert abs(beam[(0, 0)] - 1.0) < 1e-12
    dirty = dirty_from(vis, [val for _, _, _, val in vis], n, dl)
    conv = [[sum(beam[(i - a, j - b)] * sky[a][b] for a in range(n) for b in range(n)) for j in range(n)] for i in range(n)]
    assert diff(dirty, conv) < 1e-10


def test_full_patch_minor_cycle_is_exact():
    n = 10
    sky, vis, dl = make_vis(5, n, 40, ((2, 3, 1.0), (7, 6, 0.6)))
    beam = dirty_beam(vis, n, dl)
    r = dirty_from(vis, [val for _, _, _, val in vis], n, dl)
    model = [[0.0] * n for _ in range(n)]
    minor_cycle(r, model, beam, n - 1, 0.2, 0.0, 40)
    exact = dirty_from(vis, [val - p for (_, _, _, val), p in zip(vis, predict(model, vis, dl))], n, dl)
    assert diff(r, exact) < 1e-10


def test_minor_cycle_drift_is_bounded_by_the_outside_sidelobe():
    n = 12
    sky, vis, dl = make_vis(7, n, 50, ((3, 3, 1.0), (8, 9, 0.8), (5, 10, 0.5)))
    beam = dirty_beam(vis, n, dl)
    patch = 2
    far = outside_sidelobe(beam, patch)
    assert 0.0 < far < 1.0
    r = dirty_from(vis, [val for _, _, _, val in vis], n, dl)
    model = [[0.0] * n for _ in range(n)]
    minor_cycle(r, model, beam, patch, 0.2, 0.0, 30)
    exact = dirty_from(vis, [val - p for (_, _, _, val), p in zip(vis, predict(model, vis, dl))], n, dl)
    l1 = sum(abs(x) for row in model for x in row)
    assert diff(r, exact) <= far * l1 + 1e-12
    assert diff(r, exact) > 1e-3


def test_major_cycles_remove_the_drift():
    n = 16
    sky, vis, dl = make_vis(1, n, 100, PAGE_SOURCES)
    q0 = misfit(vis, [[0.0] * n for _ in range(n)], dl)
    one, _, _, _ = cotton_schwab_clean(vis, n, dl, 3, gain=0.2, cycle_factor=0.0, max_major=1, max_minor=150)
    many, res, cycles, steps = cotton_schwab_clean(vis, n, dl, 3, gain=0.2, max_major=8, max_minor=150)
    q_one, q_many = misfit(vis, one, dl), misfit(vis, many, dl)
    assert cycles == 8 and len(steps) == 8
    assert q_many < 1e-3 * q0
    assert q_many < 0.01 * q_one
    exact = dirty_from(vis, [val - p for (_, _, _, val), p in zip(vis, predict(many, vis, dl))], n, dl)
    assert diff(res, exact) < 1e-12
    assert max_abs(res) < 0.01


def test_clark_cycle_factor_versus_minor_cycles_that_go_too_far():
    n = 16
    sky, vis, dl = make_vis(1, n, 100, PAGE_SOURCES)
    deep, _, _, _ = cotton_schwab_clean(vis, n, dl, 1, gain=0.2, cycle_factor=0.0, max_major=8, max_minor=150)
    clark, _, _, _ = cotton_schwab_clean(vis, n, dl, 1, gain=0.2, max_major=8, max_minor=150)
    assert abs(misfit(vis, deep, dl) - 1.036) < 1e-3
    assert misfit(vis, clark, dl) < 1e-3


def test_threshold_stops_before_any_cycle():
    n = 8
    sky, vis, dl = make_vis(2, n, 20, ((3, 3, 1.0),))
    model, res, cycles, steps = cotton_schwab_clean(vis, n, dl, 2, threshold=10.0)
    assert cycles == 0 and steps == []
    assert max_abs(model) == 0.0
