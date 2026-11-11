# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neutralization-based-reclamation/. The authors are listed in prov/A696BX.jsonl.

import random

from neutralization_based_reclamation import NBR
from smr_sim import (ImmediateFree, SimError, World, _kind, explore, run_random, run_schedule, setup,
                     stall_peak, workload)

P2 = [[("pop",)], [("pop",), ("pop",)]]
Q1 = [[("deq",)], [("deq",)]]


def nbr(R: int = 1):
    return lambda m, n: NBR(m, n, R=R)


class IgnoresSignals(NBR):
    """Wrong: the read phase is never restartable, so a signal does not drop the references."""

    def restartable(self, t):
        return False


class ReservesLate(NBR):
    """Wrong: leaves the read phase first and writes the reservations after that."""

    def before_write(self, t, ptrs):
        self.phase[t] = False
        for i, p in enumerate(ptrs[: self.K]):
            yield ("write", "res", (t, i), p)
            self.mine[t][i] = p


class ReadsBeforeSignals(NBR):
    """Wrong: the scan reads the reservations first and sends the signals after that."""

    def retire(self, t, a):
        self.mem.note_retire(a)
        self.rlist[t].append(a)
        if len(self.rlist[t]) < self.R:
            return
        held = set()
        for q in range(self.n):
            for i in range(self.K):
                r = yield ("read", "res", (q, i))
                if r is not None:
                    held.add(r)
        for q in range(self.n):
            if q != t:
                yield ("signal", q)
        keep = []
        for a2 in self.rlist[t]:
            if a2 in held:
                keep.append(a2)
            else:
                yield ("free", a2)
        self.rlist[t] = keep


def signal_order_run(scheme) -> str:
    """Process 0 enqueues and stops just before its first reservation write. With R = 3,
    process 1 scans once, in its third dequeue, and that scan frees the tail that process 0 read.
    Process 1 runs up to its first signal; then process 0 writes its reservations; then both finish."""
    progs = [[("enq", "x")], [("enq", "y"), ("enq", "z"), ("deq",), ("deq",), ("deq",)]]
    w = World(setup(scheme, progs, "queue", initial=1))
    try:
        while not (w.ops[0][0] == "write" and w.ops[0][1] == "res"):
            w.step(0)
        while w.ops[1] is not None and w.ops[1][0] != "signal":
            w.step(1)
        while w.ops[0][0] == "write" and w.ops[0][1] == "res":
            w.step(0)
        while w.ops[1] is not None:
            w.step(1)
        while w.ops[0] is not None:
            w.step(0)
        w.finish()
    except SimError as e:
        return _kind(e)
    return "ok"


def late_reservation_run(scheme) -> str:
    """Process 0 enqueues and stops just before its first reservation write. Process 1 then
    enqueues twice and dequeues three times, which retires and frees the old tail of process 0.
    Then process 0 goes on and does its CAS on that tail."""
    progs = [[("enq", "x")], [("enq", "y"), ("enq", "z"), ("deq",), ("deq",), ("deq",)]]
    w = World(setup(scheme, progs, "queue", initial=1))
    try:
        while not (w.ops[0][0] == "write" and w.ops[0][1] == "res"):
            w.step(0)
        while w.ops[1] is not None:
            w.step(1)
        while w.ops[0] is not None:
            w.step(0)
        w.finish()
    except SimError as e:
        return _kind(e)
    return "ok"


def test_every_interleaving_is_safe() -> None:
    for progs, kind in ((P2, "stack"), (Q1, "queue")):
        r = explore(setup(nbr(), progs, kind))
        assert r.violation is None and r.finals > 0


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for kind in ("stack", "queue"):
        for R in (1, 0):
            make = setup(nbr(R), workload(4, 10, kind), kind)
            assert run_random(make, range(60)).violation is None
        w = run_schedule(setup(NBR, workload(3, 60, kind), kind), random.Random(3))
        assert w.mem.nfreed > 0


def test_ignoring_the_signal_is_unsafe() -> None:
    assert explore(setup(lambda m, n: IgnoresSignals(m, n, R=1), P2)).kind == "use-after-free"


def test_reserving_after_the_phase_change_is_unsafe() -> None:
    assert late_reservation_run(lambda m, n: ReservesLate(m, n, R=1)) == "use-after-free"
    assert late_reservation_run(nbr()) == "ok"


def test_reading_reservations_before_the_signals_is_unsafe() -> None:
    assert signal_order_run(lambda m, n: ReadsBeforeSignals(m, n, R=3)) == "use-after-free"
    assert signal_order_run(nbr(3)) == "ok"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def test_garbage_is_bounded_under_a_stall() -> None:
    n = 3
    R = 2 * n * NBR.K
    # Theorem 3: a scan leaves at most n K reserved nodes, and n K < R, so each list holds at most R.
    bound = n * R  # 36
    for kind in ("stack", "queue"):
        for m in (50, 400):
            for s in range(3):
                for after in (3, 5):
                    assert stall_peak(NBR, n, m, kind, seed=s, stall_after=after) <= bound
