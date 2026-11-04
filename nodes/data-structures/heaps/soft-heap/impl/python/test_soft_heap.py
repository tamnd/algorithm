# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-heap/. The authors are listed in prov/C1G5PQ.jsonl.

import random
from collections import Counter

import pytest

from soft_heap import Node, SoftHeap


def show(v: Node[int]) -> str:
    """Write a node as ckey{items}(children)."""
    s = f"{v.ckey}{{{','.join(map(str, v.items))}}}"
    kids = [show(c) for c in (v.left, v.right) if c is not None]
    return s + ("(" + " ".join(kids) + ")" if kids else "")


def test_page_example() -> None:
    h: SoftHeap[int] = SoftHeap(t=2)
    assert [h.size(k) for k in range(7)] == [1, 1, 1, 2, 3, 5, 8]
    for k in [5, 3, 8, 1, 7, 2, 6, 4, 9]:
        h.insert(k)
    assert [show(r) for r in h.roots] == ["2{1,2}(4{4}(6{6} 7{7}) 3{3}(5{5} 8{8}))", "9{9}"]
    assert h.corrupted() == 1 and h.links == 7
    out = []
    for _ in range(4):
        out.append((h.delete_min(), [show(r) for r in h.roots]))
        h.check_invariant()
    assert out == [
        ((2, 2), ["3{1,3}(5{5}(8{8}) 4{4}(6{6} 7{7}))", "9{9}"]),
        ((3, 3), ["4{1,4}(6{6}(7{7}) 5{5}(8{8}))", "9{9}"]),
        ((4, 4), ["5{1,5}(8{8} 6{6}(7{7}))", "9{9}"]),
        ((5, 5), ["6{1,6}(7{7} 8{8})", "9{9}"]),
    ]
    rest = [h.delete_min() for _ in range(len(h))]
    assert rest == [(6, 6), (7, 7), (8, 8), (1, 8), (9, 9)]


def test_no_corruption_below_threshold() -> None:
    h: SoftHeap[int] = SoftHeap(eps=0.25)
    assert h.t == 7
    keys = list(range(100))
    random.Random(3).shuffle(keys)
    for k in keys:
        h.insert(k)
    assert h.corrupted() == 0
    assert [h.delete_min()[0] for _ in range(100)] == list(range(100))


def test_empty_and_errors() -> None:
    h: SoftHeap[int] = SoftHeap()
    with pytest.raises(IndexError):
        h.delete_min()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(ValueError):
        SoftHeap(eps=0)
    h.insert(4)
    assert h.find_min() == (4, 4)
    assert h.delete_min() == (4, 4) and len(h) == 0 and h.roots == []
    with pytest.raises(ValueError):
        h.meld(SoftHeap(t=1))


def test_meld() -> None:
    a: SoftHeap[int] = SoftHeap(t=1)
    b: SoftHeap[int] = SoftHeap(t=1)
    for k in range(0, 40, 2):
        a.insert(k)
    for k in range(1, 40, 2):
        b.insert(k)
    a.meld(b)
    a.check_invariant()
    assert len(b) == 0 and len(a) == 40 and a.inserts == 40
    got = [a.delete_min() for _ in range(40)]
    assert sorted(e for e, _ in got) == list(range(40))
    assert [c for _, c in got] == sorted(c for _, c in got)


def test_error_bound_large() -> None:
    rng = random.Random(5)
    for eps in [0.5, 0.25, 0.1]:
        h: SoftHeap[float] = SoftHeap(eps=eps)
        for _ in range(5000):
            h.insert(rng.random())
        assert h.corrupted() <= eps * h.inserts
        h.check_invariant()


def test_random_sequences() -> None:
    rng = random.Random(20001101)
    for case in range(600):
        t = rng.choice([0, 1, 2, 3, 6])
        h: SoftHeap[int] = SoftHeap(t=t)
        present: Counter[int] = Counter()
        for _ in range(rng.randint(1, 150)):
            if rng.random() < 0.6 or not len(h):
                k = rng.randint(0, 300)
                h.insert(k)
                present[k] += 1
            elif rng.random() < 0.1:
                other: SoftHeap[int] = SoftHeap(t=t)
                for _ in range(rng.randint(0, 20)):
                    k = rng.randint(0, 300)
                    other.insert(k)
                    present[k] += 1
                h.meld(other)
            else:
                cur = min(v.ckey for v in h.nodes() if v.items)
                assert h.find_min()[1] == cur
                e, c = h.delete_min()
                assert c == cur and e <= c and present[e] > 0
                present[e] -= 1
            if case % 5 == 0:
                h.check_invariant()
        h.check_invariant()
        rest = [h.delete_min() for _ in range(len(h))]
        assert [c for _, c in rest] == sorted(c for _, c in rest)
        assert Counter(e for e, _ in rest) == +present
