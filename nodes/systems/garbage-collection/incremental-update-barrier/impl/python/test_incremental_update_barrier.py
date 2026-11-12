# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-update-barrier/. The authors are listed in prov/PCHTN8.jsonl.

import random

from incremental_update_barrier import BARRIERS, System, all_runs, reachable

# X = 0 points to Y = 1, and Y points to Z = 2. Register 0 holds X; register 2 stays None.
HEAP = {0: [1, None], 1: [2, None], 2: [None, None]}
REGS = [0, None, None]
# Copy Z into the black X, then cut the only gray path Y -> Z.
PROGRAM = [("load", 1, 0, 0), ("load", 1, 1, 0), ("store", 0, 1, 1),
           ("load", 1, 0, 0), ("store", 1, 0, 2), ("clear", 1)]


def test_lost_object_without_barrier() -> None:
    s = System(HEAP, REGS, PROGRAM, "none").run("CMMMMMM")
    assert s.lost == {2}
    assert s.fields[0][1] == 2  # X still points to the freed Z


def test_same_schedule_with_barriers() -> None:
    for b in ("dijkstra", "steele"):
        s = System(HEAP, REGS, PROGRAM, b).run("CMMMMMM")
        assert s.lost == set() and 2 not in s.freed


def test_exhaustive_interleavings() -> None:
    counts = {}
    for b in BARRIERS:
        runs = list(all_runs(System(HEAP, REGS, PROGRAM, b)))
        bad = [sched for sched, s in runs if s.lost]
        counts[b] = (len(runs), len(bad))
        if b != "none":
            assert not bad
            assert all(not s.used_freed for _, s in runs)
    assert counts["none"] == (207, 9)
    assert counts["dijkstra"] == (210, 0)


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


def random_heap(rng: random.Random, n: int) -> dict[int, list[int | None]]:
    return {x: [rng.choice([None, *range(n)]) for _ in range(2)] for x in range(n)}


def test_seeded_interleavings_never_free_a_reachable_object() -> None:
    rng = random.Random(7)
    failures = 0
    for _ in range(400):
        heap = random_heap(rng, 6)
        regs = [rng.choice([None, *range(6)]) for _ in range(3)]
        prog = random_program(rng, 3, 12)
        sched = "".join(rng.choice("MC") for _ in range(40))
        for b in ("dijkstra", "steele"):
            s = System(heap, regs, prog, b).run(sched)
            assert not s.lost and not s.used_freed
            assert set(s.fields) >= reachable(s.fields, s.regs)
        failures += bool(System(heap, regs, prog, "none").run(sched).lost)
    assert failures > 0


def test_garbage_at_start_is_freed() -> None:
    rng = random.Random(11)
    for _ in range(300):
        heap = random_heap(rng, 7)
        regs = [rng.choice([None, *range(7)]) for _ in range(3)]
        dead = set(heap) - reachable(heap, regs)
        prog = random_program(rng, 3, 10)
        sched = "".join(rng.choice("MC") for _ in range(30))
        for b in ("dijkstra", "steele"):
            assert dead <= System(heap, regs, prog, b).run(sched).freed


def test_no_mutator_means_exact_marking() -> None:
    rng = random.Random(3)
    for _ in range(200):
        heap = random_heap(rng, 8)
        regs = [rng.choice([None, *range(8)]) for _ in range(2)]
        s = System(heap, regs, [], "dijkstra").run("")
        assert set(s.fields) == reachable(heap, regs)
        assert s.floating == 0
