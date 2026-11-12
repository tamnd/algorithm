# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-sweeping/. The authors are listed in prov/60PT1Y.jsonl.

import random

import pytest

from lazy_sweeping import LazyHeap


def reachable(fields: list[list[int | None]], roots: list[int | None]) -> set[int]:
    """Oracle: breadth-first search from the roots."""
    seen = {r for r in roots if r is not None}
    queue = list(seen)
    i = 0
    while i < len(queue):
        for y in fields[queue[i]]:
            if y is not None and y not in seen:
                seen.add(y)
                queue.append(y)
        i += 1
    return seen


def check_invariant(h: LazyHeap) -> None:
    live = reachable(h.fields, h.roots)
    assert len(h.free) == len(set(h.free))
    assert not live & set(h.free)
    for a in range(h.next_block * h.size, h.n):
        if not h.marked[a]:
            assert a not in live, "an unmarked cell in an unswept block must be garbage"
    for a in range(h.next_block * h.size):
        assert not h.marked[a], "a swept block holds no marks"


def test_example() -> None:
    h = LazyHeap(3, 2, 1)
    cells = [h.allocate() for _ in range(6)]
    assert cells == [0, 1, 2, 3, 4, 5]
    for a, b in [(0, 3), (3, 5), (1, 2), (2, 1)]:
        h.fields[a][0] = b
    h.fields[4][0] = None
    h.roots = [0]
    a = h.allocate()
    assert h.collections == 1 and h.next_block == 1
    assert a == 1 and h.free == [] and h.cells_swept == 2
    b = h.allocate()
    assert b == 2 and h.next_block == 2 and h.cells_swept == 4
    c = h.allocate()
    assert c == 4 and h.next_block == 3 and h.cells_swept == 6
    with pytest.raises(MemoryError):
        h.roots = [0, a, b, c]
        h.allocate()


def test_full_cycle_frees_exactly_the_unreachable_cells() -> None:
    rng = random.Random(1982)
    for _ in range(300):
        h = LazyHeap(rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 3))
        for a in range(h.n):
            h.fields[a] = [rng.choice([None, rng.randrange(h.n)]) for _ in range(h.k)]
        h.free = []
        h.roots = [rng.choice([None, rng.randrange(h.n)]) for _ in range(rng.randint(0, 3))]
        want = reachable(h.fields, h.roots)
        snapshot = {a: list(h.fields[a]) for a in want}
        h.collect()
        assert {a for a in range(h.n) if h.marked[a]} == want
        h.sweep_all()
        assert sorted(h.free) == sorted(set(range(h.n)) - want)
        assert all(h.fields[a] == snapshot[a] for a in want)
        assert not any(h.marked)


def test_random_mutator_never_gets_a_live_cell() -> None:
    rng = random.Random(1081)
    for _ in range(500):
        h = LazyHeap(rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 2))
        h.roots = [None] * rng.randint(1, 3)
        for _ in range(40):
            live = sorted(reachable(h.fields, h.roots))
            op = rng.random()
            if op < 0.4:
                try:
                    a = h.allocate()
                except MemoryError:
                    assert len(live) == h.n
                    continue
                assert a not in live
                h.roots[rng.randrange(len(h.roots))] = a
            elif op < 0.75 and live:
                x = rng.choice(live)
                h.fields[x][rng.randrange(h.k)] = rng.choice(live + [None])
            elif op < 0.92:
                h.roots[rng.randrange(len(h.roots))] = rng.choice(live + [None])
            else:
                h.collect()
            check_invariant(h)


class NoClearHeap(LazyHeap):
    """The pitfall: a new mark phase that keeps the stale marks of unswept blocks."""

    def collect(self) -> None:
        self.next_block = self.blocks
        super().collect()


def test_stale_marks_lose_a_live_cell() -> None:
    for cls, loses in ((LazyHeap, False), (NoClearHeap, True)):
        h = cls(2, 2, 1)
        assert [h.allocate() for _ in range(4)] == [0, 1, 2, 3]
        x = 2  # a cell of block 1, which stays unswept
        h.roots = [x]
        h.collect()
        y = h.allocate()  # sweeps block 0 only
        assert y in (0, 1) and h.next_block == 1 and h.marked[x]
        h.fields[x][0] = y
        h.collect()
        h.sweep_all()
        assert (y in h.free) == loses
