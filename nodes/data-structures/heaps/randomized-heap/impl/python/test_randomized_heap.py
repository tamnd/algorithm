# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-heap/. The authors are listed in prov/E1PH4P.jsonl.

import heapq
import math
import random

import pytest

from randomized_heap import Node, RandomizedHeap, meld


class Script:
    """A coin that follows a script: 'L' gives 0.0 (left), 'R' gives 0.9 (right)."""

    def __init__(self, flips: str) -> None:
        self.flips = list(flips)
        self.used = 0

    def random(self) -> float:
        self.used += 1
        return 0.0 if self.flips.pop(0) == "L" else 0.9


class Counting:
    """A seeded coin that counts its flips."""

    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)
        self.flips = 0

    def random(self) -> float:
        self.flips += 1
        return self.rng.random()


def tree(key: int, left: "Node[int] | None" = None, right: "Node[int] | None" = None) -> Node[int]:
    v = Node(key)
    v.left, v.right = left, right
    return v


def sh(v: "Node[int] | None") -> str:
    if v is None:
        return "-"
    if v.left is None and v.right is None:
        return str(v.key)
    return f"{v.key}({sh(v.left)}, {sh(v.right)})"


def test_example_meld() -> None:
    x = tree(2, tree(6), tree(4, tree(9)))
    y = tree(3, tree(5))
    coin = Script("RLR")
    r = meld(x, y, coin)
    assert sh(r) == "2(6, 3(4(9, 5), -))"
    assert coin.used == 3


def test_example_other_coins() -> None:
    x = tree(2, tree(6), tree(4, tree(9)))
    y = tree(3, tree(5))
    r = meld(x, y, Script("LR"))
    assert sh(r) == "2(3(5, 6), 4(9, -))"


def test_empty() -> None:
    h: RandomizedHeap[int] = RandomizedHeap(random.Random(1))
    assert meld(None, None, random.Random(1)) is None
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    h.insert(4)
    assert h.delete_min() == 4 and h.is_empty()


def test_expected_path_is_logarithmic() -> None:
    coin = Counting(5)
    h: RandomizedHeap[int] = RandomizedHeap(coin)
    n = 4096
    for k in range(n):
        h.insert(k)
    assert coin.flips / n <= math.log2(n + 1) + 2
    coin.flips = 0
    out = [h.delete_min() for _ in range(n)]
    assert out == list(range(n))
    assert coin.flips / n <= 2 * math.log2(n + 1) + 2


def test_random_against_heapq() -> None:
    rng = random.Random(1998)
    for _ in range(600):
        heaps = [RandomizedHeap[int](random.Random(rng.random())) for _ in range(3)]
        refs: list[list[int]] = [[] for _ in range(3)]
        for _ in range(rng.randrange(1, 60)):
            i = rng.randrange(3)
            op = rng.random()
            if op < 0.55:
                k = rng.randrange(-20, 20)
                heaps[i].insert(k)
                heapq.heappush(refs[i], k)
            elif op < 0.85:
                if refs[i]:
                    assert heaps[i].find_min() == refs[i][0]
                    assert heaps[i].delete_min() == heapq.heappop(refs[i])
            else:
                j = rng.randrange(3)
                if i != j:
                    heaps[i].meld(heaps[j])
                    refs[i] = refs[i] + refs[j]
                    heapq.heapify(refs[i])
                    refs[j] = []
            heaps[i].check_invariant()
            assert sorted(heaps[i].keys()) == sorted(refs[i])
