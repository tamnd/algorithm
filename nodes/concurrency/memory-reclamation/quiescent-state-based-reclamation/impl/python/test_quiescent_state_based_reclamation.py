# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quiescent-state-based-reclamation/. The authors are listed in prov/RNB9XT.jsonl.

import random

from quiescent_state_based_reclamation import QSBR
from smr_sim import ImmediateFree, explore, run_random, run_schedule, setup, stall_peak, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
Q2 = [[("deq",)], [("deq",), ("deq",)]]
T3 = [[("pop",)], [("pop",)], [("push", "x")]]


def qsbr(lag: int = 2):
    return lambda m, n: QSBR(m, n, lag=lag)


class QuiescentWhileHolding(QSBR):
    """Wrong client: it reports a quiescent state in the middle of a pop, while it holds top."""

    def read(self, t, a, f):
        yield from self.quiescent(t)
        return (yield ("read", a, f))


def test_every_interleaving_is_safe() -> None:
    for progs, kind in ((P2, "stack"), (PP, "stack"), (Q2, "queue")):
        r = explore(setup(qsbr(), progs, kind))
        assert r.violation is None and r.finals > 0


def test_every_interleaving_of_three_processes_is_safe() -> None:
    for kind, progs in (("stack", T3), ("queue", [[("deq",)], [("deq",)], [("enq", "x")]])):
        r = explore(setup(qsbr(), progs, kind, initial=1))
        assert r.violation is None and r.finals > 0


def test_explicit_quiescent_states_are_safe() -> None:
    progs = [[("pop",), ("q",)], [("pop",), ("q",), ("pop",)]]
    assert explore(setup(qsbr(), progs)).violation is None


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for kind in ("stack", "queue"):
        make = setup(qsbr(), workload(4, 10, kind), kind)
        assert run_random(make, range(150)).violation is None
        w = run_schedule(make, random.Random(3))
        assert w.mem.nfreed > 0


def test_freeing_one_period_early_is_unsafe() -> None:
    assert explore(setup(qsbr(lag=1), P2)).kind == "use-after-free"


def test_a_quiescent_state_while_holding_a_node_is_unsafe() -> None:
    assert explore(setup(QuiescentWhileHolding, P2)).kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def test_a_stalled_process_makes_the_garbage_grow_without_bound() -> None:
    for kind in ("stack", "queue"):
        for m in (50, 400):
            peaks = [stall_peak(QSBR, 3, m, kind, seed=s, stall_after=3) for s in range(3)]
            # the two live processes retire m nodes in total, and none is freed
            assert min(peaks) == m


def test_without_a_stall_the_garbage_stays_small() -> None:
    for kind in ("stack", "queue"):
        for s in range(5):
            w = run_schedule(setup(QSBR, workload(3, 400, kind), kind), random.Random(s))
            # 600 retirements; the peak is a few periods of work, far below 600
            assert w.mem.nretired >= 300 and w.mem.peak <= 60
