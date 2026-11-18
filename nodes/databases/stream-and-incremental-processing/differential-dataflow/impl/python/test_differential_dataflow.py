# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-dataflow/. The authors are listed in prov/Q08Q0Y.jsonl.

import random
from collections import Counter

from differential_dataflow import Reachability, bfs, leq, lub, recompute


def test_order() -> None:
    assert leq((0, 3), (1, 3)) and not leq((0, 3), (1, 2)) and not leq((1, 2), (0, 3))
    assert lub((0, 3), (1, 0)) == (1, 3)


def test_page_example() -> None:
    rd = Reachability()
    rd.advance({1: 1}, {(1, 2): 1, (2, 3): 1})
    rd.advance({}, {(1, 2): -1, (1, 3): 1, (3, 4): 1})
    diffs = {t: dict(d) for t, d in rd.out.diffs.items()}
    assert diffs == {(0, 0): {1: 1}, (0, 1): {2: 1}, (0, 2): {3: 1},
                     (1, 1): {3: 1, 2: -1}, (1, 2): {3: -1, 4: 1}}
    assert rd.reachable(0) == {1, 2, 3}
    assert rd.reachable(1) == {1, 3, 4}
    assert [rd.reachable(1, i) for i in range(3)] == [{1}, {1, 3}, {1, 3, 4}]
    assert rd.distinct_evals == 5


def random_epochs(rng, n, epochs):
    roots, edges = Counter(), Counter()
    out = []
    for e in range(epochs):
        dr, de = Counter(), Counter()
        for _ in range(rng.randrange(0, 4)):
            x = (rng.randrange(n), rng.randrange(n))
            de[x] += -1 if edges[x] + de[x] > 0 and rng.random() < 0.5 else 1
        if e == 0 or rng.random() < 0.5:
            x = rng.randrange(n)
            dr[x] += -1 if roots[x] > 0 and rng.random() < 0.5 else 1
        roots.update(dr)
        edges.update(de)
        roots, edges = +roots, +edges
        out.append((dr, de, set(roots), set(edges)))
    return out


def test_against_recomputation_and_bfs() -> None:
    for seed in range(150):
        rng = random.Random(seed)
        n = rng.randrange(2, 7)
        rd = Reachability()
        hist = []
        for dr, de, roots, edges in random_epochs(rng, n, 6):
            rd.advance(dr, de)
            hist.append((roots, edges))
            for e, (r, g) in enumerate(hist):
                for i in range(n + 2):
                    assert rd.reachable(e, i) == recompute(r, g, i)
                assert rd.reachable(e) == bfs(r, g)


def test_differences_are_exact() -> None:
    # The stored difference at (e, i) is R(e,i) - R(e-1,i) - R(e,i-1) + R(e-1,i-1),
    # so distinct, evaluated only at closure times, misses no time.
    def as_counter(s):
        return Counter({x: 1 for x in s})

    for seed in range(80):
        rng = random.Random(1000 + seed)
        n = rng.randrange(2, 6)
        rd = Reachability()
        hist = []
        for dr, de, roots, edges in random_epochs(rng, n, 5):
            rd.advance(dr, de)
            hist.append((roots, edges))
        val = {}
        for e, (r, g) in enumerate(hist):
            for i in range(n + 3):
                val[(e, i)] = as_counter(recompute(r, g, i))
        for (e, i) in val:
            if i == n + 2:
                continue
            d = Counter(val[(e, i)])
            for (de_, di), sign in (((e - 1, i), -1), ((e, i - 1), -1), ((e - 1, i - 1), 1)):
                if (de_, di) in val:
                    for x, w in val[(de_, di)].items():
                        d[x] += sign * w
            d = Counter({x: w for x, w in d.items() if w})
            assert d == rd.out.get((e, i))
        assert set(rd.out.diffs) <= rd.closure


def test_small_change_touches_few_times() -> None:
    # A long path: adding one edge at the end changes R at one time only.
    rd = Reachability()
    rd.advance({0: 1}, {(k, k + 1): 1 for k in range(20)})
    before = rd.distinct_evals
    rd.advance({}, {(20, 21): 1})
    assert rd.reachable(1) == set(range(22))
    assert {t for t in rd.out.diffs if t[0] == 1} == {(1, 21)}
    assert rd.distinct_evals - before == 1
