# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-shift/. The authors are listed in prov/AN3FSZ.jsonl.

import math
import random

import pytest

from mean_shift import density, find_mode, mean_shift, shift


def mixture_1d(rng, n):
    centers = rng.sample([0.0, 3.0, 6.0, 10.0, 15.0], rng.randrange(1, 4))
    return [(rng.gauss(rng.choice(centers), rng.uniform(0.3, 1.0)),) for _ in range(n)]


def test_density_never_decreases():
    # Comaniciu and Meer (2002), Theorem 1: with a Gaussian kernel the density
    # along the sequence of mean shift points does not decrease.
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randrange(1, 25)
        pts = [(rng.gauss(0, 3), rng.gauss(0, 3)) for _ in range(n)]
        h = rng.uniform(0.3, 3)
        start = (rng.uniform(-8, 8), rng.uniform(-8, 8))
        trace = []
        find_mode(start, pts, h, tol=1e-9, max_iter=500, trace=trace)
        values = [density(y, pts, h) for y in trace]
        for a, b, ya, yb in zip(values, values[1:], trace, trace[1:]):
            assert b >= a - 1e-15
            # The proof gives the stronger bound f(y') - f(y) >= (G / h^2) |y' - y|^2,
            # where G is the sum of the weights g_i = exp(-|y - x_i|^2 / (2 h^2)) / 2.
            g = sum(math.exp(-((ya[0] - x[0]) ** 2 + (ya[1] - x[1]) ** 2) / (2 * h * h)) for x in pts) / 2
            step2 = (yb[0] - ya[0]) ** 2 + (yb[1] - ya[1]) ** 2
            assert b - a >= g / (h * h) * step2 / n - 1e-12


def test_shift_is_scaled_gradient():
    # m(y) = h^2 grad f(y) / f(y) for the Gaussian kernel.
    rng = random.Random(2)
    for _ in range(30):
        pts = [(rng.gauss(0, 2), rng.gauss(0, 2)) for _ in range(rng.randrange(1, 15))]
        h = rng.uniform(0.5, 2)
        y = (rng.uniform(-3, 3), rng.uniform(-3, 3))
        m = [a - b for a, b in zip(shift(y, pts, h), y)]
        e, f = 1e-6, density(y, pts, h)
        for k in range(2):
            up = tuple(y[i] + (e if i == k else 0) for i in range(2))
            down = tuple(y[i] - (e if i == k else 0) for i in range(2))
            grad = (density(up, pts, h) - density(down, pts, h)) / (2 * e)
            assert abs(m[k] - h * h * grad / f) < 1e-5 * (1 + abs(m[k]))


def grid_modes(pts, h, lo, hi, step):
    xs = [lo + i * step for i in range(int((hi - lo) / step) + 1)]
    fs = [density((x,), pts, h) for x in xs]
    return xs, fs


def grid_ascent(i, fs):
    """Walk to the higher neighbor on the grid until no neighbor is higher."""
    while True:
        best = i
        for j in (i - 1, i + 1):
            if 0 <= j < len(fs) and fs[j] > fs[best]:
                best = j
        if best == i:
            return i
        i = best


def test_modes_match_fine_grid_in_1d():
    rng = random.Random(3)
    checked = 0
    for _ in range(12):
        pts = mixture_1d(rng, rng.randrange(3, 25))
        h = rng.uniform(0.4, 1.5)
        lo, hi = min(p[0] for p in pts) - 1, max(p[0] for p in pts) + 1
        step = 0.002
        xs, fs = grid_modes(pts, h, lo, hi, step)
        labels, centers = mean_shift(pts, h, tol=1e-10)
        grid_end = [grid_ascent(round((p[0] - lo) / step), fs) for p in pts]
        minima = [i for i in range(1, len(fs) - 1) if fs[i] <= fs[i - 1] and fs[i] <= fs[i + 1]]
        safe = [j for j, p in enumerate(pts) if all(abs(p[0] - xs[i]) > 0.01 for i in minima)]
        for j in safe:
            mode = find_mode(pts[j], pts, h, tol=1e-10)
            assert abs(mode[0] - xs[grid_end[j]]) <= 2 * step
        for a in safe:
            for b in safe:
                assert (labels[a] == labels[b]) == (grid_end[a] == grid_end[b])
                checked += 1
        # The number of clusters is the number of grid maxima that some point reaches.
        if len(safe) == len(pts):
            assert len(centers) == len(set(grid_end))
    assert checked > 0


def test_iterates_stay_in_the_hull():
    rng = random.Random(4)
    pts = [(rng.uniform(0, 5),) for _ in range(20)]
    trace = []
    find_mode((40.0,), pts, 2.0, trace=trace)
    assert all(0 <= y[0] <= 5 for y in trace[1:])


def test_two_blobs():
    rng = random.Random(5)
    pts = [(rng.gauss(0, 0.5), rng.gauss(0, 0.5)) for _ in range(30)]
    pts += [(rng.gauss(6, 0.5), rng.gauss(0, 0.5)) for _ in range(30)]
    labels, centers = mean_shift(pts, 1.0)
    assert len(centers) == 2
    assert len(set(labels[:30])) == 1 and len(set(labels[30:])) == 1
    assert labels[0] != labels[30]


def test_example_of_the_page():
    pts = [(1.0,), (2.0,), (3.0,), (7.0,), (8.0,)]
    trace = []
    find_mode((1.0,), pts, 1.0, trace=trace)
    assert [round(y[0], 4) for y in trace[:5]] == [1.0, 1.5036, 1.7349, 1.8558, 1.9211]
    labels, centers = mean_shift(pts, 1.0)
    assert labels == [0, 0, 0, 1, 1]
    assert round(centers[0][0], 3) == 2.0 and round(centers[1][0], 3) == 7.5


def test_edges():
    assert mean_shift([], 1.0) == ([], [])
    labels, centers = mean_shift([(3.0, 4.0)], 1.0)
    assert labels == [0] and centers == [(3.0, 4.0)]
    with pytest.raises(ValueError):
        mean_shift([(0.0,)], 0)
