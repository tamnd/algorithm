# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-ordered-list/. The authors are listed in prov/XCTCZ1.jsonl.

import random

from explorer import NULL, Memory, Run, explore, program, random_run
from lincheck import SetSpec, lin_check, linearize
from split_ordered_list import MSB, SplitOrderedList, parent, reverse, so_dummy, so_regular


class Spec(SetSpec):
    def __init__(self, keys=()):
        self.init = frozenset(keys)


def make(procs, keys=(), objs=None, **flags):
    def setup():
        mem = Memory()
        t = SplitOrderedList(mem, keys, **flags)
        if objs is not None:
            objs[:] = [t]
        return mem, [program(t, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def all_reachable(t):
    out, n = [], t.mem.peek(("T", 0))
    while n != NULL:
        out.append(t.key(n))
        n = t.mem.peek((n, "next"))[0]
    return out


def check_structure(t):
    """The list is sorted by split-order key, and each bucket's keys are contiguous."""
    so = all_reachable(t)
    assert so == sorted(set(so)), so
    nodes = t.nodes()
    regs = [reverse(s) & ~MSB for s, d in nodes if not d]
    size = t.mem.peek("size")
    s = 1
    while s <= size:
        for b in range(s):
            pos = [i for i, k in enumerate(regs) if k % s == b]
            assert pos == list(range(pos[0], pos[0] + len(pos))) if pos else True, (s, b, regs)
        s *= 2
    order = [s for s, _ in nodes]
    dummies = t.dummies()
    for b in dummies:
        assert b < size
        i = order.index(so_dummy(b))
        j = i + 1
        while j < len(nodes) and not nodes[j][1]:
            j += 1
        seg = {reverse(s) & ~MSB for s, _ in nodes[i + 1:j]}
        assert {k for k in regs if k % size == b} <= seg, (b, size, regs)


def test_helpers() -> None:
    assert parent(1) == 0 and parent(2) == 0 and parent(3) == 1 and parent(6) == 2 and parent(13) == 5
    assert so_regular(1) % 2 == 1 and so_dummy(3) % 2 == 0
    # With 8 bits: dummy 1 = 10000000, key 1 = 10000001, dummy 5 = 10100000,
    # key 5 = 10100001, key 3 = 11000001. The keys 1 and 5 share bucket 1
    # while there are 2 or 4 buckets, and both follow dummy 1; with 8 buckets
    # dummy 5 goes between them.
    assert so_dummy(1) < so_regular(1) < so_dummy(5) < so_regular(5) < so_regular(3)


def test_random_sequential_with_growth() -> None:
    rng = random.Random(11)
    ops, model, want = [], set(), []
    for _ in range(400):
        k = rng.randrange(60)
        name = rng.choice(["insert", "insert", "delete", "contains"])
        ops.append((name, k))
        want.append(k not in model if name == "insert" else k in model)
        if name == "insert":
            model.add(k)
        elif name == "delete":
            model.discard(k)
    objs = []
    run = Run(make([ops], objs=objs, size=1, load=2))
    assert run.finish(0, limit=200000)
    assert results(run) == want
    t = objs[0]
    assert t.keys() == sorted(model)
    assert t.mem.peek("count") == len(model)
    assert t.mem.peek("size") >= 16
    check_structure(t)


def test_buckets_stay_contiguous_after_each_resize() -> None:
    objs = []
    run = Run(make([[("insert", k) for k in range(40)]], objs=objs, size=1, load=1))
    t = objs[0]
    sizes = set()
    while run.pending[0] is not None:
        run.finish_op(0)
        sizes.add(t.mem.peek("size"))
        check_structure(t)
        # Each resize moved nothing: the reachable nodes only ever gain nodes.
    assert sizes >= {2, 4, 8, 16, 32}


def test_resize_moves_no_node() -> None:
    # The successor of every regular node changes only when a node is linked
    # right after it: a resize is a single CAS on size and writes no next field.
    objs = []
    run = Run(make([[("insert", 1), ("insert", 2), ("insert", 3)]], objs=objs, size=1, load=1))
    run.finish(0)
    resize = [op for _, op, _ in run.trace if op[0] == "cas" and op[1] == "size"]
    assert resize and all(op[2] * 2 == op[3] for op in resize)


CASES = [
    # size 1, load 1: the second insert doubles the table, and the next
    # operations initialize bucket 1 at the same time.
    ((), [[("insert", 1), ("contains", 3)], [("insert", 3), ("contains", 1)]], 1),
    # size 2 with bucket 1 not yet initialized: two processes initialize it.
    ((0,), [[("insert", 1)], [("insert", 3), ("contains", 1)]], 2),
    ((0,), [[("insert", 2)], [("insert", 6)]], 4),
    ((1, 5), [[("delete", 1), ("contains", 5)], [("insert", 3)]], 4),
]


def test_exhaustive_small_cases() -> None:
    for keys, procs, size in CASES:
        objs = []
        st = explore(make(procs, keys, objs=objs, size=size, load=1), lin_check(Spec(keys)),
                     check_states=lambda run: None if all_reachable(objs[0]) == sorted(set(all_reachable(objs[0]))) else "unsorted")
        assert st.failure is None, (keys, st.failure)
        assert st.runs > 5


def test_publishing_a_bucket_early_loses_an_insert() -> None:
    # p0 initializes bucket 1, puts its dummy in T[1] and stops before it
    # links the dummy. p1 inserts 3 after that dummy. p0 then links the dummy
    # and sets its next field, and 3 is gone.
    keys, procs = (0,), [[("insert", 1)], [("insert", 3), ("contains", 3)]]
    st = explore(make(procs, keys, size=2, load=4, publish_early=True), lin_check(Spec(keys)))
    assert st.failure is not None
    objs = []
    run = Run(make(procs, keys, objs=objs, size=2, load=4, publish_early=True))
    run.until(0, lambda op: op[0] == "cas" and op[1] == ("T", 1))
    run.step(0)  # T[1] now points to a dummy that is not in the list
    run.finish_op(1)
    assert results(run, 1) == [True]
    assert run.finish(0)
    assert run.finish(1)
    assert results(run, 1) == [True, False]
    assert linearize(run.history, Spec(keys)) is None


def test_solo_cost_does_not_grow_with_n() -> None:
    # With the load bound kept, a contains alone walks one bucket: the cost
    # stays the same as the table grows (the hash here is the identity, so
    # each bucket holds one key). The first operation on a bucket may also
    # initialize it; later ones take 4 steps (size, T[b], the dummy's next,
    # the key's next).
    for n in (8, 16, 64):
        objs = []
        run = Run(make([[("contains", k) for k in range(n)] * 2], tuple(range(n)), objs=objs, size=1, load=1))
        assert objs[0].mem.peek("size") == n
        steps = [run.finish_op(0) for _ in range(2 * n)]
        assert max(steps[:n]) <= 13, (n, steps)
        assert max(steps[n:]) == 4, (n, steps)


def test_seeded_runs() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        procs = [[(rng.choice(["insert", "insert", "delete", "contains"]), rng.randrange(16)) for _ in range(5)] for _ in range(3)]
        keys = tuple(k for k in range(16) if rng.random() < 0.3)
        objs = []
        run = random_run(make(procs, keys, objs=objs, size=1, load=1), seed, max_steps=5000)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, Spec(keys)) is not None, seed
        check_structure(objs[0])
        assert objs[0].mem.peek("count") == len(objs[0].keys())
