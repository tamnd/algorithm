# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c4-collector/. The authors are listed in prov/G25N97.jsonl.

from c4_collector import C4Heap, Shadow, address, nmt, run


def strict(h: C4Heap, shadow: Shadow) -> None:
    for t in range(len(h.regs)):
        assert h.to_space_ok(t), "a mutator holds a pointer that is not marked through or is protected"
    if all(h.idle):
        assert h.logical_graph() == shadow.logical_graph()


def test_random_interleavings_keep_the_invariant() -> None:
    cycles = copies = 0
    traps = {"nmt": 0, "protected": 0}
    for seed in range(40):
        h = run(seed, check=strict)
        cycles += h.cycles
        copies += h.mutator_copies
        for k in traps:
            traps[k] += h.traps[k]
    assert cycles > 500 and copies > 0
    assert traps["nmt"] > 100 and traps["protected"] > 50


def test_one_mutator_and_a_busy_collector() -> None:
    for seed in range(20):
        run(seed, threads=1, gc_share=0.8, length=200, check=strict)


def test_without_the_barrier_the_mutator_sees_stale_pointers() -> None:
    bad = 0
    for seed in range(40):
        try:
            run(seed, barrier=False, check=strict)
        except (AssertionError, KeyError):
            bad += 1
    assert bad == 40


SETUP = [("new", 0, 1), ("new", 1, 0), ("store", 0, 0, 1), ("clear", 1)]
SETUP += [("new", 2, 0), ("clear", 2)] * 4  # four dead objects: page 0 is one third live


def at_relocation(program: list[tuple]) -> tuple[C4Heap, Shadow, object, object]:
    """Run the set-up, then the collector up to the end of the relocation checkpoint."""
    h = C4Heap(8, 6, 1, 3)
    shadow = Shadow(1, 3)
    m, gc = h.mutator(0, SETUP + program, shadow), h.collector()
    for _ in SETUP:
        next(m)
    while h.phase != "relocate":
        next(gc)
    assert h.protected == {0}
    return h, shadow, m, gc


def test_the_trap_relocates_and_heals_the_field() -> None:
    h, shadow, m, gc = at_relocation([("load", 1, 0, 0), ("load", 2, 0, 0)])
    a = address(h.regs[0][0])
    assert h.page(address(h.memory[a].fields[0])) == 0  # the field points into a protected page
    for _ in range(4):  # the first load: test, copy, install, heal
        next(m)
    assert h.traps == {"nmt": 0, "protected": 1} and h.mutator_copies == 1
    b = h.regs[0][1]
    assert h.page(address(b)) not in h.protected and nmt(b) == h.expected
    assert h.memory[a].fields[0] == b  # self-healed
    next(m)  # the second load does not trap
    assert h.traps["protected"] == 1 and h.regs[0][2] == b
    assert h.logical_graph() == shadow.logical_graph()


def test_the_collector_wins_the_race() -> None:
    h, shadow, m, gc = at_relocation([("load", 1, 0, 0)])
    next(m)
    next(m)  # the mutator copies the object
    next(gc)  # the collector copies it too
    next(gc)  # and installs its copy first
    next(m)  # the mutator's compare-and-swap fails
    next(m)
    assert h.lost_races == {"mutator": 1, "gc": 0} and h.mutator_copies == 0
    assert h.page(address(h.regs[0][1])) == h.alloc_page["gc"]
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
    assert h.page(address(h.regs[0][1])) == h.alloc_page["m0"]
    assert h.logical_graph() == shadow.logical_graph()


def test_quick_release_and_remap_in_the_next_marking() -> None:
    h, shadow, m, gc = at_relocation([("load", 1, 0, 0)])
    while h.phase != "idle":
        next(gc)
    # Quick release: the memory of page 0 is gone, but the page stays protected and the forwarding data stay.
    assert h.state[0] == "released" and 0 in h.protected and h.forwarding
    assert not any(h.page(a) == 0 for a in h.memory)
    a = address(h.regs[0][0])
    stale = h.memory[a].fields[0]
    assert h.page(address(stale)) == 0  # nobody loaded it yet
    while not h.marking:
        next(gc)
    next(m)
    next(m)
    next(m)  # one trap remaps through the forwarding data and marks the object
    assert h.traps == {"nmt": 1, "protected": 1}
    b = address(h.regs[0][1])
    assert b in h.marked and h.memory[a].fields[0] == h.regs[0][1]
    while h.cycles < 2:
        next(gc)
    assert h.state[0] in ("free", "alloc", "used") and 0 not in h.protected
    assert h.logical_graph() == shadow.logical_graph()


def test_the_flip_makes_every_old_pointer_trap_once() -> None:
    h = C4Heap(8, 6, 1, 3)
    shadow = Shadow(1, 3)
    prog = [("new", 0, 1), ("new", 1, 0), ("store", 0, 0, 1), ("load", 2, 0, 0), ("load", 2, 0, 0), ("load", 2, 0, 0)]
    m, gc = h.mutator(0, prog, shadow), h.collector()
    for _ in range(3):
        next(m)
    next(gc)  # the checkpoint flips the expected NMT value
    assert h.marking and nmt(h.memory[address(h.regs[0][0])].fields[0]) != h.expected
    for _ in range(3):  # the first load traps, marks and heals
        next(m)
    next(m)
    next(m)  # the later loads do not trap
    assert h.traps == {"nmt": 1, "protected": 0}
    assert address(h.regs[0][2]) in h.marked or h.live_now(address(h.regs[0][2]))
    assert h.logical_graph() == shadow.logical_graph()
