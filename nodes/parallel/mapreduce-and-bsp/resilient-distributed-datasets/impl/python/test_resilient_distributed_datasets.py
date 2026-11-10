# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resilient-distributed-datasets/. The authors are listed in prov/RWTK7Z.jsonl.

import random
from fractions import Fraction

from resilient_distributed_datasets import Context, pagerank_rdd


def test_transformations_match_plain_python():
    rng = random.Random(1)
    for _ in range(30):
        data = [(rng.randint(0, 9), rng.randint(-5, 5)) for _ in range(rng.randint(0, 40))]
        P = rng.randint(1, 5)
        ctx = Context()
        r = ctx.parallelize(data, P)
        assert r.collect() == data
        assert r.map(lambda kv: (kv[0], 2 * kv[1])).collect() == [(k, 2 * v) for k, v in data]
        assert r.filter(lambda kv: kv[1] > 0).collect() == [kv for kv in data if kv[1] > 0]
        sums = {}
        for k, v in data:
            sums[k] = sums.get(k, 0) + v
        got = r.reduce_by_key(lambda a, b: a + b, rng.randint(1, 4)).collect()
        assert sorted(got) == sorted(sums.items())
        other = [(rng.randint(0, 9), rng.randint(0, 3)) for _ in range(10)]
        o = ctx.parallelize(other, rng.randint(1, 4))
        want = sorted((k, (v, w)) for k, v in data for k2, w in other if k == k2)
        assert sorted(r.join(o).collect()) == want
        # The co-partitioned join is narrow and gives the same answer.
        a, b = r.partition_by(3), o.partition_by(3)
        j = a.join(b)
        assert [kind for _, kind in j.deps] == ["narrow", "narrow"]
        assert sorted(j.collect()) == want


def test_lazy_evaluation():
    ctx = Context()
    r = ctx.parallelize(list(range(10)), 2).map(lambda x: x + 1, name="m")
    assert ctx.computed == {}
    r.collect()
    assert ctx.computed == {"input": 2, "m": 2}


def test_narrow_recovery_recomputes_only_lost_partitions():
    for seed in range(40):
        rng = random.Random(seed)
        P = rng.randint(1, 8)
        ctx = Context()
        data = list(range(50))
        a = ctx.parallelize(data, P).map(lambda x: x * x, name="a").persist()
        b = a.map(lambda x: x + 1, name="b")
        first = b.collect()
        assert ctx.computed == {"input": P, "a": P, "b": P}
        lost = ctx.lose(rng, 0.4)
        assert b.collect() == first
        # b is not persisted, so it runs again; a and its input run only for the lost partitions.
        assert ctx.computed == {"input": P + lost, "a": P + lost, "b": 2 * P}


def test_wide_recovery_needs_all_parent_partitions():
    for seed in range(40):
        rng = random.Random(seed)
        P = rng.randint(2, 6)
        for persist_parent in (True, False):
            ctx = Context()
            data = [(i % 7, i) for i in range(60)]
            a = ctx.parallelize(data, P).map(lambda kv: kv, name="a")
            if persist_parent:
                a.persist()
            c = a.reduce_by_key(lambda x, y: x + y, P, name="c").persist()
            first = c.collect()
            assert ctx.computed["a"] == P  # each parent partition once, for all child partitions
            # Lose one partition of c: the stored shuffle outputs rebuild it.
            before = dict(ctx.computed)
            del ctx.cache[(c.id, 0)]
            assert c.collect() == first
            assert ctx.computed["c"] - before["c"] == 1
            assert ctx.computed["a"] == before["a"]
            # Lose it again with all shuffle outputs: every parent partition is needed.
            before = dict(ctx.computed)
            del ctx.cache[(c.id, 0)]
            ctx.shuffle.clear()
            assert c.collect() == first
            assert ctx.computed["a"] - before["a"] == (0 if persist_parent else P)


def test_checkpoint_cuts_the_lineage():
    ctx = Context()
    r = ctx.parallelize(list(range(20)), 4)
    for t in range(10):
        r = r.map(lambda x: x + 1, name="m%d" % t)
    assert r.lineage_depth() == 11
    want = r.collect()
    r.checkpoint()
    assert r.lineage_depth() == 1
    before = dict(ctx.computed)
    ctx.cache.clear()
    assert r.map(lambda x: x, name="after").collect() == want
    assert all(ctx.computed[k] == before[k] for k in before)


def test_nondeterministic_operations_break_recovery():
    differ = 0
    for seed in range(20):
        noise = random.Random(seed)
        ctx = Context()
        a = ctx.parallelize(list(range(30)), 3).map(lambda x: x + noise.randint(0, 1), name="a").persist()
        first = a.collect()
        ctx.cache.clear()
        differ += a.collect() != first
    assert differ > 0


def power_iteration(n, links, k, alpha):
    x = [Fraction(1, n)] * n
    for _ in range(k):
        y = [alpha / n] * n
        for u, targets in links:
            for v in targets:
                y[v] += (1 - alpha) * x[u] / len(targets)
        x = y
    return x


def test_pagerank_lineage_and_recovery():
    rng = random.Random(3)
    alpha = Fraction(15, 100)
    for _ in range(12):
        n = rng.randint(2, 12)
        links = []
        for u in range(n):
            t = {(u + 1) % n} | {rng.randrange(n) for _ in range(rng.randint(0, 3))}
            links.append((u, sorted(t)))
        k = rng.randint(1, 5)
        P = rng.randint(1, 4)
        ctx = Context()
        ranks, links_rdd = pagerank_rdd(ctx, links, n, k, alpha, P)
        want = power_iteration(n, links, k, alpha)
        got = dict(ranks.collect())
        assert [got[v] for v in range(n)] == want
        # The links RDD is the only persisted one, so the input is read once.
        assert ctx.computed["input"] == P
        # Lose cached partitions of links; the answer is the same.
        ctx.lose(rng, 0.5)
        got = dict(ranks.collect())
        assert [got[v] for v in range(n)] == want
        assert ranks.lineage_depth() == 3 + 4 * k


def test_pagerank_drops_a_vertex_with_no_in_link():
    # The worked example of the page: vertex 3 has no in-link.
    alpha = Fraction(15, 100)
    links = [(0, [1, 2]), (1, [2]), (2, [0]), (3, [0, 2])]
    ranks, _ = pagerank_rdd(Context(), links, 4, 3, alpha, 2)
    got = dict(ranks.collect())
    assert sorted(got) == [0, 1, 2]
    assert got != dict(enumerate(power_iteration(4, links, 3, alpha)[:3]))
    # With the edge 2 -> 3 added, every vertex has an in-link and the answer is exact.
    links[2] = (2, [0, 3])
    ranks, _ = pagerank_rdd(Context(), links, 4, 3, alpha, 2)
    got = dict(ranks.collect())
    assert [got[v] for v in range(4)] == power_iteration(4, links, 3, alpha)
