# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hazard-pointers/. The authors are listed in prov/319C81.jsonl.

import random

from hazard_pointers import HazardPointers
from smr_sim import ImmediateFree, World, explore, run_random, run_schedule, setup, stall_peak, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
Q1 = [[("deq",)], [("deq",)]]


def hp(R: int = 1, validate: bool = True):
    return lambda m, n: HazardPointers(m, n, R=R, validate=validate)


def test_every_interleaving_is_safe_on_the_stack() -> None:
    for progs in (P2, PP):
        r = explore(setup(hp(), progs))
        assert r.violation is None and r.finals > 0


def test_every_interleaving_is_safe_on_the_queue() -> None:
    r = explore(setup(hp(), Q1, "queue"))
    assert r.violation is None and r.finals > 0


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for kind in ("stack", "queue"):
        make = setup(hp(R=2), workload(4, 10, kind), kind)
        assert run_random(make, range(150)).violation is None
        rng = random.Random(7)
        w = run_schedule(make, rng)
        assert w.mem.nfreed > 0 and w.mem.unreclaimed() <= 4 * 2


def test_without_the_validation_read_a_node_is_used_after_free() -> None:
    r = explore(setup(hp(validate=False), P2))
    assert r.kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"
    assert explore(setup(ImmediateFree, Q1, "queue")).kind == "use-after-free"


def test_garbage_is_bounded_by_n_times_R_with_a_stalled_process() -> None:
    n = 3
    R = 2 * n * HazardPointers.K
    for kind in ("stack", "queue"):
        peaks = [stall_peak(HazardPointers, n, m, kind, seed=s, stall_after=3) for m in (50, 400) for s in range(3)]
        assert max(peaks) <= n * R


def test_a_scan_frees_all_but_the_protected_nodes() -> None:
    # one process pops 3 nodes with R = 3; at the scan its own slot 0 still
    # names the node it has just popped, so that node stays in the list
    w = World(setup(lambda m, n: HazardPointers(m, n, R=3), [[("pop",)] * 3], initial=3))
    while not w.done():
        w.step(0)
    w.finish()
    assert w.mem.nretired == 3 and w.mem.nfreed == 2 and w.scheme.rlist[0] == [1]
