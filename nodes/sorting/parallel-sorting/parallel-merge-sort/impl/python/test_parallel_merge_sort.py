# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-merge-sort/. The authors are listed in prov/J1JZCG.jsonl.

import math
import random

from parallel_merge_sort import p_merge, p_merge_sort


def test_example() -> None:
    a = [38, 27, 43, 3, 9, 82, 10]
    p_merge_sort(a)
    assert a == [3, 9, 10, 27, 38, 43, 82]


def test_merge_example() -> None:
    x, y = [3, 27, 38, 43], [9, 10, 82]
    z = [0] * 7
    p_merge(x, 0, 4, y, 0, 3, z, 0)
    assert z == [3, 9, 10, 27, 38, 43, 82]


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3]):
        b = list(a)
        p_merge_sort(b)
        assert b == sorted(a)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    a = [Key(2, "a"), Key(1, "b"), Key(2, "c"), Key(1, "d"), Key(2, "e"), Key(1, "f")]
    p_merge_sort(a)
    assert [x.tag for x in a] == ["b", "d", "f", "a", "c", "e"]


def test_merge_work_is_linear_and_span_polylog() -> None:
    rng = random.Random(3)
    for n in (1, 2, 5, 64, 1000, 4096):
        keys = sorted(rng.sample(range(10 * n + 10), 2 * n))
        x, y = keys[0::2], keys[1::2]
        z = [0] * (2 * n)
        work, span = p_merge(x, 0, n, y, 0, n, z, 0)
        assert z == keys
        big = 2 * n
        assert work <= 8 * big + 2
        assert span <= (math.log(big, 4 / 3) + 2) * (math.log2(big) + 2)


def test_random_against_sorted() -> None:
    rng = random.Random(11)
    for _ in range(300):
        a = [rng.randint(-30, 30) for _ in range(rng.randint(0, 70))]
        b = list(a)
        p_merge_sort(b)
        assert b == sorted(a)
