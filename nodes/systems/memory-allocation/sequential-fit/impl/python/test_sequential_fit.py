# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-fit/. The authors are listed in prov/CY94WX.jsonl.

import random

import pytest

from sequential_fit import BEST, FIRST, MIN_BLOCK, NEXT, WORST, Heap, check, fit_malloc, sequential_fit

POLICIES = {"first": FIRST, "next": NEXT, "best": BEST, "worst": WORST}


class RefHeap:
    """Naive reference: [start, size, used] in address order, and a rover for next fit."""

    def __init__(self, H: int, name: str) -> None:
        self.b = [[0, H, 0]]
        self.name = name
        self.rover = None

    def free_starts(self) -> list[int]:
        return [a for a, _, u in self.b if not u]

    def succ(self, fl: list[int], x: int) -> int | None:
        later = [a for a in fl if a > x]
        return later[0] if later else None

    def choose(self, need: int) -> int | None:
        size = {a: s for a, s, _ in self.b}
        fl = self.free_starts()
        fits = [a for a in fl if size[a] >= need]
        if not fits:
            return None
        if self.name == "first":
            return fits[0]
        if self.name == "best":
            return min(fits, key=lambda a: (size[a], a))
        if self.name == "worst":
            return min(fits, key=lambda a: (-size[a], a))
        k = fl.index(self.rover) if self.rover is not None else 0
        return next(a for a in fl[k:] + fl[:k] if size[a] >= need)

    def malloc(self, n: int) -> int | None:
        need = max(MIN_BLOCK, n + 2)
        fl = self.free_starts()
        a = self.choose(need)
        if a is None:
            return None
        i = next(j for j, x in enumerate(self.b) if x[0] == a)
        s = self.b[i][1]
        if s - need >= MIN_BLOCK:
            self.b[i:i + 1] = [[a, need, 1], [a + need, s - need, 0]]
            if self.name == "next":
                self.rover = a + need
        else:
            self.b[i][2] = 1
            if self.name == "next":
                self.rover = self.succ(fl, a)
        return a + 1

    def free(self, p: int) -> None:
        i = next(k for k, x in enumerate(self.b) if x[0] == p - 1)
        fl = self.free_starts()
        self.b[i][2] = 0
        if i + 1 < len(self.b) and not self.b[i + 1][2]:
            u = self.b[i + 1][0]
            if self.rover == u:
                self.rover = self.succ(fl, u)
            fl.remove(u)
            self.b[i][1] += self.b.pop(i + 1)[1]
        if i > 0 and not self.b[i - 1][2]:
            low = self.b[i - 1][0]
            if self.rover == low:
                self.rover = self.succ(fl, low)
            self.b[i - 1][1] += self.b.pop(i)[1]

    def blocks(self) -> list[tuple[int, int, int]]:
        return [tuple(x) for x in self.b]


def example_heap() -> Heap:
    h = Heap(64)
    ps = [fit_malloc(h, n, FIRST) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    return h


def test_one_request_four_policies() -> None:
    """malloc(6) needs 8 words; free blocks (0, 12) (16, 8) (28, 16) (48, 16)."""
    got = {}
    for name, pol in POLICIES.items():
        h = example_heap()
        if name == "next":
            h.rover = 28
        got[name] = (fit_malloc(h, 6, pol), h.probes - 6)  # 6 probes were used to build the heap
        check(h)
    assert got == {"first": (1, 1), "next": (29, 1), "best": (17, 2), "worst": (29, 4)}


@pytest.mark.parametrize("name", list(POLICIES))
@pytest.mark.parametrize("seed", range(15))
def test_against_reference(name: str, seed: int) -> None:
    rng = random.Random(1000 * seed + len(name))
    H = rng.randint(4, 400)
    h, r = Heap(H), RefHeap(H, name)
    live: list[int] = []
    for _ in range(300):
        if live and rng.random() < 0.45:
            p = live.pop(rng.randrange(len(live)))
            h.free(p)
            r.free(p)
        else:
            n = rng.randint(1, 40)
            p = fit_malloc(h, n, POLICIES[name])
            assert p == r.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h) == r.blocks()
        if name == "next":
            assert (h.rover if h.rover >= 0 else None) == r.rover


@pytest.mark.parametrize("order", ["lifo", "fifo"])
def test_list_order_is_part_of_the_policy(order: str) -> None:
    rng = random.Random(11)
    h, live = Heap(600, order), []
    for _ in range(400):
        if live and rng.random() < 0.45:
            h.free(live.pop(rng.randrange(len(live))))
            continue
        need = max(MIN_BLOCK, rng.randint(1, 40) + 2)
        fl = h.free_list()
        fits = [a for a in fl if h.size(a) >= need]
        want = {
            "first": fits[0] if fits else -1,
            "best": min(fits, key=h.size) if fits else -1,
            "worst": max(fits, key=h.size) if fits else -1,
        }
        for name in want:
            assert sequential_fit(h, need, POLICIES[name]) == want[name]
        p = h.malloc(need - 2, lambda hh, nd: sequential_fit(hh, nd, FIRST))
        if p is not None:
            live.append(p)
        check(h)


def run_trace(pol, seed: int) -> tuple[int, int, int]:
    """Return (sum of list lengths, probes, largest free block at the end)."""
    rng = random.Random(seed)
    trace = [rng.random() for _ in range(3000)]
    r = random.Random(5)
    h, live, total = Heap(1 << 14), [], 0
    for x in trace:
        if live and x < 0.5:
            h.free(live.pop(r.randrange(len(live))))
        else:
            p = fit_malloc(h, r.randint(1, 64), pol)
            if p is not None:
                live.append(p)
        total += len(h.free_list())
    check(h)
    return total, h.probes, max(h.size(a) for a in h.free_list())


def test_measured_trace() -> None:
    """The table of the page, on the trace with seed 3 of the next-fit page."""
    assert run_trace(FIRST, 3) == (27675, 7527, 13246)
    assert run_trace(NEXT, 3) == (35700, 1642, 7095)
    assert run_trace(BEST, 3) == (21764, 10345, 13313)
    assert run_trace(WORST, 3) == (35880, 17974, 3151)
