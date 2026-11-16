# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree-occupancy-map/. The authors are listed in prov/34SSST.jsonl.

import itertools
import random

import pytest

import robest
from octree_occupancy_map import OctreeOccupancyMap


def clamp(v, lo, hi):
    return min(hi, max(lo, v))


def block_max(model, key, side):
    """The value of the block of the given side that holds key: max over its known voxels."""
    low = [k - k % side for k in key]
    vals = [model[v] for v in itertools.product(*(range(c, c + side) for c in low)) if v in model]
    return max(vals) if vals else None


def canonical_nodes(model, low, side):
    """The number of nodes of the fully pruned octree of the block, from the dense model."""
    keys = list(itertools.product(*(range(c, c + side) for c in low)))
    known = [model[k] for k in keys if k in model]
    if not known:
        return 0
    if len(known) == len(keys) and all(v == known[0] for v in known):
        return 1
    h = side // 2
    return 1 + sum(
        canonical_nodes(model, (low[0] + dx, low[1] + dy, low[2] + dz), h)
        for dx in (0, h) for dy in (0, h) for dz in (0, h)
    )


def open_box_meets_segment(t, key, a, b):
    """Brute force: does the open cube of voxel key meet the segment ab?"""
    lo, hi = 0.0, 1.0
    for ax in range(3):
        c0 = t.origin[ax] + key[ax] * t.res
        c1 = c0 + t.res
        p, d = a[ax], b[ax] - a[ax]
        if d == 0:
            if not c0 < p < c1:
                return False
            continue
        t0, t1 = sorted(((c0 - p) / d, (c1 - p) / d))
        lo, hi = max(lo, t0), min(hi, t1)
    return lo < hi


def brute_voxels(t, a, b):
    ka, kb = t.key_of(a), t.key_of(b)
    rng = [range(min(ka[ax], kb[ax]), max(ka[ax], kb[ax]) + 1) for ax in range(3)]
    return {k for k in itertools.product(*rng) if open_box_meets_segment(t, k, a, b)}


def test_keys():
    t = OctreeOccupancyMap(3, res=0.5, origin=(-1.0, 0.0, 2.0))
    assert t.size == 8
    assert t.key((-1.0, 0.0, 2.0)) == (0, 0, 0)
    assert t.key((-0.51, 0.49, 2.5)) == (0, 0, 1)
    assert t.key((2.99, 3.99, 5.99)) == (7, 7, 7)
    assert t.key((3.0, 1.0, 3.0)) is None
    assert t.key_of((-1.2, 0.0, 2.0)) == (-1, 0, 0)


def test_paper_values():
    assert robest.logodds(0.7) == pytest.approx(0.85, abs=3e-3)
    assert robest.logodds(0.4) == pytest.approx(-0.4, abs=6e-3)
    assert robest.logodds(0.12) == pytest.approx(-2.0, abs=1e-2)
    assert robest.logodds(0.97) == pytest.approx(3.5, abs=3e-2)
    t = OctreeOccupancyMap(2)
    for n in range(1, 6):
        t.update((0, 0, 0), t.l_occ)
        t.update((3, 3, 3), t.l_free)
        if n == 4:
            assert t.search((0, 0, 0)) < t.l_max and t.search((3, 3, 3)) > t.l_min
    assert t.search((0, 0, 0)) == 3.5  # five agreeing hits reach the bound
    assert t.search((3, 3, 3)) == -2.0
    assert t.search((1, 1, 1)) is None


def test_empty_map():
    t = OctreeOccupancyMap(3)
    t.check_invariant()
    assert t.num_nodes() == 1
    assert t.search((1, 2, 3)) is None and t.search((1, 2, 3), 0) is None
    assert t.probability((1, 2, 3)) is None


def test_pruning_and_expansion():
    t = OctreeOccupancyMap(2)
    for _ in range(5):
        for k in itertools.product(range(4), repeat=3):
            t.update(k, t.l_free)
    t.check_invariant()
    assert t.num_nodes() == 1
    assert t.leaves() == [((0, 0, 0), 4, -2.0)]
    t.update((1, 2, 3), t.l_occ)
    t.check_invariant()
    assert t.num_nodes() == 17
    assert t.search((1, 2, 3)) == pytest.approx(-1.15, abs=1e-12)
    assert t.search((0, 0, 0)) == -2.0
    assert t.search((1, 2, 3), 1) == t.search((1, 2, 3))
    assert t.search((3, 0, 0), 1) == -2.0
    assert t.search((3, 3, 3), 0) == t.search((1, 2, 3))
    for _ in range(3):
        t.update((1, 2, 3), t.l_free)
    t.check_invariant()
    assert t.num_nodes() == 1


