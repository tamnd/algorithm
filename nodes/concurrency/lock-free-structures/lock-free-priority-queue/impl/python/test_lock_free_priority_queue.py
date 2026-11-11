# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-priority-queue/. The authors are listed in prov/F7GS7Y.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from lincheck import EMPTY, lin_check, linearize
from lock_free_priority_queue import LindenJonssonPQ


class Spec:
    """A priority queue of keys that may repeat: insert returns True, delete_min the least key or EMPTY."""

    def __init__(self, keys=()):
        self.init = tuple(sorted(keys))

    def step(self, s, name, arg):
        if name == "insert":
            return [(tuple(sorted(s + (arg[0],))), True)]
        if name == "delete_min":
            return [(s[1:], s[0])] if s else [(s, EMPTY)]
        raise ValueError(name)


def make(procs, keys=(), objs=None, **flags):
    def setup():
        mem = Memory()
        q = LindenJonssonPQ(mem, keys, **flags)
        if objs is not None:
            objs[:] = [q]
        return mem, [program(q, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def sequential_ops(seed, n, kmax):
    rng = random.Random(seed)
    ops, model, want = [], [], []
    for _ in range(n):
        if rng.random() < 0.55:
            k = rng.randrange(kmax)
            ops.append(("insert", k))
            model.append(k)
            want.append(True)
        else:
            ops.append(("delete_min",))
            if model:
                m = min(model)
                model.remove(m)
                want.append(m)
            else:
                want.append(EMPTY)
    return ops, sorted(model), want


def test_random_sequential_against_a_heap() -> None:
    ops, model, want = sequential_ops(1, 300, 40)
    for bound in (0, 1, 3):
        objs = []
        run = Run(make([ops], objs=objs, maxl=4, bound=bound))
        assert run.finish(0, limit=100000)
        assert results(run) == want
        q = objs[0]
        assert q.live_keys() == model
        assert q.prefix_length() <= bound + 1


T = {1: 1, 2: 0, 3: 1, 4: 0}  # top levels with maxl = 2
CASES = [
    ((2,), [[("insert", 1)], [("delete_min",)]], 1),
    ((), [[("insert", 2)], [("insert", 1), ("delete_min",)]], 1),
    ((1, 3), [[("delete_min",)], [("delete_min",)]], 0),
    ((1, 3), [[("delete_min",), ("delete_min",)], [("insert", 2)]], 0),
    ((1, 2), [[("delete_min",)], [("insert", 1), ("delete_min",)]], 0),
    ((), [[("insert", 3), ("delete_min",)], [("insert", 1), ("delete_min",)]], 0),
]


def test_exhaustive_small_cases() -> None:
    for keys, procs, bound in CASES:
        objs = []
        st = explore(make(procs, keys, objs=objs, maxl=2, levels=T, bound=bound), lin_check(Spec(keys)),
                     check_states=lambda run: None if objs[0].live_keys() == sorted(objs[0].live_keys()) else "unsorted")
        assert st.failure is None, (keys, procs, st.failure)
        assert st.runs > 5


def test_a_deletion_flag_in_the_node_loses_an_insert() -> None:
    # p0 deletes 1. p1 inserts 0: it finds pred = node 1 (deleted) and
    # succ = node 2, and stops before its CAS. p0 deletes 2 and stops before
    # it cuts the prefix. p1 links 0 after node 1. p0 moves the head past
    # node 1, and node 0 is gone. With the mark in the predecessor's pointer,
    # p0's delete of 2 marked node 1's pointer, so p1's CAS fails and p1
    # searches again.
    keys = (1, 2, 3)
    procs = [[("delete_min",), ("delete_min",), ("delete_min",)], [("insert", 0)]]
    for bug in (False, True):
        objs = []
        run = Run(make(procs, keys, objs=objs, maxl=2, levels=T, bound=0, flag_in_node=bug))
        q = objs[0]
        run.finish_op(0)
        run.until(1, lambda op: op[0] == "cas")
        run.until(0, lambda op: op[0] == "cas" and op[1] == (q.head, "l0"))
        assert run.finish(1) and run.finish(0)
        assert results(run, 0) == ([1, 2, 3] if bug else [1, 2, 0])
        assert (linearize(run.history, Spec(keys)) is None) == bug
    st = explore(make([[("delete_min",), ("delete_min",), ("delete_min",)], [("insert", 0)]], (1, 2),
                      maxl=1, bound=0, flag_in_node=True), lin_check(Spec((1, 2))))
    assert st.failure is not None


def test_delete_min_writes_one_word_besides_the_head() -> None:
    # Alone, each delete_min changes exactly one pointer that is not in the
    # head: the one its fetch-and-or marks. Its other writes go to the head.
    ops, _, _ = sequential_ops(5, 200, 30)
    objs = []
    run = Run(make([ops], objs=objs, maxl=3, bound=2))
    run.finish(0, limit=100000)
    q = objs[0]
    pos = 0
    for (_, name, n), want in zip(run.op_steps, results(run)):
        steps = run.trace[pos:pos + n]
        pos += n
        if name != "delete_min":
            continue
        assert all(op[0] in ("read", "mark", "cas") for _, op, _ in steps)
        changed = [op for _, op, v in steps if op[0] == "mark" and not v[1]]
        assert len(changed) == (0 if want == EMPTY else 1)
        assert all(op[1][0] == q.head for _, op, _ in steps if op[0] == "cas")


def test_solo_cost() -> None:
    # Alone, delete_min walks the deleted prefix (at most bound + 1 nodes,
    # three steps each) and may then move the head pointers (a few steps per
    # level). Measured: at most 3 (bound + 2) + 2 + 5 L steps. An insert
    # alone costs O(L) steps in a perfect skip list, as in any skip list.
    for L in (4, 6, 8):
        n = 2 ** L - 1
        for bound in (0, 2, 4):
            ops = [("delete_min",)] * (n + 1)
            run = Run(make([ops], tuple(range(n)), maxl=L, bound=bound))
            steps = [run.finish_op(0) for _ in ops]
            assert max(steps) <= 3 * (bound + 2) + 2 + 5 * L, (L, bound, max(steps))
    run = Run(make([[("insert", k) for k in range(1, 64)]], (0,), maxl=6))
    steps = [run.finish_op(0) for _ in range(63)]
    assert max(steps) <= 8 * 6 + 8, max(steps)


def test_seeded_runs() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        procs = [[("insert", rng.randrange(8)) if rng.random() < 0.5 else ("delete_min",) for _ in range(5)]
                 for _ in range(3)]
        keys = tuple(rng.randrange(8) for _ in range(rng.randrange(5)))
        objs = []
        run = random_run(make(procs, keys, objs=objs, maxl=3, bound=seed % 3), seed, max_steps=5000)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, Spec(keys)) is not None, seed
        live = objs[0].live_keys()
        assert live == sorted(live)


def test_others_finish_when_a_deleter_stops() -> None:
    # p0 stops right after its fetch-and-or. The others go on.
    procs = [[("delete_min",)], [("insert", 0), ("delete_min",), ("delete_min",)], [("delete_min",), ("insert", 5)]]
    run = Run(make(procs, (1, 2, 3), maxl=2, levels=T, bound=0))
    run.until(0, lambda op: op[0] == "mark")
    run.step(0)
    assert run.finish(1) and run.finish(2)
    assert linearize(run.history, Spec((1, 2, 3))) is not None
