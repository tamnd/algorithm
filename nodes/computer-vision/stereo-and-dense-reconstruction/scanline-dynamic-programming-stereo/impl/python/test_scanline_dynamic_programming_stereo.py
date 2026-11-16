# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scanline-dynamic-programming-stereo/. The authors are listed in prov/ZQ13H8.jsonl.

import random

from scanline_dynamic_programming_stereo import (
    dp_stereo,
    is_valid_matching,
    matching_cost,
    scanline_dp,
)


def all_matchings(W, D):
    """Every matching of one row: strictly increasing pairs in the band."""
    out = []

    def grow(last_i, last_j, cur):
        out.append(list(cur))
        for i in range(last_i + 1, W):
            for j in range(max(last_j + 1, i - D + 1), i + 1):
                cur.append((i, j))
                grow(i, j, cur)
                cur.pop()

    grow(-1, -1, [])
    return out


def test_least_cost_equals_brute_force():
    rng = random.Random(1)
    for _ in range(400):
        W, D = rng.randint(1, 6), rng.randint(2, 4)
        lrow = [rng.randint(0, 9) for _ in range(W)]
        rrow = [rng.randint(0, 9) for _ in range(W)]
        kappa = rng.choice([0, 1, 2, 3, 5, 10])
        best, disp, pairs = scanline_dp(lrow, rrow, D, kappa)
        assert is_valid_matching(pairs, W, D)
        assert matching_cost(lrow, rrow, pairs, kappa) == best
        brute = min(matching_cost(lrow, rrow, m, kappa) for m in all_matchings(W, D))
        assert best == brute
        for (i, j) in pairs:
            assert disp[i] == i - j
        assert sum(d is not None for d in disp) == len(pairs)


def test_worked_example():
    lrow = [4, 5, 9, 1, 7, 7]
    rrow = [5, 9, 1, 7, 7, 3]
    best, disp, pairs = scanline_dp(lrow, rrow, 3, 2)
    assert best == 4
    assert disp == [None, 1, 1, 1, 1, 1]
    assert pairs == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)]


def make_pair(rng, W, H, dmap, noise=0):
    """Left rows of random texture; the right row shows, at each column j,
    the left pixel u with u - d(u) = j of the largest disparity (the
    nearest surface). Columns that no left pixel reaches get new texture.
    Returns (left, right, truth) where truth is None at left pixels that
    are hidden in the right image."""
    left, right, truth = [], [], []
    for v in range(H):
        lrow = [rng.randint(0, 255) for _ in range(W)]
        owner = [None] * W
        for u in range(W):
            j = u - dmap[v][u]
            if j >= 0 and (owner[j] is None or dmap[v][owner[j]] < dmap[v][u]):
                owner[j] = u
        rrow = [lrow[owner[j]] if owner[j] is not None else rng.randint(0, 255)
                for j in range(W)]
        rrow = [min(255, max(0, x + rng.randint(-noise, noise))) for x in rrow]
        t = [None] * W
        for j in range(W):
            if owner[j] is not None:
                t[owner[j]] = dmap[v][owner[j]]
        left.append(lrow)
        right.append(rrow)
        truth.append(t)
    return left, right, truth


def test_recovers_a_step_with_occlusion():
    rng = random.Random(7)
    W, H, D = 40, 6, 8
    dmap = [[2 if u < 18 else 6 for u in range(W)] for _ in range(H)]
    left, right, truth = make_pair(rng, W, H, dmap, noise=3)
    disp = dp_stereo(left, right, D, kappa=20)
    good = total = 0
    for v in range(H):
        for u in range(W):
            if truth[v][u] is not None:
                total += 1
                good += disp[v][u] == truth[v][u]
    assert good >= 0.95 * total


def test_rows_are_independent():
    rng = random.Random(3)
    left = [[rng.randint(0, 9) for _ in range(7)] for _ in range(3)]
    right = [[rng.randint(0, 9) for _ in range(7)] for _ in range(3)]
    disp = dp_stereo(left, right, 3, 2)
    for v in range(3):
        assert disp[v] == scanline_dp(left[v], right[v], 3, 2)[1]


def test_large_kappa_matches_everything_and_zero_kappa_matches_nothing():
    rng = random.Random(4)
    for _ in range(50):
        W = rng.randint(1, 8)
        lrow = [rng.randint(0, 9) for _ in range(W)]
        rrow = [rng.randint(0, 9) for _ in range(W)]
        _, disp, pairs = scanline_dp(lrow, rrow, 3, 100)
        assert len(pairs) == W and disp == [0] * W
        best, _, pairs = scanline_dp(lrow, rrow, 3, 0)
        assert best == 0
