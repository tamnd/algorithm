# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-heap/. The authors are listed in prov/PDF2MC.jsonl.

import random

import pytest

from position_heap import PositionHeap


def occurrences(t: str, p: str) -> list[int]:
    return [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)]


def test_example() -> None:
    h = PositionHeap("abaabab")
    h.check_invariant()
    n = 7
    nodes = {}
    stack = [(0, "")]
    while stack:
        x, s = stack.pop()
        if x:
            nodes[s] = n - h.length[x]
        stack.extend((y, s + c) for c, y in h.children[x].items())
    assert nodes == {"a": 5, "aa": 2, "ab": 3, "aba": 0, "b": 6, "ba": 4, "baa": 1}
    assert h.search("ab") == [0, 3, 5]
    assert h.search("abab") == [3]
    assert h.search("b") == [1, 4, 6]
    assert h.search("bb") == []


def test_edges() -> None:
    h = PositionHeap()
    h.check_invariant()
    assert h.search("a") == []
    h = PositionHeap("aaaaa")
    h.check_invariant()
    assert max(h.depth) == 5
    assert h.search("aa") == [0, 1, 2, 3]
    assert h.search("aaaaaa") == []
    with pytest.raises(ValueError):
        h.search("")


def test_prepend_online() -> None:
    h = PositionHeap()
    t = ""
    for c in "mississippi"[::-1]:
        h.prepend(c)
        t = c + t
        h.check_invariant()
        assert h.text == t
        assert h.search("ss") == occurrences(t, "ss")


def test_random_against_scan() -> None:
    rng = random.Random(2011)
    for _ in range(600):
        t = "".join(rng.choice("ab" if rng.random() < 0.5 else "abc") for _ in range(rng.randint(0, 30)))
        h = PositionHeap(t)
        h.check_invariant()
        for _ in range(4):
            p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 5)))
            assert h.search(p) == occurrences(t, p)
