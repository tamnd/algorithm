# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-fit-allocation/. The authors are listed in prov/DY2NDA.jsonl.

import random

import pytest

from best_fit_allocation import (
    MIN_BLOCK,
    Heap,
    IndexedHeap,
    best_fit,
    best_fit_malloc,
    check,
    first_fit,
)


class RefHeap:
    """Naive reference: [start, size, used] in address order."""

    def __init__(self, H: int) -> None:
        self.b = [[0, H, 0]]

    def malloc(self, n: int) -> int | None:
        need = max(MIN_BLOCK, n + 2)
        fits = [(s, a, i) for i, (a, s, u) in enumerate(self.b) if not u and s >= need]
        if not fits:
            return None
        s, a, i = min(fits)  # the smallest size, then the lowest address
        if s - need >= MIN_BLOCK:
            self.b[i:i + 1] = [[a, need, 1], [a + need, s - need, 0]]
        else:
            self.b[i][2] = 1
        return a + 1

    def free(self, p: int) -> None:
        i = next(k for k, x in enumerate(self.b) if x[0] == p - 1)
        self.b[i][2] = 0
        if i + 1 < len(self.b) and not self.b[i + 1][2]:
            self.b[i][1] += self.b.pop(i + 1)[1]
        if i > 0 and not self.b[i - 1][2]:
            self.b[i - 1][1] += self.b.pop(i)[1]

    def blocks(self) -> list[tuple[int, int, int]]:
        return [tuple(x) for x in self.b]


def example_heap(cls=Heap) -> Heap:
    h = cls(64)
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    return h


@pytest.mark.parametrize("cls", [Heap, IndexedHeap])
def test_example_trace(cls) -> None:
    h = example_heap(cls)
    got = []
    for n in (6, 2, 10, 12):
        p = best_fit_malloc(h, n)
        got.append((p, [(a, s) for a, s, u in check(h) if not u]))
    assert got == [
        (17, [(0, 12), (28, 16), (48, 16)]),
        (1, [(4, 8), (28, 16), (48, 16)]),
        (29, [(4, 8), (40, 4), (48, 16)]),
        (49, [(4, 8), (40, 4)]),
    ]


def test_probes_of_the_list_scan() -> None:
    h = example_heap()
    counts = []
    for n in (6, 2, 10, 12):
        h.probes = 0
        best_fit_malloc(h, n)
        counts.append(h.probes)
    assert counts == [2, 3, 3, 3]  # the first search stops at an exact fit


def test_edges() -> None:
    for cls in (Heap, IndexedHeap):
        h = cls(4)
        assert best_fit_malloc(h, 3) is None
        assert best_fit_malloc(h, 2) == 1 and h.head == -1
        assert best_fit_malloc(h, 1) is None
        h = cls(7)
        assert best_fit_malloc(h, 1) == 1 and check(h) == [(0, 7, 1)]


@pytest.mark.parametrize("seed", range(25))
def test_against_reference(seed: int) -> None:
    rng = random.Random(seed)
    H = rng.randint(4, 400)
    h, x, r = Heap(H), IndexedHeap(H), RefHeap(H)
    live: list[int] = []
    for _ in range(300):
        if live and rng.random() < 0.45:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            x.free(p)
            r.free(p)
        else:
            n = rng.randint(1, 40)
            p = best_fit_malloc(h, n)
            assert p == best_fit_malloc(x, n) == r.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h) == check(x) == r.blocks()


@pytest.mark.parametrize("order", ["lifo", "fifo"])
def test_other_list_orders(order: str) -> None:
    rng = random.Random(7)
    h, live = Heap(500, order), []
    for _ in range(400):
        if live and rng.random() < 0.45:
            h.free(live.pop(rng.randrange(len(live))))
        else:
            need = max(MIN_BLOCK, rng.randint(1, 40) + 2)
            fl = h.free_list()
            fits = [a for a in fl if h.size(a) >= need]
            want = min(fits, key=lambda a: h.size(a)) if fits else -1  # first smallest in list order
            assert best_fit(h, need) == want
            p = h.malloc(need - 2, best_fit)
            if p is not None:
                live.append(p)
        check(h)


def run_trace(cls, pol, seed: int) -> tuple[int, int]:
    """Return (sum of the free-list lengths, total probes) on a seeded trace."""
    rng = random.Random(seed)
    trace = [rng.random() for _ in range(3000)]
    r = random.Random(5)
    h, live, total = cls(1 << 14), [], 0
    for x in trace:
        if live and x < 0.5:
            h.free(live.pop(r.randrange(len(live))))
        else:
            p = pol(h, r.randint(1, 64))
            if p is not None:
                live.append(p)
        total += len(h.free_list())
    check(h)
    return total, h.probes


def test_measured_trace() -> None:
    """The measured numbers of the page, on the trace with seed 3."""
    assert run_trace(Heap, lambda h, n: h.malloc(n, first_fit), 3) == (27675, 7527)
    assert run_trace(Heap, best_fit_malloc, 3) == (21764, 10345)
    assert run_trace(IndexedHeap, best_fit_malloc, 3) == (21764, 4298)
