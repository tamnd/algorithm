# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/drop-the-anchor/. The authors are listed in prov/M2X7MT.jsonl.

import drop_the_anchor as D
from smr_sim import ImmediateFree, explore, run_random, run_stall, setup, stall_peak, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
Q1 = [[("deq",)], [("deq",)]]
EQ = [[("enq", "x")], [("deq",), ("deq",)]]
FD = [[("find", "zz")], [("deq",), ("deq",)]]
FD3 = [[("find", "zz")], [("deq",), ("deq",), ("deq",)]]


def anchors(**kw):
    return lambda m, n: D.Anchors(m, n, **kw)


class AnchorOnly(D.Anchors):
    """Wrong: an anchor guards only the node it names, not the K nodes after it."""

    def guards(self, an: tuple, x: int, sx) -> bool:
        return an[1] == (x if an[0] == "node" else sx)


def test_every_interleaving_is_safe() -> None:
    for progs in (P2, PP):
        r = explore(setup(anchors(R=1), progs))
        assert r.violation is None and r.finals > 0, r.violation
    for progs, K, initial in ((Q1, 2, 2), (EQ, 2, 2), (FD, 1, 3), (FD, 2, 4), (FD3, 1, 4)):
        r = explore(D.setup(progs, K=K, R=1, initial=initial))
        assert r.violation is None and r.finals > 0, (progs, K, r.violation)


def test_random_schedules_are_safe() -> None:
    assert run_random(setup(anchors(), workload(4, 10)), range(60)).violation is None
    assert run_random(D.setup(workload(4, 10, "queue")), range(60)).violation is None
    progs = workload(4, 10, "queue")
    progs[0] = [("find", "zz"), ("enq", "y"), ("find", "y")] * 3
    assert run_random(D.setup(progs, K=2, initial=6), range(60)).violation is None


def test_anchor_without_the_check_is_unsafe() -> None:
    # The traversal moves its anchor to a node that was already dequeued and freed.
    assert explore(D.setup(FD3, K=1, R=1, initial=4, validate=False)).kind == "use-after-free"
    assert explore(setup(anchors(R=1, validate=False), P2)).kind == "use-after-free"


def test_anchor_that_guards_only_its_node_is_unsafe() -> None:
    def make():
        m, gens, S, check = D.setup(FD3, K=1, R=1, initial=4)()
        S.__class__ = AnchorOnly
        return m, gens, S, check

    assert explore(make).kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"
    assert explore(setup(ImmediateFree, Q1, "queue")).kind == "use-after-free"


def test_garbage_stays_bounded_under_a_stall() -> None:
    n, K = 3, 2
    bound = n * 2 * n * (K + 1)  # n R with R = 2 n (K + 1): each anchor guards at most K + 1 nodes
    for m in (50, 400):
        for s in range(3):
            assert stall_peak(anchors(), n, m, "stack", s, 3) <= bound
            for op, after in ((("find", "zz"), 6), (("find", "zz"), 12), (("deq",), 3)):
                progs = workload(n, m, "queue")
                progs[0] = [op]
                w = run_stall(D.setup(progs, initial=6), s, after)
                assert w.mem.peak <= bound
                assert w.mem.nfreed >= w.mem.nretired - bound  # the others keep freeing while process 0 is stopped
