# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shenandoah-collector/. The authors are listed in prov/1QJAF8.jsonl.

import pytest

from shenandoah_collector import Shadow, ShenandoahHeap, run


def strict(h: ShenandoahHeap, shadow: Shadow) -> None:
    for t in range(len(h.regs)):
        assert h.to_space_ok(t), "a register points into the collection set, or to freed memory"
    assert h.from_space_writes == 0, "a write went to an object that is being moved"
    if all(h.idle):
        assert h.logical_graph() == shadow.logical_graph()


@pytest.mark.parametrize("mode", ["lrb", "brooks"])
def test_random_interleavings_keep_the_graph(mode: str) -> None:
    cycles = 0
    for seed in range(40):
        cycles += run(seed, mode=mode, check=strict).cycles
    assert cycles > 600


@pytest.mark.parametrize("mode", ["lrb", "brooks"])
def test_one_mutator_and_a_busy_collector(mode: str) -> None:
    for seed in range(20):
        run(seed, mode=mode, threads=1, gc_share=0.8, length=200, check=strict)


@pytest.mark.parametrize("mode, least", [("lrb", 30), ("brooks", 15)])
def test_without_the_barriers_runs_break(mode: str, least: int) -> None:
    bad = 0
    for seed in range(40):
        try:
            run(seed, mode=mode, barrier=False, check=strict)
        except (AssertionError, KeyError):
            bad += 1
    assert bad >= least


SETUP = [("new", 0, 1), ("new", 1, 1), ("store", 0, 0, 1), ("clear", 1)]
SETUP += [("new", 2, 0), ("clear", 2)] * 4  # four dead objects: region 0 is one third live


def at_evacuation(mode: str, program: list[tuple], barrier: bool = True):
    """Run the set-up, then the collector up to the end of the Final Mark pause."""
    h = ShenandoahHeap(8, 6, 1, 3, mode=mode, barrier=barrier)
    shadow = Shadow(1, 3)
    m, gc = h.mutator(0, SETUP + program, shadow), h.collector()
    for _ in SETUP:
        next(m)
    while h.phase != "evac":
        next(gc)
    assert h.cset == {0}
    assert not h.in_cset(h.regs[0][0])  # the pause evacuated the root object A
    return h, shadow, m, gc


def test_lrb_evacuates_and_heals_the_field() -> None:
    h, shadow, m, gc = at_evacuation("lrb", [("load", 1, 0, 0), ("load", 2, 0, 0)])
    a = h.regs[0][0]
    assert h.in_cset(h.memory[a].fields[0])  # A's copy still points to B in from-space
    for _ in range(4):  # read, copy, CAS on the forwarding pointer, heal
        next(m)
    b = h.regs[0][1]
    assert h.mutator_copies == 1 and not h.in_cset(b)
    assert h.memory[a].fields[0] == b  # healed
    next(m)  # the second load finds a to-space pointer
    assert h.mutator_copies == 1 and h.regs[0][2] == b
    assert h.logical_graph() == shadow.logical_graph()


def test_lrb_the_collector_wins_the_race() -> None:
    h, shadow, m, gc = at_evacuation("lrb", [("load", 1, 0, 0)])
    next(m)
    next(m)  # the mutator copies B
    next(gc)  # the collector copies B too
    next(gc)  # and installs its forwarding pointer first
    next(m)  # the mutator's CAS fails
    next(m)
    assert h.lost_races == {"mutator": 1, "gc": 0} and h.mutator_copies == 0
    assert h.region(h.regs[0][1]) == h.alloc_region["gc"]
    assert h.logical_graph() == shadow.logical_graph()


def test_lrb_the_mutator_wins_the_race() -> None:
    h, shadow, m, gc = at_evacuation("lrb", [("load", 1, 0, 0)])
    next(gc)  # the collector copies B
    next(m)
    next(m)  # the mutator copies B too
    next(m)  # and installs its forwarding pointer first
    next(gc)  # the collector's CAS fails
    next(m)
    assert h.lost_races == {"mutator": 0, "gc": 1} and h.mutator_copies == 1
    assert h.region(h.regs[0][1]) == h.alloc_region["m0"]
    assert h.logical_graph() == shadow.logical_graph()


def brooks_write(barrier: bool):
    """The mutator loads a from-space pointer to B, then writes into B while it is moved."""
    h, shadow, m, gc = at_evacuation("brooks", [("load", 1, 0, 0), ("store", 1, 0, 0)], barrier)
    next(gc)
    next(gc)  # the collector copies B and installs the forwarding pointer
    next(m)  # load: Brooks lets the register hold the from-space address
    b = h.regs[0][1]
    assert h.in_cset(b) and h.memory[b].fwd is not None
    next(m)  # the store begins
    while not h.idle[0]:
        next(m)
    return h, shadow, gc, b


def test_brooks_writes_go_to_the_copy() -> None:
    h, shadow, gc, b = brooks_write(True)
    assert h.memory[b].fields[0] is None  # from-space is untouched
    assert h.memory[h.fwd(b)].fields[0] is not None
    assert h.from_space_writes == 0
    while h.cycles < 1:
        next(gc)
    assert not h.in_cset(h.regs[0][1]) and h.regs[0][1] in h.memory  # the final pause fixed the root
    assert h.logical_graph() == shadow.logical_graph()


def test_brooks_without_the_write_barrier_loses_the_write() -> None:
    h, shadow, gc, b = brooks_write(False)
    assert h.from_space_writes == 1
    assert h.memory[b].fields[0] is not None and h.memory[h.fwd(b)].fields[0] is None
    while h.cycles < 1:
        next(gc)
    assert h.logical_graph() != shadow.logical_graph()


def satb_case(barrier: bool) -> ShenandoahHeap:
    """A -> B. Marking starts; the mutator moves B into a register and cuts A.f before A is scanned."""
    h = ShenandoahHeap(8, 6, 1, 3, barrier=barrier)
    m = h.mutator(0, [("new", 0, 1), ("new", 1, 0), ("store", 0, 0, 1), ("clear", 1),
                      ("load", 2, 0, 0), ("store", 0, 0, 1)])
    for _ in range(4):
        next(m)
    gc = h.collector()
    while h.cycles < 1:
        next(gc)  # one whole cycle, so that A and B are old
    next(gc)  # the next Init Mark pause: A is a root
    assert h.phase == "mark" and h.stack and h.regs[0][1] is None
    next(m)  # register 2 = B
    next(m)  # A.f = nil
    while h.mark_step():
        pass
    return h


def test_the_satb_barrier_keeps_an_object_moved_into_a_register() -> None:
    h = satb_case(True)
    assert h.regs[0][2] in h.marked


def test_without_the_satb_barrier_marking_misses_it() -> None:
    h = satb_case(False)
    assert h.regs[0][2] not in h.marked
