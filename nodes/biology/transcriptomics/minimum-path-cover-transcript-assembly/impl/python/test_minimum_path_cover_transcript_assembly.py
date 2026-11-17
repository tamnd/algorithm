# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-path-cover-transcript-assembly/. The authors are listed in prov/9NY424.jsonl.

import random
from itertools import combinations

from minimum_path_cover_transcript_assembly import min_path_cover, precedes, reach


def contains(path, frag):
    n = len(frag)
    return any(tuple(path[i:i + n]) == tuple(frag) for i in range(len(path) - n + 1))


def all_paths(n, edges):
    """Every source-to-sink path of the DAG."""
    succ = {u: [] for u in range(n)}
    has_pred = set()
    for u, v in edges:
        succ[u].append(v)
        has_pred.add(v)
    out, stack = [], [[s] for s in range(n) if s not in has_pred]
    while stack:
        p = stack.pop()
        if not succ[p[-1]]:
            out.append(p)
        for v in succ[p[-1]]:
            stack.append(p + [v])
    return out


def random_instance(rng: random.Random):
    n = rng.randint(2, 7)
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.45]
    succ = {u: [v for a, v in edges if a == u] for u in range(n)}
    frags = []
    for _ in range(rng.randint(1, 6)):
        f = [rng.randrange(n)]
        for _ in range(rng.randint(0, 3)):
            if not succ[f[-1]]:
                break
            f.append(rng.choice(succ[f[-1]]))
        frags.append(f)
    return n, edges, frags


def brute_cover(n, edges, frags):
    """The fewest source-to-sink paths that hold every fragment."""
    paths = all_paths(n, edges)
    for k in range(1, len(frags) + 1):
        for choice in combinations(paths, k):
            if all(any(contains(p, f) for p in choice) for f in frags):
                return k
    raise AssertionError("every fragment is on some source-to-sink path")


def test_worked_example():
    # The splice graph of the page: v1 -> v2 -> v3 -> v4 and v1 -> v3, v1 -> v4 (0-based here).
    edges = [(0, 1), (1, 2), (2, 3), (0, 2), (0, 3)]
    frags = [[0, 1], [1, 2], [2, 3], [0, 2], [0, 3]]
    paths = min_path_cover(4, edges, frags)
    assert paths == [[0, 1, 2], [0, 2, 3], [0, 3]]
    # A contained fragment and a duplicate change nothing.
    assert min_path_cover(4, edges, frags + [[2], [0, 1]]) == paths


def test_precedes_is_a_strict_partial_order():
    rng = random.Random(1)
    for _ in range(300):
        n, edges, frags = random_instance(rng)
        r = reach(n, edges)
        fs = sorted(set(tuple(f) for f in frags))
        fs = [x for x in fs if not any(x != y and contains(y, x) for y in fs)]
        for x in fs:
            assert not precedes(x, x, r)
            for y in fs:
                for z in fs:
                    if precedes(x, y, r) and precedes(y, z, r):
                        assert precedes(x, z, r)


def test_precedes_means_a_common_path():
    rng = random.Random(2)
    for _ in range(300):
        n, edges, frags = random_instance(rng)
        r = reach(n, edges)
        paths = all_paths(n, edges)
        fs = sorted(set(tuple(f) for f in frags))
        fs = [x for x in fs if not any(x != y and contains(y, x) for y in fs)]
        for x in fs:
            for y in fs:
                if x[0] < y[0]:
                    both = any(contains(p, x) and contains(p, y) for p in paths)
                    assert precedes(x, y, r) == both


def test_against_brute_force():
    rng = random.Random(3)
    for _ in range(500):
        n, edges, frags = random_instance(rng)
        out = min_path_cover(n, edges, frags)
        eset = set(edges)
        for p in out:
            assert all((u, v) in eset for u, v in zip(p, p[1:]))
        for f in frags:
            assert any(contains(p, f) for p in out)
        assert len(out) == brute_cover(n, edges, frags)


def test_dilworth_antichain():
    # The number of paths equals the largest set of fragments of which no two fit on one path.
    rng = random.Random(4)
    for _ in range(300):
        n, edges, frags = random_instance(rng)
        paths = all_paths(n, edges)
        fs = sorted(set(tuple(f) for f in frags))
        fs = [x for x in fs if not any(x != y and contains(y, x) for y in fs)]
        best = 0
        for k in range(1, len(fs) + 1):
            for sub in combinations(fs, k):
                if all(not any(contains(p, x) and contains(p, y) for p in paths)
                       for x, y in combinations(sub, 2)):
                    best = k
        assert len(min_path_cover(n, edges, frags)) == best
