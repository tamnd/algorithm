# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xjoin/. The authors are listed in prov/NRZ4EB.jsonl.

import random
from collections import Counter

import dbrel
from xjoin import BLOCK, R, S, XJoin, xjoin


def oracle(schema_r, schema_s, r_rows, s_rows):
    return dbrel.natural_join(dbrel.Relation(schema_r, r_rows), dbrel.Relation(schema_s, s_rows)).rows


def sub_bag(a: Counter, b: Counter) -> bool:
    return all(b[t] >= c for t, c in a.items())


def random_events(rng, r_rows, s_rows, p_block):
    tags = [R] * len(r_rows) + [S] * len(s_rows)
    rng.shuffle(tags)
    it = {R: iter(r_rows), S: iter(s_rows)}
    events = []
    for side in tags:
        if rng.random() < p_block:
            events.append((BLOCK,))
        events.append((side, next(it[side])))
    return events


def run_and_check(schema_r, schema_s, events, partitions, memory):
    j = XJoin(schema_r, schema_s, partitions, memory)
    seen = {R: [], S: []}
    out = Counter()
    for e in events:
        if e[0] == BLOCK:
            out.update(j.blocked())
        else:
            out.update(j.arrive(e[0], e[1]))
            seen[e[0]].append(tuple(e[1]))
        # Never a tuple that is not in the join of the prefixes, never twice.
        assert sub_bag(out, oracle(schema_r, schema_s, seen[R], seen[S]))
        assert j.in_memory <= memory
    out.update(j.finish())
    assert out == oracle(schema_r, schema_s, seen[R], seen[S])
    return j, out


def test_page_example() -> None:
    events = [(R, (1, 10)), (S, (10, "p")), (R, (2, 10)), (R, (3, 10)), (BLOCK,),
              (S, (10, "q")), (BLOCK,), (R, (4, 10)), (S, (10, "s"))]
    steps, j = xjoin(("A", "B"), ("B", "C"), events, partitions=1, memory=3)
    assert [len(x) for x in steps] == [0, 1, 1, 1, 0, 0, 3, 2, 1, 3]
    assert j.stats == {"stage1": 6, "stage2": 3, "stage3": 3, "disk_writes": 6, "disk_reads": 12}
    assert steps[-1] == [(1, 10, "s"), (2, 10, "s"), (3, 10, "s")]
    assert [r.dts for r in j.disk[R][0]] == [5, 5, 5] and j.hist[R][0] == [6, 8]
    run_and_check(("A", "B"), ("B", "C"), events, 1, 3)


def test_large_memory_is_symmetric_hash_join() -> None:
    rng = random.Random(3)
    r_rows = dbrel.random_relation(rng, ("A", "B"), 20, 3).sorted_rows()
    s_rows = dbrel.random_relation(rng, ("B", "C"), 20, 3).sorted_rows()
    events = random_events(rng, r_rows, s_rows, 0.0)
    j = XJoin(("A", "B"), ("B", "C"), 3, 1000)
    seen = {R: [], S: []}
    out = Counter()
    for e in events:
        out.update(j.arrive(e[0], e[1]))
        seen[e[0]].append(e[1])
        assert out == oracle(("A", "B"), ("B", "C"), seen[R], seen[S])
    assert j.finish() == [] and j.stats["disk_writes"] == 0


def test_hand_cases() -> None:
    # Empty input, one tuple, NULL keys, and all tuples with one key under tiny memory.
    assert xjoin(("A", "B"), ("B", "C"), [])[0] == [[]]
    assert xjoin(("A", "B"), ("B", "C"), [(R, (1, 2))])[0] == [[], []]
    run_and_check(("A", "B"), ("B", "C"), [(R, (1, None)), (S, (None, 1)), (BLOCK,)], 2, 1)
    events = [(R, (i, 0)) for i in range(5)] + [(BLOCK,)] + [(S, (0, k)) for k in range(4)] + [(BLOCK,)] * 3
    j, out = run_and_check(("A", "B"), ("B", "C"), events, 2, 2)
    assert sum(out.values()) == 20


def test_random_runs() -> None:
    schemas = [(("A", "B"), ("B", "C")), (("A", "B", "C"), ("B", "C", "D")), (("A",), ("A",))]
    used = Counter()
    for seed in range(80):
        rng = random.Random(seed)
        schema_r, schema_s = schemas[seed % len(schemas)]
        r_rows = dbrel.random_relation(rng, schema_r, rng.randrange(0, 22), 3, null_rate=0.05).sorted_rows()
        s_rows = dbrel.random_relation(rng, schema_s, rng.randrange(0, 22), 3, null_rate=0.05).sorted_rows()
        rng.shuffle(r_rows)
        rng.shuffle(s_rows)
        events = random_events(rng, r_rows, s_rows, rng.choice([0.0, 0.2, 0.5]))
        j, _ = run_and_check(schema_r, schema_s, events, rng.randrange(1, 5), rng.randrange(1, 10))
        for stage in ("stage1", "stage2", "stage3"):
            used[stage] += j.stats[stage] > 0
    # The random runs exercise all three stages.
    assert all(used[s] > 10 for s in ("stage1", "stage2", "stage3"))


def test_without_timestamps_pairs_repeat() -> None:
    # The duplicate test is needed: without it some pair is emitted twice.
    repeated = 0
    for seed in range(30):
        rng = random.Random(seed)
        r_rows = dbrel.random_relation(rng, ("A", "B"), 15, 3).sorted_rows()
        s_rows = dbrel.random_relation(rng, ("B", "C"), 15, 3).sorted_rows()
        events = random_events(rng, r_rows, s_rows, 0.3)
        steps, _ = xjoin(("A", "B"), ("B", "C"), events, 2, 4, avoid_duplicates=False)
        out = Counter(t for x in steps for t in x)
        assert sub_bag(oracle(("A", "B"), ("B", "C"), r_rows, s_rows), out)
        repeated += out != oracle(("A", "B"), ("B", "C"), r_rows, s_rows)
    assert repeated > 20
