# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lsh-forest/. The authors are listed in prov/TVZ64D.jsonl.

import random

from lsh_forest import LSHForest, angle

P = [(4, 1), (3, 2), (1, 3), (-2, 3), (-3, -1), (1, -3), (4, -1)]
PLANES = [[(1, 0), (0, 1), (1, 1)], [(1, -1), (0, 1), (-1, 2)]]


def test_example() -> None:
    forest = LSHForest(P, 3, 2, planes=PLANES)
    assert [forest.trees[0][1][j] for j in range(7)] == [4, 3, 5, 6, 0, 1, 2]
    q = (2, 1)
    assert forest.candidates(q, 2) == ({0, 1, 2}, 3)
    assert forest.candidates(q, 4) == ({0, 1, 2, 5, 6}, 1)
    assert forest.candidates(q, 6) == (set(range(7)), 0)
    assert forest.query(q, 1, 2) == [1]
    assert forest.query(q, 2, 4) == [1, 0]


def test_edges() -> None:
    empty = LSHForest([], 4, 2)
    assert empty.query((1.0, 0.0), 3, 5) == []
    one = LSHForest([(1.0, 1.0)], 4, 2, seed=3)
    assert one.query((-1.0, 0.0), 1, 1) == [0]
    zero_depth = LSHForest(P, 0, 1, seed=1)
    assert zero_depth.candidates((1, 0), 1) == (set(range(7)), 0)


def shared(a, b):
    n = 0
    while n < len(a) and a[n] == b[n]:
        n += 1
    return n


def test_random_against_brute_force() -> None:
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(1, 40)
        dim = rng.randint(2, 5)
        pts = [tuple(rng.gauss(0, 1) for _ in range(dim)) for _ in range(n)]
        depth, trees = rng.randint(1, 8), rng.randint(1, 4)
        forest = LSHForest(pts, depth, trees, seed=rng.randrange(10**6))
        q = tuple(rng.gauss(0, 1) for _ in range(dim))
        m, k = rng.randint(1, n + 3), rng.randint(1, 5)
        lams = [forest.label(r, q) for r in forest.planes]
        labs = [[forest.label(r, p) for p in pts] for r in forest.planes]

        def cset(x):
            return {i for i in range(n) if any(shared(labs[t][i], lams[t]) >= x for t in range(trees))}

        xs = [x for x in range(depth + 1) if len(cset(x)) >= min(m, n)]
        x_star = max(xs)
        cand, x = forest.candidates(q, m)
        assert x == x_star and cand == cset(x_star)
        best = sorted(cand, key=lambda i: (angle(pts[i], q), i))[:k]
        assert forest.query(q, k, m) == best
        if m >= n:
            assert forest.query(q, k, m) == sorted(range(n), key=lambda i: (angle(pts[i], q), i))[:k]
