# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timing-wheel/. The authors are listed in prov/GFWMKW.jsonl.

import heapq
import random

import pytest

from timing_wheel import HashedWheel, HierarchicalWheel


class HeapTimers:
    """Reference: a binary heap of (expiry, start number) with lazy deletion."""

    def __init__(self) -> None:
        self.now, self.count, self.heap, self.live = 0, 0, [], {}

    def start_timer(self, tid, interval: int) -> None:
        heapq.heappush(self.heap, (self.now + interval, self.count, tid))
        self.live[tid] = self.count
        self.count += 1

    def stop_timer(self, tid) -> bool:
        return self.live.pop(tid, None) is not None

    def tick(self) -> list:
        self.now += 1
        fired = []
        while self.heap and self.heap[0][0] <= self.now:
            e, c, tid = heapq.heappop(self.heap)
            if self.live.get(tid) == c:
                assert e == self.now
                del self.live[tid]
                fired.append(tid)
        return fired


def test_hashed_example() -> None:
    w = HashedWheel(8)
    w.start_timer("A", 3)
    w.start_timer("B", 11)
    w.start_timer("C", 8)
    w.start_timer("D", 5)
    assert w.buckets[3] == {"A": 0, "B": 1}
    assert w.buckets[0] == {"C": 0} and w.buckets[5] == {"D": 0}
    log = {}
    for t in range(1, 13):
        if t == 3:
            assert w.stop_timer("D")
        fired = w.tick()
        if fired:
            log[t] = fired
        if t == 3:
            assert w.buckets[3] == {"B": 0}  # A fired, B used one turn
    assert log == {3: ["A"], 8: ["C"], 11: ["B"]}
    assert len(w) == 0


def test_hierarchical_example() -> None:
    w = HierarchicalWheel(4, 3)  # base 4 digits, 64 ticks per top turn
    w.start_timer("X", 21)  # 21 = 1*16 + 1*4 + 1
    assert w.wheels[2][1] == {"X": True}
    fired = {}
    for t in range(1, 22):
        f = w.tick()
        if f:
            fired[t] = f
        if t == 16:
            assert w.wheels[1][1] == {"X": True}
        if t == 20:
            assert w.wheels[0][1] == {"X": True}
    assert fired == {21: ["X"]} and w.moves == 2


def run_against_heap(wheel, rng, steps, max_interval) -> int:
    ref = HeapTimers()
    nxt, running, total = 0, [], 0
    for _ in range(steps):
        for _ in range(rng.randrange(0, 4)):
            j = rng.randrange(1, max_interval + 1)
            wheel.start_timer(nxt, j)
            ref.start_timer(nxt, j)
            running.append(nxt)
            nxt += 1
        if running and rng.random() < 0.3:
            tid = running.pop(rng.randrange(len(running)))
            assert wheel.stop_timer(tid) == ref.stop_timer(tid)
        got, want = wheel.tick(), ref.tick()
        assert got == want  # same timers, at the same tick, in start order
        total += len(got)
        fired = set(got)
        running = [x for x in running if x not in fired]
        assert len(wheel) == len(ref.live)
    return total


def test_hashed_wheel_against_heap() -> None:
    rng = random.Random(1)
    for size in (1, 2, 7, 16):
        assert run_against_heap(HashedWheel(size), rng, 600, 50) > 0


def test_simple_wheel_has_no_rounds() -> None:
    # Scheme 4: the wheel is longer than every interval, so no timer waits
    # more than one turn, and every count is 0.
    rng = random.Random(2)
    w = HashedWheel(64)
    ref = HeapTimers()
    for t in range(500):
        j = rng.randrange(1, 64)
        w.start_timer(t, j)
        ref.start_timer(t, j)
        assert all(r == 0 for b in w.buckets for r in b.values())
        assert w.tick() == ref.tick()


def test_hierarchical_wheel_against_heap() -> None:
    rng = random.Random(3)
    for size, levels, top in ((2, 1, 9), (4, 3, 100), (3, 2, 40), (8, 2, 200)):
        assert run_against_heap(HierarchicalWheel(size, levels), rng, 700, top) > 0


def test_each_timer_moves_at_most_levels_times() -> None:
    # With intervals below size**levels, a timer is placed again at most once
    # from the overflow list and once per level above 0.
    rng = random.Random(4)
    w = HierarchicalWheel(4, 3)
    started = 0
    for _ in range(2000):
        if rng.random() < 0.5:
            w.start_timer(started, rng.randrange(1, 64))
            started += 1
        w.tick()
    while len(w):
        w.tick()
    assert w.moves <= 3 * started


def test_edges() -> None:
    w = HashedWheel(4)
    with pytest.raises(ValueError):
        w.start_timer("a", 0)
    w.start_timer("a", 1)
    with pytest.raises(ValueError):
        w.start_timer("a", 2)
    assert not w.stop_timer("zz")
    assert w.tick() == ["a"] and not w.stop_timer("a")
    with pytest.raises(ValueError):
        HashedWheel(0)
    h = HierarchicalWheel(2, 2)
    h.start_timer("b", 1000)  # far beyond one top turn of 4 ticks
    assert all(h.tick() == [] for _ in range(999)) and h.tick() == ["b"]
