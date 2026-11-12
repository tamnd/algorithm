# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-garbage-collector/. The authors are listed in prov/TPVW7Y.jsonl.

from z_garbage_collector import MARKED0, REMAPPED, Shadow, ZHeap, address, run


def strict(h: ZHeap, shadow: Shadow) -> None:
    for t in range(len(h.regs)):
        assert h.to_space_ok(t), "a mutator holds a bad pointer or a pointer to memory being moved"
    if all(h.idle):
        assert h.logical_graph() == shadow.logical_graph()


def test_random_interleavings_keep_the_to_space_invariant() -> None:
    cycles = copies = slow = 0
    for seed in range(40):
        h = run(seed, check=strict)
        cycles += h.cycles
        copies += h.mutator_copies
        slow += h.slow_paths
    # Random schedules rarely catch a mutator in front of the collector; the directed tests below do.
    assert cycles > 500 and slow > 100 and copies > 0


def test_one_mutator_and_a_busy_collector() -> None:
    for seed in range(20):
        run(seed, threads=1, gc_share=0.8, length=200, check=strict)


def test_without_the_load_barrier_the_mutator_sees_stale_pointers() -> None:
    bad = 0
    for seed in range(40):
        try:
            run(seed, barrier=False, check=strict)
        except (AssertionError, KeyError):
            bad += 1
    assert bad == 40


SETUP = [("new", 0, 1), ("new", 1, 0), ("store", 0, 0, 1), ("clear", 1)]
SETUP += [("new", 2, 0), ("clear", 2)] * 4  # four dead objects: page 0 is one third live


def at_relocation(program: list[tuple]) -> tuple[ZHeap, Shadow, object, object]:
    """Run the set-up, then the collector up to the end of the relocate-start pause."""
    h = ZHeap(8, 6, 1, 3)
    shadow = Shadow(1, 3)
    m, gc = h.mutator(0, SETUP + program, shadow), h.collector()
    for _ in SETUP:
        next(m)
    while h.phase != "relocate":
        next(gc)
    assert h.reloc == {0}
    return h, shadow, m, gc


def test_the_barrier_relocates_and_heals_the_field() -> None:
    h, shadow, m, gc = at_relocation([("load", 1, 0, 0), ("load", 2, 0, 0)])
    a = address(h.regs[0][0])
    assert h.memory[a].fields[0] & MARKED0  # stale color from the marking
    for _ in range(4):  # the first load: fast-path test, copy, install, heal
        next(m)
    assert h.slow_paths == 1 and h.mutator_copies == 1
    b = h.regs[0][1]
    assert b & REMAPPED and h.page(address(b)) not in h.reloc
    assert h.memory[a].fields[0] == b  # self-healed
    next(m)  # the second load takes the fast path
    assert h.slow_paths == 1 and h.regs[0][2] == b
    assert h.logical_graph() == shadow.logical_graph()


def test_the_collector_wins_the_race_and_the_mutator_uses_its_copy() -> None:
    h, shadow, m, gc = at_relocation([("load", 1, 0, 0)])
    next(m)  # load the stale pointer
    next(m)  # the mutator copies the object
    next(gc)  # the collector copies it too
    next(gc)  # and installs its copy first
    next(m)  # the mutator's compare-and-swap fails
    next(m)
    assert h.lost_races == {"mutator": 1, "gc": 0}
    b = address(h.regs[0][1])
    assert h.page(b) == h.alloc_page["gc"]  # the collector's copy
    assert h.logical_graph() == shadow.logical_graph()


def test_the_mutator_wins_the_race() -> None:
    h, shadow, m, gc = at_relocation([("load", 1, 0, 0)])
    next(gc)  # the collector copies the object
    next(m)
    next(m)  # the mutator copies it too
    next(m)  # and installs its copy first
    next(gc)  # the collector's compare-and-swap fails
    next(m)
    assert h.lost_races == {"mutator": 0, "gc": 1}
    b = address(h.regs[0][1])
    assert h.page(b) == h.alloc_page["m0"]
    assert h.logical_graph() == shadow.logical_graph()


def test_a_late_mutator_finds_the_entry_after_relocation_ends() -> None:
    h, shadow, m, gc = at_relocation([("load", 1, 0, 0)])
    next(m)
    next(m)  # the mutator copies the object, then is not scheduled for a while
    while h.phase != "idle":
        next(gc)  # the collector copies everything and retires the forwarding table
    next(m)  # the late compare-and-swap must see the retired entry
    next(m)
    assert h.lost_races["mutator"] == 1 and h.mutator_copies == 0
    assert h.to_space_ok(0)
    assert h.logical_graph() == shadow.logical_graph()


def test_the_next_marking_remaps_and_frees_the_pages() -> None:
    h, shadow, m, gc = at_relocation([])
    while h.phase != "idle":
        next(gc)
    assert h.state[0] == "gone" and h.old_forwarding  # memory released, table kept
    while h.cycles < 2:
        next(gc)
    assert h.state[0] == "free" and not h.old_forwarding
    assert h.logical_graph() == shadow.logical_graph()
