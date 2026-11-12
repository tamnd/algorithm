# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/worst-fit/. The authors are listed in prov/VRPHKK.jsonl.

import random

import pytest

from worst_fit import MIN_BLOCK, Heap, best_fit, check, first_fit, worst_fit, worst_fit_malloc


class RefHeap:
    """Naive reference: [start, size, used] in address order."""

    def __init__(self, H: int) -> None:
        self.b = [[0, H, 0]]

    def malloc(self, n: int) -> int | None:
        need = max(MIN_BLOCK, n + 2)
        fits = [(-s, a, i) for i, (a, s, u) in enumerate(self.b) if not u and s >= need]
        if not fits:
            return None
        s, a, i = min(fits)  # the largest size, then the lowest address
        s = -s
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


def example_heap() -> Heap:
    h = Heap(64)
    ps = [h.malloc(n, first_fit) for n in (10, 2, 6, 2, 14, 2)]
    for p in ps[0::2]:
        h.free(p)
    return h


def test_example_trace() -> None:
    h = example_heap()
    got = []
    for n in (6, 2, 10, 12):
        h.probes = 0
        p = worst_fit_malloc(h, n)
        got.append((p, h.probes, [(a, s) for a, s, u in check(h) if not u]))
    assert got == [
        (29, 4, [(0, 12), (16, 8), (36, 8), (48, 16)]),
        (49, 4, [(0, 12), (16, 8), (36, 8), (52, 12)]),
        (1, 4, [(16, 8), (36, 8), (52, 12)]),
        (None, 3, [(16, 8), (36, 8), (52, 12)]),
    ]


def two_holes() -> Heap:
    """H = 28: free (0, 8), used (8, 4), free (12, 12), used (24, 4)."""
    h = Heap(28)
    a = h.malloc(6, first_fit)
    h.malloc(2, first_fit)
    b = h.malloc(10, first_fit)
    h.malloc(2, first_fit)
    h.free(a)
    h.free(b)
    assert check(h) == [(0, 8, 0), (8, 4, 1), (12, 12, 0), (24, 4, 1)]
    return h


def serve(pol, reqs: list[int]) -> list[int | None]:
    h = two_holes()
    out = []
    for n in reqs:
        out.append(h.malloc(n, pol))
        check(h)
    return out


def test_worst_fit_fails_where_best_fit_succeeds() -> None:
    # needs 4 then 12: worst fit splits the 12-word hole for the small request
    assert serve(best_fit, [2, 10]) == [1, 13]
    assert serve(worst_fit, [2, 10]) == [13, None]


def test_best_fit_fails_where_worst_fit_succeeds() -> None:
    # needs 4, 8, 8: best fit leaves two 4-word remainders
    assert serve(best_fit, [2, 6, 6]) == [1, 13, None]
    assert serve(worst_fit, [2, 6, 6]) == [13, 1, 17]


def test_edges() -> None:
    h = Heap(4)
    assert worst_fit_malloc(h, 3) is None
    assert worst_fit_malloc(h, 2) == 1 and h.head == -1
    h = Heap(7)
    assert worst_fit_malloc(h, 1) == 1 and check(h) == [(0, 7, 1)]


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
            p = worst_fit_malloc(h, n)
            assert p == r.malloc(n)
            if p is not None:
                live.append(p)
        assert check(h) == r.blocks()


def run_trace(pol, seed: int) -> tuple[int, int, int, int]:
    """Return (sum of list lengths, probes, largest free, total free) on a seeded trace."""
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
    sizes = [h.size(a) for a in h.free_list()]
    return total, h.probes, max(sizes), sum(sizes)


def test_measured_trace() -> None:
    """The measured numbers of the page, on the trace with seed 3."""
    assert run_trace(first_fit, 3) == (27675, 7527, 13246, 14141)
    assert run_trace(best_fit, 3) == (21764, 10345, 13313, 14131)
    assert run_trace(worst_fit, 3) == (35880, 17974, 3151, 14159)
