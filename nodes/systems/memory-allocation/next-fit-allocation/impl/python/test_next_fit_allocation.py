# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-fit-allocation/. The authors are listed in prov/EC8DYH.jsonl.

import random

import pytest

from next_fit_allocation import MIN_BLOCK, Heap, check, first_fit, next_fit, next_fit_malloc


class RefHeap:
    """Naive reference: [start, size, used] in address order and a rover address."""

    def __init__(self, H: int) -> None:
        self.b = [[0, H, 0]]
        self.rover = None

    def listed(self) -> list[int]:
        return [a for a, _, u in self.b if not u]

    @staticmethod
    def succ(fl: list[int], x: int) -> int | None:
        later = [a for a in fl if a > x]
        return later[0] if later else None

    def malloc(self, n: int) -> int | None:
        need = max(MIN_BLOCK, n + 2)
        fl = self.listed()
        if not fl:
            return None
        k = fl.index(self.rover) if self.rover is not None else 0
        size = {a: s for a, s, _ in self.b}
        order = fl[k:] + fl[:k]
        fit = [a for a in order if size[a] >= need]
        if not fit:
            return None
        a = fit[0]
        i = next(j for j, x in enumerate(self.b) if x[0] == a)
        s = self.b[i][1]
        if s - need >= MIN_BLOCK:
            self.b[i:i + 1] = [[a, need, 1], [a + need, s - need, 0]]
            self.rover = a + need
        else:
            self.b[i][2] = 1
            self.rover = self.succ(fl, a)
        return a + 1

    def free(self, p: int) -> None:
        i = next(k for k, x in enumerate(self.b) if x[0] == p - 1)
        fl = self.listed()  # the list before the freed block is linked
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
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    return h


def test_example_trace() -> None:
    got = []
    h = example_heap()
    for n in (6, 6, 2, 2):
        h.probes = 0
        p = next_fit_malloc(h, n)
        got.append((p, h.probes, h.rover, [(a, s) for a, s, u in check(h) if not u]))
    assert got == [
        (1, 1, 8, [(8, 4), (16, 8), (28, 16), (48, 16)]),
        (17, 2, 28, [(8, 4), (28, 16), (48, 16)]),
        (29, 1, 32, [(8, 4), (32, 12), (48, 16)]),
        (33, 1, 36, [(8, 4), (36, 8), (48, 16)]),
    ]
    h = example_heap()
    for n in (6, 6, 2, 2):
        h.malloc(n, first_fit)
    assert [(a, s) for a, s, u in check(h) if not u] == [(32, 12), (48, 16)]


def test_wraps_around() -> None:
    h = example_heap()
    assert next_fit_malloc(h, 14) == 29  # (28, 16) is used whole
    assert h.rover == 48  # its successor on the list
    h = example_heap()
    h.rover = 48
    assert next_fit_malloc(h, 6) == 49 and h.rover == 56
    h.probes = 0
    assert next_fit_malloc(h, 10) == 1  # (56, 8) is too small, wrap to (0, 12)
    assert h.probes == 2 and h.rover == 16


def test_failure_keeps_rover() -> None:
    h = example_heap()
    h.rover, h.probes = 28, 0
    assert next_fit_malloc(h, 20) is None and h.rover == 28
    assert h.probes == 4
    assert next_fit_malloc(Heap(4), 3) is None


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
            p = next_fit_malloc(h, n)
            assert p == r.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h) == r.blocks()
        assert (h.rover if h.rover >= 0 else None) == r.rover


def run_trace(pol, seed: int) -> tuple[int, int]:
    """Return (sum of the free-list lengths, total probes) on a seeded trace."""
    rng = random.Random(seed)
    trace = [rng.random() for _ in range(3000)]
    r = random.Random(5)
    h, live, total = Heap(1 << 14), [], 0
    for x in trace:
        if live and x < 0.5:
            h.free(live.pop(r.randrange(len(live))))
        else:
            p = h.malloc(r.randint(1, 64), pol)
            if p is not None:
                live.append(p)
        total += len(h.free_list())
    check(h)
    return total, h.probes


def test_next_fit_trades_probes_for_free_blocks() -> None:
    """The measured numbers of the page, on the trace with seed 3."""
    assert run_trace(first_fit, 3) == (27675, 7527)
    assert run_trace(next_fit, 3) == (35700, 1642)
