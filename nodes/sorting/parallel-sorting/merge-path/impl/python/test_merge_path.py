# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merge-path/. The authors are listed in prov/8R73CV.jsonl.

import random

import pytest

from merge_path import co_rank, merge_path, sequential_merge


A = [1, 4, 6, 9]
B = [2, 3, 7, 8, 10]


def test_example_co_ranks() -> None:
    assert [co_rank(k, A, B) for k in (0, 3, 6, 9)] == [(0, 0), (1, 2), (3, 3), (4, 5)]


def test_example() -> None:
    assert merge_path(A, B, 3) == [1, 2, 3, 4, 6, 7, 8, 9, 10]


def test_edges() -> None:
    assert merge_path([], [], 4) == []
    assert merge_path([1, 2], [], 3) == [1, 2]
    assert merge_path([], [1, 2], 5) == [1, 2]
    with pytest.raises(ValueError):
        merge_path([1], [2], 0)


def test_stable_ties() -> None:
    a = [(2, "a0"), (5, "a1")]
    b = [(2, "b0"), (5, "b1")]

    class K:
        def __init__(self, pair: tuple[int, str]) -> None:
            self.k, self.tag = pair

        def __lt__(self, other: "K") -> bool:
            return self.k < other.k

    ka, kb = [K(x) for x in a], [K(x) for x in b]
    for p in (1, 2, 3, 4):
        assert [x.tag for x in merge_path(ka, kb, p)] == ["a0", "b0", "a1", "b1"]


def test_co_rank_matches_merge_prefix() -> None:
    rng = random.Random(1)
    for _ in range(300):
        a = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 12)))
        b = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 12)))
        tagged = sequential_merge([(x, 0) for x in a], [(x, 1) for x in b])
        for k in range(len(a) + len(b) + 1):
            i, j = co_rank(k, a, b)
            assert i == sum(1 for _, src in tagged[:k] if src == 0)
            assert i + j == k


def test_random_against_sorted() -> None:
    rng = random.Random(2)
    for _ in range(300):
        a = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 40)))
        b = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 40)))
        assert merge_path(a, b, rng.randint(1, 10)) == sorted(a + b)
