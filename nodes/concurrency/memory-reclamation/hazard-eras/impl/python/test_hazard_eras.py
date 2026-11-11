# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hazard-eras/. The authors are listed in prov/D8CRRV.jsonl.

import random

from hazard_eras import HazardEras
from smr_sim import ImmediateFree, explore, run_random, run_schedule, setup, stall_peak, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
Q1 = [[("deq",)], [("deq",)]]


def he(R: int = 1):
    return lambda m, n: HazardEras(m, n, R=R)


class NoRecheck(HazardEras):
    """Wrong: publishes the era once and uses the pointer without checking that the clock stayed."""

    def protect(self, t, i, a, f):
        p = yield ("read", a, f)
        e = yield ("read", "he", "clock")
        yield ("write", "he", (t, i), e)
        return p


def test_every_interleaving_is_safe() -> None:
    for progs, kind in ((P2, "stack"), (Q1, "queue")):
        r = explore(setup(he(), progs, kind))
        assert r.violation is None and r.finals > 0


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for kind in ("stack", "queue"):
        for R in (1, 0):
            make = setup(he(R), workload(4, 10, kind), kind)
            assert run_random(make, range(60)).violation is None
        w = run_schedule(setup(HazardEras, workload(3, 60, kind), kind), random.Random(3))
        assert w.mem.nfreed > 0


def test_missing_the_clock_recheck_is_unsafe() -> None:
    assert explore(setup(lambda m, n: NoRecheck(m, n, R=1), P2)).kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def test_garbage_is_bounded_under_a_stall() -> None:
    n, K, initial = 3, HazardEras.K, 4
    R = 2 * n * K
    # Theorem 3 gives n (R + n K L), where L is the number of nodes alive in one era. In this
    # workload we take L = initial + 3n: the nodes in the structure, plus one being pushed
    # and one being popped per process. The bound is checked, not proved, for this L.
    L = initial + 3 * n
    proved = n * (R + n * K * L)  # 270
    workload_bound = n * R + n * K * L  # 114: only the stalled process holds eras for long
    for kind in ("stack", "queue"):
        for m in (50, 400):
            for s in range(3):
                peak = stall_peak(HazardEras, n, m, kind, seed=s, stall_after=3)
                assert peak <= workload_bound <= proved
