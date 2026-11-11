# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-reference-counting/. The authors are listed in prov/YM4G39.jsonl.

import random

import lock_free_reference_counting as L
from smr_sim import ImmediateFree, explore, run_random, run_schedule, run_stall, setup, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
EQ = [[("enq", "x")], [("deq",), ("deq",)]]
Q1 = [[("deq",)], [("deq",)]]


def test_every_interleaving_is_safe() -> None:
    for mode, progs, kind in (("valois", P2, "stack"), ("valois", EQ, "queue"), ("dcas", EQ, "queue")):
        r = explore(L.setup(progs, mode, kind))
        assert r.violation is None and r.finals > 0, (mode, kind, r.violation)


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for mode in ("valois", "dcas"):
        for kind in ("stack", "queue"):
            assert run_random(L.setup(workload(4, 10, kind), mode, kind), range(60)).violation is None
            w = run_schedule(L.setup(workload(3, 60, kind), mode, kind), random.Random(3))
            assert w.mem.nfreed > 0 and not w.mem.retired


def test_increment_after_free_is_unsafe() -> None:
    # Without a type-stable pool, the increment at L2 can hit a node that was already freed.
    assert explore(L.setup(P2, "naive")).kind == "use-after-free"
    assert explore(L.setup(Q1, "naive", "queue")).kind == "use-after-free"


def test_without_the_claim_bit_two_processes_free_the_same_node() -> None:
    assert explore(L.setup(P2, "noclaim")).kind == "double-free"
    assert run_random(L.setup(workload(4, 10, "queue"), "noclaim", "queue"), range(100)).kind == "double-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def stalled(mode: str, kind: str, m: int, seed: int, after: int) -> int:
    progs = workload(3, m, kind)
    progs[0] = [("pop",) if kind == "stack" else ("deq",)]
    if kind == "stack":
        progs[1] = [("pop",)] * 4 + progs[1]  # drain the stack, so the held node is removed
    return run_stall(L.setup(progs, mode, kind, initial=4), seed, after).mem.peak


def test_garbage_under_a_stall() -> None:
    for mode in ("valois", "dcas"):
        for s in range(3):
            for after in (3, 5):
                # Stack: next fields never change after a push, so a stopped process keeps alive
                # only the 4 nodes below what it holds, plus what running processes hold for a moment.
                assert stalled(mode, "stack", 50, s, after) <= 8
                assert stalled(mode, "stack", 400, s, after) <= 8
            # Queue: the held node links to every node enqueued later, so nothing is freed.
            assert stalled(mode, "queue", 50, s, 5) >= 50
            assert stalled(mode, "queue", 400, s, 5) >= 400
