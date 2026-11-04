# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-way-merge/. The authors are listed in prov/04PNZQ.jsonl.

import random

from k_way_merge import k_way_merge


def test_example() -> None:
    runs = [[3, 17, 25], [8, 9], [1, 12, 30], [4, 4, 20]]
    assert k_way_merge(runs) == [1, 3, 4, 4, 8, 9, 12, 17, 20, 25, 30]


def test_edges() -> None:
    assert k_way_merge([]) == []
    assert k_way_merge([[], [], []]) == []
    assert k_way_merge([[1, 2, 3]]) == [1, 2, 3]
    assert k_way_merge([[], [5], []]) == [5]
    assert k_way_merge([[2, 2], [2], [2, 2, 2]]) == [2] * 6
    assert k_way_merge([["b", "d"], ["a", "c"]]) == ["a", "b", "c", "d"]


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: tuple[int, int]) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(11)
    runs = []
    for i in range(6):
        ks = sorted(rng.randint(0, 3) for _ in range(rng.randint(0, 8)))
        runs.append([Key(k, (i, j)) for j, k in enumerate(ks)])
    out = k_way_merge(runs)
    flat = [x for r in runs for x in r]
    want = sorted(flat, key=lambda x: (x.k, x.tag))
    assert [x.tag for x in out] == [x.tag for x in want]


def test_random_against_sorted() -> None:
    rng = random.Random(2024)
    for _ in range(800):
        k = rng.randint(0, 12)
        runs = [sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 15))) for _ in range(k)]
        assert k_way_merge(runs) == sorted(x for r in runs for x in r)
