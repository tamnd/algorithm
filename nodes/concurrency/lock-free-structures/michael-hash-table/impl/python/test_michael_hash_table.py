# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/michael-hash-table/. The authors are listed in prov/Z81DZW.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from lincheck import SetSpec, lin_check, linearize
from michael_hash_table import Handle, MichaelHashTable


class Spec(SetSpec):
    def __init__(self, keys=()):
        self.init = frozenset(keys)


def make(procs, keys=(), m=2, objs=None, reuse=True, **flags):
    def setup():
        mem = Memory(reuse=reuse)
        t = MichaelHashTable(mem, m, keys, nprocs=len(procs), **flags)
        if objs is not None:
            objs[:] = [t]
        return mem, [program(Handle(t, p), ops) for p, ops in enumerate(procs)]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def no_uaf(run):
    return "use after free: %r" % run.mem.uaf if run.mem.uaf else None


def test_random_sequential_against_set() -> None:
    rng = random.Random(7)
    ops, model, want = [], set(), []
    for _ in range(300):
        k = rng.randrange(12)
        name = rng.choice(["insert", "delete", "contains"])
        ops.append((name, k))
        want.append(k not in model if name == "insert" else k in model)
        if name == "insert":
            model.add(k)
        elif name == "delete":
            model.discard(k)
    objs = []
    run = Run(make([ops], m=3, objs=objs))
    assert run.finish(0, limit=100000)
    assert results(run) == want
    assert objs[0].keys() == sorted(model)
    for i in range(3):
        assert objs[0].bucket_keys(i) == sorted(k for k in model if k % 3 == i)
    assert not run.mem.uaf


# With m = 2, the odd keys share bucket 1 and the even keys share bucket 0.
CASES = [
    ((1, 5), [[("delete", 1)], [("insert", 3), ("contains", 3)]]),
    ((1, 3), [[("delete", 1)], [("delete", 3), ("contains", 1)]]),
    ((1, 3, 5), [[("delete", 3)], [("delete", 1)]]),
    ((), [[("insert", 1), ("delete", 1)], [("insert", 1), ("contains", 1)]]),
    ((1,), [[("delete", 1), ("insert", 3)], [("contains", 1), ("insert", 1)]]),
    ((1, 2), [[("delete", 1)], [("insert", 3), ("contains", 2)]]),
]


def test_exhaustive_linearizable_and_no_use_after_free() -> None:
    # Memory is reused as soon as a node is freed, and each retire scans (R = 1).
    for keys, procs in CASES:
        st = explore(make(procs, keys), lin_check(Spec(keys)), check_states=no_uaf)
        assert st.failure is None, (keys, st.failure)
        assert st.runs > 5


def first_node(t, i):
    return t.mem.peek(("bucket", i))[0]


def test_without_hazard_pointers_a_reader_uses_a_freed_node() -> None:
    # Bucket 1 is 1 -> 3. p0 runs contains(3) and is about to read node 1.
    # p1 deletes 1 and, with no hazard pointers, frees it at once.
    procs = [[("contains", 3)], [("delete", 1), ("delete", 3)]]
    objs = []
    run = Run(make(procs, (1, 3), objs=objs, hazard=False))
    n1 = first_node(objs[0], 1)
    run.until(0, lambda op: op == ("read", (n1, "next")))
    run.finish_op(1)
    assert n1 not in run.mem.live
    assert run.pending[0] == ("read", (n1, "next"))  # the next step of p0 reads freed memory
    # The same schedule with hazard pointers: p0's hp1 holds node 1, so the
    # scan of p1 keeps it, and p0 goes on safely.
    objs = []
    run = Run(make(procs, (1, 3), objs=objs))
    n1 = first_node(objs[0], 1)
    run.until(0, lambda op: op == ("read", (n1, "next")))
    run.finish_op(1)
    assert n1 in run.mem.live and objs[0].retired[1] == [n1]
    assert run.finish(0)
    assert results(run, 0) == [True]
    n3 = first_node(objs[0], 1)
    run.finish(1)  # delete(3) retires node 3 and scans: node 1 is now free
    assert n1 not in run.mem.live
    assert n3 in run.mem.live  # p0's hp1 still holds node 3
    assert not run.mem.uaf
    assert linearize(run.history, Spec((1, 3))) is not None


def test_buckets_do_not_share_words() -> None:
    # An operation on key k touches only bucket k mod m, its nodes and the
    # hazard pointers.
    objs = []
    run = Run(make([[("insert", 4), ("delete", 2), ("contains", 6)]], (2, 6, 1, 3), m=2, objs=objs))
    odd = set()
    n = first_node(objs[0], 1)
    while n:
        odd.add(n)
        n = objs[0].mem.peek((n, "next"))[0]
    assert run.finish(0)
    for _, op, _ in run.trace:
        w = op[1]
        assert w != ("bucket", 1) and not (isinstance(w, tuple) and w[0] in odd), op


def test_solo_operations_are_bounded() -> None:
    # Alone, FIND takes 3 steps to start and 7 for each node it passes:
    # at most 7b + 10 steps for an operation on a bucket of b nodes.
    for b in (0, 1, 4, 10):
        keys = tuple(2 * i for i in range(b))  # all in bucket 0 when m = 2
        for name, k in (("contains", 2 * b), ("insert", 2 * b), ("delete", 2 * b - 2)):
            if k < 0:
                continue
            run = Run(make([[(name, k)]], keys))
            steps = run.finish_op(0)
            assert steps is not None and steps <= 7 * b + 10, (name, b, steps)


def test_seeded_runs_with_reuse() -> None:
    for seed in range(80):
        rng = random.Random(seed)
        P, R = 3, 2
        procs = [[(rng.choice(["insert", "delete", "contains"]), rng.randrange(6)) for _ in range(5)] for _ in range(P)]
        keys = tuple(k for k in range(6) if rng.random() < 0.5)
        objs = []
        run = random_run(make(procs, keys, m=2, objs=objs, R=R), seed)
        assert all(op is None for op in run.pending)
        assert not run.mem.uaf, seed
        assert linearize(run.history, Spec(keys)) is not None, seed
        t = objs[0]
        # A scan keeps only nodes that some hazard pointer holds.
        for p in range(P):
            assert len(t.retired[p]) <= 3 * P + R - 1
        # Every live node is in the table or retired and not yet freed.
        in_table = set()
        for i in range(2):
            n = first_node(t, i)
            while n:
                in_table.add(n)
                n = t.mem.peek((n, "next"))[0]
        assert run.mem.live <= in_table | {n for r in t.retired for n in r}
