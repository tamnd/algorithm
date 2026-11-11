# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyaline/. The authors are listed in prov/XC1TS5.jsonl.

import random

from hyaline import Hyaline
from smr_sim import ImmediateFree, explore, run_random, run_schedule, setup, stall_peak, workload

# a batch has n + 1 = 3 nodes, so process 1 pops three times to fill one
HY = [[("pop",)], [("pop",), ("pop",), ("pop",)]]
HYQ = [[("deq",)], [("deq",), ("deq",), ("deq",)]]
PU = [[("pop",)], [("push", "a"), ("pop",), ("push", "b"), ("pop",), ("push", "c"), ("pop",)]]


def hy(robust: bool, F: int = 1):
    return lambda m, n: Hyaline(m, n, robust=robust, F=F)


class DecrementFirst(Hyaline):
    """Wrong: leave() subtracts from the batch counter before it reads the link of the list node."""

    def end(self, t):
        _, p = yield ("swap", "hy", ("H", t), (0, None))
        while p is not None:
            ref = yield ("read", p, "bref")
            if (yield ("faa", ref, "nref", -1)) == 1:
                yield from self.free_batch(ref)
            p = yield ("read", p, "blink")


class NoEraRecheck(Hyaline):
    """Wrong: Hyaline-1S that publishes the era after the read and does not read the pointer again."""

    def protect(self, t, i, a, f):
        p = yield ("read", a, f)
        e = yield ("read", "hy", "era")
        if e != self.access[t]:
            yield ("write", "hy", ("A", t), e)
            self.access[t] = e
        return p


def test_every_interleaving_is_safe() -> None:
    for robust in (False, True):
        assert explore(setup(hy(robust), HY, initial=4)).violation is None
        assert explore(setup(hy(robust), HYQ, "queue", initial=4)).violation is None


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for robust in (False, True):
        assert run_random(setup(hy(robust), PU, initial=0), range(100)).violation is None
        for kind in ("stack", "queue"):
            make = setup(hy(robust, 2), workload(4, 12, kind), kind)
            assert run_random(make, range(40)).violation is None
            w = run_schedule(setup(hy(robust, 2), workload(3, 60, kind), kind), random.Random(3))
            assert w.mem.nfreed > 0


def test_decrement_before_reading_the_link_is_unsafe() -> None:
    bad = lambda m, n: DecrementFirst(m, n)  # noqa: E731
    assert explore(setup(bad, HY, initial=4)).kind == "use-after-free"
    assert explore(setup(bad, HYQ, "queue", initial=4)).kind == "use-after-free"


def test_era_without_the_recheck_is_unsafe() -> None:
    # process 0 reads a node born after its published era; the batch skips its slot
    bad = lambda m, n: NoEraRecheck(m, n, robust=True, F=1)  # noqa: E731
    assert explore(setup(bad, PU, initial=0)).kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, HY, initial=4)).kind == "use-after-free"


def test_hyaline_1_keeps_everything_under_a_stall() -> None:
    for kind in ("stack", "queue"):
        for m in (50, 400):
            assert stall_peak(hy(False, 2), 3, m, kind, seed=1, stall_after=5) >= m


def test_hyaline_1s_is_bounded_under_a_stall() -> None:
    n, F, initial = 3, 2, 4
    # Partial batches: at most n nodes per process. The stopped slot holds only batches with a
    # node born at or before its era, here era 1: at most B = initial + n (F - 1) = 7 batches of
    # n + 1 nodes (Theorem 3). The test allows 2 (n - 1) more batches in the slots of the running
    # processes, which they free at their next leave; that part is a check for this workload.
    B = initial + n * (F - 1)
    bound = n * n + (n + 1) * (B + 2 * (n - 1))  # 9 + 4 * 11 = 53
    for kind in ("stack", "queue"):
        for m in (50, 400):
            for s in range(3):
                for after in (3, 5):
                    assert stall_peak(hy(True, F), n, m, kind, seed=s, stall_after=after) <= bound
