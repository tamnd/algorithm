# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-skip-list/. The authors are listed in prov/BMT1MG.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from lincheck import SetSpec, lin_check, linearize
from lock_free_skip_list import LockFreeSkipList


class Spec(SetSpec):
    def __init__(self, keys=()):
        self.init = frozenset(keys)


def make(procs, keys=(), objs=None, **flags):
    def setup():
        mem = Memory()
        s = LockFreeSkipList(mem, keys, **flags)
        if objs is not None:
            objs[:] = [s]
        return mem, [program(s, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def check_levels(s):
    """Each level is sorted, and each unmarked node of a level is in the level below."""
    for i in range(s.maxl):
        allk = s.level_keys(i, unmarked=False)
        assert allk == sorted(set(allk)), (i, allk)
    for i in range(1, s.maxl):
        assert set(s.level_keys(i)) <= set(s.level_keys(i - 1)) | set(s.level_keys(i - 1, unmarked=False))


def test_random_sequential_against_set() -> None:
    rng = random.Random(2)
    ops, model, want = [], set(), []
    for _ in range(400):
        k = rng.randrange(30)
        name = rng.choice(["add", "remove", "contains"])
        ops.append((name, k))
        want.append(k not in model if name == "add" else k in model)
        if name == "add":
            model.add(k)
        elif name == "remove":
            model.discard(k)
    objs = []
    run = Run(make([ops], objs=objs, maxl=4))
    assert run.finish(0, limit=200000)
    assert results(run) == want
    s = objs[0]
    assert s.keys() == sorted(model)
    check_levels(s)
    # Alone, remove unlinks the node at every level.
    for i in range(4):
        assert s.level_keys(i, unmarked=False) == [k for k in sorted(model) if s.level(k) >= i]


T = {1: 1, 2: 0, 3: 1, 4: 1}  # the top level of each key in the small cases (maxl = 2)
CASES = [
    ((1, 3), [[("remove", 1)], [("add", 2), ("contains", 2)]]),
    ((), [[("add", 1), ("remove", 1)], [("add", 3), ("contains", 1)]]),
    ((1,), [[("remove", 1)], [("remove", 1)]]),
    ((3,), [[("add", 1)], [("remove", 3), ("contains", 1)]]),
    ((), [[("add", 3)], [("add", 1), ("remove", 3)]]),
]


def test_exhaustive_small_cases() -> None:
    for keys, procs in CASES:
        objs = []
        st = explore(make(procs, keys, objs=objs, maxl=2, levels=T), lin_check(Spec(keys)))
        assert st.failure is None, (keys, st.failure)
        assert st.runs > 5


def test_deciding_at_the_top_level_lets_two_removes_win() -> None:
    # p0 marks level 1 of node 1 and stops. p1 sees level 1 marked, marks
    # level 0 and returns True. If p0 counts its top-level mark as a win, it
    # returns True too: one key removed twice.
    keys, procs = (1,), [[("remove", 1)], [("remove", 1)]]
    st = explore(make(procs, keys, maxl=2, levels=T, decide_at_top=True), lin_check(Spec(keys)))
    assert st.failure is not None
    for bad in (True, False):
        objs = []
        run = Run(make(procs, keys, objs=objs, maxl=2, levels=T, decide_at_top=bad))
        run.until(0, lambda op: op[0] == "cas")
        run.step(0)  # p0 marks level 1
        assert run.finish(1)
        assert run.finish(0)
        assert results(run, 1) == [True]
        assert results(run, 0) == [bad]
        assert (linearize(run.history, Spec(keys)) is None) == bad


def test_a_late_add_can_link_a_removed_node() -> None:
    # p0 adds 1 (top level 1), links level 0 and stops before its CAS at
    # level 1. p1 removes 1 completely. p0 then links the removed node at
    # level 1. The set is still right (the node is marked), and the next
    # find of 1 unlinks it. So a node is not garbage when its remover returns.
    objs = []
    run = Run(make([[("add", 1)], [("remove", 1)], [("remove", 1)]], objs=objs, maxl=2, levels={1: 1}))
    run.until(0, lambda op: op[0] == "cas" and op[1][1] == "l1")
    assert run.finish(1)
    assert run.finish(0)
    s = objs[0]
    assert s.level_keys(0, unmarked=False) == [] and s.level_keys(1, unmarked=False) == [1]
    assert s.keys() == []
    assert run.finish(2)
    assert s.level_keys(1, unmarked=False) == []
    assert results(run) == [True, True, False]
    assert linearize(run.history, Spec()) is not None


def test_contains_never_writes() -> None:
    objs = []
    run = Run(make([[("contains", k) for k in range(12)]], tuple(range(0, 12, 2)), objs=objs, maxl=3))
    run.finish(0)
    assert results(run) == [k % 2 == 0 for k in range(12)]
    assert all(op[0] == "read" for _, op, _ in run.trace)


def test_solo_search_uses_the_levels() -> None:
    # A perfect skip list: n = 2^L - 1 keys, key k at level = trailing ones
    # of k, L levels. A contains alone reads at most 3L - 1 words: two at
    # the first node of each level and at most one more step to the right.
    # That is O(log n), far fewer than n.
    for L in (4, 6, 8, 10):
        n = 2 ** L - 1
        run = Run(make([[("contains", k) for k in range(n)]], tuple(range(n)), maxl=L))
        steps = [run.finish_op(0) for _ in range(n)]
        assert max(steps) <= 3 * L - 1, (n, max(steps))


def test_seeded_runs() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        procs = [[(rng.choice(["add", "remove", "contains"]), rng.randrange(8)) for _ in range(5)] for _ in range(3)]
        keys = tuple(k for k in range(8) if rng.random() < 0.5)
        objs = []
        run = random_run(make(procs, keys, objs=objs, maxl=3), seed, max_steps=5000)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, Spec(keys)) is not None, seed
        check_levels(objs[0])


def test_others_finish_when_a_remover_stops() -> None:
    # p0 stops after it marked level 0 of node 3. The others skip or unlink
    # node 3 and finish.
    keys = (1, 3, 5)
    procs = [[("remove", 3)], [("add", 4), ("contains", 3), ("add", 3)], [("contains", 5), ("remove", 5)]]
    objs = []
    run = Run(make(procs, keys, objs=objs, maxl=2, levels={1: 1, 3: 1, 4: 0, 5: 1}))
    run.until(0, lambda op: op[0] == "cas" and op[1][1] == "l0")
    run.step(0)
    assert run.finish(1) and run.finish(2)
    assert results(run, 1) == [True, False, True]
    assert results(run, 2) == [True, True]
    assert objs[0].keys() == [1, 3, 4]
    assert linearize(run.history, Spec(keys)) is not None
