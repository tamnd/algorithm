# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epoch-based-reclamation/. The authors are listed in prov/E1V1VX.jsonl.

import random

from epoch_based_reclamation import EpochBased
from smr_sim import ImmediateFree, explore, run_random, run_schedule, setup, stall_peak, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
Q2 = [[("deq",)], [("deq",), ("deq",)]]
T3 = [[("pop",)], [("pop",)], [("push", "x")]]


def ebr(lag: int = 2):
    return lambda m, n: EpochBased(m, n, lag=lag)


def test_every_interleaving_is_safe() -> None:
    for progs, kind in ((P2, "stack"), (PP, "stack"), (Q2, "queue")):
        r = explore(setup(ebr(), progs, kind))
        assert r.violation is None and r.finals > 0


def test_every_interleaving_of_three_processes_is_safe() -> None:
    r = explore(setup(ebr(), T3, initial=1))
    assert r.violation is None and r.finals > 0


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for kind in ("stack", "queue"):
        make = setup(ebr(), workload(4, 10, kind), kind)
        assert run_random(make, range(150)).violation is None
        w = run_schedule(make, random.Random(3))
        assert w.mem.nfreed > 0


def test_freeing_one_epoch_early_is_unsafe() -> None:
    assert explore(setup(ebr(lag=1), P2)).kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def test_a_stalled_process_makes_the_garbage_grow_without_bound() -> None:
    for kind in ("stack", "queue"):
        for m in (50, 400):
            peaks = [stall_peak(EpochBased, 3, m, kind, seed=s, stall_after=3) for s in range(3)]
            # the two live processes retire m nodes in total, and none is freed
            assert min(peaks) == m


def test_without_a_stall_the_garbage_stays_small() -> None:
    # the same 600 retirements as in the stalled run, but the peak stays near a few epochs of work
    for kind in ("stack", "queue"):
        for s in range(5):
            w = run_schedule(setup(EpochBased, workload(3, 400, kind), kind), random.Random(s))
            assert w.mem.nretired >= 300 and w.mem.peak <= 20
