# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-hash-join/. The authors are listed in prov/Y1EV4Y.jsonl.

import random
from collections import Counter

from dbrel import Relation, evaluate
from radix_hash_join import count_misses, h, radix_cluster, radix_join

PASSES = ([], [1], [2], [1, 1], [3, 2], [2, 2, 2], [6])


def oracle(r_rows, s_rows):
    """The bag join by dbrel, with the columns in the order (k, a, k, b)."""
    db = {"R": Relation(("k", "a"), r_rows), "S": Relation(("k", "b"), s_rows)}
    res = evaluate(("join", ("scan", "R"), ("scan", "S")), db).reorder(("k", "a", "b"))
    return Counter({(k, a, k, b): c for (k, a, b), c in res.rows.items()})


def test_example() -> None:
    r = [(k, f"r{i}") for i, k in enumerate([3, 1, 4, 1, 5, 9, 2, 6])]
    s = [(k, f"s{i}") for i, k in enumerate([1, 4, 1, 8, 5, 9])]
    x, bounds, moves = radix_cluster(r, 0, [1, 1])
    assert [t[1] for t in x] == ["r2", "r1", "r3", "r4", "r5", "r6", "r7", "r0"]
    assert bounds == [0, 1, 5, 7, 8] and moves == [8, 8]
    out, stats = radix_join(r, s, 0, 0, [1, 1])
    assert Counter(out) == oracle(r, s) and len(out) == 7
    assert stats["compares"] == 8


def test_cluster_property() -> None:
    rng = random.Random(3)
    for passes in PASSES:
        rows = [(rng.randrange(50), i) for i in range(rng.randrange(0, 120))]
        x, bounds, moves = radix_cluster(rows, 0, passes)
        b = sum(passes)
        assert len(bounds) == (1 << b) + 1 and Counter(x) == Counter(rows)
        assert moves == [len(rows)] * len(passes)
        for i in range(1 << b):
            part = x[bounds[i]:bounds[i + 1]]
            assert all(h(t[0]) % (1 << b) == i for t in part)
            # The clustering is stable: the input order is kept inside a cluster.
            assert [t[1] for t in part] == sorted(t[1] for t in part)


def test_random_against_oracle() -> None:
    rng = random.Random(7)
    for trial in range(60):
        dom = rng.choice([3, 5, 40])
        r = [(rng.randrange(dom), f"a{i}") for i in range(rng.randrange(0, 60))]
        s = [(rng.randrange(dom), f"b{i}") for i in range(rng.randrange(0, 60))]
        want = oracle(r, s)
        for passes in PASSES:
            out, _ = radix_join(r, s, 0, 0, passes)
            assert Counter(out) == want


def test_edges_and_nulls() -> None:
    assert radix_join([], [], 0, 0, [2])[0] == []
    assert radix_join([(1, "x")], [], 0, 0, [2])[0] == []
    same_r = [(7, i) for i in range(5)]
    same_s = [(7, i) for i in range(4)]
    out, _ = radix_join(same_r, same_s, 0, 0, [2, 1])
    assert len(out) == 20
    r = [(None, "x"), (1, "y"), (None, "z")]
    s = [(None, "u"), (1, "v")]
    out, _ = radix_join(r, s, 0, 0, [1])
    assert out == [(1, "y", 1, "v")]


def test_cache_misses_in_lru_model() -> None:
    # 200 tuples per input, a cache of 16 lines of 4 words.
    rng = random.Random(1)
    r = [(rng.randrange(1000), i) for i in range(200)]
    s = [(rng.randrange(1000), i) for i in range(200)]
    misses = {}
    for passes in ([6], [3, 3]):
        trace = []
        radix_cluster(r, 0, passes, trace)
        misses[tuple(passes)] = count_misses(trace, 16, 4)
    assert misses[(6,)] == 472 and misses[(3, 3)] == 305
    join_misses = {}
    for passes in ([], [4], [3, 3]):
        trace = []
        radix_join(r, s, 0, 0, passes, trace)
        join_misses[tuple(passes)] = count_misses(trace, 16, 4)
    assert join_misses == {(): 808, (4,): 147, (3, 3): 105}


def test_lru_simulator() -> None:
    assert count_misses([0, 1, 2, 3], 1, 4) == 1
    assert count_misses([0, 4, 0, 4], 1, 4) == 4
    assert count_misses([0, 4, 0, 4], 2, 4) == 2
    assert count_misses([0, 4, 8, 0], 2, 4) == 4
