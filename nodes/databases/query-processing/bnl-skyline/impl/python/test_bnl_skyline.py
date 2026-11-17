# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bnl-skyline/. The authors are listed in prov/E97Y5D.jsonl.

import random

import pytest

from bnl_skyline import bnl_skyline, dominates

# The example of the page: (price, distance) of hotels a to h.
HOTELS = [(5, 5), (4, 6), (6, 2), (3, 7), (5, 4), (2, 9), (7, 1), (6, 6)]


def brute_force(points):
    return {i for i, p in enumerate(points)
            if not any(dominates(q, p) for q in points)}


def test_dominates() -> None:
    assert dominates((1, 2), (1, 3))
    assert not dominates((1, 3), (1, 3))
    assert not dominates((1, 3), (2, 2))
    assert dominates((0,), (1,))


def test_example() -> None:
    st = {}
    order = bnl_skyline(HOTELS, 2, st)
    assert ["abcdefgh"[i] for i in order] == ["b", "e", "c", "f", "d", "g"]
    assert st["passes"] == 3 and st["writes"] == 6
    assert set(order) == brute_force(HOTELS)


def test_large_window_is_one_pass() -> None:
    st = {}
    assert sorted(bnl_skyline(HOTELS, 8, st)) == sorted(brute_force(HOTELS))
    assert st == {"passes": 1, "comparisons": st["comparisons"], "writes": 0}


def test_ties_and_duplicates() -> None:
    pts = [(1, 1), (1, 1), (0, 2), (2, 0), (1, 2), (0, 2), (2, 2)]
    for w in range(1, 8):
        out = bnl_skyline(pts, w)
        assert len(out) == len(set(out))
        assert set(out) == {0, 1, 2, 3, 5}


def test_random_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(1500):
        n, d = rng.randrange(0, 40), rng.randrange(1, 5)
        levels = rng.choice([2, 3, 10, 1000])
        pts = [tuple(rng.randrange(levels) for _ in range(d)) for _ in range(n)]
        if rng.random() < 0.3 and pts:                   # add exact duplicates
            pts += [rng.choice(pts) for _ in range(rng.randrange(1, 5))]
        w = rng.randrange(1, 8)
        st = {}
        out = bnl_skyline(pts, w, st)
        assert len(out) == len(set(out))
        assert set(out) == brute_force(pts)
        assert st["comparisons"] <= len(pts) * w * st["passes"]
        assert st["comparisons"] <= len(pts) * (len(pts) - 1) // 2   # each pair meets once


def test_anticorrelated_needs_many_passes() -> None:
    pts = [(i, 100 - i) for i in range(100)]             # all in the skyline
    st = {}
    assert sorted(bnl_skyline(pts, 10, st)) == list(range(100))
    assert st["passes"] == 10


def test_bad_window() -> None:
    with pytest.raises(ValueError):
        bnl_skyline(HOTELS, 0)
