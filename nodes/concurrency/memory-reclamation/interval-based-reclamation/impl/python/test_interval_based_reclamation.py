# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-based-reclamation/. The authors are listed in prov/8KPT1J.jsonl.

import random

from interval_based_reclamation import IntervalBased
from smr_sim import ImmediateFree, explore, run_random, run_schedule, setup, stall_peak, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
PU = [[("pop",)], [("push", "a"), ("pop",), ("pop",)]]
PU2 = [[("pop",)], [("push", "a"), ("pop",), ("push", "b"), ("pop",)]]
Q2 = [[("deq",)], [("deq",), ("deq",)]]


def ibr(R: int = 1, F: int = 1):
    return lambda m, n: IntervalBased(m, n, R=R, F=F)


class NoUpperRaise(IntervalBased):
    """Wrong: reserves only the epoch at the start of the operation and never raises the upper end."""

    def protect(self, t, i, a, f):
        return (yield ("read", a, f))


def test_every_interleaving_is_safe() -> None:
    for progs, kind in ((P2, "stack"), (PP, "stack"), (PU, "stack"), (Q2, "queue")):
        r = explore(setup(ibr(), progs, kind))
        assert r.violation is None and r.finals > 0


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for kind in ("stack", "queue"):
        for R, F in ((1, 1), (0, 2)):
            make = setup(ibr(R, F), workload(4, 10, kind), kind)
            assert run_random(make, range(60)).violation is None
        w = run_schedule(setup(IntervalBased, workload(3, 60, kind), kind), random.Random(3))
        assert w.mem.nfreed > 0


def test_a_fixed_interval_misses_nodes_born_later() -> None:
    # process 0 reserves [1, 1]; process 1 pushes a, born in epoch 2, and process 0 reads it.
    # Process 1 pops a, pushes b (epoch 3) and pops b; that scan sees [1, 1] and [3, 3] and frees a.
    assert explore(setup(ibr(), PU2, initial=0)).violation is None
    r = explore(setup(lambda m, n: NoUpperRaise(m, n, R=1, F=1), PU2, initial=0))
    assert r.kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def test_garbage_is_bounded_under_a_stall() -> None:
    n, F, initial = 3, 2, 4
    R = 2 * n
    # each list holds at most R nodes before a scan, plus what a scan keeps. The stalled
    # process reserved [1, 1], and at most initial + n (F - 1) nodes are born in epoch 1.
    # The live intervals are one operation long; for them we allow n + 2 n F nodes each.
    # The total is checked for this workload, not proved in general.
    bound = n * R + n * (initial + n + 2 * n * F)  # 18 + 57 = 75
    for kind in ("stack", "queue"):
        for m in (50, 400):
            for s in range(3):
                assert stall_peak(IntervalBased, n, m, kind, seed=s, stall_after=3) <= bound
