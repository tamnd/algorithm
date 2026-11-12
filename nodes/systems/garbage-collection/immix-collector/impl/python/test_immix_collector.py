# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/immix-collector/. The authors are listed in prov/2YV2TJ.jsonl.

import random

import pytest

from immix_collector import Immix, OutOfMemory


class Checked(Immix):
    """Immix that checks after every collection that no hole holds a byte of a live object."""

    def collect(self, defrag: bool = False) -> None:
        super().collect(defrag)
        live = sorted((a, a + o.size) for a, o in self.objects.items())
        for b in range(self.nblocks):
            base = b * self.block_size
            for s, e in self.holes(b):
                lo, hi = base + s * self.line, base + e * self.line
                assert all(hi <= a or end <= lo for a, end in live), "a live object lies in a recycled line"


def check_layout(h: Immix) -> None:
    spans = sorted((a, a + o.size) for a, o in h.objects.items())
    for (a, e), (b, _) in zip(spans, spans[1:]):
        assert e <= b, "two objects overlap"
    for a, e in spans:
        assert a // h.block_size == (e - 1) // h.block_size, "an object crosses a block"


class Shadow:
    """The same operations on a graph of identities, with no collector."""

    def __init__(self, registers: int) -> None:
        self.roots: list[int | None] = [None] * registers
        self.cells: dict[int, tuple[int, list[int | None]]] = {}
        self.next = 0

    def new(self, reg: int, size: int, nfields: int) -> None:
        self.cells[self.next] = (size, [None] * nfields)
        self.roots[reg] = self.next
        self.next += 1

    def load(self, dst: int, src: int, f: int) -> None:
        x = self.roots[src]
        if x is not None and f < len(self.cells[x][1]):
            self.roots[dst] = self.cells[x][1][f]

    def store(self, dst: int, f: int, src: int) -> None:
        x = self.roots[dst]
        if x is not None and f < len(self.cells[x][1]):
            self.cells[x][1][f] = self.roots[src]

    def move(self, dst: int, src: int) -> None:
        self.roots[dst] = self.roots[src]

    def logical_graph(self) -> tuple:
        seen: dict[int, tuple] = {}
        stack = [x for x in self.roots if x is not None]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            size, fields = self.cells[x]
            seen[x] = (size, tuple(fields))
            stack.extend(y for y in fields if y is not None)
        return tuple(self.roots), tuple(sorted(seen.items()))


def random_run(seed: int, defrag: bool, line: int, lpb: int, blocks: int, steps: int) -> Checked:
    rng = random.Random(seed)
    regs = 4
    h, s = Checked(blocks, regs, line=line, lines_per_block=lpb, headroom=1, defrag=defrag), Shadow(regs)
    big = h.block_size // 4
    for _ in range(steps):
        op = rng.random()
        r1, r2, f = rng.randrange(regs), rng.randrange(regs), rng.randrange(3)
        if op < 0.4:
            u = rng.random()
            size = rng.randint(1, line) if u < 0.7 else rng.randint(line + 1, big) if u < 0.97 else big
            nf = rng.randrange(4)
            try:
                h.new(r1, size, nf)
            except OutOfMemory:
                break
            s.new(r1, size, nf)
        elif op < 0.65:
            h.load(r1, r2, f)
            s.load(r1, r2, f)
        elif op < 0.85:
            h.store(r1, f, r2)
            s.store(r1, f, r2)
        elif op < 0.95:
            h.move(r1, r2)
            s.move(r1, r2)
        else:
            h.roots[r1] = s.roots[r1] = None
        check_layout(h)
        assert h.logical_graph() == s.logical_graph()
    return h


@pytest.mark.parametrize("defrag", [False, True])
@pytest.mark.parametrize("line,lpb,blocks,steps", [(16, 16, 12, 1500), (16, 16, 24, 3000), (128, 256, 4, 1500)])
def test_random_runs_keep_the_graph_and_never_reuse_a_live_line(defrag: bool, line: int, lpb: int, blocks: int,
                                                                 steps: int) -> None:
    collections = evacuated = 0
    for seed in range(12):
        h = random_run(seed, defrag, line, lpb, blocks, steps)
        collections += h.collections
        evacuated += h.evacuated
    assert collections >= 12 * 3
    if not defrag:
        assert evacuated == 0
    elif line == 128:
        assert evacuated > 100


