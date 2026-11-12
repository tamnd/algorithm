# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coalescing/. The authors are listed in prov/E7EWV1.jsonl.

import random

import pytest

from coalescing import NIL, Heap, NoMergeHeap, check, coalesce_all, first_fit


def lowest_fit(h: Heap, need: int) -> int:
    """The fitting free block of lowest address, for any list order."""
    best, a = NIL, h.head
    while a != NIL:
        if h.size(a) >= need and (best == NIL or a < best):
            best = a
        a = h.nxt(a)
    return best


def merged(bl):
    """Merge runs of adjacent free blocks in a block list, by address scan."""
    out = []
    for a, s, u in bl:
        if out and not u and not out[-1][2]:
            out[-1] = (out[-1][0], out[-1][1] + s, 0)
        else:
            out.append((a, s, u))
    return out


class Model:
    """A naive heap: a list of (start, size, used) blocks in address order."""

    def __init__(self, H: int, merge: bool) -> None:
        self.bl, self.merge = [(0, H, 0)], merge

    def malloc(self, n: int):
        need = max(4, n + 2)
        for i, (a, s, u) in enumerate(self.bl):
            if not u and s >= need:
                if s - need >= 4:
                    self.bl[i : i + 1] = [(a, need, 1), (a + need, s - need, 0)]
                else:
                    self.bl[i] = (a, s, 1)
                return a + 1
        return None

    def free(self, p: int) -> None:
        i = next(i for i, b in enumerate(self.bl) if b[0] == p - 1)
        self.bl[i] = (self.bl[i][0], self.bl[i][1], 0)
        if self.merge:
            self.bl = merged(self.bl)


def example(cls):
    h = cls(64)
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    return h, ps


def test_example_only_the_merging_heap_serves() -> None:
    for cls in (Heap, NoMergeHeap):
        h, ps = example(cls)
        assert [(a, h.size(a)) for a in h.free_list()] == [(0, 12), (16, 8), (28, 16), (48, 16)]
    h, ps = example(Heap)
    h.free(ps[1])  # (12, 4) joins (0, 12) and (16, 8)
    assert [(a, h.size(a)) for a in h.free_list()] == [(0, 24), (28, 16), (48, 16)]
    assert h.malloc(20, first_fit) == 1
    g, ps = example(NoMergeHeap)
    g.free(ps[1])
    assert [(a, g.size(a)) for a in g.free_list()] == [(0, 12), (12, 4), (16, 8), (28, 16), (48, 16)]
    assert g.malloc(20, first_fit) is None
    assert coalesce_all(g) == 2
    check(g)
    assert [(a, g.size(a)) for a in g.free_list()] == [(0, 24), (28, 16), (48, 16)]
    assert g.malloc(20, first_fit) == 1


def test_four_cases_of_free() -> None:
    def fresh():
        h = Heap(40)
        return h, [h.malloc(6, first_fit) for _ in range(5)]  # five blocks of 8

    h, ps = fresh()  # both neighbours used
    h.free(ps[2])
    assert check(h)[2] == (16, 8, 0)
    h, ps = fresh()  # upper neighbour free
    h.free(ps[3]); h.free(ps[2])
    assert check(h)[2] == (16, 16, 0)
    h, ps = fresh()  # lower neighbour free
    h.free(ps[1]); h.free(ps[2])
    assert check(h)[1] == (8, 16, 0)
    h, ps = fresh()  # both neighbours free
    h.free(ps[1]); h.free(ps[3]); h.free(ps[2])
    assert check(h)[1] == (8, 24, 0) and h.free_list() == [8]


def test_errors() -> None:
    h = Heap(16)
    p = h.malloc(2, first_fit)
    h.free(p)
    with pytest.raises(ValueError):
        h.free(p)


@pytest.mark.parametrize("order", ["addr", "lifo", "fifo"])
@pytest.mark.parametrize("seed", range(10))
def test_immediate_matches_model(order: str, seed: int) -> None:
    rng = random.Random(seed)
    H = rng.randint(4, 500)
    h, m, live = Heap(H, order), Model(H, True), []
    for _ in range(300):
        if live and rng.random() < 0.5:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            m.free(p)
        else:
            n = rng.randint(1, 40)
            p = h.malloc(n, lowest_fit)
            assert p == m.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h) == m.bl


@pytest.mark.parametrize("seed", range(10))
def test_sweep_matches_model(seed: int) -> None:
    rng = random.Random(seed)
    H = rng.randint(4, 500)
    h, m, live = NoMergeHeap(H), Model(H, False), []
    for step in range(300):
        if live and rng.random() < 0.5:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            m.free(p)
        else:
            n = rng.randint(1, 40)
            p = h.malloc(n, first_fit)
            assert p == m.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h, coalesced=False) == m.bl
        if step % 50 == 49:
            before = len(h.free_list())
            k = coalesce_all(h)
            m.bl = merged(m.bl)
            assert check(h) == m.bl and k == before - len(h.free_list())


def trace(cls, seed: int = 3):
    rng = random.Random(seed)
    h, live, fails, total = cls(1 << 12), [], 0, 0
    for _ in range(3000):
        if live and rng.random() < 0.5:
            h.free(live.pop(rng.randrange(len(live))))
        else:
            p = h.malloc(rng.randint(1, 64), first_fit)
            if p is None:
                fails += 1
            else:
                live.append(p)
        total += len(h.free_list())
    sizes = [h.size(a) for a in h.free_list()]
    return fails, total, h.probes, len(sizes), max(sizes), sum(sizes)


def test_trace_numbers() -> None:
    a = trace(Heap)
    b = trace(NoMergeHeap)
    assert a == (0, 25504, 6407, 18, 2171, 2761)
    assert b == (4, 464017, 128309, 259, 62, 2999)
