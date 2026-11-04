# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rank-pairing-heap/. The authors are listed in prov/Q9AZES.jsonl.

import random
from typing import Optional

import pytest

from rank_pairing_heap import Node, RankPairingHeap, type2_rank


def show(x: Optional[Node[int]]) -> str:
    """Write a half tree as key:rank(left, right), with - for a missing child."""
    if x is None:
        return "-"
    s = f"{x.key}:{x.rank}"
    if x.left is None and x.right is None:
        return s
    return f"{s}({show(x.left)}, {show(x.right)})"


def dump(h: RankPairingHeap[int]) -> str:
    return "  ".join(show(r) for r in h.roots())


def test_page_example() -> None:
    h: RankPairingHeap[int] = RankPairingHeap()
    nodes = {k: h.insert(k) for k in range(10, 100, 10)}
    assert h.delete_min() == 10 and h.links == 7
    assert dump(h) == "20:3(60:2(80:1(90:0, 70:0), 40:1(50:0, 30:0)), -)"
    h.decrease_key(nodes[30], 25)
    assert dump(h) == "20:3(60:2(80:1(90:0, 70:0), 40:1(50:0, -)), -)  25:0"
    h.decrease_key(nodes[80], 75)
    assert dump(h) == "20:3(60:2(70:0, 40:1(50:0, -)), -)  25:0  75:1(90:0, -)"
    h.rank_steps = 0
    h.decrease_key(nodes[50], 45)
    assert h.rank_steps == 3
    assert dump(h) == "20:2(60:1(70:0, 40:0), -)  25:0  75:1(90:0, -)  45:0"
    h.check_invariant()
    h.links = 0
    assert h.delete_min() == 20 and h.links == 2
    assert dump(h) == "45:0  75:1(90:0, -)  25:2(60:1(70:0, 40:0), -)"
    h.check_invariant()


def test_type2_rank() -> None:
    assert type2_rank(None, None) == 0
    n0: Node[int] = Node(1)
    n3: Node[int] = Node(2)
    n3.rank = 3
    assert type2_rank(n0, None) == 1
    assert type2_rank(n3, n0) == 3
    n2: Node[int] = Node(3)
    n2.rank = 2
    assert type2_rank(n3, n2) == 4
    assert type2_rank(n2, n2) == 3


def test_edge_cases() -> None:
    h: RankPairingHeap[int] = RankPairingHeap()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    x = h.insert(5)
    h.decrease_key(x, 2)
    with pytest.raises(ValueError):
        h.decrease_key(x, 3)
    assert h.delete_min() == 2 and len(h) == 0
    h.check_invariant()


def test_meld() -> None:
    a: RankPairingHeap[int] = RankPairingHeap()
    b: RankPairingHeap[int] = RankPairingHeap()
    for k in [4, 8, 6]:
        a.insert(k)
    for k in [5, 1, 9]:
        b.insert(k)
    a.meld(b)
    a.check_invariant()
    assert len(b) == 0
    assert [a.delete_min() for _ in range(6)] == [1, 4, 5, 6, 8, 9]


def live(h: RankPairingHeap[int]) -> set[int]:
    seen: set[int] = set()
    for r in h.roots():
        stack = [r]
        while stack:
            v = stack.pop()
            seen.add(id(v))
            stack.extend(c for c in (v.left, v.right) if c is not None)
    return seen


def test_random_against_model() -> None:
    rng = random.Random(2011)
    for _ in range(600):
        h: RankPairingHeap[int] = RankPairingHeap()
        ref: dict[int, Node[int]] = {}
        for _ in range(rng.randrange(1, 80)):
            op = rng.random()
            if op < 0.45 or not ref:
                x = h.insert(rng.randrange(1000))
                ref[id(x)] = x
            elif op < 0.75:
                x = rng.choice(list(ref.values()))
                h.decrease_key(x, x.key - rng.randrange(0, 60))
            else:
                assert h.delete_min() == min(x.key for x in ref.values())
                alive = live(h)
                gone = [k for k in ref if k not in alive]
                assert len(gone) == 1
                del ref[gone[0]]
            h.check_invariant()
            assert len(h) == len(ref)
