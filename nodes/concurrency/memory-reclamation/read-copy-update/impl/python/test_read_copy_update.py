# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-copy-update/. The authors are listed in prov/0AQA6S.jsonl.
"""Tests for read-copy-update on the poisoning allocator of smr_sim.py.

The allocator reuses freed addresses and makes every access to a freed node
fail, so a reader that still holds an old version after it was freed is
caught as a use-after-free.
"""

import random

import read_copy_update as R
from smr_sim import ImmediateFree, explore, run_random, run_schedule, run_stall, setup, workload

P2 = [[("pop",)], [("pop",)]]
PP = [[("push", "a"), ("pop",)], [("pop",), ("push", "b")]]
Q1 = [[("deq",)], [("deq",)]]
EQ = [[("enq", "a"), ("deq",)], [("deq",), ("enq", "b")]]
SMALL = [(P2, "stack", 2), (PP, "stack", 2), (Q1, "queue", 2), (EQ, "queue", 1)]


def rcu(**kw):
    return lambda m, n: R.RCU(m, n, **kw)


def test_config_update_exhaustive():
    for nreaders, values, reads in [(2, ["v1", "v2"], 1), (2, ["v1"], 2), (1, ["v1", "v2"], 2)]:
        r = explore(R.setup(nreaders, values, reads=reads))
        assert r.violation is None, (nreaders, values, r.violation, r.schedule)
        assert r.finals > 0


def test_config_update_without_grace_period_fails():
    r = explore(R.setup(1, ["v1"], sync=False, reads=1))
    assert r.kind == "use-after-free"


def test_stack_and_queue_exhaustive():
    for progs, kind, initial in SMALL:
        for kw in [{}, {"defer": True, "R": 1}]:
            r = explore(setup(rcu(**kw), progs, kind, initial))
            assert r.violation is None, (progs, kind, kw, r.violation, r.schedule)


def test_stack_and_queue_random():
    for kind in ["stack", "queue"]:
        for kw in [{}, {"defer": True, "R": 2}]:
            r = run_random(setup(rcu(**kw), workload(3, 8, kind), kind, 2), range(200))
            assert r.violation is None, (kind, kw, r.violation, r.schedule)


def test_deferred_mode_frees_without_a_stall():
    for kind in ["stack", "queue"]:
        w = run_schedule(setup(rcu(defer=True, R=2), workload(3, 40, kind), kind, 2), random.Random(3))
        assert w.done() and w.mem.nfreed > 0


def test_unsafe_versions_fail():
    for progs, kind, initial in SMALL:
        assert explore(setup(rcu(sync=False), progs, kind, initial)).kind == "use-after-free"
    assert explore(setup(ImmediateFree, P2, "stack", 2)).kind == "use-after-free"
    assert explore(setup(ImmediateFree, Q1, "queue", 2)).kind == "use-after-free"


def stalled(kind, m, **kw):
    progs = workload(3, m, kind)
    progs[0] = [("pop",) if kind == "stack" else ("deq",)]
    return run_stall(setup(rcu(**kw), progs, kind, initial=4), 1, 2)


def test_stall_blocks_synchronous_updaters():
    # Process 0 stops inside its read-side section. The other two each remove
    # one node, then wait for a grace period that never ends: no progress, and
    # at most n - 1 = 2 nodes wait to be freed.
    for kind in ["stack", "queue"]:
        for m in [50, 400]:
            w = stalled(kind, m)
            assert not w.done()
            assert all(op is not None and op[0] == "wait" for op in w.ops[1:])
            assert w.mem.peak <= 2


def test_stall_grows_garbage_in_deferred_mode():
    # With call_rcu the others go on, but no grace period ends, so nothing is freed.
    for kind in ["stack", "queue"]:
        peaks = []
        for m in [50, 400]:
            w = stalled(kind, m, defer=True, R=4)
            assert w.mem.nfreed == 0
            peaks.append(w.mem.peak)
        assert peaks[0] >= 50 and peaks[1] >= 8 * peaks[0] - 50