def test_partial_block_is_not_pruned():
    t = OctreeOccupancyMap(1)
    keys = list(itertools.product(range(2), repeat=3))
    for k in keys[:7]:
        for _ in range(5):
            t.update(k, t.l_occ)
    t.check_invariant()
    assert t.num_nodes() == 8
    assert t.search(keys[7]) is None
    assert t.search(keys[7], 0) == 3.5
    for _ in range(5):
        t.update(keys[7], t.l_occ)
    assert t.num_nodes() == 1


def test_random_operations_against_a_dense_model():
    rng = random.Random(31)
    for clamped in (True, False):
        t = OctreeOccupancyMap(3) if clamped else OctreeOccupancyMap(3, l_min=None, l_max=None)
        model = {}
        pruned_seen = False
        for step in range(1500):
            hot = rng.random() < 0.6
            if hot:  # a block of 2 x 2 x 2 voxels that gets mostly free updates, so that it is pruned
                key = (4 + rng.randrange(2), rng.randrange(2), 2 + rng.randrange(2))
            else:
                key = tuple(rng.randrange(8) for _ in range(3))
            if rng.random() < 0.65:
                if hot:
                    v = t.l_free if rng.random() < 0.9 else t.l_occ
                else:
                    v = rng.choice([t.l_occ, t.l_free, rng.uniform(-1.0, 1.0)])
                t.update(key, v)
                model[key] = clamp(model.get(key, 0.0) + v, t.l_min, t.l_max)
            d = rng.randrange(4)
            assert t.search(key, d) == block_max(model, key, 1 << (3 - d))
            if step % 50 == 0:
                t.check_invariant()
                want = max(1, canonical_nodes(model, (0, 0, 0), 8))
                assert t.num_nodes() == want
                pruned_seen = pruned_seen or any(side > 1 for _, side, _ in t.leaves())
        t.check_invariant()
        for k in itertools.product(range(8), repeat=3):
            assert t.search(k) == model.get(k)
        if clamped:
            assert pruned_seen


def test_voxels_on_segment_against_brute_force():
    rng = random.Random(7)
    t = OctreeOccupancyMap(3, res=0.3, origin=(-0.4, 0.2, -1.0))
    for _ in range(200):
        a = tuple(rng.uniform(-1.0, 1.5) for _ in range(3))
        b = tuple(rng.uniform(-1.0, 1.5) for _ in range(3))
        cells = t.voxels_on_segment(a, b)
        assert cells[0] == t.key_of(a) and cells[-1] == t.key_of(b)
        for p, q in zip(cells, cells[1:]):
            assert sum(abs(x - y) for x, y in zip(p, q)) == 1
        assert len(set(cells)) == len(cells)
        assert set(cells) == brute_voxels(t, a, b)


def test_insert_scan_updates_each_voxel_once_and_occupied_wins():
    t = OctreeOccupancyMap(4, res=0.1)
    s = (0.05, 0.05, 0.05)
    t.insert_scan(s, [(0.55, 0.05, 0.05), (0.35, 0.05, 0.05)])
    t.check_invariant()
    got = [t.search((i, 0, 0)) for i in range(7)]
    assert got == [-0.4, -0.4, -0.4, 0.85, -0.4, 0.85, None]
    assert t.search((0, 1, 0)) is None


def test_insert_scan_against_a_dense_model():
    rng = random.Random(13)
    t = OctreeOccupancyMap(4, res=0.25, origin=(-0.5, -0.5, -0.5))
    model = {}
    for _ in range(10):
        s = tuple(rng.uniform(0.0, 3.0) for _ in range(3))
        pts = [tuple(c + rng.uniform(-1.0, 1.0) for c in s) for _ in range(20)]
        free, occ = set(), set()
        for z in pts:
            end = t.key_of(z)
            occ.add(end)
            free |= brute_voxels(t, s, z) - {end}
        t.insert_scan(s, pts)
        for k in free - occ:
            if t.inside(k):
                model[k] = clamp(model.get(k, 0.0) + t.l_free, t.l_min, t.l_max)
        for k in occ:
            if t.inside(k):
                model[k] = clamp(model.get(k, 0.0) + t.l_occ, t.l_min, t.l_max)
        t.check_invariant()
    for k in itertools.product(range(16), repeat=3):
        assert t.search(k) == model.get(k)


def test_invalid_arguments():
    with pytest.raises(ValueError):
        OctreeOccupancyMap(0)
    with pytest.raises(ValueError):
        OctreeOccupancyMap(2, l_min=0.5)
    with pytest.raises(ValueError):
        OctreeOccupancyMap(2).update((4, 0, 0), 0.85)
