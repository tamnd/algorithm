# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grid-file/. The authors are listed in prov/0WX5ZW.jsonl.

import random

import pytest

from grid_file import GridFile


def regions(g: GridFile) -> list:
    return sorted(((b.c0, b.c1, b.r0, b.r1), sorted(b.points)) for b in g.buckets)


def test_page_example() -> None:
    g = GridFile(2)
    for p in [(10, 10), (60, 20), (30, 70), (80, 80), (40, 40), (70, 60), (20, 30)]:
        assert g.insert(p)
        g.check_invariant()
    assert not g.insert((40, 40))
    assert g.xs == [30, 60] and g.ys == [70]
    assert regions(g) == [
        ((0, 1, 0, 2), [(10, 10), (20, 30)]),
        ((1, 2, 0, 1), [(40, 40)]),
        ((1, 3, 1, 2), [(30, 70), (80, 80)]),
        ((2, 3, 0, 1), [(60, 20), (70, 60)]),
    ]
    assert g.bucket_of((90, 90)) is g.bucket_of((40, 75))
    assert sorted(g.range_search((25, 25), (65, 65))) == [(40, 40)]
    assert g.delete((80, 80)) and len(g.buckets) == 4
    assert g.delete((70, 60)) and not g.delete((70, 60))
    g.check_invariant()
    assert regions(g) == [
        ((0, 1, 0, 2), [(10, 10), (20, 30)]),
        ((1, 3, 0, 1), [(40, 40), (60, 20)]),
        ((1, 3, 1, 2), [(30, 70)]),
    ]


def test_edges() -> None:
    g = GridFile(1)
    assert g.range_search((0, 0), (5, 5)) == []
    assert not g.delete((1, 1))
    for i in range(50):
        assert g.insert((i, 0))
        g.check_invariant()
    assert len(g.buckets) == 50 and g.ys == []
    assert sorted(g.range_search((10, -1), (12, 1))) == [(10, 0), (11, 0), (12, 0)]
    h = GridFile(3)
    for i in range(20):
        h.insert((7, i))
    h.check_invariant()
    assert h.xs == [] and len(h.ys) > 0
    with pytest.raises(ValueError):
        GridFile(0)


def test_random_against_oracle() -> None:
    rng = random.Random(20261104)
    for case in range(600):
        cap = rng.randint(1, 5)
        g = GridFile(cap)
        live: set = set()
        span = rng.choice([4, 10, 100, 1000])
        for _ in range(rng.randint(1, 60)):
            p = (rng.randrange(span), rng.randrange(span))
            if live and rng.random() < 0.35:
                d = rng.choice(sorted(live))
                assert d in g and g.delete(d)
                live.discard(d)
            assert g.insert(p) == (p not in live)
            live.add(p)
        g.check_invariant()
        assert sorted(g.points()) == sorted(live)
        for _ in range(3):
            x0, x1 = sorted(rng.randrange(-1, span + 1) for _ in range(2))
            y0, y1 = sorted(rng.randrange(-1, span + 1) for _ in range(2))
            want = sorted(q for q in live if x0 <= q[0] <= x1 and y0 <= q[1] <= y1)
            assert sorted(g.range_search((x0, y0), (x1, y1))) == want
        q = (rng.randrange(span), rng.randrange(span))
        assert (q in g) == (q in live)
