# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-garbage-collection/. The authors are listed in prov/RV18E3.jsonl.

import random

import pytest

from incremental_garbage_collection import Heap, OutOfMemory, pacing_bound, run_mutator, run_queue


def test_bound_values() -> None:
    assert pacing_bound(16, 64, 4) == (20, True)
    assert pacing_bound(16, 64, 3) == (27, False)


@pytest.mark.parametrize("seed", range(6))
def test_paced_collector_never_runs_out(seed: int) -> None:
    live, size = 16, 64
    k = 4
    m, ok = pacing_bound(live, size, k)
    assert ok
    heap = Heap(size, registers=4, k=k, trigger=m)
    run_mutator(heap, live, 3000, random.Random(seed))
    assert heap.max_units <= k
    assert heap.cycles >= 5


def test_bound_holds_for_many_sizes() -> None:
    rng = random.Random(99)
    for _ in range(25):
        live = rng.randrange(4, 20)
        size = rng.randrange(2 * live, 6 * live)
        k = next(k for k in range(1, 100) if pacing_bound(live, size, k)[1])
        heap = Heap(size, registers=3, k=k, trigger=pacing_bound(live, size, k)[0])
        run_mutator(heap, live, 800, rng)
        assert heap.max_units <= k


def test_queue_workload_at_the_bound() -> None:
    # H = 48, L = 16, k = 4 gives m = 16 and H = L + 2m exactly.
    assert pacing_bound(16, 48, 4) == (16, True)
    heap = Heap(48, registers=2, k=4, trigger=16)
    run_queue(heap, 16, 3000)
    assert heap.cycles == 175 and heap.max_units == 4
    # k = 3 breaks the sufficient condition but still survives this workload.
    heap = Heap(48, registers=2, k=3, trigger=pacing_bound(16, 48, 3)[0])
    run_queue(heap, 16, 3000)
    # k = 2 runs out of memory in the second cycle.
    heap = Heap(48, registers=2, k=2, trigger=pacing_bound(16, 48, 2)[0])
    with pytest.raises(OutOfMemory):
        run_queue(heap, 16, 3000)
    assert heap.cycles == 2


def test_too_small_a_tax_can_run_out() -> None:
    failures = 0
    for seed in range(20):
        heap = Heap(64, registers=4, k=1, trigger=4)
        try:
            run_mutator(heap, 16, 3000, random.Random(seed))
        except OutOfMemory:
            failures += 1
    assert failures > 0


def test_cycle_frees_exactly_the_garbage_at_its_start() -> None:
    heap = Heap(8, registers=2, k=100, trigger=0)
    a, b, c = heap.allocate(), heap.allocate(), heap.allocate()
    heap.regs[0] = a
    heap.write(a, 0, b)  # a -> b, and c is garbage
    heap.begin_cycle()
    heap.collect_work(100)
    assert heap.phase == "idle"
    assert heap.is_free[c] and not heap.is_free[a] and not heap.is_free[b]
    assert not any(heap.marked)
