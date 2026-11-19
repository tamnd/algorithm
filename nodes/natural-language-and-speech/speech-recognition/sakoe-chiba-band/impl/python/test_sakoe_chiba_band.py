# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sakoe-chiba-band/. The authors are listed in prov/HMGHCC.jsonl.

import random

import pytest

from sakoe_chiba_band import band_dtw, full_dtw


def all_paths(n, m):
    out = []

    def go(path):
        i, j = path[-1]
        if (i, j) == (n, m):
            out.append(list(path))
            return
        for di, dj in ((1, 1), (1, 0), (0, 1)):
            if i + di <= n and j + dj <= m:
                path.append((i + di, j + dj))
                go(path)
                path.pop()

    go([(1, 1)])
    return out


def cost(x, y, path):
    return sum(abs(x[i - 1] - y[j - 1]) for i, j in path)


def test_against_brute_force_inside_the_band():
    rng = random.Random(1)
    cache = {}
    for _ in range(200):
        n, m = rng.randint(1, 6), rng.randint(1, 6)
        r = rng.randint(abs(n - m), 5)
        x = [rng.randint(0, 9) for _ in range(n)]
        y = [rng.randint(0, 9) for _ in range(m)]
        if (n, m) not in cache:
            cache[(n, m)] = all_paths(n, m)
        inside = [p for p in cache[(n, m)] if all(abs(i - j) <= r for i, j in p)]
        c, path, _ = band_dtw(x, y, r)
        assert c == min(cost(x, y, p) for p in inside)
        assert path in inside and cost(x, y, path) == c


def test_wide_band_equals_full_dtw():
    rng = random.Random(2)
    for _ in range(100):
        x = [rng.randint(0, 9) for _ in range(rng.randint(1, 12))]
        y = [rng.randint(0, 9) for _ in range(rng.randint(1, 12))]
        r = max(len(x), len(y)) - 1
        assert band_dtw(x, y, r)[0] == full_dtw(x, y)


def test_band_misses_the_optimum():
    x, y = [0, 0, 0, 5], [0, 5, 5, 5]
    assert full_dtw(x, y) == 0
    assert band_dtw(x, y, 2)[0] == 0
    c1, path, _ = band_dtw(x, y, 1)
    assert c1 == 5 and path == [(1, 1), (2, 1), (3, 2), (4, 3), (4, 4)]
    assert band_dtw(x, y, 0)[0] == 10


def test_cost_does_not_increase_with_r():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(1, 10)
        x = [rng.randint(0, 9) for _ in range(n)]
        y = [rng.randint(0, 9) for _ in range(n)]
        costs = [band_dtw(x, y, r)[0] for r in range(n)]
        assert all(costs[k + 1] <= costs[k] for k in range(n - 1))
        assert costs[-1] == full_dtw(x, y)


def test_cells_filled():
    x = list(range(100))
    for r in (0, 1, 5, 10):
        _, _, cells = band_dtw(x, x, r)
        assert cells == sum(min(100, i + r) - max(1, i - r) + 1 for i in range(1, 101))
        assert cells <= 100 * (2 * r + 1)


def test_no_path_in_a_narrow_band():
    with pytest.raises(ValueError):
        band_dtw([1, 2, 3, 4], [1, 2], 1)
    assert band_dtw([1, 2, 3, 4], [1, 2], 2)[0] == full_dtw([1, 2, 3, 4], [1, 2])
