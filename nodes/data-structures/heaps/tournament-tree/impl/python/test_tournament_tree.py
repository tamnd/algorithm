# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-tree/. The authors are listed in prov/A58YZQ.jsonl.

import heapq
import random

import pytest

from tournament_tree import LoserTree, WinnerTree, k_way_merge, tournament_sort

KEYS = [31, 4, 15, 92, 65, 35, 89, 7]


def test_example_winner_tree() -> None:
    w = WinnerTree(KEYS)
    w.check_invariant()
    assert w.t[1:8] == [1, 1, 7, 1, 2, 5, 7]
    assert w.winner() == 1
    w.update(1, None)
    w.check_invariant()
    assert w.t[1:8] == [7, 2, 7, 0, 2, 5, 7]
    assert w.winner() == 7


def test_example_loser_tree() -> None:
    lt = LoserTree(KEYS)
    lt.check_invariant()
    assert lt.l == [1, 7, 2, 5, 0, 3, 4, 6]
    lt.comparisons = 0
    lt.update(1, 50)
    assert lt.l == [7, 2, 0, 5, 1, 3, 4, 6]
    assert lt.comparisons == 3
    lt.check_invariant()


def test_example_merge() -> None:
    runs = [[2, 9, 15], [5, 6], [1, 7, 20], [3, 4, 30]]
    assert list(k_way_merge(runs)) == [1, 2, 3, 4, 5, 6, 7, 9, 15, 20, 30]


def test_edge_cases() -> None:
    with pytest.raises(ValueError):
        WinnerTree([])
    with pytest.raises(ValueError):
        LoserTree([])
    w = WinnerTree([5])
    assert w.winner() == 0
    w.update(0, 2)
    assert w.winner() == 0
    assert list(k_way_merge([])) == []
    assert list(k_way_merge([[], [], []])) == []
    assert list(k_way_merge([[1, 1], [1]])) == [1, 1, 1]
    assert tournament_sort([]) == []
    w5 = WinnerTree([8, 3, 6, 1, 5])
    w5.check_invariant()
    assert w5.winner() == 3


def test_ties_go_to_smaller_index() -> None:
    w = WinnerTree([4, 2, 2, 9, 2])
    assert w.winner() == 1
    lt = LoserTree([4, 2, 2, 9, 2])
    assert lt.winner() == 1


def test_random_winner_tree_updates() -> None:
    rng = random.Random(7)
    for _ in range(600):
        k = rng.randrange(1, 17)
        keys: list[int | None] = [rng.randrange(-9, 9) for _ in range(k)]
        w = WinnerTree(keys)
        for _ in range(rng.randrange(1, 20)):
            i = rng.randrange(k)
            new = None if rng.random() < 0.2 else rng.randrange(-9, 9)
            keys[i] = new
            w.update(i, new)
            w.check_invariant()
            live = [(x, j) for j, x in enumerate(keys) if x is not None]
            if live:
                assert w.winner() == min(live)[1]


def test_random_merge_and_sort() -> None:
    rng = random.Random(11)
    for _ in range(600):
        k = rng.randrange(1, 9)
        runs = [sorted(rng.randrange(0, 50) for _ in range(rng.randrange(0, 8))) for _ in range(k)]
        assert list(k_way_merge(runs)) == list(heapq.merge(*runs))
        data = [rng.randrange(-20, 20) for _ in range(rng.randrange(0, 30))]
        assert tournament_sort(data) == sorted(data)


def test_loser_tree_replay_cost() -> None:
    rng = random.Random(3)
    for k in (2, 3, 5, 8, 13, 16):
        lt = LoserTree([rng.randrange(100) for _ in range(k)])
        for _ in range(50):
            i = lt.winner()
            lt.comparisons = 0
            lt.update(i, rng.randrange(100))
            depth = (k + i).bit_length() - 1
            assert lt.comparisons == depth
            lt.check_invariant()
