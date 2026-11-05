# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-quicksort/. The authors are listed in prov/X4M2NF.jsonl.

import math
import random

from parallel_quicksort import pack, parallel_quicksort


def test_example() -> None:
    out, _ = parallel_quicksort([5, 2, 8, 2, 9, 1, 5, 3], random.Random(1))
    assert out == [1, 2, 2, 3, 5, 5, 8, 9]


def test_pack() -> None:
    assert pack([5, 2, 8, 2, 9], [0, 1, 0, 1, 1]) == [2, 2, 9]
    assert pack([5, 2], [0, 0]) == []


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1, 1], [3, 2, 1], [1, 2, 3]):
        out, _ = parallel_quicksort(a)
        assert out == sorted(a)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(5)
    for _ in range(50):
        a = [Key(rng.randint(0, 5), i) for i in range(40)]
        out, _ = parallel_quicksort(a, rng)
        assert [(x.k, x.tag) for x in out] == sorted((x.k, x.tag) for x in a)


def test_depth_is_logarithmic() -> None:
    rng = random.Random(7)
    for n in (100, 1000, 10000):
        a = list(range(n))
        rng.shuffle(a)
        out, cost = parallel_quicksort(a, rng)
        assert out == sorted(a)
        k = math.ceil(math.log(n, 4 / 3)) + 1
        assert cost.depth <= 8 * k
        assert cost.work <= 5 * n * (cost.depth + 1) + 2 * n + 1


def test_sorted_and_all_equal_inputs() -> None:
    rng = random.Random(9)
    out, cost = parallel_quicksort([4] * 500, rng)
    assert out == [4] * 500 and cost.depth == 1
    out, _ = parallel_quicksort(list(range(2000)), rng)
    assert out == list(range(2000))


def test_random_against_sorted() -> None:
    rng = random.Random(11)
    for _ in range(300):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 80))]
        out, _ = parallel_quicksort(a, rng)
        assert out == sorted(a)
