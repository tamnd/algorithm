# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferred-coalescing/. The authors are listed in prov/26G2FC.jsonl.

import random

import pytest

from deferred_coalescing import NIL, Heap, QuickHeap, check, check_quick, first_fit


def lowest_fit(h: Heap, need: int) -> int:
    """The fitting free block of lowest address, for any list order."""
    best, a = NIL, h.head
    while a != NIL:
        if h.size(a) >= need and (best == NIL or a < best):
            best = a
        a = h.nxt(a)
    return best


class Model:
    """A naive heap: blocks [start, size, state] with state U, Q or F."""

    def __init__(self, H: int, Q: int) -> None:
        self.bl, self.Q, self.stack = [[0, H, "F"]], Q, {}

    def _merge(self) -> None:
        out = []
        for b in self.bl:
            if out and b[2] == "F" and out[-1][2] == "F":
                out[-1][1] += b[1]
            else:
                out.append(b)
        self.bl = out

    def _fit(self, need: int):
        for i, (a, s, st) in enumerate(self.bl):
            if st == "F" and s >= need:
                if s - need >= 4:
                    self.bl[i : i + 1] = [[a, need, "U"], [a + need, s - need, "F"]]
                else:
                    self.bl[i][2] = "U"
                return a + 1
        return None

    def malloc(self, n: int):
        need = max(4, n + 2)
        if self.stack.get(need):
            a = self.stack[need].pop()
            next(b for b in self.bl if b[0] == a)[2] = "U"
            return a + 1
        p = self._fit(need)
        if p is None and any(self.stack.values()):
            self.stack = {}
            for b in self.bl:
                if b[2] == "Q":
                    b[2] = "F"
            self._merge()
            p = self._fit(need)
        return p

    def free(self, p: int) -> None:
        b = next(b for b in self.bl if b[0] == p - 1)
        if b[1] <= self.Q:
            b[2] = "Q"
            self.stack.setdefault(b[1], []).append(b[0])
        else:
            b[2] = "F"
            self._merge()

    def view(self):
        return [(a, s, int(st != "F")) for a, s, st in self.bl]


def test_quick_hit_reuses_the_block() -> None:
    h = QuickHeap(64, 8)
    p = h.malloc(2, first_fit)  # needs 4 words
    q = h.malloc(10, first_fit)  # needs 12 words, above Q
    h.free(p)
    assert h.quick_blocks() == [0] and h.free_list() == [16]
    assert check_quick(h)[0] == (0, 4, 1)  # still tagged used
    assert h.malloc(2, first_fit) == p and h.hits == 1 and h.probes == 2
    h.free(q)  # above Q: merged at once with the free block above it
    assert [(a, h.size(a)) for a in h.free_list()] == [(4, 60)] and h.merges == 1


def test_consolidation_on_failure() -> None:
    h = QuickHeap(32, 8)
    ps = [h.malloc(2, first_fit) for _ in range(8)]  # eight blocks of 4 words
    assert h.malloc(1, first_fit) is None  # the heap is full
    for p in ps:
        h.free(p)
    assert h.free_list() == [] and len(h.quick_blocks()) == 8
    assert h.malloc(20, first_fit) == 1  # needs 22: only a merged block fits
    assert h.consolidations == 1 and h.quick_blocks() == []
    assert check_quick(h) == [(0, 22, 1), (22, 10, 0)]


def test_errors() -> None:
    h = QuickHeap(32, 8)
    p = h.malloc(2, first_fit)
    h.free(p)
    with pytest.raises(ValueError):
        h.free(p)
    with pytest.raises(ValueError):
        h.malloc(0, first_fit)


@pytest.mark.parametrize("order", ["addr", "lifo", "fifo"])
@pytest.mark.parametrize("seed", range(10))
def test_matches_model(order: str, seed: int) -> None:
    rng = random.Random(seed)
    H, Q = rng.randint(4, 500), rng.choice((4, 8, 12, 16))
    h, m, live = QuickHeap(H, Q, order), Model(H, Q), []
    for _ in range(300):
        if live and rng.random() < 0.5:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            m.free(p)
        else:
            n = rng.choice((1, 2, 3, 6, 10)) if rng.random() < 0.8 else rng.randint(1, 60)
            p = h.malloc(n, lowest_fit)
            assert p == m.malloc(n)
            if p is not None:
                live.append(p)
        assert check_quick(h) == m.view()
        assert sorted(h.quick_blocks()) == sorted(a for a, _, st in m.bl if st == "Q")
    h.consolidate()
    bl = check(h)
    assert all(u or v for (_, _, u), (_, _, v) in zip(bl, bl[1:]))


def trace(h: Heap, seed: int = 3):
    rng = random.Random(seed)
    live, fails = [], 0
    for _ in range(3000):
        if live and rng.random() < 0.5:
            h.free(live.pop(rng.randrange(len(live))))
        else:
            if rng.random() < 0.9:
                n = rng.choice((2, 2, 4, 6, 6, 14))
            else:
                n = rng.randint(32, 400)
            p = h.malloc(n, first_fit)
            if p is None:
                fails += 1
            else:
                live.append(p)
    return fails, h.probes, h.merges, getattr(h, "hits", 0), getattr(h, "consolidations", 0)


def test_trace_numbers() -> None:
    assert trace(Heap(1 << 12)) == (0, 2818, 991, 0, 0)
    assert trace(QuickHeap(1 << 12, 16)) == (0, 376, 126, 1317, 0)
    assert trace(Heap(1 << 10)) == (31, 3135, 950, 0, 0)
    assert trace(QuickHeap(1 << 10, 16)) == (32, 1485, 240, 1126, 27)
