# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-fit-allocation/. The authors are listed in prov/F9XWJQ.jsonl.

import random

import pytest

from first_fit_allocation import MIN_BLOCK, Heap, check, first_fit, first_fit_malloc


class RefHeap:
    """Naive reference: a Python list of [start, size, used] in address order."""

    def __init__(self, H: int) -> None:
        self.H = H
        self.b = [[0, H, 0]]

    def malloc(self, n: int) -> int | None:
        need = max(MIN_BLOCK, n + 2)
        for i, (a, s, u) in enumerate(self.b):  # lowest address that fits
            if not u and s >= need:
                if s - need >= MIN_BLOCK:
                    self.b[i:i + 1] = [[a, need, 1], [a + need, s - need, 0]]
                else:
                    self.b[i][2] = 1
                return a + 1
        return None

    def free(self, p: int) -> None:
        i = next(k for k, x in enumerate(self.b) if x[0] == p - 1)
        self.b[i][2] = 0
        if i + 1 < len(self.b) and not self.b[i + 1][2]:
            self.b[i][1] += self.b.pop(i + 1)[1]
        if i > 0 and not self.b[i - 1][2]:
            self.b[i - 1][1] += self.b.pop(i)[1]

    def blocks(self) -> list[tuple[int, int, int]]:
        return [tuple(x) for x in self.b]


def example_heap() -> Heap:
    h = Heap(64)
    ps = [first_fit_malloc(h, n) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    return h


def test_example_trace() -> None:
    h = example_heap()
    assert [(a, s) for a, s, u in check(h) if not u] == [(0, 12), (16, 8), (28, 16), (48, 16)]
    got = []
    for n in (6, 6, 2, 10):
        h.probes = 0
        got.append((first_fit_malloc(h, n), h.probes))
        check(h)
    assert got == [(1, 1), (17, 2), (9, 1), (29, 1)]
    assert [(a, s) for a, s, u in check(h) if not u] == [(40, 4), (48, 16)]
    h.free(17)  # merges with nothing: 12 and 24 hold live blocks
    assert [(a, s) for a, s, u in check(h) if not u] == [(16, 8), (40, 4), (48, 16)]
    h.free(29)  # merges with (40, 4) on its right
    assert [(a, s) for a, s, u in check(h) if not u] == [(16, 8), (28, 16), (48, 16)]


def test_edges() -> None:
    h = Heap(4)
    assert first_fit_malloc(h, 3) is None
    p = first_fit_malloc(h, 2)
    assert p == 1 and first_fit_malloc(h, 1) is None
    h.free(p)
    assert check(h) == [(0, 4, 0)]
    with pytest.raises(ValueError):
        h.free(p)
    with pytest.raises(ValueError):
        first_fit_malloc(h, 0)
    h = Heap(7)  # a remainder of 3 words is too small to split off
    assert first_fit_malloc(h, 2) == 1 and check(h) == [(0, 7, 1)]


@pytest.mark.parametrize("seed", range(25))
def test_against_reference(seed: int) -> None:
    rng = random.Random(seed)
    H = rng.randint(4, 400)
    h, r = Heap(H), RefHeap(H)
    live: list[int] = []
    for _ in range(300):
        if live and rng.random() < 0.45:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            r.free(p)
        else:
            n = rng.randint(1, 40)
            p = first_fit_malloc(h, n)
            assert p == r.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h) == r.blocks()


@pytest.mark.parametrize("order", ["lifo", "fifo"])
def test_other_list_orders(order: str) -> None:
    rng = random.Random(7)
    h = Heap(500, order)
    live: list[int] = []
    for _ in range(600):
        if live and rng.random() < 0.45:
            h.free(live.pop(rng.randrange(len(live))))
        else:
            n = rng.randint(1, 40)
            need = max(MIN_BLOCK, n + 2)
            fits = [a for a in h.free_list() if h.size(a) >= need]
            p = first_fit_malloc(h, n)
            assert p == (fits[0] + 1 if fits else None)
            if p is not None:
                live.append(p)
        check(h)
