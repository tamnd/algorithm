# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-filter-skyline/. The authors are listed in prov/6QMS6V.jsonl.

import random

import pytest

from sort_filter_skyline import dominates, entropy, sort_filter_skyline

# The example of the page: (price, distance) of hotels a to h.
HOTELS = [(5, 5), (4, 6), (6, 2), (3, 7), (5, 4), (2, 9), (7, 1), (6, 6)]


def brute_force(points):
    return {i for i, p in enumerate(points)
            if not any(dominates(q, p) for q in points)}


def names(idx):
    return ["abcdefgh"[i] for i in idx]


def test_example_sum() -> None:
    st = {}
    out = sort_filter_skyline(HOTELS, 2, sum, st)
    assert names(st["order"]) == ["c", "g", "e", "d", "b", "a", "f", "h"]
    assert names(out) == ["c", "g", "e", "d", "b", "f"]
    assert (st["passes"], st["writes"]) == (3, 7)


def test_example_entropy() -> None:
    st = {}
    out = sort_filter_skyline(HOTELS, 8, entropy, st)
    assert names(out) == ["g", "c", "e", "f", "d", "b"]
    assert st["passes"] == 1


def presort_is_topological(points, order):
    """No tuple is dominated by a tuple that comes later in the order."""
    return not any(dominates(points[order[b]], points[order[a]])
                   for a in range(len(order)) for b in range(a + 1, len(order)))


def test_random_against_brute_force_and_presort() -> None:
    rng = random.Random(6)
    for _ in range(1500):
        n, d = rng.randrange(0, 40), rng.randrange(1, 5)
        if rng.random() < 0.5:
            levels = rng.choice([2, 3, 10, 1000])
            pts = [tuple(rng.randrange(levels) for _ in range(d)) for _ in range(n)]
        else:
            pts = [tuple(rng.random() for _ in range(d)) for _ in range(n)]
        if rng.random() < 0.3 and pts:                   # add exact duplicates
            pts += [rng.choice(pts) for _ in range(rng.randrange(1, 5))]
        w = rng.randrange(1, 8)
        score = rng.choice([entropy, sum])
        st = {}
        out = sort_filter_skyline(pts, w, score, st)
        assert len(out) == len(set(out))
        sky = brute_force(pts)
        assert set(out) == sky
        assert presort_is_topological(pts, st["order"])
        assert st["comparisons"] <= len(pts) * (len(pts) - 1) // 2   # each pair meets once
        assert st["passes"] == -(-len(sky) // w)          # each pass but the last outputs w
        if pts:
            assert out[0] == st["order"][0]               # the first tuple is output at once
        if w >= len(pts):                                 # one pass: output in presorted order
            assert st["passes"] <= 1
            assert out == [i for i in st["order"] if i in sky]


def test_rounded_score_ties() -> None:
    # 1e16 + 1 rounds to 1e16, so both sums are equal; the tie-break by the
    # tuple must still put the dominating tuple first.
    pts = [(1e16, 1.0), (1e16, 0.0)]
    assert sort_filter_skyline(pts, 1, sum) == [1]


def test_anticorrelated() -> None:
    pts = [(i, 100 - i) for i in range(100)]
    st = {}
    assert sorted(sort_filter_skyline(pts, 10, sum, st)) == list(range(100))
    assert st["passes"] == 10


def test_bad_window() -> None:
    with pytest.raises(ValueError):
        sort_filter_skyline(HOTELS, 0)
