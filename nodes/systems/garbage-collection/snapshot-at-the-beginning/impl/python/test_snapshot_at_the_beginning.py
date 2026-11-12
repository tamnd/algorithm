# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snapshot-at-the-beginning/. The authors are listed in prov/4TDCX9.jsonl.

import random

from snapshot_at_the_beginning import BARRIERS, BLACK, System, all_runs, reachable

# X = 0 points to Y = 1, and Y points to Z = 2. Register 0 holds X; register 2 stays None.
HEAP = {0: [1, None], 1: [2, None], 2: [None, None]}
REGS = [0, None, None]
# Copy Z into the black X, then cut the only gray path Y -> Z.
PROGRAM = [("load", 1, 0, 0), ("load", 1, 1, 0), ("store", 0, 1, 1),
           ("load", 1, 0, 0), ("store", 1, 0, 2), ("clear", 1)]


def test_lost_object_without_barrier() -> None:
    s = System(HEAP, REGS, PROGRAM, "none").run("CMMMMMM")
    assert s.lost == {2}


def test_same_schedule_with_satb() -> None:
    s = System(HEAP, REGS, PROGRAM, "satb").run("CMMMMMM")
    assert not s.lost and s.color[2] == BLACK


def test_exhaustive_interleavings() -> None:
    result = {}
    for b in BARRIERS:
        runs = list(all_runs(System(HEAP, REGS, PROGRAM, b)))
        result[b] = (len(runs), sum(1 for _, s in runs if s.lost))
    assert result["satb"][1] == 0 and result["dijkstra"][1] == 0
    assert result["none"][1] > 0


def random_program(rng: random.Random, regs: int, length: int) -> list[tuple]:
    prog = []
    for _ in range(length):
        kind = rng.choice(["load", "load", "store", "store", "clear", "alloc"])
        if kind == "load":
            prog.append(("load", rng.randrange(regs), rng.randrange(regs), rng.randrange(2)))
        elif kind == "store":
            prog.append(("store", rng.randrange(regs), rng.randrange(2), rng.randrange(regs)))
        else:
            prog.append((kind, rng.randrange(regs)))
    return prog


def random_case(rng: random.Random, n: int = 6, regs: int = 3, length: int = 12):
    heap = {x: [rng.choice([None, *range(n)]) for _ in range(2)] for x in range(n)}
    roots = [rng.choice([None, *range(n)]) for _ in range(regs)]
    return heap, roots, random_program(rng, regs, length)


def test_seeded_interleavings_keep_the_snapshot() -> None:
    rng = random.Random(7)
    failures = 0
    for _ in range(400):
        heap, roots, prog = random_case(rng)
        sched = "".join(rng.choice("MC") for _ in range(40))
        s = System(heap, roots, prog, "satb").run(sched)
        assert not s.lost and not s.used_freed
        new = set(range(len(heap), s.next_name))
        kept = set(s.fields)
        # exactly the objects reachable at the start, plus the new ones, survive
        assert kept == (s.snapshot | new) - (new & s.freed)
        assert not (new & s.freed)
        failures += bool(System(heap, roots, prog, "none").run(sched).lost)
    assert failures > 0


def test_satb_floats_at_least_as_much_as_incremental_update() -> None:
    rng = random.Random(5)
    total = {"satb": 0, "dijkstra": 0, "runs": 0}
    for _ in range(500):
        heap, roots, prog = random_case(rng)
        sched = "".join(rng.choice("MC") for _ in range(40))
        a = System(heap, roots, prog, "satb").run(sched)
        b = System(heap, roots, prog, "dijkstra").run(sched)
        assert set(b.fields) <= set(a.fields)
        if a.sweep_pc == b.sweep_pc:  # both sweeps see the same heap graph
            assert b.floating <= a.floating
            total["satb"] += a.floating
            total["dijkstra"] += b.floating
            total["runs"] += 1
    assert total == {"satb": 980, "dijkstra": 820, "runs": 443}


def test_no_final_rescan_needed() -> None:
    # A list hangs off X; the mutator takes its head into a register and unlinks it.
    heap = {0: [1, None], 1: [2, None], 2: [3, None], 3: [4, None], 4: [None, None]}
    prog = [("load", 1, 0, 0), ("store", 0, 0, 2)]
    a = System(heap, [0, None, None], prog, "satb").run("MMC")
    b = System(heap, [0, None, None], prog, "dijkstra").run("MMC")
    assert not a.lost and not b.lost
    assert a.remark_scans == 0 and b.remark_scans == 4
