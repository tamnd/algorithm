# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/debra/. The authors are listed in prov/K7CR9Y.jsonl.

import random

from debra import Debra
from smr_sim import (ImmediateFree, SimError, World, _kind, explore, run_random, run_schedule, setup,
                     stall_peak, workload)

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
Q2 = [[("deq",)], [("deq",), ("deq",)]]
T3 = [[("pop",)], [("pop",)], [("push", "x")]]
T3Q = [[("deq",)], [("deq",)], [("enq", "x")]]


def plus(T: int = 8):
    return lambda m, n: Debra(m, n, plus=True, T=T)


class TwoBags(Debra):
    """Wrong: frees the bag of the previous epoch instead of the one two epochs back."""

    BAGS = 2


class IgnoresSignals(Debra):
    """Wrong DEBRA+: the signalled process goes on reading as if nothing happened."""

    def on_signal(self, t):
        return False


def test_every_interleaving_is_safe() -> None:
    for progs, kind in ((P2, "stack"), (PP, "stack"), (Q2, "queue")):
        r = explore(setup(Debra, progs, kind))
        assert r.violation is None and r.finals > 0


def test_every_interleaving_of_three_processes_is_safe() -> None:
    for progs, kind in ((T3, "stack"), (T3Q, "queue")):
        r = explore(setup(Debra, progs, kind, initial=1))
        assert r.violation is None and r.finals > 0


def test_every_interleaving_with_neutralization_is_safe() -> None:
    # T = 1: every failed check sends a signal, the most aggressive setting
    for progs, kind, init in ((P2, "stack", 2), (Q2, "queue", 2)):
        r = explore(setup(plus(T=1), progs, kind, initial=init))
        assert r.violation is None and r.finals > 0


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for scheme in (Debra, plus(T=1), plus(T=8)):
        for kind in ("stack", "queue"):
            make = setup(scheme, workload(4, 10, kind), kind)
            assert run_random(make, range(60)).violation is None
            w = run_schedule(setup(scheme, workload(3, 60, kind), kind), random.Random(3))
            assert w.mem.nfreed > 0


def reads_next(w: World) -> bool:
    op = w.ops[0]
    return op is not None and op[0] == "read" and op[2] == "next"


def scripted(scheme, pops: int, reader_first: bool) -> str:
    """Process 0 pops once and stops just before it reads top.next; process 1 pops `pops` times; then 0 goes on.

    With reader_first=False, process 1 first runs until it has moved G to 1, so that the
    reader announces epoch 1. Returns "ok" or the kind of violation.
    """
    w = World(setup(scheme, [[("pop",)], [("pop",)] * pops], initial=pops))
    try:
        if not reader_first:
            while w.mem.cells["debra"]["G"] == 0:
                w.step(1)
        while not reads_next(w):
            w.step(0)
        while w.ops[1] is not None:
            w.step(1)
        while w.ops[0] is not None:
            w.step(0)
        w.finish()
    except SimError as e:
        return _kind(e)
    return "ok"


def test_two_bags_free_too_early() -> None:
    # process 1 retires the node in epoch 1 into the bag of epoch 0, and two rotations later
    # frees it while the reader, which announced epoch 1, still holds it
    assert scripted(TwoBags, 5, reader_first=False) == "use-after-free"
    assert scripted(Debra, 5, reader_first=False) == "ok"


def test_ignoring_the_signal_is_unsafe() -> None:
    # the reader is signalled and counted as quiescent; the epoch moves three times past it
    bad = lambda m, n: IgnoresSignals(m, n, plus=True, T=1)  # noqa: E731
    assert scripted(bad, 7, reader_first=True) == "use-after-free"
    assert scripted(plus(T=1), 7, reader_first=True) == "ok"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def test_plain_debra_garbage_grows_under_a_stall() -> None:
    for kind in ("stack", "queue"):
        for m in (50, 400):
            peaks = [stall_peak(Debra, 3, m, kind, seed=s, stall_after=3) for s in range(3)]
            assert min(peaks) == m


def test_debra_plus_garbage_is_bounded_under_a_stall() -> None:
    n, T, K = 3, 8, Debra.K
    bound = n * (T + 3 * (n + 1) + 3 * n * K)  # 114, Theorem 4 of the proof
    for kind in ("stack", "queue"):
        for m in (50, 400):
            for s in range(3):
                assert stall_peak(plus(T), n, m, kind, seed=s, stall_after=3) <= bound
