# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-join/. The authors are listed in prov/5SQ32K.jsonl.

import random
from fractions import Fraction as F
from math import isqrt, lcm, prod

from generic_join import generic_join

TRI = [("A", "B"), ("B", "C"), ("A", "C")]


def nested_loop(edges, rels, order):
    """Reference: join the relations one by one with nested loops."""
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
    """Exactly decide count <= prod sizes_e^(x_e)."""
    d = lcm(*(w.denominator for w in x))
    return count ** d <= prod(n ** int(d * w) for n, w in zip(sizes, x))


def test_example() -> None:
    r = {(1, 1), (1, 2), (2, 1), (2, 3)}
    s = {(1, 2), (2, 3), (3, 1), (1, 3)}
    t = {(1, 2), (1, 3), (2, 3), (2, 1)}
    st = {}
    assert sorted(generic_join(TRI, [r, s, t], "ABC", st)) == [(1, 1, 2), (1, 1, 3), (1, 2, 3), (2, 1, 3), (2, 3, 1)]
    assert st["work"] == [2, 4, 6]


def test_edges() -> None:
    assert generic_join(TRI, [set(), {(1, 1)}, {(1, 1)}]) == []
    assert generic_join([("A",)], [{(5,), (6,)}]) in ([(5,), (6,)], [(6,), (5,)])
    assert sorted(generic_join([("A",), ("B",)], [{(1,), (2,)}, {(3,)}])) == [(1, 3), (2, 3)]


QUERIES = [
    (TRI, (F(1, 2),) * 3),
    ([("A", "B"), ("B", "C"), ("C", "D"), ("A", "D")], (F(1, 2),) * 4),
    ([("A", "B", "C"), ("A", "B", "D"), ("A", "C", "D"), ("B", "C", "D")], (F(1, 3),) * 4),
    ([("A", "B"), ("B", "C")], (F(1), F(1))),
    ([("A", "B", "C"), ("C", "D"), ("B", "D")], (F(1), F(1), F(0))),
]


def test_against_nested_loop_and_bound() -> None:
    rng = random.Random(42)
    for _ in range(200):
        edges, cover = rng.choice(QUERIES)
        dom = rng.randrange(2, 6)
        rels = [{tuple(rng.randrange(dom) for _ in e) for _ in range(rng.randrange(0, 25))} for e in edges]
        attrs = sorted({v for e in edges for v in e})
        order = rng.sample(attrs, len(attrs))
        st = {}
        got = sorted(generic_join(edges, rels, order, st))
        assert got == nested_loop(edges, rels, order)
        sizes = [len(r) for r in rels]
        if min(sizes) > 0:
            for w in st["work"]:
                assert within(w, sizes, cover)


def skewed(m):
    return {(0, i) for i in range(1, m + 1)} | {(i, 0) for i in range(1, m + 1)}


def test_skewed_triangle() -> None:
    for m in (10, 50, 200):
        r = skewed(m)
        n = len(r)
        # Each pairwise plan joins two relations on one attribute first.
        pair = sum(1 for (a, b) in r for (b2, c) in r if b == b2)
        assert pair == m * m + m
        st = {}
        assert generic_join(TRI, [r, r, r], "ABC", st) == []
        total = sum(st["work"])
        assert all(w * w <= n ** 3 for w in st["work"])
        assert total <= 3 * isqrt(n ** 3)
        assert total <= 4 * n            # in fact linear on this instance


def test_random_triangle_scaling() -> None:
    rng = random.Random(7)
    for n in (50, 200, 800):
        rels = []
        for _ in range(3):
            r = set()
            while len(r) < n:
                # half the tuples on a heavy value, half spread out
                r.add((0, rng.randrange(n)) if rng.random() < 0.5 else (rng.randrange(n), rng.randrange(n)))
            rels.append(r)
        st = {}
        out = generic_join(TRI, rels, "ABC", st)
        assert sorted(out) == nested_loop(TRI, rels, "ABC") if n <= 200 else True
        assert all(w * w <= n ** 3 for w in st["work"])
