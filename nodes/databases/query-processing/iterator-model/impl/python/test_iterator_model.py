# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterator-model/. The authors are listed in prov/4TQNVH.jsonl.

import random
from collections import Counter

from iterator_model import (
    HashAggregate,
    HashJoin,
    Limit,
    NestedLoopJoin,
    Project,
    Scan,
    Select,
    Sort,
    run,
)


def rand_rel(rng, n, arity, dom):
    return [tuple(rng.randrange(dom) for _ in range(arity)) for _ in range(n)]


def test_plan_equals_direct_evaluation():
    """pi_(a,d) (sigma_(a<3) R join_(R.b=S.b) S join_(S.c=T.c) T) as a multiset."""
    rng = random.Random(7)
    for trial in range(500):
        R = rand_rel(rng, rng.randrange(8), 2, 5)  # (a, b)
        S = rand_rel(rng, rng.randrange(8), 2, 5)  # (b, c)
        T = rand_rel(rng, rng.randrange(8), 2, 5)  # (c, d)
        want = Counter(
            (a, d) for (a, b) in R if a < 3 for (b2, c) in S if b == b2 for (c2, d) in T if c == c2
        )
        rs = HashJoin(Select(Scan(R), lambda t: t[0] < 3), Scan(S), lambda t: t[1], lambda t: t[0])
        if trial % 2:
            rs = NestedLoopJoin(Select(Scan(R), lambda t: t[0] < 3), Scan(S), lambda r, s: r[1] == s[0])
        rst = NestedLoopJoin(rs, Scan(T), lambda x, t: x[3] == t[0])
        plan = Project(rst, [0, 5])
        assert Counter(run(plan)) == want
        # The same plan can run twice: open resets the state.
        assert Counter(run(plan)) == want


def test_sort_and_aggregate():
    rng = random.Random(3)
    for _ in range(300):
        R = rand_rel(rng, rng.randrange(12), 2, 4)
        assert run(Sort(Scan(R), key=lambda t: t)) == sorted(R)
        got = Counter(run(HashAggregate(Scan(R), [0])))
        want = Counter((a, c) for a, c in Counter(t[0] for t in R).items())
        assert got == want


def test_pipelining_pulls_only_what_is_needed():
    base = Scan([(i,) for i in range(1000)])
    out = run(Limit(Select(base, lambda t: t[0] % 10 == 0), 3))
    assert out == [(0,), (10,), (20,)]
    assert base.produced == 21  # the scan stopped after the third match


def test_blocking_sort_reads_everything():
    base = Scan([(i,) for i in range(1000)])
    out = run(Limit(Sort(base, key=lambda t: -t[0]), 1))
    assert out == [(999,)]
    assert base.produced == 1000


def test_hash_join_build_is_blocking_and_probe_is_pipelined():
    build = Scan([(i, i) for i in range(50)])
    probe = Scan([(i % 50,) for i in range(500)])
    out = run(Limit(HashJoin(build, probe, lambda t: t[0], lambda t: t[0]), 2))
    assert out == [(0, 0, 0), (1, 1, 1)]
    assert build.produced == 50 and probe.produced == 2


def test_nested_loop_rescans_inner():
    outer, inner = Scan([(1,), (2,), (3,)]), Scan([(1,), (3,)])
    out = run(NestedLoopJoin(outer, inner, lambda r, s: r[0] == s[0]))
    assert out == [(1, 1), (3, 3)]
    assert inner.opens == 3 and inner.produced == 6


def test_empty_inputs():
    assert run(Scan([])) == []
    assert run(NestedLoopJoin(Scan([]), Scan([(1,)]), lambda r, s: True)) == []
    assert run(HashJoin(Scan([]), Scan([(1,)]), lambda t: t, lambda t: t)) == []
    assert run(Limit(Scan([(1,)]), 0)) == []
