# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pass-the-buck/. The authors are listed in prov/HJDC4M.jsonl.

import random

from pass_the_buck import PassTheBuck
from smr_sim import ImmediateFree, explore, run_random, run_schedule, setup, stall_peak, workload

P2 = [[("pop",)], [("pop",), ("pop",)]]
PP = [[("pop",), ("push", "a")], [("pop",), ("pop",)]]
Q1 = [[("deq",)], [("deq",)]]


def ptb(R: int = 1):
    return lambda m, n: PassTheBuck(m, n, R=R)


class NoRecheck(PassTheBuck):
    """Wrong: posts the guard but does not read the source again."""

    def protect(self, t, i, a, f):
        p = yield ("read", a, f)
        yield ("write", "ptb", ("P", t * self.K + i), p)
        return p


class TakesTrapped(PassTheBuck):
    """Wrong: at L9 takes the handed-off value out even when the guard still posts it."""

    def liberate(self, vs):
        for g in range(self.G):
            attempts = 0
            h = yield ("read", "ptb", ("H", g))
            v = yield ("read", "ptb", ("P", g))
            if v is not None and v in vs:
                while True:
                    if (yield ("cas", "ptb", ("H", g), h, (v, h[1] + 1))):
                        vs.discard(v)
                        if h[0] is not None:
                            vs.add(h[0])
                        break
                    attempts += 1
                    if attempts == 3:
                        break
                    h = yield ("read", "ptb", ("H", g))
                    if attempts == 2 and h[0] is not None:
                        break
                    if v != (yield ("read", "ptb", ("P", g))):
                        break
            elif h[0] is not None:
                if (yield ("cas", "ptb", ("H", g), h, (None, h[1] + 1))):
                    vs.add(h[0])
        return vs


class CountsHandoffs(PassTheBuck):
    handoffs = 0

    def liberate(self, vs):
        before = set(vs)
        out = yield from super().liberate(vs)
        CountsHandoffs.handoffs += len(before - out)
        return out


def test_every_interleaving_is_safe() -> None:
    for progs, kind in ((P2, "stack"), (PP, "stack"), (Q1, "queue")):
        r = explore(setup(ptb(), progs, kind))
        assert r.violation is None and r.finals > 0


def test_random_schedules_free_nodes_and_stay_safe() -> None:
    for kind in ("stack", "queue"):
        for R in (1, 0):
            assert run_random(setup(ptb(R), workload(4, 10, kind), kind), range(60)).violation is None
        w = run_schedule(setup(PassTheBuck, workload(3, 60, kind), kind), random.Random(3))
        assert w.mem.nfreed > 0


def test_values_are_handed_off_and_freed_later() -> None:
    CountsHandoffs.handoffs = 0
    for s in range(40):
        w = run_schedule(setup(lambda m, n: CountsHandoffs(m, n, R=1), workload(3, 12), "stack"), random.Random(s))
        assert w.mem.nfreed > 0
    assert CountsHandoffs.handoffs > 0


def test_no_recheck_is_unsafe() -> None:
    assert explore(setup(lambda m, n: NoRecheck(m, n, R=1), P2)).kind == "use-after-free"


def test_taking_a_trapped_value_is_unsafe() -> None:
    assert explore(setup(lambda m, n: TakesTrapped(m, n, R=1), P2)).kind == "use-after-free"


def test_immediate_free_is_unsafe() -> None:
    assert explore(setup(ImmediateFree, P2)).kind == "use-after-free"


def test_garbage_is_bounded_under_a_stall() -> None:
    n = 3
    G = n * PassTheBuck.K
    R = 2 * G
    # Theorem 3: each value set holds at most R + G values, and the handoff words at most G.
    bound = n * (R + G) + G  # 60
    for kind in ("stack", "queue"):
        for m in (50, 400):
            for s in range(3):
                for after in (3, 5):
                    assert stall_peak(PassTheBuck, n, m, kind, seed=s, stall_after=after) <= bound
