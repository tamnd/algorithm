# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-heapsort/. The authors are listed in prov/KTRHK1.jsonl.

import itertools
import math
import random

from weak_heapsort import weak_heapsort


def worst(n: int) -> int:
    k = math.ceil(math.log2(n))
    return n * k - 2**k + n - k


def test_example() -> None:
    a = [5, 1, 4, 2, 8, 3, 7, 6]
    assert weak_heapsort(a) == 19
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def test_all_small_permutations() -> None:
    for n in range(2, 8):
        most = 0
        for p in itertools.permutations(range(n)):
            a = list(p)
            most = max(most, weak_heapsort(a))
            assert a == list(range(n))
        assert most == worst(n)


def test_bound_on_random_input() -> None:
    rng = random.Random(3)
    for n in (9, 100, 1000, 1500):
        a = [rng.randrange(n) for _ in range(n)]
        b = sorted(a)
        c = weak_heapsort(a)
        assert a == b
        assert c <= worst(n)
        assert c <= n * math.log2(n) + 0.087 * n


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [1, 2, 3]):
        b = list(a)
        weak_heapsort(b)
        assert b == sorted(a)
