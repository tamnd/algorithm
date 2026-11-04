# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-hashing/. The authors are listed in prov/D6C9DX.jsonl.
import random

import pytest

from spatial_hashing import SpatialHash, intersects

BOXES = {"A": (2, 3, 8, 7), "B": (15, 5, 27, 12),
         "C": (-6, -4, -1, 4), "D": (31, 31, 33, 33)}


def test_page_example():
    s = SpatialHash(10, 8)
    for k, v in BOXES.items():
        s.insert(k, v)
    assert [s.bucket(*c) for c in s.cells_of(BOXES["B"])] == [5, 2, 2, 5]
    assert [s.bucket(*c) for c in s.cells_of(BOXES["C"])] == [2, 3]
    assert s.bucket(3, 3) == 2 and s.bucket(0, 0) == 0
    assert [len(b) for b in s.table] == [1, 0, 4, 1, 0, 2, 0, 0]
    assert s.entry_count() == 8 and s.size == 4
    assert sorted(s.query((5, 4, 16, 9))) == ["A", "B"]
    assert sorted(s.query((-3, -3, 12, 6))) == ["A", "C"]
    assert s.query((30, 30, 30.5, 30.5)) == []
    assert s.delete("B", BOXES["B"]) and s.entry_count() == 4
    assert not s.delete("B", BOXES["B"])
    assert s.query((5, 4, 16, 9)) == ["A"]


def test_edge_cases():
    s = SpatialHash(1.0, 1)  # every cell collides into one bucket
    s.insert(1, (0, 0, 1, 1))  # corner on a cell boundary: 4 cells
    s.insert(2, (1, 1, 2, 2))
    assert s.entry_count() == 8
    assert sorted(s.query((1, 1, 1, 1))) == [1, 2]  # closed boxes touch
    assert s.close_pairs() == {(1, 2)}
    assert s.query((5, 5, 6, 6)) == []
    with pytest.raises(ValueError):
        SpatialHash(0)
    with pytest.raises(ValueError):
        s.insert(3, (2, 0, 1, 1))


def rand_box(rng):
    x, y = rng.uniform(-50, 50), rng.uniform(-50, 50)
    return (x, y, x + rng.uniform(0, 15), y + rng.uniform(0, 15))


def test_random_against_brute_force():
    rng = random.Random(1104)
    for trial in range(500):
        s = SpatialHash(rng.choice([2.0, 5.0, 10.0]), rng.choice([1, 7, 64]))
        live = {}
        for k in range(rng.randint(0, 25)):
            b = rand_box(rng)
            s.insert(k, b)
            live[k] = b
        for k in list(live)[: rng.randint(0, len(live))]:
            if rng.random() < 0.4:
                assert s.delete(k, live.pop(k))
        for _ in range(4):
            q = rand_box(rng)
            got = s.query(q)
            assert len(got) == len(set(got))
            assert set(got) == {k for k, b in live.items() if intersects(q, b)}
        if trial % 5 == 0:
            ks = sorted(live)
            want = {frozenset((a, c)) for x, a in enumerate(ks) for c in ks[x + 1:]
                    if intersects(live[a], live[c])}
            assert {frozenset(p) for p in s.close_pairs()} == want
