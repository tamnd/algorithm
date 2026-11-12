# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concurrent-garbage-collection/. The authors are listed in prov/0GJMF8.jsonl.

import random

import pytest

from concurrent_garbage_collection import Heap, all_runs, apply, run

# r0 holds A, A.f0 = B and B.f0 = Z. The mutator moves Z from B into A and
# drops every register copy of it: the classic lost-object program.
PROGRAM = [("load", 1, 0, 0), ("load", 2, 1, 0), ("store", 0, 1, 2),
           ("store", 1, 0, None), ("clear", 1), ("clear", 2)]


def lost_object_heap(**options) -> Heap:
    h = Heap(4, registers=3, **options)
    a, b, z = h.allocate(), h.allocate(), h.allocate()
    h.regs[0] = a
    h.write(a, 0, b)
    h.write(b, 0, z)
    return h


def test_every_interleaving_without_the_barrier() -> None:
    assert all_runs(lost_object_heap(card=1, barrier=False), PROGRAM) == (4978, 18)


@pytest.mark.parametrize("card,preclean,runs", [(1, True, 7147), (1, False, 4978), (2, True, 6531)])
def test_every_interleaving_with_the_card_barrier(card: int, preclean: bool, runs: int) -> None:
    assert all_runs(lost_object_heap(card=card, preclean=preclean), PROGRAM) == (runs, 0)


@pytest.mark.parametrize("seed", range(8))
def test_random_interleavings_free_no_reachable_cell(seed: int) -> None:
    h = Heap(48, registers=4, card=4, trigger=16)
    assert run(h, 16, 3000, random.Random(seed)) == 0
    assert h.cycles >= 10


def test_precleaning_shortens_the_remark() -> None:
    totals = {}
    for preclean in (True, False):
        pauses = []
        for seed in range(20):
            h = Heap(48, registers=4, card=4, trigger=16, preclean=preclean)
            assert run(h, 16, 3000, random.Random(seed)) == 0
            pauses += h.remark_pauses
        totals[preclean] = (len(pauses), sum(pauses), max(pauses))
    assert totals[True] == (296, 1184, 4)  # only the 4 roots are left to the pause
    assert totals[False] == (297, 1984, 12)


def test_a_slow_collector_falls_back_to_a_pause() -> None:
    failures = 0
    for seed in range(20):
        h = Heap(48, registers=4, card=4, trigger=16)
        assert run(h, 16, 3000, random.Random(seed), collector_share=0.15) == 0
        failures += h.failures
    assert failures == 483


def test_remark_finds_a_store_into_a_scanned_cell() -> None:
    h = lost_object_heap(card=1, preclean=False)
    a, b, z = 0, 1, 2
    h.initial_mark()
    h.collector_step()  # scan A: B is gray, Z is white
    assert h.marked[:3] == [True, True, False]
    for op in PROGRAM:
        apply(h, op)
    assert h.dirty[a] and h.dirty[b]
    while h.phase != "idle":
        h.collector_step()
    assert not h.is_free[z] and h.fields[a][1] == z
