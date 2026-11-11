# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimistic-access/. The authors are listed in prov/HH6AVD.jsonl.
"""Tests for the simplified optimistic access scheme.

The memory is a type-stable pool that reuses the last freed address first.
A read of a freed node is allowed and returns stale data, as the scheme
assumes; a write to a freed node is a use-after-free, and a lost or
duplicated value at the end of a run is a corruption.
"""

from optimistic_access import OptimisticAccess
from smr_sim import ImmediateFree, Memory, explore, run_random, run_stall, setup, workload


def TS():
    return Memory(type_stable=True)


def oa(**kw):
    return lambda m, n: OptimisticAccess(m, n, **kw)


P1 = [[("pop",)], [("pop",)]]
ABA1 = [[("pop",)], [("pop",), ("push", "x")]]
QQ = [[("deq",)], [("deq",)]]
QE = [[("deq",)], [("enq", "x")]]
BAD = [[("pop",)], [("pop",), ("pop",), ("push", "x")]]


def test_exhaustive():
    for progs, kind, initial in [(P1, "stack", 2), (ABA1, "stack", 2), (QQ, "queue", 2), (QE, "queue", 1)]:
        r = explore(setup(oa(R=1), progs, kind, initial, mem=TS))
        assert r.violation is None, (progs, kind, r.violation, r.schedule)
        assert r.finals > 0


def test_random():
    for kind in ["stack", "queue"]:
        for R in [1, 0]:
            r = run_random(setup(oa(R=R), workload(4, 10, kind), kind, mem=TS), range(100))
            assert r.violation is None, (kind, R, r.violation, r.schedule)


def test_without_the_check_fails():
    # With no warning-bit check, a pop uses a stale next pointer and its CAS succeeds (ABA).
    r = explore(setup(oa(R=1, check=False), BAD, "stack", initial=3, mem=TS))
    assert r.kind == "corrupt"


def test_immediate_free_fails():
    assert explore(setup(ImmediateFree, ABA1, "stack", mem=TS)).kind == "corrupt"
    assert explore(setup(ImmediateFree, P1, "stack")).kind == "use-after-free"


def test_stall_bound():
    # Each list holds fewer than R = 2 n K nodes after a recycle keeps at most
    # n K of them, so at most n R = 36 retired nodes are unfreed for n = 3.
    n, K = 3, OptimisticAccess.K
    bound = n * 2 * n * K
    for kind in ["stack", "queue"]:
        rem = ("pop",) if kind == "stack" else ("deq",)
        for m in [50, 400]:
            for seed in range(3):
                progs = [[rem]] + workload(n, m, kind)[1:]
                w = run_stall(setup(OptimisticAccess, progs, kind, initial=4, mem=TS), seed, 3)
                assert w.mem.peak <= bound, (kind, m, seed, w.mem.peak)
                assert w.mem.nfreed >= w.mem.nretired - bound