def spill_heap(skip: bool) -> Immix:
    """A live object of 100 bytes at address 64 spills from line 0 into line 1."""
    h = Immix(2, 3, headroom=0, skip_next_line=skip)
    assert h.new(0, 64, 0) == 0
    assert h.new(1, 100, 0) == 64
    h.roots[0] = None
    h.collect()
    assert h.line_mark[:3] == [True, False, False]
    return h


def test_the_line_after_a_marked_line_is_skipped() -> None:
    h = spill_heap(skip=True)
    assert h.holes(0) == [(2, 256)]
    assert h.new(2, 64, 0) == 256
    check_layout(h)


def test_without_the_skip_a_live_object_is_overwritten() -> None:
    h = spill_heap(skip=False)
    assert h.holes(0) == [(1, 256)]
    assert h.new(2, 64, 0) == 128  # inside the live object at [64, 164)
    with pytest.raises(AssertionError):
        check_layout(h)


def test_a_medium_object_marks_all_its_lines() -> None:
    h = Immix(2, 2, headroom=0)
    h.new(0, 300, 0)  # [0, 300): lines 0, 1 and 2
    h.collect()
    assert h.line_mark[:4] == [True, True, True, False]
    assert h.holes(0)[0] == (4, 256)


def test_a_medium_object_that_does_not_fit_goes_to_an_overflow_block() -> None:
    h = Immix(3, 2, headroom=0)
    h.new(0, 16, 0)
    h.collect()  # line 0 is marked: block 0 is recyclable with one hole, lines 2 to 255
    assert list(h.recyclable) == [0] and list(h.free_blocks) == [1, 2]
    a = h.new(1, 100, 0)  # small: into the hole of block 0
    assert a == 2 * 128
    b = h.new(1, 1000, 0)  # medium: fits the rest of the hole
    assert b == a + 100
    h.cursor = h.limit - 50  # pretend the hole is almost full
    c = h.new(1, 500, 0)  # medium and does not fit: overflow block
    assert c == 1 * h.block_size


def fragmented(defrag_second: bool) -> tuple[Immix, int, int]:
    h = Immix(16, 2, line=16, lines_per_block=16, headroom=2)
    for i in range(160):  # 160 objects of one line fill 10 blocks; keep every fourth
        h.new(1, 16, 1)
        if i % 4 == 0:
            h.store(1, 0, 0)
            h.move(0, 1)
    h.roots[1] = None
    graph = h.logical_graph()
    h.collect()
    free_before = len(h.free_blocks)
    assert all(h.last_holes[b] == 4 for b in range(10))
    h.collect(defrag=defrag_second)
    assert h.logical_graph() == graph
    return h, free_before, len(h.free_blocks)


def test_defragmentation_frees_the_fragmented_blocks() -> None:
    h, before, after = fragmented(True)
    assert (before, after, h.evacuated) == (6, 13, 40)
    h2, before2, after2 = fragmented(False)
    assert (before2, after2, h2.evacuated) == (6, 6, 0)


def test_evacuation_is_opportunistic() -> None:
    # All 10 blocks are candidates but one free block holds only 16 copies; the rest stay in place.
    h = Immix(11, 2, line=16, lines_per_block=16, headroom=1)
    for i in range(160):
        h.new(1, 16, 1)
        if i % 4 == 0:
            h.store(1, 0, 0)
            h.move(0, 1)
    h.roots[1] = None
    graph = h.logical_graph()
    h.collect()
    assert list(h.free_blocks) == [10]
    h.candidates = lambda: set(range(10))
    h.collect(defrag=True)
    assert h.logical_graph() == graph
    assert h.evacuated == 16 and len(h.objects) == 40
    check_layout(h)
