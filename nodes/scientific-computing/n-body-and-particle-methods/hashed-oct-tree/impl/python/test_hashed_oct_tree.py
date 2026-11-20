# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hashed-oct-tree/. The authors are listed in prov/4795RQ.jsonl.
import random

import pytest

from hashed_oct_tree import HashedOctTree, child, deinterleave, interleave, level_of, parent


def points(n, seed, clustered=False):
    rng = random.Random(seed)
    if not clustered:
        return [tuple(rng.random() for _ in range(3)) for _ in range(n)]
    out = []
    for _ in range(n):
        c = rng.choice([(0.2, 0.2, 0.2), (0.7, 0.6, 0.8)])
        out.append(tuple(c[d] + rng.gauss(0, 0.02) for d in range(3)))
    return out


def inside(p, lo, s):
    return all(lo[d] <= p[d] < lo[d] + s for d in range(3))


def test_small_keys():
    assert interleave(0, 0, 0, 0) == 1
    assert [interleave(i, j, k, 1) for k in (0, 1) for j in (0, 1) for i in (0, 1)] == list(range(8, 16))
    assert interleave(1, 0, 0, 2) == 0o101  # 1, then digit 0 at level 1, digit 1 at level 2
    assert interleave(3, 3, 3, 2) == 0o177
    assert parent(0o177) == 0o17 and parent(0o17) == 1
    assert child(1, 5) == 13 and level_of(13) == 1


def test_key_round_trip():
    rng = random.Random(3)
    for _ in range(500):
        lev = rng.randint(0, 21)
        i, j, k = (rng.randrange(1 << lev) for _ in range(3))
        key = interleave(i, j, k, lev)
        assert deinterleave(key) == (lev, i, j, k)
        assert level_of(key) == lev
        if lev:
            assert deinterleave(parent(key)) == (lev - 1, i >> 1, j >> 1, k >> 1)


@pytest.mark.parametrize("clustered", [False, True])
@pytest.mark.parametrize("leaf_size", [1, 4])
def test_cells_match_brute_force(clustered, leaf_size):
    x = points(300, 11, clustered)
    t = HashedOctTree(x, leaf_size=leaf_size)
    for key in t.table:
        lo, s = t.bounds(key)
        want = sorted(n for n, p in enumerate(x) if inside(p, lo, s))
        assert sorted(t.lookup(key)) == want
        if key != 1:
            assert parent(key) in t.table
        kids = t.children(key)
        if kids:
            assert len(want) > leaf_size
            assert sorted(n for c in kids for n in t.lookup(c)) == want
        else:
            assert len(want) <= leaf_size


def test_leaf_of_and_missing_keys():
    x = points(200, 5)
    t = HashedOctTree(x, leaf_size=2)
    for n, p in enumerate(x):
        leaf = t.leaf_of(p)
        assert t.is_leaf(leaf)
        assert n in t.lookup(leaf)
    missing = next(child(k, c) for k in t.table for c in range(8)
                   if child(k, c) not in t.table and not t.is_leaf(k))
    with pytest.raises(KeyError):
        t.lookup(missing)


def test_sorted_order_is_z_order():
    x = points(100, 8)
    t = HashedOctTree(x)
    assert t.keys == sorted(t.keys)
    for key, (start, end) in t.table.items():
        assert end > start  # no empty cell is stored


def test_coincident_points_stop_at_depth():
    x = [(0.5, 0.5, 0.5)] * 3 + [(0.1, 0.9, 0.3)]
    t = HashedOctTree(x, leaf_size=1, depth=6)
    deep = [k for k in t.table if level_of(k) == 6]
    assert len(deep) == 1 and len(t.lookup(deep[0])) == 3
