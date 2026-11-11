# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-blocking-bst/. The authors are listed in prov/H9D744.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from lincheck import SetSpec, lin_check, linearize
from non_blocking_bst import EFRBTree


class Spec(SetSpec):
    def __init__(self, keys=()):
        self.init = frozenset(keys)


def make(procs, keys=(), objs=None, **flags):
    def setup():
        mem = Memory()
        t = EFRBTree(mem, keys, **flags)
        if objs is not None:
            objs[:] = [t]
        return mem, [program(t, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def test_random_sequential_against_a_set() -> None:
    rng = random.Random(1)
    ops, model, want = [], set(), []
    for _ in range(400):
        k = rng.randrange(30)
        name = rng.choice(["insert", "delete", "find"])
        ops.append((name, k))
        if name == "insert":
            want.append(k not in model)
            model.add(k)
        elif name == "delete":
            want.append(k in model)
            model.discard(k)
        else:
            want.append(k in model)
    objs = []
    run = Run(make([ops], objs=objs))
    assert run.finish(0, limit=100000)
    assert results(run) == want
    t = objs[0]
    assert t.leaves() == sorted(model)
    assert t.check_shape() is None


CASES = [
    ((1, 3), [[("insert", 2)], [("delete", 3)]]),
    ((1, 3), [[("delete", 1)], [("delete", 3)]]),
    ((1, 2, 3), [[("delete", 2)], [("delete", 3)]]),
    ((1, 3), [[("delete", 3)], [("insert", 4)]]),
    ((), [[("insert", 1)], [("insert", 2)]]),
    ((1,), [[("delete", 1)], [("insert", 1)]]),
    ((2,), [[("insert", 1)], [("delete", 2)]]),
    ((1, 3), [[("find", 3)], [("delete", 3), ("insert", 3)]]),
]


def test_exhaustive_small_cases() -> None:
    for keys, procs in CASES:
        objs = []
        st = explore(make(procs, keys, objs=objs), lin_check(Spec(keys)),
                     check_states=lambda run: objs[0].check_shape())
        assert st.failure is None, (keys, procs, st.failure)
        assert st.runs > 5


def test_three_processes_on_neighbours() -> None:
    # Too many interleavings to visit all of them: 300 seeded schedules.
    keys = (1, 3)
    procs = [[("delete", 1)], [("delete", 3)], [("insert", 2), ("find", 1)]]
    for seed in range(300):
        objs = []
        run = random_run(make(procs, keys, objs=objs), seed)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, Spec(keys)) is not None, seed
        assert objs[0].check_shape() is None


def test_without_the_mark_an_insert_is_lost() -> None:
    # Tree for {1, 3}: root -> I(INF1) -> [I(3) -> [1, 3], INF1].
    # p0 deletes 3: gp = I(INF1), p = I(3). It flags gp, reads the sibling
    # (leaf 1), and stops before it swings gp's child. p1 inserts 2 under
    # p = I(3). Without the mark, p1's flag on p succeeds and p1 returns true;
    # then p0 replaces p by leaf 1, and leaf 2 is gone. With the mark, p1
    # finds p marked, helps the delete, and inserts 2 under gp.
    keys = (1, 3)
    procs = [[("delete", 3)], [("insert", 2), ("find", 2)]]
    for bug in (False, True):
        objs = []
        run = Run(make(procs, keys, objs=objs, mark_parent=not bug))
        run.until(0, lambda op: op[0] == "cas" and op[1][1] in ("left", "right"))
        assert run.finish_op(1) and run.finish(0) and run.finish(1)
        assert results(run, 1) == [True, not bug]
        assert (2 in objs[0].leaves()) != bug
        assert (linearize(run.history, Spec(keys)) is None) == bug
    st = explore(make([[("delete", 3)], [("insert", 2)]], keys, objs=objs, mark_parent=False),
                 lambda run, tr: None if 2 in objs[0].leaves() or results(run, 1) != [True] else "lost insert")
    assert st.failure is not None


def test_find_only_reads() -> None:
    objs = []
    run = Run(make([[("find", k) for k in range(8)]], (1, 3, 5, 6), objs=objs))
    run.finish(0)
    assert all(op[0] == "read" for _, op, _ in run.trace)
    assert results(run) == [k in (1, 3, 5, 6) for k in range(8)]


def balanced(lo, hi):
    """An insert order that gives a balanced tree for the keys lo..hi-1."""
    if lo >= hi:
        return []
    mid = (lo + hi) // 2
    return [mid] + balanced(lo, mid) + balanced(mid + 1, hi)


def test_solo_cost_is_two_steps_per_level_plus_seven() -> None:
    # Alone, a search reads update and a child at each internal node of the
    # path: 2 d steps for d internal nodes. An insert adds four allocations
    # and three CAS steps; a delete adds one allocation, two CAS steps, at
    # most two reads and two more CAS steps. So each update costs at most
    # 2 d + 7 steps and a find exactly 2 d.
    for n in (7, 31, 127):
        keys = [2 * k for k in balanced(0, n)]
        rng = random.Random(n)
        ops = [(rng.choice(["insert", "delete", "find"]), rng.randrange(2 * n + 2)) for _ in range(60)]
        objs = []
        run = Run(make([ops], keys, objs=objs))
        t = objs[0]
        for name, k in ops:
            d = t.internal_depth(k)
            steps = run.finish_op(0)
            assert steps <= 2 * d + 7, (name, k, d, steps)
            if name == "find":
                assert steps == 2 * d


def test_seeded_runs() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        procs = [[(rng.choice(["insert", "delete", "find"]), rng.randrange(6)) for _ in range(4)] for _ in range(3)]
        keys = tuple(sorted(set(rng.randrange(6) for _ in range(rng.randrange(4)))))
        objs = []
        run = random_run(make(procs, keys, objs=objs), seed, max_steps=4000)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, Spec(keys)) is not None, seed
        assert objs[0].check_shape() is None


def test_others_finish_when_an_updater_stops() -> None:
    # p0 stops right after its flag (or its mark). The others help its
    # operation to finish and then do their own.
    for stop in ("dflag", "mark", "iflag"):
        keys = (1, 3, 5)
        first = [("insert", 4)] if stop == "iflag" else [("delete", 3)]
        procs = [first, [("delete", 1), ("insert", 2), ("find", 3)], [("delete", 5), ("insert", 3)]]
        objs = []
        run = Run(make(procs, keys, objs=objs))
        run.until(0, lambda op: op[0] == "cmpxchg")
        run.step(0)
        if stop == "mark":
            run.step(0)
        assert run.finish(1) and run.finish(2)
        assert linearize(run.history, Spec(keys)) is not None, stop
        assert objs[0].check_shape() is None
