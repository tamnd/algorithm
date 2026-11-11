# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treiber-stack/. The authors are listed in prov/YJWGPQ.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from lincheck import EMPTY, StackSpec, lin_check, linearize
from treiber_stack import TreiberStack, push_all


def make(procs, init=(), tagged=True, reclaim=True, reuse=True):
    def setup():
        mem = Memory(reuse=reuse)
        s = TreiberStack(mem, tagged=tagged, reclaim=reclaim)
        push_all(mem, s, list(init))
        return mem, [program(s, ops) for ops in procs]

    return setup


def test_example_sequential() -> None:
    run = Run(make([[("push", 1), ("push", 2), ("pop",), ("push", 3), ("pop",), ("pop",), ("pop",)]]))
    run.finish(0)
    results = [ev[2] for ev in run.history if ev[1] == "res"]
    assert results == [None, None, 2, None, 3, 1, EMPTY]


def test_random_sequential_against_list() -> None:
    rng = random.Random(1986)
    for _ in range(500):
        ops = [("push", rng.randint(0, 9)) if rng.random() < 0.55 else ("pop",) for _ in range(rng.randint(0, 12))]
        run = Run(make([ops], tagged=rng.random() < 0.5))
        run.finish(0)
        model: list[int] = []
        expect = []
        for op in ops:
            if op[0] == "push":
                model.append(op[1])
                expect.append(None)
            else:
                expect.append(model.pop() if model else EMPTY)
        assert [ev[2] for ev in run.history if ev[1] == "res"] == expect


def test_solo_steps_are_bounded() -> None:
    run = Run(make([[("push", 1), ("pop",), ("pop",)]]))
    assert run.finish_op(0) == 4
    assert run.finish_op(0) == 5
    assert run.finish_op(0) == 1


def test_exhaustive_linearizable_with_tags() -> None:
    cases = [
        ([[("push", 1), ("pop",)], [("push", 2), ("pop",)]], ()),
        ([[("pop",)], [("pop",)], [("push", 3)]], (1, 2)),
        ([[("pop",)], [("pop",), ("pop",), ("push", 9), ("pop",)]], ("c", "b", "a")),
    ]
    for procs, init in cases:
        st = explore(make(procs, init), lin_check(StackSpec() if not init else Spec(init)))
        assert st.failure is None, st.failure
        assert st.runs > 0


class Spec(StackSpec):
    def __init__(self, init):
        self.init = tuple(init)


def test_exhaustive_without_reclamation_is_safe_without_tags() -> None:
    procs = [[("pop",)], [("pop",), ("pop",), ("push", 9), ("pop",)]]
    st = explore(make(procs, ("c", "b", "a"), tagged=False, reclaim=False), lin_check(Spec(("c", "b", "a"))))
    assert st.failure is None


def aba_schedule(tagged):
    run = Run(make([[("pop",)], [("pop",), ("pop",), ("push", "x"), ("pop",)]], ("c", "b", "a"), tagged=tagged))
    run.until(0, lambda op: op[0] == "cas")  # p0 has read top = A and A.next = B
    for _ in range(3):
        run.finish_op(1)  # p1 pops a, pops b, pushes x into the reused address of A
    run.finish_op(0)
    run.finish_op(1)
    return run


def test_aba_run_without_tags() -> None:
    run = aba_schedule(tagged=False)
    assert linearize(run.history, Spec(("c", "b", "a"))) is None
    assert run.mem.uaf  # the last pop read the freed node B


def test_tags_stop_the_aba_run() -> None:
    run = aba_schedule(tagged=True)
    assert linearize(run.history, Spec(("c", "b", "a"))) is not None
    assert [ev[2] for ev in run.history if ev[1] == "res"][-2:] == ["x", "c"]


def test_explorer_finds_aba_without_tags() -> None:
    procs = [[("pop",)], [("pop",), ("pop",), ("push", 9), ("pop",)]]
    st = explore(make(procs, ("c", "b", "a"), tagged=False), lin_check(Spec(("c", "b", "a"))))
    assert st.failure is not None


def test_not_wait_free_a_pop_can_fail_forever() -> None:
    k = 25
    run = Run(make([[("pop",)], [("push", i) for i in range(k)]], ("a",)))
    for _ in range(k):
        run.until(0, lambda op: op[0] == "cas")
        run.finish_op(1)
        run.step(0)  # the CAS fails: top changed
    assert run.pending[0] is not None
    assert sum(1 for ev in run.history if ev[0] == 0 and ev[1] == "res") == 0
    assert sum(1 for ev in run.history if ev[0] == 1 and ev[1] == "res") == k


def test_random_schedules_linearizable() -> None:
    rng = random.Random(5118)
    for seed in range(300):
        procs = [[("push", 10 * p + i) if rng.random() < 0.5 else ("pop",) for i in range(3)] for p in range(4)]
        run = random_run(make(procs, (1, 2)), seed)
        assert all(q is None for q in run.pending)
        assert linearize(run.history, Spec((1, 2))) is not None
