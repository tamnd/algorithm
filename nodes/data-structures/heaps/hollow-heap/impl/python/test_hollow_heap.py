# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hollow-heap/. The authors are listed in prov/AQJK5W.jsonl.

import heapq
import random

import pytest

from hollow_heap import HollowHeap, Node, _children


def show(x: Node) -> str:
    s = f"{x.item.value if x.item else 'H'}{x.key}/r{x.rank}"
    ch = _children(x)
    return s + ("[" + " ".join(show(c) for c in ch) + "]" if ch else "")


def test_example() -> None:
    h: HollowHeap[int, str] = HollowHeap()
    it = {v: h.insert(v, k) for v, k in [("a", 5), ("b", 3), ("c", 8), ("d", 6), ("e", 7)]}
    assert show(h.root) == "b3/r0[e7/r0 d6/r0 c8/r0 a5/r0]"
    h.decrease_key(it["c"], 1)
    assert show(h.root) == "c1/r0[b3/r0[e7/r0 d6/r0 H8/r0 a5/r0] H8/r0]"
    h.decrease_key(it["e"], 2)
    assert show(h.root) == "c1/r0[e2/r0[H7/r0] b3/r0[H7/r0 d6/r0 H8/r0 a5/r0] H8/r0]"
    h.check_invariant()
    assert h.delete_min() == ("c", 1)
    assert show(h.root) == "e2/r1[b3/r0[H7/r0 d6/r0 H8/r0 a5/r0] H7/r0]"
    assert h.delete_min() == ("e", 2)
    assert show(h.root) == "b3/r0[H7/r0 d6/r0 H8/r0 a5/r0]"
    assert h.delete_min() == ("b", 3)
    assert show(h.root) == "a5/r1[d6/r0]"
    h.check_invariant()
    assert len(h) == 2


def test_empty_and_errors() -> None:
    h: HollowHeap[int, int] = HollowHeap()
    h.check_invariant()
    with pytest.raises(IndexError):
        h.find_min()
    with pytest.raises(IndexError):
        h.delete_min()
    e = h.insert(1, 10)
    with pytest.raises(ValueError):
        h.decrease_key(e, 11)
    h.decrease_key(e, 4)
    assert h.find_min() == (1, 4)
    h.delete(e)
    with pytest.raises(KeyError):
        h.delete(e)
    with pytest.raises(KeyError):
        h.decrease_key(e, 0)
    assert len(h) == 0


def test_meld() -> None:
    a: HollowHeap[int, int] = HollowHeap()
    b: HollowHeap[int, int] = HollowHeap()
    for k in [9, 4, 7]:
        a.insert(k, k)
    for k in [8, 2, 6]:
        b.insert(k, k)
    a.meld(b)
    assert len(a) == 6 and len(b) == 0
    a.check_invariant()
    assert [a.delete_min()[1] for _ in range(6)] == [2, 4, 6, 7, 8, 9]


def test_sort() -> None:
    rng = random.Random(7)
    keys = [rng.randrange(1000) for _ in range(300)]
    h: HollowHeap[int, int] = HollowHeap()
    for i, k in enumerate(keys):
        h.insert(i, k)
    out = [h.delete_min()[1] for _ in keys]
    assert out == sorted(keys)


def test_random_against_model() -> None:
    rng = random.Random(2015)
    for _ in range(600):
        h: HollowHeap[int, int] = HollowHeap()
        model: dict[int, int] = {}
        items = {}
        nxt = 0
        for _ in range(rng.randrange(1, 50)):
            op = rng.randrange(5)
            if op <= 1 or not model:
                k = rng.randrange(40)
                items[nxt] = h.insert(nxt, k)
                model[nxt] = k
                nxt += 1
            elif op == 2:
                v, k = h.delete_min()
                assert k == min(model.values())
                assert model.pop(v) == k
            elif op == 3:
                v = rng.choice(sorted(model))
                k = rng.randrange(model[v] + 1)
                h.decrease_key(items[v], k)
                model[v] = k
            else:
                v = rng.choice(sorted(model))
                h.delete(items[v])
                del model[v]
            h.check_invariant()
            assert len(h) == len(model)
            if model:
                assert h.find_min()[1] == min(model.values())


def test_dijkstra_pattern() -> None:
    rng = random.Random(3)
    n = 60
    adj = [[(rng.randrange(n), rng.randrange(1, 20)) for _ in range(4)] for _ in range(n)]
    ref = [float("inf")] * n
    ref[0] = 0
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > ref[u]:
            continue
        for v, w in adj[u]:
            if d + w < ref[v]:
                ref[v] = d + w
                heapq.heappush(pq, (d + w, v))
    dist = [float("inf")] * n
    dist[0] = 0
    h: HollowHeap[float, int] = HollowHeap()
    handle = {0: h.insert(0, 0)}
    done = set()
    while len(h):
        u, d = h.delete_min()
        done.add(u)
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                if v in handle and handle[v].node is not None:
                    h.decrease_key(handle[v], d + w)
                else:
                    handle[v] = h.insert(v, d + w)
    assert dist == ref
