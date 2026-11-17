# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leapfrog-triejoin/. The authors are listed in prov/R8QS9W.jsonl.

import random
from fractions import Fraction as F
from math import lcm, prod

from leapfrog_triejoin import Leapfrog, TrieIterator, leapfrog_triejoin

TRI = [("A", "B"), ("B", "C"), ("A", "C")]


def nested_loop(edges, rels, order):
    cur = [{}]
    for e, r in zip(edges, rels):
        nxt = []
        for asg in cur:
            for t in r:
                if all(asg.get(v, a) == a for v, a in zip(e, t)):
                    d = dict(asg)
                    d.update(zip(e, t))
                    nxt.append(d)
        cur = nxt
    return sorted({tuple(d[v] for v in order) for d in cur})


def within(count, sizes, x):
    d = lcm(*(w.denominator for w in x))
    return count ** d <= prod(n ** int(d * w) for n, w in zip(sizes, x))


def unary(keys):
    it = TrieIterator(sorted((k,) for k in keys))
    it.open()
    return it


def test_leapfrog_intersection() -> None:
    rng = random.Random(1)
    for _ in range(300):
        sets = [set(rng.sample(range(40), rng.randrange(1, 30))) for _ in range(rng.randrange(1, 5))]
        lf = Leapfrog([unary(s) for s in sets])
        lf.init()
        got = []
        while not lf.done:
            got.append(lf.key)
            lf.next()
        assert got == sorted(set.intersection(*sets))
        m, fewest = len(sets), min(len(s) for s in sets)
        assert lf.moves <= m * (fewest + 1)


def test_iterator_seek_next() -> None:
    it = TrieIterator(sorted({(1, 5), (1, 7), (3, 2), (3, 4), (3, 9), (8, 1)}))
    it.open()
    assert it.key() == 1
    it.seek(2)
    assert it.key() == 3
    it.open()
    assert it.key() == 2
    it.seek(5)
    assert it.key() == 9
    it.next()
    assert it.at_end()
    it.up()
    assert it.key() == 3
    it.next()
    assert it.key() == 8
    it.next()
    assert it.at_end()


def test_example() -> None:
    r = {(1, 1), (1, 2), (2, 1), (2, 3)}
    s = {(1, 2), (2, 3), (3, 1), (1, 3)}
    t = {(1, 2), (1, 3), (2, 3), (2, 1)}
    assert leapfrog_triejoin(TRI, [r, s, t], "ABC") == [(1, 1, 2), (1, 1, 3), (1, 2, 3), (2, 1, 3), (2, 3, 1)]
    assert leapfrog_triejoin(TRI, [set(), s, t]) == []


QUERIES = [
    (TRI, (F(1, 2),) * 3),
    ([("A", "B"), ("B", "C"), ("C", "D"), ("A", "D")], (F(1, 2),) * 4),
    ([("A", "B", "C"), ("A", "B", "D"), ("A", "C", "D"), ("B", "C", "D")], (F(1, 3),) * 4),
    ([("A", "B"), ("B", "C")], (F(1), F(1))),
    ([("A", "B", "C"), ("C", "D"), ("B", "D")], (F(1), F(1), F(0))),
]


def test_against_nested_loop_and_bounds() -> None:
    rng = random.Random(42)
    for _ in range(200):
        edges, cover = rng.choice(QUERIES)
        dom = rng.randrange(2, 6)
        rels = [{tuple(rng.randrange(dom) for _ in e) for _ in range(rng.randrange(0, 25))} for e in edges]
        attrs = sorted({v for e in edges for v in e})
        order = rng.sample(attrs, len(attrs))
        st = {}
        got = leapfrog_triejoin(edges, rels, order, st)
        assert got == nested_loop(edges, rels, order)   # also in sorted order
        level_work = [0] * len(order)
        for i, moves, m, fewest in st["calls"]:
            assert moves <= m * (fewest + 1)
            level_work[i] += fewest
        sizes = [len(r) for r in rels]
        if min(sizes) > 0:
            assert all(within(w, sizes, cover) for w in level_work)


def test_skewed_triangle() -> None:
    for m in (10, 50, 200):
        r = {(0, i) for i in range(1, m + 1)} | {(i, 0) for i in range(1, m + 1)}
        n = len(r)
        st = {}
        assert leapfrog_triejoin(TRI, [r, r, r], "ABC", st) == []
        moves = sum(c[1] for c in st["calls"])
        assert moves <= 10 * n           # linear here, while pairwise plans make m*m + m tuples
